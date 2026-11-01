from PIL import Image
from PIL.ExifTags import TAGS
import re

#B1
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

#B2
date = open("probe/ascuns.png", "rb").read()
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

#B3
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)
gps = exif[34853]
def la_zecimal(grade, minute, secunde, emisfera):
    val = grade + minute / 60 + secunde / 3600
    if emisfera in ("S", "W"):
        val = -val
    return val
lat = float(la_zecimal(*gps[2], gps[1]))
lon = float(la_zecimal(*gps[4], gps[3]))
print(lat, lon)

#B4
date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
if i != -1:
    with open("gasit.zip", "wb") as f:
        f.write(date[i:])
    print("arhiva extrasa de la octetul", i)

#B5
from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj) + "00000000"  # terminator

px_nou = []
idx = 0
for (r, g, b) in px:
    if idx < len(biti):
        r = (r & ~1) | int(biti[idx]); idx += 1
    if idx < len(biti):
        g = (g & ~1) | int(biti[idx]); idx += 1
    if idx < len(biti):
        b = (b & ~1) | int(biti[idx]); idx += 1
    px_nou.append((r, g, b))

img.putdata(px_nou)
img.save("stego.png")

#B6
px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""
for (r, g, b) in px:
    biti += str(r & 1) + str(g & 1) + str(b & 1)

octeti = bytearray()
for i in range(0, len(biti), 8):
    octet = int(biti[i:i+8], 2)
    if octet == 0:
        break
    octeti.append(octet)

print(octeti.decode())