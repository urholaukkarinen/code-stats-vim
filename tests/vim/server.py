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
        assert re.match(r'code-stats-vim/\d+\.\d+\.\d+(-.*)?',
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
        # if url is /123/api/... respond with 123
        try:
            code = int(self.path[1:4])
        except ValueError:
            code = self.code
        self.send_response(code)
        self.end_headers()
        self.wfile.write(b"Response message from test_server.py")

        # check response (doesn't fail if we crash here)
        self.assert_valid_request_headers()
        self.assert_valid_request_body()


def run():
    server_address = ('', 38080)
    with HTTPServer(server_address, RequestHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    run()
