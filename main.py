#!/usr/bin/env python3

from http_helpers import HTTP_Protocol
import asyncio as aio
import sys

if sys.version_info < (3, 7):
    print('Please update to Python 3.7 or newer.')
    exit(37)


async def main():
    # Create the backend server object using a custom HTTP handler
    hostname = '127.0.0.1'
    port = 8080
    webapp_root = './webapp/'
    loop = aio.get_running_loop()
    server = await loop.create_server(lambda: HTTP_Protocol(webapp_root),
                                      hostname, port, start_serving=False)

    # Begin accepting connections
    # `async with` block automatically handles cleanup on close
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    if sys.version_info >= (3, 7):
        aio.run(main())
