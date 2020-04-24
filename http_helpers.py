from asyncio import Protocol
from base64 import standard_b64decode
from http.server import BaseHTTPRequestHandler
from io import BytesIO, StringIO
from mimetypes import guess_type
from urllib.parse import unquote_plus, urlparse

import json

from csv import import_csv
from gort.gort_types import *

# Nasty little hack to let the stdlib parse the request
class HTTP_Handler (BaseHTTPRequestHandler):
    # Manually build the handler around a bytes object and a transport.
    # Necessary because the Server in asyncio accepts a Protocol factory
    # in the constructor which is separate from the request handlers
    # used in the http.server module.
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

    # Update the handler's data to have all the body
    def update_data (self, data, index):
        self.rfile = BytesIO(data[index:])

    # Set error variables, but don't actually send anything
    # (theres no client connection to write to)
    def send_error (self, error_code, error_msg, explain):
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
        )

    # Sets the payload and adds Content-Type, -Encoding, and -Length headers
    def add_payload (self, payload, type_):
        self.payload = bytes(payload)
        self.add_header('Content-Type', type_[0])
        if type_[1] != None:
            self.add_header('Content-Encoding', type_[1])
        self.add_header('Content-Length', len(self.payload))

    # Builds a basic HTML response
    def generate_html_response (self, error, msg):
        self.add_response_line(error)
        self.add_payload(
            (
                f'<html>\n'
                f'{error} {self.responses[error][0]}<br/>\n'
                f'{msg}\n'
                f'</html>\n'
            ).encode(),
            ('text/html', None)
        )

    # Sends the response
    # Automatically adds the required blank line between headers and data
    # If no payload data, add 'Content-Length: 0' header
    # Also add the 'Connection: close' to tell client the socket will close
    # Reset the response and payload variables
    def send_response (self):
        if self.payload == None:
            self.add_header('Content-Length', 0)

        self.add_header('Connection', 'close')

        response = (
            f'{self.response}\r\n'.encode()
            + (self.payload if self.payload else b'')
        )
        self.transport.write(response)

        self.response = ''
        self.payload = None

    # Validates the POST headers
    # Checks for Content-Length header
    # Checks if the Content-Type matches
    # Checks if the Content-Encoding matches, default is no encoding
    def validate_POST_headers (self, type_, encoding=None):
        # Test for Content-Length header
        # If missing, send 411 Length Required
        if self.headers['content-length'] == None:
            self.generate_html_response(
                411,
                'Content-Length required'
            )
            self.send_response()
            return False

        # Test the Content-Type
        # If incorrect, send 415 Unsupported Media
        if self.headers['content-type'] != type_:
            self.generate_html_response(
                415,
                f'Unsuported type: {self.headers["content-type"]}'
            )
            self.send_response()
            return False

        # Test the encoding if given
        # If incorrect encoding, send 422 Unprocessable Entity
        if encoding != None and self.headers['content-encoding'] != encoding:
            self.generate_html_response(
                422,
                f'Unsuported encoding: {self.headers["content-encoding"]}'
            )
            self.send_response()
            return False

        # All tests passed
        return True

    # Handle incoming GET and HEAD requests, default is GET
    def do_GET (self, is_HEAD=False):
        payload = None
        pl_type = None
        implicit_index = False

        # Open the file from the request, send a 303 or send a 404
        try:
            pl_file = None
            if self.parse_result.path == '/':
                implicit_index = True
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
            self.generate_html_response(404, self.parse_result.path)
            # Remove payload if HEAD request
            if is_HEAD:
                self.payload = b''
            self.send_response()
        else:
            # Builds and sends the response
            # For implicit index, send 303 See Other if >=HTTP/1.1
            # Send 302 Found <HTTP/1.1
            # Add the Location header
            if implicit_index:
                if float(self.request_version.split('/')[1]) >= 1.1:
                    self.add_response_line(303)
                else:
                    self.add_response_line(302)
                self.add_header('Location', '/index.html')
            else:
                self.add_response_line(200)
                self.add_payload(payload, pl_type)
            # Remove payload if HEAD request
            if is_HEAD:
                self.payload = b''
            self.send_response()

    # Handle incoming POST requests
    def do_POST (self):
        payload = None
        pl_type = None

        # CSV data passed in:
        #   Content-Type: text/csv
        #   Content-Encoding: base64
        #   Content-Length: [length of encoded data]
        if self.parse_result.path == '/post_csv':
            # Validate the headers for CSV data
            if not self.validate_POST_headers('text/csv', 'base64'):
                return

            length = int(self.headers['content-length'])
            post_data = self.rfile.read(length)
            post_str = standard_b64decode(post_data).decode()
            csv_entries = import_csv(StringIO(post_str))
            students = []
            # Turn into array of Student
            for c in csv_entries:
                students.append(Student(
                    f'{c.fname} {c.lname}',
                    c.lname,
                    c.fname,
                    c.age,
                    # TODO: instrument
                    0,
                    c.book,
                    # TODO: prefTeach
                    0
                ))

            # Print to stdout for now
            for s in students:
                print(s)

            # Send 204 No Content
            self.add_response_line(204)
            self.send_response()
        # Constraint data passed in
        #   Content-Type: application/json
        #   Content-Length: [length of JSON data]
        elif self.parse_result.path == '/post_constraints':
            # Validate the headers for JSON data
            if not self.validate_POST_headers('application/json'):
                return

            # Read the JSON data
            post_json = json.load(self.rfile)
            # Print to stdout for now
            print(post_json)

            # Send 204 No Content
            self.add_response_line(204)
            self.send_response()
        # Invalid target, send 400 Bad Request
        else:
            self.generate_html_response(
                400,
                f'Invalid target: {self.parse_result.path}'
            )
            self.send_response()

    # Handles unknown request types
    # Sends a 405 Method Not Allowed
    def do_UNK (self):
        self.generate_html_response(
            405,
            f'Unsupported method: {self.command}'
        )
        self.add_header('Allow', 'GET, HEAD, POST')
        self.send_response()

    # Override the method from BaseHTTPRequestHandler because the way the
    # request is passed in and dealt with is different
    def handle_one_request (self):
        # Test for Range header
        # If found, send 501 Not Implemented
        if self.headers['range']:
            self.generate_html_response(
                501,
                'Byte serving not available'
            )
            self.send_response()
            return

        # Test the different methods
        if self.command == 'GET':
            self.do_GET()
        elif self.command == 'HEAD':
            self.do_GET(is_HEAD = True)
        elif self.command == 'POST':
            self.do_POST()
        else:
            self.do_UNK()

