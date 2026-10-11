import hashlib
import json
import re
import socket
import ssl
import time
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import certifi
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

#ex35
parsat = urlparse("https://cybercor.org/path?x=1#top")
print(parsat.scheme, parsat.netloc, parsat.path, parsat.query, parsat.fragment)

#ex36
for legatura in ["/about", "contact.html", "../index.html"]:
    print(urljoin(BASE_URL, legatura))

#ex37
def extract_links(html:str ) -> list:
    legaturi = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(legaturi))

pagina = requests.get(BASE_URL, timeout=TIMEOUT)
links = extract_links(pagina.text)
print(len(links), "legaturi gasite")
time.sleep(1)

#ex38
def split_links(links: list, domain: str) -> tuple:
    interne, externe = [], []
    for link in links:
        complet = urljoin("https://" + domain, link)
        if urlparse(complet).netloc == domain:
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe

interne, externe = split_links(links, "cybercor.org")
print(len(interne), "interne,", len(externe), "externe")

#ex39
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")

finder = ImageFinder()
finder.feed(pagina.text)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)
print(pagina.text.lower().count("<img"))
time.sleep(1)

#ex40
def page_fingerprint(url:str) -> str:
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()

print(page_fingerprint(BASE_URL))
#amprentele difera daca pagina s-a schimbat intre cereri
time.sleep(1)

#ex41
response = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json","w", encoding="utf-8") as fisier:
    json.dump(dict(response.headers), fisier, indent=2)

with open("headers.json", encoding="utf-8") as fisier:
    antete = json.load(fisier)
print(antete.get("Content-Type"))

#ex42
def resolve(hostname:str) -> str:
    return socket.gethostbyname(hostname)

print(resolve("cybercor.org"))

#ex43
def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context(cafile=certifi.where())
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificat = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(certificat["notAfter"])
    return int((expira - time.time()) / 86400)

print(cert_days_left("cybercor.org"))
