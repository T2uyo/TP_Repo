import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

#ex21&23
def fetch(url,timeout=10):
   return requests.get(url,timeout=timeout)

#ex22
def get_status(url: str) -> int:
    return requests.get(url,timeout=TIMEOUT).status_code

#ex24&25
def get_title(html: str) -> str:
    """Returnează titlul paginii din șirul HTML primit (fără rețea)."""
    start = html.find("<title>") + len("<title>")
    final = html.find("</title>")
    return html[start:final]

print(get_title(fetch(BASE_URL).text))
help(get_title)

#ex26
try:
    get_status(123)
except requests.RequestException as e:
    print("eruare", e)

#ex27
def page_exists(url:str) -> bool:
    try:
        return requests.get(url,timeout=TIMEOUT).ok
    except requests.RequestException:
        return False

print(page_exists(BASE_URL))
print(page_exists("https://this-domain-does-not-exist.invalid"))
time.sleep(1)

#ex28
def check_paths(base,paths):
    rezultat = {}
    for cale in paths:
        rezultat[cale] = get_status(base + cale)
        time.sleep(1)
    return rezultat

print(check_paths(BASE_URL,["/","/robots.txt","/sitemap.xml"]))

#ex29
def get_header(url:str, name:str, default:str = "lipseste") -> str:
    return requests.get(url,timeout=TIMEOUT).headers.get(name,default)

print(get_header(BASE_URL, name="Server"))
time.sleep(1)

#ex30
def security_headers(url:str) -> dict:
    antete = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]
    raspuns = requests.get(url, timeout=TIMEOUT)
    return {a: a in raspuns.headers for a in antete}

print(security_headers(BASE_URL))
time.sleep(1)

#ex31
def score_headers(results:dict) -> str:
    return f"{sum(results.values())}/{len(results)}"

print(score_headers(security_headers(BASE_URL)))
time.sleep(1)

#ex32
def fetch_robots(base:str):
    try:
        r = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    except requests.RequestException:
        return None
    return r.text if r.ok else None

def disallowed_paths(robots_text:str) -> list:
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        linie = linie.strip()
        if linie.lower().startswith("disallow"):
            valoare = linie.split(":", 1)[1].strip()
            if valoare:
                cai.append(valoare)

    return cai

print(disallowed_paths(fetch_robots(BASE_URL)))
print(disallowed_paths(None))
time.sleep(1)

#ex33
def response_times(*urls:str) -> dict:
    timpi = {}
    for url in urls:
        start = time.perf_counter()
        requests.get(url, timeout=TIMEOUT)
        timpi[url] = time.perf_counter() - start
        time.sleep(1)
    return timpi

print(response_times(BASE_URL, BASE_URL + "/robots.txt"))

#ex34
def log(message, **details):
    parti = [message] + [f"{k}: {v}" for k, v in details.items()]
    print(" | ".join(parti))

log("verificat", url=BASE_URL, status=200)



