"""A tiny programmable HTTP server so client behaviour can be tested offline."""

import json
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class StubServer:
    def __init__(self):
        self.requests = []          # list of dicts: method, path, headers, body
        self._queue = deque()       # programmed responses, consumed in order
        self.default = (200, {"ok": True}, {}, 0.0)
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def _handle(self):
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
                stub.requests.append({"method": self.command, "path": self.path,
                                      "headers": dict(self.headers), "body": body})
                status, payload, headers, delay = stub._queue.popleft() if stub._queue else stub.default
                if delay:
                    time.sleep(delay)
                data = json.dumps(payload).encode()
                try:
                    self.send_response(status)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(data)))
                    for k, v in headers.items():
                        self.send_header(k, v)
                    self.end_headers()
                    self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):
                    pass  # client gave up (timeout test)

            do_GET = do_POST = do_PUT = do_DELETE = _handle

            def log_message(self, *args):
                pass

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def enqueue(self, status=200, payload=None, headers=None, delay=0.0):
        self._queue.append((status, {} if payload is None else payload, headers or {}, delay))
        return self

    def start(self):
        self._thread.start()
        return self

    def stop(self):
        self._server.shutdown()
        self._server.server_close()
