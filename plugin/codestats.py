import datetime
import json
import sys
import threading
import time
import vim

from ssl import CertificateError

# Python 2 and 3 have different modules for urllib2
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from urllib.parse import urljoin
    from http.client import HTTPException
except ImportError:
    from urllib2 import Request, urlopen, URLError
    from urlparse import urljoin
    from httplib import HTTPException

# Vim has thread-safe Python, Neovim does not; feature detect and wrap
# see https://gitlab.com/code-stats/code-stats-vim/-/issues/14
try:
    _async_call = vim.async_call
except AttributeError:
    def _async_call(f, *args, **kwargs):
        f(*args, **kwargs)


# because of vim, we need to get the current folder
# into the path to load other modules
# NOTE: codestats_path has been set in .vim before loading this file
if codestats_path not in sys.path:              # noqa: F821
    sys.path.append(codestats_path)             # noqa: F821

from codestats_filetypes import filetype_map
from localtz import LOCAL_TZ

# globals
INTERVAL = 10                # interval at which stats are sent
SLEEP_INTERVAL = 0.1         # sleep interval for timeslicing
VERSION = '1.1.1'            # versioning
TIMEOUT = 2                  # request timeout value (in seconds)


class CodeStats():
    def __init__(self, xp_dict, base_url, api_key):
        self.xp_dict = xp_dict
        self.pulse_url = urljoin(base_url, 'api/my/pulses')
        self.api_key = api_key

        self.sem = threading.Semaphore()

        # start the main thread
        self.cs_thread = threading.Thread(target=self.main_thread, args=())
        self.cs_thread.daemon = True
        self.cs_thread.start()

    def add_xp(self, filetype, xp):
        if xp == 0:
            return

        # get the langauge type based on what vim passed to us
        language_type = filetype_map.get(filetype, filetype)

        # insert the filetype into the dictionary.  Sem sections
        # are super small so this should be quick if it blocks
        self.sem.acquire()
        count = self.xp_dict.setdefault(language_type, 0)
        self.xp_dict[language_type] = count + xp
        self.sem.release()

    def send_xp(self, exiting=False):
        if len(self.xp_dict) == 0:
            return

        # acquire the lock to get the list of xp to send
        self.sem.acquire()
        xp_list = [dict(language=ft, xp=xp) for ft, xp in self.xp_dict.items()]
        self.xp_dict = {}
        self.sem.release()

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'code-stats-vim/{0}'.format(VERSION),
            'X-API-Token': self.api_key,
            'Accept': '*/*'
        }

        # after lock is released we can send the payload
        utc_now = datetime.datetime.now().replace(
                microsecond=0,
                tzinfo=LOCAL_TZ).isoformat()
        pulse_json = json.dumps(
                {
                    "coded_at": '{0}'.format(utc_now),
                    "xps": xp_list
                }).encode('utf-8')
        req = Request(url=self.pulse_url, data=pulse_json, headers=headers)
        error = ''
        try:
            response = urlopen(req, timeout=5)
            response.read()
            # connection might not be closed without .read()
        except URLError as e:
            try:
                # HTTP error
                error = '{0} {1}'.format(e.code, e.read().decode("utf-8"))
            except AttributeError:
                # non-HTTP error, eg. no network
                error = e.reason
        except CertificateError as e:
            # SSL certificate error (eg. a public wifi redirects traffic)
            error = e
        except HTTPException as e:
            error = 'HTTPException on send data. Msg: {0}\nDoc?:{1}'.format(
                e.message, e.__doc__)

        # hacky way to get around exiting and not needing to set the error
        if exiting is False and error != '':
            _async_call(
                vim.command,
                'call codestats#set_error("{0}")'.format(
                    str(error).replace('"', '\\"'))
            )

    def main_thread(self):
        """Main thread

        Needs to be able to send XP at an interval and also be able to stop
        when vim is exited without pausing until the interval is done.
        """
        while True:
            cur_time = 0
            while cur_time < INTERVAL:
                time.sleep(SLEEP_INTERVAL)
                cur_time += SLEEP_INTERVAL

            self.send_xp()

    def exit(self):
        self.send_xp(exiting=True)


# plugin startup.  Need to allow for vimrc getting reloaded and
# this module getting restarted, potentially with pending xp
def init_codestats(base_url, api_key):
    global codestats

    xp_dict = {}
    # allow reentrancy
    if 'codestats' in globals():
        xp_dict = codestats.xp_dict    # noqa: F821
        del(codestats)

    codestats = CodeStats(xp_dict, base_url, api_key)
