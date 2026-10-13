import requests
from requests import status_codes

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

#p1
def build_url(host, path):
    return "https://" + host + "/" + path

def is_https(url):
    return url.startswith("https://")

#p2
def show_response(url):
    r = requests.get(url, timeout=5)
    return{
        "status": r.status_code,
        "content-type": r.headers.get("Content-Type",)
    }


#p3-
def check_site(url):
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return {"status": None, "error": type(e).__name__}

    content_type = r.headers.get("Content-Type","").split(";")[0]
    return{
        "status": r.status_code,
        "content-type": content_type,
        "length": len(r.content),
        "server": r.headers.get("Server", ""),
    }
#p4
def scan_sites():
    rezultate = []
    for url in SITES:
        info = check_site(url)
        info["url"] = url
        rezultate.append(info)
    working = [r for r in rezultate if r["status"] == "200"]
    working.sort(key=lambda r: r["length"], reverse=True)

    return{
        "working": working,
        "ok": len(working),
        "failed": len(rezultate)-len(working),
        }

def check_headers(url):
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return {"status": None, "error": type(e).__name__}

    present = [h for h in SECURITY_HEADERS if h in r.headers]
    missing = [h for h in SECURITY_HEADERS if h not in r.headers]
    score = len(present) * 100 // len(SECURITY_HEADERS)
    return{
        "present": present,
        "missing": missing,
        "score": score,
        }

def retry_check(url, attempts=3):
    status = None
    error = None
    made = 0
    for _ in range(attempts):
        made += 1
        try:
            r = requests.get(url, timeout=5)
        except requests.RequestException as e:
            status = None
            error = type(e).__name__
            continue
        status = r.status_code
        error = None
        if status < 500:
            break
    result = {"status": status, "attempts": made}
    if error is not None:
        result["error"] = error
    return result
