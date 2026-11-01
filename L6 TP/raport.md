# Laboratorul 6 — Informații invizibile: forensics și steganografie

## Lucrarea A — encoding, XOR, hash

### A1–A4: mesajul ascuns în straturi de encoding
Fișierul `probe/mesaj.txt` conținea textul codat pe trei straturi: base64 peste base64 peste hex.
Desfăcându-le pe rând (folosind `ghici_strat` pentru a recunoaște fiecare strat și `desfa` pentru a-l elimina), am obținut:

```
FLAG{straturi_de_encoding}
```

### A5: spargerea criptării XOR
`probe/xor.bin` a fost criptat cu XOR pe un singur octet (256 chei posibile). Prin forță brută, filtrând rezultatele care conțin doar caractere imprimabile (`citibil`), am obținut mai mulți candidați, dar doar unul formează text coerent:

- **Cheia:** 128 (0x80)
- **Mesajul:** `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`

### A6: spargerea hash-ului prin dicționar
Primul hash din `probe/hashuri.txt` (32 caractere → MD5) a fost comparat cu hash-urile cuvintelor din `probe/wordlist.txt`, până la potrivire:

- **Parola găsită:** `password`

### A7: unealta completă
`arsenal/forensics/decode.py` combină A1–A6 într-o unealtă de linie de comandă:
- fără `--fisier`: desface un șir text printr-un singur strat de encoding (`desfa`)
- cu `--fisier`: aplică forța brută XOR pe un fișier binar

Rezultatul fiecărei rulări se salvează în `arsenal/forensics/fisa.json`.
Testul `teste/test_decode.py` verifică funcția `desfa` pe un caz simplu (`U2FsdXQ=` → `base64`, `Salut`) și trece cu succes (`pytest`).

---

## Lucrarea B — forensics pe fișiere și steganografie

### B1: tipul real al fișierelor (magic bytes)
Verificarea primilor octeți, independent de extensie:
- `probe/foto.jpg` → semnătură JPEG (`\xff\xd8`)
- `probe/ascuns.png` → semnătură PNG (`\x89PNG`)

### B2: text ascuns în binar (strings)
Căutând secvențe de caractere imprimabile în `probe/ascuns.png`, pe lângă chunk-urile normale de PNG (`IHDR`, `IDAT`, `IEND`), a apărut:

```
secret.txtFLAG{ascuns_prin_carving}
PK
```

Indiciu clar că la coada fișierului e lipită o arhivă ZIP.

### B3: metadate EXIF și GPS
`probe/foto.jpg` conține metadate EXIF: `Make = Apple`, `Model = iPhone 13`, `DateTime = 2026:09:14 10:30:00`.
Coordonatele GPS, convertite din grade/minute/secunde în zecimal:

- **Latitudine:** 47.0167
- **Longitudine:** 28.8575

(coordonate din apropierea Chișinăului)

### B4: file carving — extragerea arhivei ascunse
Căutând semnătura ZIP (`PK\x03\x04`) în `probe/ascuns.png`, arhiva a fost găsită lipită la coada fișierului, de la **octetul 782**. Extrasă și dezarhivată, conținea `secret.txt` cu:

```
FLAG{ascuns_prin_carving}
```

### B5–B6: steganografie LSB
Am scris un mesaj (`FLAG{ascuns_in_pixeli}`) în ultimul bit al fiecărui canal de culoare (R, G, B) al pixelilor din `probe/foto.jpg`, salvat ca `stego.png` (format fără pierderi — un JPEG ar distruge biții ascunși prin recompresie).

Citind înapoi ultimul bit al fiecărui canal din `stego.png` și regrupându-i câte 8, am reconstituit mesajul exact:

```
FLAG{ascuns_in_pixeli}
```

---

## Concluzie

Laboratorul a arătat patru idei principale:
1. Codările (base64, hex, URL) sunt reversibile și pot fi desfăcute în straturi.
2. O criptare cu cheie foarte mică (XOR pe un octet) cedează ușor la forță brută.
3. Un hash nu se „decriptează" — se verifică prin încercare (atac de dicționar).
4. Datele pot fi ascunse în moduri pe care extensia sau vizualizarea unui fișier nu le dezvăluie: metadate EXIF, octeți lipiți la coada fișierului, sau biți individuali din pixeli.
