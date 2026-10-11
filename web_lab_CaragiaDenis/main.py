import argparse
import time

import webtools                                        # exercițiul 44
from webtools import get_title, security_headers      # exercițiul 45
from webtools import DEFAULT_HEADERS                   # exercițiul 47

# Exercițiul 45: dacă main.py ar avea propria funcție get_title, definiția ei
# ar înlocui funcția importată, pentru că ultimul nume definit câștigă.

# Exercițiul 46: când rulez python webtools.py, Python îi dă numele "__main__",
# deci autotestul din blocul final se execută. Când main.py îl importă, numele
# devine "webtools", condiția este falsă și autotestul este sărit.


def main() -> None:
    """Citește adresa din linia de comandă și rulează analiza."""
    parser = argparse.ArgumentParser(description="Raport despre un site web")
    parser.add_argument("url", help="adresa site-ului, ex. https://cybercor.org")
    url = parser.parse_args().url                      # exercițiul 48

    print(webtools.get_title(webtools.fetch(url).text))    # exercițiul 44
    time.sleep(1)
    print(security_headers(url))                       # exercițiul 45
    print(DEFAULT_HEADERS)                             # exercițiul 47
    time.sleep(1)

    rezultate = webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
    webtools.save_csv(rezultate)                       # exercițiul 49

    webtools.site_report(url)                          # exercițiul 50


if __name__ == "__main__":
    main()