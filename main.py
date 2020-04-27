#!/usr/bin/env python3

from http_helpers import HTTP_Protocol
import asyncio as aio
import sys
import webbrowser

if sys.version_info < (3, 7):
    print('Please update to Python 3.7 or newer.')
    exit(37)

# Open the page in the browser
async def open_browser (hostname, port):
    webbrowser.open_new_tab(f'http://{hostname}:{port}')

async def main ():
    # Create the backend server object using a custom HTTP handler
    hostname = '127.0.0.1'
    port = 8080
    webapp_root = './webapp/'
    loop = aio.get_running_loop()
    server = await loop.create_server(lambda: HTTP_Protocol(webapp_root),
                                      hostname, port, start_serving=False)
    start_server = aio.create_task(server.serve_forever())
    start_browser = aio.create_task(open_browser(hostname, port))

    print(f'Open the website at http://{hostname}:{port}')

    # Begin accepting connections
    await start_server
    # Open the page
    await start_browser

if __name__ == '__main__':
    if sys.version_info >= (3, 7):
        aio.run(main())
