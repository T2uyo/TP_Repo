from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

# Partea 1
print("Partea 1, build_url:", build_url("example.com", "login"))
print("Partea 1, build_url cu /:", build_url("example.com", "/login"))
print("Partea 1, is_https:", is_https("https://example.com"))
print("Partea 1, is_https:", is_https("http://example.com"))

# Partea 2
for url in ["https://example.com", "https://httpbin.org/status/404"]:
    r = show_response(url)
    print("Partea 2, show_response", url)
    print("Status:", r["status"])
    print("Content-Type:", r["content_type"])

# Partea 3
print("Partea 3, check_site:", check_site("https://example.com"))
print("Partea 3, check_site inexistent:", check_site("http://this-site-does-not-exist.invalid"))

# Partea 4
print("Partea 4, scan_sites:")
summary = scan_sites()
for r in summary["working"]:
    print(f"{r['url']} -> {r['status']}, {r['length']} octeți")
print(f"Reușite: {summary['ok']} | Eșuate: {summary['failed']}")

# Partea 5
print("Partea 5, fără antete:", check_headers("https://example.com"))
print("Partea 5, cu antete:", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, litere mici:", check_headers("https://httpbin.org/response-headers?x-frame-options=DENY"))
print("Partea 5, inexistent:", check_headers("http://this-site-does-not-exist.invalid"))

# Partea 6
print("Partea 6, retry 200:", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry 404:", retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry 500:", retry_check("https://httpbin.org/status/500"))
print("Partea 6, retry 500, 2 încercări:", retry_check("https://httpbin.org/status/500", attempts=2))
print("Partea 6, retry inexistent:", retry_check("http://this-site-does-not-exist.invalid"))