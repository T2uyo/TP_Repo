from bs4 import BeautifulSoup

import webtools


def get_title_bs(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else ""

def extract_links_bs(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    return list(dict.fromkeys(a["href"] for a in soup.find_all("a", href=True)))

html_test = """
<html><head><TITLE lang="ro">  Salut lume  </TITLE></head>
<body>
  <a href='/despre'>Despre</a>
  <A HREF="/contact">Contact</A>
  <a href="/contact">Contact din nou</a>
</body></html>
"""

print("Versiunea veche:")
print("  titlu:  ", repr(webtools.get_title(html_test)))
print("  legături:", webtools.extract_links(html_test))

print("Versiunea BeautifulSoup:")
print("  titlu:  ", repr(get_title_bs(html_test)))
print("  legături:", extract_links_bs(html_test))

# Comparație: versiunile cu BeautifulSoup nu sunt mult mai scurte, dar sunt mult
# mai sigure. Versiunile vechi caută șiruri fixe ("<title>", href="...") și
# greșesc la majuscule, la atribute în <title> sau la ghilimele simple (în
# testul de mai sus au returnat un titlu fără sens și au pierdut o legătură).
# BeautifulSoup înțelege structura HTML-ului și tratează singur cazul în care
# lipsește <title>.