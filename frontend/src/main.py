"""Main file"""

import os
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

PATH: str = "./"
PORT: int = 3000


def main():
    '''Main function: start frontend server'''

    if os.path.exists(PATH) is False:
        print(f"Path {PATH} not found. Currently executing from {os.getcwd()}")
        sys.exit(1)

    server_partial: partial[SimpleHTTPRequestHandler] = partial(
        SimpleHTTPRequestHandler, directory=PATH)

    server = HTTPServer(("0.0.0.0", PORT), server_partial)

    print(f"Serving at port {PORT}")

    server.serve_forever()


if __name__ == "__main__":
    main()