# Bridge between the HTTP_Handler class and the asyncio Server system
class HTTP_Protocol (Protocol):
    # Pass the root directory of the webapp to the rest of the system
    def __init__ (self, webapp_root):
        self.webapp_root = webapp_root
        self.data = bytes()
        self.handler = None
        self.total = 0

    # Run every time a connection is made
    def connection_made (self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        print(f'Connection from: {self.peername}')

    # Run whenever the server recieves data
    # Waits for all data to be recieved before continuing
    def data_received (self, data):
        # Append the data recieved
        self.data += bytes(data)
        body_start = self.data.find(b'\r\n\r\n') + 4

        # Set up handler once all the headers have been recieved
        # find() returns -1 if not found, +4 for the entire 4 byte delimiter
        if self.handler == None and body_start > 3:
            self.handler = HTTP_Handler(self.data, self.transport,
                self.webapp_root)
            # Close connection if handler setup fails
            if self.handler.error_code:
                print(
                    f'Error code: {self.hadler.error_code}'
                    f' {self.handler.error_message}'
                )
                self.transport.close()
                print(f'Closed connection with: {self.peername}')
                return
            # body_start is the length of the request line + headers
            # Content-Length gives the body length
            cont_len = self.handler.headers['content-length']
            self.total = body_start + (int(cont_len) if cont_len else 0)

        # Handle the request once the entire body is recieved
        if self.handler and len(self.data) >= self.total:
            self.handler.update_data(self.data, body_start)
            self.handler.handle_one_request()

    # Run once when the connection is lost or closed
    def connection_lost (self, exc):
        self.transport.close()
        print(f'Closed connection with: {self.peername}')
