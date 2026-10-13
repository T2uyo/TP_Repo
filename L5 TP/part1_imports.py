
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import time
#ex1
import requests
print(requests.__version__)
import urllib.request
#requests a avut nevoie de pip install pentru ca este o biblioteca externa
#iar urllib face parte din biblioteca standard

#ex2
from requests import get
response = requests.get(BASE_URL, timeout=TIMEOUT)
print(response.status_code)

#avantajul la import requests este ca se vede clar de unde vine functia
#deci codul e mai usor de inteles si nu exista conflicte de nume
#avantaj la from requests import get este ca scriem mai putin, apeland direct get()

#ex 3
import requests as rq
responsse = rq.get(BASE_URL, timeout=TIMEOUT)
print(response.status_code)
#Alias este util cand numele e lung si repetat
#face codul mai greu de citit cand aliasul e obscur si nu se stie ce reprezinta
time.sleep(1)

#ex4
import urllib.request
import ssl
import certifi

context = ssl.create_default_context(cafile=certifi.where())
cerere = urllib.request.Request(BASE_URL, headers={"User-Agent": "WebLab"})
with urllib.request.urlopen(cerere, timeout=TIMEOUT, context=context) as resp:
    print(resp.status)
    corp = resp.read().decode("utf-8")
    print(corp[:200])
time.sleep(1)

#ex5
print(dir(requests))
# get = functie, session = clasa, exeptions = modul

#ex6
help(requests.get(BASE_URL, timeout=5))
time.sleep(1)

start = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
final = time.perf_counter()
print(final - start)
print(response.elapsed.total_seconds())
#perf_counter masoara tot timpul scurs in cod, inclusiv procesarea de catre requests;
#elapsed masoara doar de la trimiterea cererii pana la primirea antetelor raspunsului.

try:
    import bs4
except ImportError:
    print("instaleaza modulul")