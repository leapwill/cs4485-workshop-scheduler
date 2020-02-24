from http.server import BaseHTTPRequestHandler
from io import BytesIO
import asyncio as aio

# Nasty little hack to let the stdlib parse the request
class HTTP_Request (BaseHTTPRequestHandler):
    # Build the handler around input string instead of a connection
    def __init__ (self, request):
        self.rfile = BytesIO(request)
        self.raw_requestline = self.rfile.readline()
        self.error_code = None
        self.error_message = None
        self.parse_request()

    # Set error variables, but don't actually send anything
    # (theres no client connection to write to)
    def send_error (self, error_code, error_msg):
        self.error_code = error_code
        self.error_message = error_msg

# Handler for an HTTP request
class HTTP_Protocol (aio.Protocol):
    # Run every time a connection is made
    def connection_made (self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        print("Connection from: {}".format(self.peername))

    # Run whenever the server recieves a request
    def data_received (self, data):
        msg = data.decode()
        request = HTTP_Request(data)
        print("Request type: {}".format(request.command))
        # Text to display
        response_txt = (
            '<html>'
            'Request type: ' + request.command + ''
            '</html>'
        )
        # Builds the response
        response = (
            f'{request.request_version} 200 OK\r\n'
            f'Content-Length: {len(response_txt)}\r\n'
            '\r\n'
            f'{response_txt}\r\n'
            '\r\n'
        )
        # Sends the response back to the client
        self.transport.write(response.encode())

    # Run once when the client closes the connection
    def eof_received (self):
        print("Cloosed connection with: {}".format(self.peername))
        self.transport.close()
