import csv
import json
import re
import socket
import ssl
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import certifi
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-NumeStudent"}


def fetch(url: str, timeout: int = TIMEOUT):
    """Returnează obiectul răspuns pentru url, cu antetele implicite."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Returnează titlul paginii din șirul HTML primit (fără rețea)."""
    start = html.find("<title>") + len("<title>")
    final = html.find("</title>")
    return html[start:final].strip()


def security_headers(url: str) -> dict:
    """Returnează {antet: True/False} pentru cinci antete de securitate."""
    antete = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]
    raspuns = fetch(url)
    return {a: a in raspuns.headers for a in antete}


def score_headers(results: dict) -> str:
    """Primește rezultatul din security_headers și returnează un scor, ex. '3/5'."""
    return f"{sum(results.values())}/{len(results)}"


def resolve(hostname: str) -> str:
    """Returnează adresa IP a domeniului dat."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returnează câte zile mai sunt până la expirarea certificatului."""
    # certifi: magazinul de certificate din Windows a respins conexiunea
    context = ssl.create_default_context(cafile=certifi.where())
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificat = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(certificat["notAfter"])
    return int((expira - time.time()) / 86400)  # 86400 = secundele dintr-o zi


def extract_links(html: str) -> list:
    """Returnează legăturile (href) din html, fără duplicate."""
    legaturi = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(legaturi))


def split_links(links: list, domain: str) -> tuple:
    """Împarte legăturile în (interne, externe) față de domeniul dat."""
    interne, externe = [], []
    for link in links:
        complet = urljoin("https://" + domain, link)
        if urlparse(complet).netloc == domain:
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe


def fetch_robots(base: str):
    """Returnează textul din /robots.txt sau None dacă lipsește."""
    try:
        r = fetch(base + "/robots.txt")
    except requests.RequestException:
        return None
    return r.text if r.ok else None


def disallowed_paths(robots_text) -> list:
    """Returnează lista valorilor Disallow din textul robots.txt."""
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        linie = linie.strip()
        if linie.lower().startswith("disallow:"):
            valoare = linie.split(":", 1)[1].strip()
            if valoare:
                cai.append(valoare)
    return cai


def check_paths(base: str, paths: list) -> dict:
    """Returnează {cale: cod_de_stare} pentru fiecare cale din listă."""
    rezultat = {}
    for cale in paths:
        rezultat[cale] = get_status(base + cale)
        time.sleep(1)
    return rezultat


def redirect_chain(url: str) -> list:
    """Returnează redirecționările pornind de la varianta http:// a site-ului."""
    raspuns = fetch("http://" + urlparse(url).netloc)
    return [f"{p.status_code} -> {p.headers.get('Location', '?')}" for p in raspuns.history]


def save_csv(results: dict, path: str = "report.csv") -> None:
    """Salvează {cale: status} în CSV, cu coloanele path, status, checked_at."""
    moment = datetime.now().isoformat()
    with open(path, "w", newline="", encoding="utf-8") as fisier:
        scriitor = csv.writer(fisier)
        scriitor.writerow(["path", "status", "checked_at"])
        for cale, status in results.items():
            scriitor.writerow([cale, status, moment])


def site_report(url: str, path: str = "report.json") -> dict:
    """Colectează informații despre site, le afișează și le salvează în JSON."""
    hostname = urlparse(url).netloc

    raspuns = fetch(url)
    time.sleep(1)
    scor = score_headers(security_headers(url))
    time.sleep(1)
    lant = redirect_chain(url)
    time.sleep(1)
    robots = disallowed_paths(fetch_robots(url))

    try:
        zile = cert_days_left(hostname)
    except OSError:
        zile = None  # fără HTTPS sau certificat indisponibil

    interne, externe = split_links(extract_links(raspuns.text), hostname)

    raport = {
        "url": url,
        "status_code": raspuns.status_code,
        "final_url": raspuns.url,
        "title": get_title(raspuns.text),
        "ip": resolve(hostname),
        "redirects": lant,
        "security_score": scor,
        "cert_days_left": zile,
        "internal_links": len(interne),
        "external_links": len(externe),
        "disallowed_paths": robots,
    }

    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {raport['status_code']}")
    print(f"Titlu:             {raport['title']}")
    print(f"Adresă IP:         {raport['ip']}")
    print(f"Redirecționări:    {', '.join(lant) if lant else 'niciuna'}")
    print(f"Scor securitate:   {scor}")
    if zile is not None:
        print(f"Certificat:        {zile} de zile rămase")
    else:
        print("Certificat:        indisponibil")
    print(f"Legături:          {len(interne)} interne, {len(externe)} externe")
    print(f"Căi interzise:     {', '.join(robots) if robots else 'niciuna'}")

    with open(path, "w", encoding="utf-8") as fisier:
        json.dump(raport, fisier, indent=2, ensure_ascii=False)
    print(f"Salvat în {path}")
    return raport


# Autotestul rulează doar când fișierul este pornit direct (python webtools.py)
if __name__ == "__main__":
    print("Autotest:", get_status(BASE_URL))