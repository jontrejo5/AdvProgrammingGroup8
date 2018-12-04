from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import time
import threading
import socket
import os
import time
import mistune
import cgi
import glob

# HOST_NAME = 0.0.0.0 makes it so that it serves on every interface
HOST_NAME = '0.0.0.0'
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

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })


        page_save(form.getvalue("page-name"),form.getvalue("page-edit"))
        # Begin the response
        self.send_response(301)
        self.send_header('Location', '/page/' + form.getvalue("page-name"))
        self.end_headers()

    # setup the header, then if the client accepts it, display the content
    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


        # open file


        # make the processing take a long time to test multithreading
        # time.sleep(5)
        print(path)

        try:
            if path == "/":
                with open(os.getcwd() + '/views/home.html', 'r') as htmlfile:
                    content = htmlfile.read().replace('\n', '')

            elif path[:5] == '/page':
                with open(os.getcwd() + '/views/' + path + '.md', 'r') as mdfile:
                    mdparsed = mistune.markdown(mdfile.read())
                with open(os.getcwd() + '/views/template.html', 'r') as htmlfile:
                    content = htmlfile.read().replace('\n', '').replace('<!-- ~!BODY!~ -->', mdparsed)\
                                             .replace('<!-- ~!TITLE!~ -->', path.split('/')[2].replace('_', ' '))
            elif path[:5] == '/edit':
                with open(os.getcwd() + '/views/page/' + path.split('=')[1] + '.md', 'r') as mdfile:
                    md = mdfile.read()
                with open(os.getcwd() + '/views/edit.html', 'r') as htmlfile:
                    if __name__ == '__main__':
                        content = htmlfile.read().replace('\n', '').replace('<!-- ~!MDEDIT!~ -->', md)\
                                                                   .replace('<!-- ~!NAME!~ -->', path.split('=')[1])
            elif path == '/categories':
                l = dir_list_html(os.getcwd() + "/views/page")
                with open(os.getcwd() + '/views/categories.html', 'r') as htmlfile:
                    content = htmlfile.read().replace('\n', '').replace('<!-- ~!DIRLIST!~ -->', l)

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

def page_save(page_name, page_data):
    with open(os.getcwd() + '/views/page/' + page_name + '.md', 'w') as page:
            page.write(page_data)


def dir_list_html(dir):
    out = ""
    l = glob.glob(dir + "/*.md")

    for f in l:
        out += "<a href=\"page/" + f.split('/')[-1][:-3] + "\">"+ f.split('/')[-1][:-3].replace('_',' ') + "<br>"

    print (out)

    return out





# define the lock for threading
serv_lock = threading.Lock()

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), handler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))

    # secure the socket connection via
    # httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='host.key', certfile='host.cert', server_side=True)

    try:
        while True:
            # this is like 'accept' for sockets
            req, addr = httpd.get_request()

            # make sure the request is OK
            if httpd.verify_request(req, addr):
                # process the request on a new thread and continue on
                threading.Thread(target=httpd.process_request, args=(req, addr)).start()

    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))


