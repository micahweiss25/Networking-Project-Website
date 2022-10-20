from http import server
import time

hostName = "localhost"
serverPort = 8080


global lastModified
lastModified = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
# https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming I used this web page that I found when working on a side project. I used the code to figure out how to format the get request.
# https://docs.python.org/3/library/http.server.html I don't think I have to site python docs, but I used this site ase well
# https://www.life.illinois.edu/edtech/html/styles/ I used this link to figure out static css formating
class MyServer(server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        ts = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        if self.path == '/':
            with open('templates/index.html', 'rb') as f:
                self.custom_headers(ts, f.read(), 200, "text/html", False)
        elif self.path == "/willy_wonka.gif":
            with open("content/willy_wonka.gif", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "image/gif", False)
        elif self.path == '/image1':
            with open("templates/image1.jpg", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "image/jpeg", False)
        elif self.path == '/superSecret':
            with open("templates/superSecret.html", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "text/html", False)
        elif self.path == '/dank_gif.gif':
            with open("content/dank_gif.gif", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "image/gif", False)
        else:
            self.send_error(404, f'File Not Found: {self.path}')

    def do_GET(self):
        ts = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        if self.path == '/':
            with open('templates/index.html', 'rb') as f:
                self.custom_headers(ts, f.read(), 200, "text/html", True)
        elif self.path == "/willy_wonka.gif":
            with open("content/willy_wonka.gif", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "image/gif", True)
        elif self.path == "/image1":
            with open("templates/image1.jpg", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "image/jpeg", True)
        elif self.path == '/superSecret':
            with open("templates/superSecret.html", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "text/html", True)
        elif self.path == "/dank_gif.gif":
            with open("content/dank_gif.gif", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "image/gif", True)
        elif self.path == "/respect_the_drip.css":
            with open("static/respect_the_drip.css", "rb") as f:
                self.custom_headers(ts, f.read(), 200, "text/css", True)
        else:
            self.send_error(404, f'File Not Found: {self.path}')
    def custom_headers(self, ts, webFile, response, content_type, get):
        if "If-Modified-Since" in self.headers and self.headers["If-Modified-Since"] == ts:
            self.send_response(304)
            self.end_headers()
        else:
            self.send_response(response)
            #self.send_header("Date", ts)
            #self.send_header("Server", "BaseHTTP/0.6 Python/3.8.10")
            self.send_header("Content-type", content_type)
            self.send_header("Connection", "close")
            self.send_header("Last-Modified", lastModified)
            self.send_header("Content-Length", len(webFile))
            self.end_headers()
            if get:
                self.wfile.write(webFile)


def run(server_class=server.HTTPServer, handler_class=MyServer):
    server_address = hostName, serverPort
    httpd = server_class(server_address, handler_class)
    print(f"Serving website at {hostName}:{serverPort}")
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
    server.httpd.server_close()