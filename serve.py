import http.server
import socketserver
import os

PORT = 8004
DIRECTORY = "_build/html"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def serve():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(DIRECTORY):
        print("Error: _build/html directory not found. Please build the book first with:")
        print("jupyter-book build .")
    else:
        serve()