import re
import base64
import hashlib
import argparse
import json
from urllib.parse import unquote


# A2
def ghici_strat(s):
    if "%" in s:
        return "url"
    if re.fullmatch(r"[0-9a-f]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"
    return "necunoscut"


# A3
def desfa(s):
    strat = ghici_strat(s)
    if strat == "url":
        return strat, unquote(s).encode()
    elif strat == "hex":
        return strat, bytes.fromhex(s)
    elif strat == "base64":
        return strat, base64.b64decode(s)
    return strat, s.encode()


# A4
def citibil(b):
    return all(32 <= c < 127 for c in b)


if __name__ == "__main__":
    # A1
    s = "Salut"
    b = s.encode()
    print(b, b[0])
    print(bytes.fromhex(b.hex()))

    # A2 teste
    print(ghici_strat("%2Fetc"))
    print(ghici_strat("48656c6c6f"))
    print(ghici_strat("SGVsbG8gd29ybGQ="))

    # A4
    val = "NTM1OTU3NTk="
    for _ in range(8):
        if ghici_strat(val) == "necunoscut":
            print("final:", val)
            break
        strat, b = desfa(val)
        if not citibil(b):
            print("final:", val)
            break
        print(strat, b)
        val = b.decode()

    # A5
    date = open("probe/xor.bin", "rb").read()
    for k in range(256):
        clar = bytes(x ^ k for x in date)
        if citibil(clar):
            print("cheie:", k, clar.decode())

    # A6
    tinta = open("probe/hashuri.txt").readline().strip()
    print(len(tinta))
    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("gasit:", cuv)
            break

    # A7
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()
    if a.fisier:
        with open(a.intrare, "rb") as f:
            date = f.read()
        strat = "xor"
        rezultat = None
        for k in range(256):
            clar = bytes(x ^ k for x in date)
            if citibil(clar):
                rezultat = clar
                break
    else:
        strat, rezultat = desfa(a.intrare)

    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump({"strat": strat, "rezultat": rezultat.decode(errors="replace")}, f, indent=4)