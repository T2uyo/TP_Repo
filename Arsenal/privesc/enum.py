import argparse, json, os

#A1
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        linii = [ln.strip() for ln in f]
        return [ln for ln in linii if ln and not ln.startswith("#")]

#A2
def nume(cale):
    return cale.rsplit("/", 1)[-1]

#A3
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
def suid_constatari(cale):
    unice = sorted(set(citeste_linii(cale)))
    return [{"cale": c,
             "nume": nume(c),
             "risc": "mare" if nume(c) in GTFO else "normal"}
            for c in unice]

#A4
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)
        out.append({"user": user.strip(),
                    "drept": drept.strip(),
                    "risc": "mare" if "NOPASSWD" in drept else "normal"})
    return out


def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        if len(campuri) < 7:
            continue
        out.append({"user": campuri[5],
                    "comanda": " ".join(campuri[6:])})
    return out


def enumereaza(d):
    return {
        "suid": suid_constatari(d + "/suid.txt"),
        "sudo": sudo_constatari(d + "/sudo.txt"),
        "cron": cron_constatari(d + "/crontab.txt"),
    }

#A5
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    useri = ({c["user"] for c in raport["sudo"]} |
             {c["user"] for c in raport["cron"]})
    print("utilizatori implicati:", ", ".join(sorted(useri)))

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
