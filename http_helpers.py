from http.server import BaseHTTPRequestHandler
from io import BytesIO
from mimetypes import guess_type
from urllib.parse import unquote_plus, urlparse
import asyncio as aio

# Nasty little hack to let the stdlib parse the request
class HTTP_Handler (BaseHTTPRequestHandler):
    # Manually build the handler around a bytes object and a transport.
    # Necessary because the Server in asyncio accepts a Protocol factory
    # in the constructor which is separate from the request handlers
    # used in the https.server module.
    def __init__ (self, request, transport, webapp_root):
        self.transport = transport
        self.rfile = BytesIO(request)
        self.response = ''
        self.payload = None
        self.webapp_root = webapp_root

        self.raw_requestline = self.rfile.readline()
        self.error_code = None
        self.error_message = None
        self.parse_request()

        unquoted = unquote_plus(self.path)
        self.parse_result = urlparse(unquoted, allow_fragments = True)

    # Set error variables, but don't actually send anything
    # (theres no client connection to write to)
    def send_error (self, error_code, error_msg):
        self.error_code = error_code
        self.error_message = error_msg

    # Initializes a response with the proper response line
    def add_response_line (self, code):
        self.response = (
            f'{self.request_version}'
            f' {code}'
            f' {self.responses[code][0]}'
            '\r\n'
        )

    # Add miscellaneous headers
    # Format: [name]: [value]
    def add_header (self, name, value):
        self.response += (
            f'{name}:'
            f' {value}'
            '\r\n'
        );

    # Sets the payload and adds Content-Type, -Encoding, and -Length headers
    def add_payload (self, payload, type_):
        self.payload = bytes(payload)
        self.add_header('Content-Type', type_[0])
        if type_[1] is not None:
            self.add_header('Content-Encoding', type_[1])
        self.add_header('Content-Length', len(self.payload))

    # Sends the response
    # Automatically adds the required blank line between headers and data
    # Reset the response and payload variables
    def send_response (self):
        response = bytes(self.response.encode() + b'\r\n'
            + (self.payload if self.payload != None else bytes()))
        self.transport.write(response)

        self.response = ''
        self.payload = None

    # Handle incoming GET requests
    def do_GET (self):
        payload = None
        pl_type = None

        # Open the file from the request or send a 404
        try:
            pl_file = None
            if self.parse_result.path == '/':
                pl_file = open(self.webapp_root + '/index.html', mode = 'rb')
            else:
                pl_file = open(
                    self.webapp_root + self.parse_result.path,
                    mode = 'rb'
                )

            # Guess the MIME type
            pl_type = guess_type(pl_file.name)
            payload = pl_file.read()
            pl_file.close()
        except OSError as o:
            # 404 Error
            self.add_response_line(404)
            self.add_payload(
                (
                    b'<html>\r\n'
                    b'404 Not Found\r\n'
                    b'</html>\r\n'
                ),
                ('text/html', None)
            )
            self.send_response()
        else:
            # Builds and sends the response
            self.add_response_line(200)
            self.add_payload(payload, pl_type)
            self.send_response()

    # Handle incoming POST requests
    def do_POST (self):
        pass

    # Handles unknown request types
    def do_UNK (self):
        pass

    # Override the method from BaseHTTPRequestHandler because the way the
    # request is passed in and dealt with is different
    def handle_one_request (self):
        if self.command == 'GET':
            self.do_GET()
        else:
            self.do_UNK()

# Bridge between the HTTP_Handler class and the asyncio Server system
class HTTP_Protocol (aio.Protocol):
    # Pass the root directory of the webapp to the rest of the system
    def __init__ (self, webapp_root):
        self.webapp_root = webapp_root

    # Run every time a connection is made
    def connection_made (self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        print(f'Connection from: {self.peername}')

    # Run whenever the server recieves a request
    def data_received (self, data):
        handler = HTTP_Handler(data, self.transport, self.webapp_root)
        if handler.error_code == None:
            handler.handle_one_request()
        else:
            print(f'Error code: {hadler.error_code} {handler.error_message}')

    # Run once when the client closes the connection
    def eof_received (self):
        self.transport.close()
        print(f'Closed connection with: {self.peername}')
