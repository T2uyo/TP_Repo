from dataclasses import dataclass, asdict
import json

#A1
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str
    def e_suspect(self):
        return any(c in self.cale for c in CAI_SUSPECTE)
p = Proces(3120,"update.exe","ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")

#A2
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

#A3
SUSPECTE_ID = {4625, 1102, 7045}

@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"

#A4
def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]
#B1
@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)
#B2
    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        rez = {}
        for p in self.procese:
            rez.setdefault(p.user, []).append(p.nume)
        return rez

inv = Inventar.din_json("arsenal/windows/start/procese.json")


#B3
def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("capturi")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    suspecte = inv.suspecte()
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "suspecte": [asdict(p) for p in suspecte],
            "alarma": [asdict(e) for e in alarma],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
        for p in suspecte:
            print(f"  [{p.pid}] {p.nume}  ({p.user})  {p.cale}")
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()

