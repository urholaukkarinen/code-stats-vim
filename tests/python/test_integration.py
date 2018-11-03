"""Integration tests for all the Python components"""
import sys
from time import sleep

# setup mocks
import vim
vim.set_eval({
    's:codestats_path': '',
    'g:codestats_api_key': 'FAKE_API_KEY',
    'g:codestats_api_url': 'http://codestats.invalid'
})


def test_codestats_init():
    _run_codestats_py()
    assert('codestats' in globals())
    _stop()


def test_codestats_hot_reload():
    global codestats
    _run_codestats_py()
    codestats.instance = "FIRST INSTANCE"
    _run_codestats_py()
    assert(not hasattr(codestats, 'instance'))
    _stop()


def test_log_and_check_xp():
    def fake_urlopen(req, **args):
        return MockHttpResponse()

    from codestats import Codestats
    cs = Codestats(fake_urlopen)
    cs.log_xp("cpp", 13)
    cs.log_xp("python", 8)
    sleep(0.1)  # bad, but needed because multiprocessing
    cs.check_xp()

    cmds = vim.get_commands()
    vim.clear_commands()
    assert(len(cmds) == 1)
    assert(cmds[0] == "call s:xp_was_sent(21)")


def test_network_error():
    def fail_urlopen(req, **args):
        try:
            from urllib.error import URLError
        except ImportError:
            from urllib2 import URLError
        raise URLError("FAKE ERROR")

    from codestats import Codestats
    cs = Codestats(fail_urlopen)
    cs.log_xp("cpp", 13)
    sleep(0.1)
    cs.check_xp()

    cmds = vim.get_commands()
    vim.clear_commands()
    assert(len(cmds) == 1)
    assert(cmds[0] == "let g:codestats_error = 'FAKE ERROR'")


def _run_codestats_py():
    """Run codestats.py like Vim does it, for both Python 2/3"""
    filename = 'plugin/codestats.py'
    scope = sys._getframe(1).f_globals
    scope['__name__'] = '__main__'  # Vim runs `pyfile` this way
    if sys.version_info.major == 2:
        execfile(filename, scope, scope)  # noqa F821
    else:
        with open(filename, 'rb') as f:
            code = compile(f.read(), filename, 'exec')
            exec(code, scope, scope)


def _stop():
    """Stop the plugin (because multiprocessing)"""
    global codestats
    del codestats


class MockHttpResponse(object):
    def read(self):
        return ""
