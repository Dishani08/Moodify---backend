
#!/usr/bin/env python3
"""
One-shot test script that exercises all Moodify functionality once and exits
"""
import os
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer

HOST = '127.0.0.1'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class OneShotHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the file
        super().do_GET()
        # If this request is for root or index.html, signal main thread once
        if not getattr(self.server, "page_requested", False):
            if self.path in ('/', '/index.html'):
                self.server.page_requested = True
                self.server.request_event.set()
                print(f"[run_once] Detected page request: {self.path}")


def main():
    cwd = os.getcwd()
    try:
        server = HTTPServer((HOST, PORT), OneShotHandler)
    except OSError as e:
        print(f"Failed to bind {HOST}:{PORT} — {e}")
        print("Try a different port: python run_once.py 8080")
        return

    server.request_event = threading.Event()
    server.page_requested = False

    serve_thread = threading.Thread(target=server.serve_forever, daemon=True)
    serve_thread.start()

    url = f'http://{HOST}:{PORT}/'
    print(f"Serving folder {cwd} at {url}")
    try:
        webbrowser.open(url)
    except Exception:
        print(f"Open the URL manually: {url}")

    print("Waiting for a page request (GET / or GET /index.html)...")
    server.request_event.wait()  # wait until handler signals first request

    print("Page was requested. The server will keep running until you press Enter.")
    try:
        input("Press Enter to shut down the server...")
    except KeyboardInterrupt:
        print("\nInterrupted, shutting down.")

    server.shutdown()
    serve_thread.join()
    print("Server stopped.")


if __name__ == '__main__':
    main()