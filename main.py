#!/usr/bin/env python3

from objects import MusicClass, ElectiveClass
from http_helpers import HTTP_Protocol
import asyncio as aio
import sys

import csv

if sys.version_info < (3, 7):
    print('Please update to Python 3.7 or newer.')
    exit(37)

async def main():
    # Create the backend server object using a custom HTTP handler
    hostname = "127.0.0.1"
    port = 80
    loop = aio.get_running_loop()
    server = await loop.create_server(lambda: HTTP_Protocol(),
        hostname, port, start_serving = False)

    async with server:
        await server.serve_forever();

if __name__ == "__main__":
    if sys.version_info >= (3, 7):
        aio.run(main())
