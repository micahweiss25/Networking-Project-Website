import time
from http.client import HTTPConnection
host = '127.0.0.1'
H1 = HTTPConnection(host, 8080)
# send not modified since header
#ts = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
ts = "Thu, 01 Jan 1970 00:00:00 GMT".encode("utf-8")
extraHeaders = {"If-Modified-Since": ts}
H1.request('GET', '/', headers=extraHeaders)

response = H1.getresponse()
data = response.read().decode("utf-8")
print(data)
print(response.status, response.reason)