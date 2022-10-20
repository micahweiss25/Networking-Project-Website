from http.client import HTTPConnection
import re
host = 'robert.ryan.cs484.eecs.net'
H1 = HTTPConnection(host, 80)
H1.request('GET', '/')
response = H1.getresponse()
print(response.status, response.reason)

data = response.read().decode("utf-8")
with open('downloads/index.html', 'w') as f:
    f.write(data)
links = re.findall("href=\".*?\"|src=\".*?\"", data)
links = [link.replace("href=\"", "").replace("src=\"", "").replace("\"", "") for link in links]
print(links)
for link in links:
    if link[0] != '/': link = '/images/' + link 
    H2 = HTTPConnection(host, 80)
    H2.request('GET', link)
    response = H2.getresponse()
    print(response.status, response.reason)
    data = response.read()
    with open("downloads/"+link.replace("/", "_"), "wb") as f:
        f.write(data)