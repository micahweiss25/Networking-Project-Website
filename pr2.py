from http import server
import time
import os

hostName = "10.4.84.56"
serverPort = 80

global dir_list
cur_path = os.getcwd()
dir_list = os.listdir(cur_path)

global moved_dict
with open("moved", "r") as f:
    moved_dict = {y[0]: y[1] for y in [x.split(" ") for x in f.read().split("\n")]}
    print(moved_dict)



global lastModified
lastModified = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())



# https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming I used this web page that I found when working on a side project. I used the code to figure out how to format the get request.
# https://docs.python.org/3/library/http.server.html I don't think I have to site python docs, but I used this site ase well
# https://www.life.illinois.edu/edtech/html/styles/ I used this link to figure out static css formating
# https://www.w3schools.com/html/default.asp used this cite to learn how to format text

class MyServer(server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        ts = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        if self.path == '/' or self.path == '/index.html':
            with open('templates/windows.html', 'rb') as f:
                self.custom_headers(ts, f.read(), 200, "text/html", False)
        else:
            try:
                with open(self.path[1:], 'rb') as f:
                    ext = os.path.splitext(self.path.split("/")[-1])[1]
                    self.custom_headers(ts, f.read(), 200, ext, False)
            except:
                if self.path[1:] in list(moved_dict.keys()):
                    self.send_header("Location", moved_dict[self.path[1:]])
                    self.send_error(301, "Moved Permanently")
                else:
                    self.send_error(404, "File Not Found")

    def do_GET(self):
        print(cur_path)
        ts = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        print(f"file path: {self.path}")
        if self.path == '/' or self.path =='/index.html':
            with open('templates/windows.html', 'rb') as f:
                self.custom_headers(ts, f.read(), 200, ".html", True)
        else:
            try:
                with open(self.path[1:], 'rb') as f:
                    ext = os.path.splitext(self.path.split("/")[-1])[1]
                    self.custom_headers(ts, f.read(), 200, ext, True)
            except:
                if self.path[1:] in list(moved_dict.keys()):
                    self.send_header("Location", moved_dict[self.path[1:]])
                    self.send_error(301, f"Moved Permanently to {moved_dict[self.path[1:]]}")
                else:
                    self.send_error(404, "File Not Found")

    def custom_headers(self, ts, webFile, response, content_type, get):
        if "If-Modified-Since" in self.headers and self.headers["If-Modified-Since"] == ts:
            self.send_response(304)
            self.end_headers()
        else:
            self.send_response(response)
            if content_type == ".jpg":
                self.send_header("Content-type", "image/jpg")
            elif content_type == ".css":
                self.send_header("Content-type", "text/css")
            elif content_type == ".gif":
                self.send_header("Content-type", "image/gif")
            elif content_type == ".html":
                self.send_header("Content-type", "text/html")
            elif content_type == ".mp4":
                self.send_header("Content-type", "video/mp4")
            else:
                self.send_error(404, "unknown extension")
            #self.send_header("Date", ts)
            #self.send_header("Server", "BaseHTTP/0.6 Python/3.8.10")
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