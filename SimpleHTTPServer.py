from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import time
import threading
import socket
import os

HOST_NAME = 'localhost'
PORT_NUMBER = 5000

# handler is a process that runs in response to a request
class handler(BaseHTTPRequestHandler):

    # setup headers for server requests
    def do_HEAD(self):

        # HTML response code: OK
        self.send_response(200)
        # https://www.stubbornjava.com/posts/what-is-a-content-type
        self.send_header('Content-type', 'text/html')
        # end the header setup
        self.end_headers()

    # get the path
    def do_GET(self):

        if self.path =='/':
            self.path = "../views/home.html"


        try:
            sendReply = False

            if self.path.endswith("html"):
                mimetype ='text/html'
                sendReply = True
            return

        except IOError:
            self.send_error(404,"File Not Found: ")

    # setup the header, then if the client accepts it, display the content
    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        content = "<html><header><title>This is library</title></header><body>hello</body></html>".format(path)
        return bytes(content, 'UTF-8')
    #
    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)




if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), handler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))

    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='host.key', certfile='host.cert', server_side=True)

    httpd.serve_forever()

    try:
        threading.Thread(httpd.serve_forever())
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))



