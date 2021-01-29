from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import threading


class RSSRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        paths = {
            '/rss': self.handle_rss
        }

        handler = paths.get(self.path)
        if handler:
            handler()
        else:
            self.send_response(404)

    def handle_rss(self):
        with open('./rss/tests/guardian_rss.xml') as f:
            data = f.read()
        self.write_response(data)

    def write_response(self, body, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/xml')
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        # prevent from printing logs during tests
        return


class RSSMockServer:
    def __init__(self, port=None):
        self.port = port or self.get_free_port()
        self.server = HTTPServer(('localhost', self.port),
                                 RSSRequestHandler)

    @staticmethod
    def get_free_port():
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        return port

    @property
    def address(self):
        return f'http://localhost:{self.port}'

    def start(self):
        self.process = threading.Thread(
            target=self.server.serve_forever,
            daemon=True
        )
        self.process.start()

    def shutdown(self):
        self.server.server_close()
        self.server.shutdown()
        self.process.join()
