import time
import requests
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

#ex9
response = requests.get(BASE_URL, timeout =TIMEOUT)
print(response.status_code) #atribut
print(response.ok)          #atribut
print(response.url)         #atribut
print(response.encoding)    #atribut
time.sleep(1)

#ex10
response.raise_for_status()
try:
    r = requests.get(BASE_URL + "/this-page-doess-not-exist")
except requests.HTTPError:
    print("pagina ceruta nu exista")
time.sleep(1)

#ex11
for nume, valoare in response.headers.items():
    print(f"{nume} : {valoare}")

#ex12
print(response.headers.get("Server","lipseste"))
print(response.headers.get("Content-Type","lipseste"))
print(response.headers.get("content-type","lipseste"))
#literele mari sau mici dau acelasi rezultat, antelele nu tin cont de majuscule

#ex13
print(response.text.lower().count("cyber"))
#se pot inlantui pentru ca .lower() returneaza un sir nou, iar sirurile au metoda .count()

#ex14
html = response.text
start = html.find("<title>")
final = html.find("</title>")
print(html[start:final].strip())

#ex15
lines = html.splitlines()
print(len(lines))
print(len(max(lines, key=len)))

#ex16
if response.url.startswith("https://"):
    print("conectiune securizata")
else:
    print("conectiune nesecurizata")
time.sleep(1)

#ex17
r = requests.get("http://cybercor.org", timeout = TIMEOUT)
for pas in r.history:
    print(pas.status_code, pas.url)
print(r.url)
time.sleep(1)

#ex18
r_head = requests.head(BASE_URL, timeout = TIMEOUT)
r_get = requests.get(BASE_URL, timeout = TIMEOUT)
print(len(r_head.content))
print(len(r_get.content))
time.sleep(1)
# head aduce doar antetele, fara corp, deci lungimea o sa fie 0, get aduce si pagina

#ex19
if len(response.cookies) == 0:
    print("niciun cookie setat")
for cookie in response.cookies:
    print(cookie.name, cookie.secure)

#ex20
session = requests.Session()
session.headers.update({"User-Agent": "Weblab-T2uyo"})
r = session.get(ECHO_URL + "/headers", timeout = TIMEOUT)
print(r.text)


