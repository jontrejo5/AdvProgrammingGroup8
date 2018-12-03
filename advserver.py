from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import time
import threading
import socket
import os
import time

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

    def do_GET(self):
        paths = {
            '/home': {'status': 200},
            '/': {'status': 200}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    # setup the header, then if the client accepts it, display the content
    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


        # open file



        try:
            if path == "/":
                with open(os.getcwd() + '/views/home.html', 'r') as htmlfile:
                    content = htmlfile.read().replace('\n', '')
            else:
                with open(os.getcwd() + '/views/' + path + '.html', 'r') as htmlfile:
                    content = htmlfile.read().replace('\n', '')
        except IOError as e:
            with open(os.getcwd() + '/views/error.html', 'r') as htmlfile:
                content = htmlfile.read().replace('\n', '')

        # content = '''
        # <html><head><title>Title goes here.</title>
        # <link rel='icon' href='favicon.ico' type='image/x-icon'/</head>
        # <body><p>This is a test.</p>
        # <p>You accessed path: {}</p>
        # </body></html>
        # '''.format(path)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)


# define the lock for threading
serv_lock = threading.Lock()

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), handler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))

    # secure the socket connection via
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='host.key', certfile='host.cert', server_side=True)

    try:
        t = threading.Thread(httpd.serve_forever())
        t.start()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))



