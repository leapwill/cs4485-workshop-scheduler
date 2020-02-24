from http.server import BaseHTTPRequestHandler
from io import BytesIO
import asyncio as aio

class HTTP_Request (BaseHTTPRequestHandler):
    def __init__ (self, request):
        self.rfile = BytesIO(request)
        self.raw_requestline = self.rfile.readline()
        self.error_code = None
        self.error_message = None
        self.parse_request()

    def send_error (self, error_code, error_msg):
        self.error_code = error_code
        self.error_message = error_msg

class HTTP_Protocol (aio.Protocol):
    def connection_made (self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        print("Connection from: {}".format(self.peername))

    def data_received (self, data):
        msg = data.decode()
        request = HTTP_Request(data)
        print("Request type: {}".format(request.command))
        response_txt = (
            '<html>'
            'Request type: ' + request.command + ''
            '</html>'
        )
        response = (
            f'{request.request_version} 200 OK\r\n'
            f'Content-Length: {len(response_txt)}\r\n'
            '\r\n'
            f'{response_txt}\r\n'
            '\r\n'
        )
        self.transport.write(response.encode())

    def eof_received (self):
        print("Cloosed connection with: {}".format(self.peername))
        self.transport.close()
