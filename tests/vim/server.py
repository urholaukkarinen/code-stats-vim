"""A trivial mock server for integration tests

- validates requests
- responds with given code"""

import re
import json
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    code = 200

    # disable logging
    def log_message(self, format, *args):
        return

    def assert_valid_request_headers(self):
        assert re.match('code-stats-vim/\d+\.\d+\.\d+(-.*)?',
                        self.headers['user-agent'])
        assert self.headers['X-Api-Token'] == 'MOCK_API_KEY'

    def assert_valid_request_body(self):
        content_length = int(self.headers['content-length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        assert len(data) == 2

        # strip timezone, it's local time anyway
        timestamp = datetime.strptime(data['coded_at'][:-6],
                                      '%Y-%m-%dT%H:%M:%S')
        timediff = datetime.now() - timestamp
        assert timediff < timedelta(minutes=1)

        xps = data['xps']
        assert len(xps) == 1
        assert xps[0]['language'] == 'automatedtest'
        assert xps[0]['xp'] == 13

    def do_POST(self):
        # respond in any case
        self.send_response(self.code)
        self.end_headers()
        self.wfile.write(b"Response message from test_server.py")

        # check response (doesn't fail if we crash here)
        self.assert_valid_request_headers()
        self.assert_valid_request_body()


def run(_code=200):
    class HttpCodeHandler(RequestHandler):
        code = _code

    server_address = ('', 38080)
    httpd = HTTPServer(server_address, HttpCodeHandler)
    # only handle one request
    httpd.handle_request()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(int(argv[1]))
    else:
        run()
