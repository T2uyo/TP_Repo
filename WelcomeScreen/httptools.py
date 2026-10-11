import requests
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]


# Partea 1: parametri în URL
def search(params):
    r = requests.get(BASE + "/get", params=params)
    return r.json()["args"]

def search_url(params):
    r = requests.get(BASE + "/get", params=params)
    return r.url

# Partea 2: anteturi
def fetch_with_agent(agent):
    r = requests.get(BASE + "/headers", headers={"User-Agent": agent})
    return r.json()["headers"]["User-Agent"]

def default_agent():
    r = requests.get(BASE + "/headers")
    return r.json()["headers"]["User-Agent"]

# Partea 3: trimiterea datelor
def post_json(data):
    r = requests.post(BASE + "/post", json=data)
    return r.json()["json"]

def post_form(data):
    r = requests.post(BASE + "/post", data=data)
    return r.json()["form"]


# Partea 4: coduri de stare
def describe_status(code):
    r = requests.get(BASE + "/status/" + str(code))

    if 200 <= r.status_code < 300:
        return "succes"
    elif 300 <= r.status_code < 400:
        return "eroare client"
    elif 400 <= r.status_code < 500:
        return "eroare server"

def is_ok(code):
    r = requests.get(BASE + "/status/" + str(code))
    try:
        r.raise_for_status()
        return True
    except requests.HTTPError:
        return False

# Partea 5: redirecționări
def count_redirects(n):
    r = requests.get(BASE + "/redirect/" + str(n))
    return len(r.history)

def final_url(n):
    r = requests.get(BASE + "/redirect/" + str(n))
    return r.url

def first_hop(n):
    r = requests.get(BASE + "/redirect/" + str(n), allow_redirects=False)
    return r.headers["Location"]

# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    s = requests.Session()
    s.get(BASE + "/cookies/set", cookies={name : value})
    r = s.get(BASE + "/cookies")
    return r.json()["cookies"]

def no_session_demo(name, value):
    requests.get(BASE + "/cookies/set", cookies={name : value})
    r = requests.get(BASE + "/cookies")
    return r.json()["cookies"]

# Partea 7: raportul final
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    try:
        r = requests.get(BASE + path, timeout=3)

        return {
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "seconds": r.elapsed.total_seconds(),
            "content_type": r.headers.get("Content-Type")
        }

    except requests.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }


def main():
    rezultate = []
    for path in PATHS:
        rezultat = report(path)
        rezultat["path"] = path
        rezultate.append(rezultat)

    reusite = [
        r for r in rezultate
        if r["status"] == 200
    ]

    reusite.sort(
        key=lambda r: r["seconds"],
        reverse=True
    )

# Bonus: autentificare
def check_login(user, password):
    try:
        r = requests.get(
            BASE + "/basic-auth/admin/secret",
            auth=(user, password),
            timeout=3
        )

        return r.status_code == 200

    except requests.RequestException:
        return False



if __name__ == "__main__":
    main()

