from http.server import BaseHTTPRequestHandler, HTTPServer
import time


HOST_NAME = 'localhost'
PORT_NUMBER = 9000

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

        # if the requested path leades to either of these, send the following response
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        # if the path exists, then send the user to it
        if self.path in paths:
            self.respond(paths[self.path])
        # otherwise, just send a 500 status
        else:
            self.respond({'status': 500})


    # setup the header, then if the client accepts it, display the content
    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        content = "<html><header><title>This is library</title></header><body>hi</body></html>".format(path)
        return bytes(content, 'UTF-8')
    #
    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), handler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))