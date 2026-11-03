import re
import sys
from collections import Counter
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")

#A1
def esec(linie):
    m = TIPAR.search(linie)
    if m is not None:
        return m.group(1), m.group(2)
    return None

#A2
def citeste_esecuri(cale):
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
    return esecuri

#A3
def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)


#A4
def main():
    cale = sys.argv[1]
    esecuri = citeste_esecuri(cale)
    counts = pe_ip(esecuri)
    print("Esecuri de autentificare:", len(esecuri))
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")

if __name__ == "__main__":
    main()
