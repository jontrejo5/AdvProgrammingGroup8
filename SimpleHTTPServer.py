import SimpleHTTPServer
import SimpleWebSocketServer

PORT = 8000

Handler = SimpleHTTPServer.Handler

httpd = SimpleWebSocketServer.TCPServer(("", PORT), Handler)

print ("serving at port", PORT)
httpd.serve_forever()