import argparse, json, os

#A1
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        linii = [ln.strip() for ln in f]
        return [ln for ln in linii if ln and not ln.startswith("#")]

cai = citeste_linii("start/suid.txt")
print("linii SUID:", len(cai))

#A2
def nume(cale):
    return cale.rsplit("/", 1)[-1]

nume_unice = {nume(c) for c in cai}  # set comprehension
print("SUID distincte:", len(nume_unice))

#A3
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}


def suid_constatari(cale):
    unice = sorted(set(citeste_linii(cale)))
    return [{"cale": c,
             "nume": nume(c),
             "risc": "mare" if nume(c) in GTFO else "normal"}
            for c in unice]

suid = suid_constatari("start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted(c["nume"] for c in mari))

