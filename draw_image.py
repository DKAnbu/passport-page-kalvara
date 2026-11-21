#!/usr/bin/env python3
"""Draw the Kalvara passport spread (entry.png) with PIL only.

Everything is drawn from shapes and text: no external images.
Output: 1024x680 PNG, an open passport spread for the fictional
Republic of Kalvara. Run locally; main.py only copies this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 680
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_O = SANS  # DejaVu Sans has no oblique face on this system
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

PAPER = (243, 236, 219)
PAPER2 = (238, 229, 208)
INK = (28, 42, 66)
NAVY = (31, 52, 96)
GOLD = (150, 112, 42)
GREY = (110, 105, 92)
LIGHT = (214, 205, 184)


def font(path, size):
    return ImageFont.truetype(path, size)


def text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def mrz_check(s):
    """ICAO 9303 check digit."""
    vals = {}
    for i in range(10):
        vals[str(i)] = i
    for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = 10 + i
    vals["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def guilloche(draw, x0, y0, x1, y1, color, step=7, amp=2.2):
    """Fine wavy security lines across a rectangle."""
    y = y0 + 4
    while y < y1:
        pts = []
        for x in range(x0, x1 + 1, 6):
            pts.append((x, y + amp * math.sin((x - x0) / 26.0 + y / 9.0)))
        draw.line(pts, fill=color, width=1)
        y += step


def coat_of_arms(draw, cx, cy, s):
    """Gull over a salt crystal, drawn from shapes."""
    # salt crystal (diamond)
    cr = [(cx, cy - 0.9 * s), (cx + 0.55 * s, cy - 0.1 * s),
          (cx, cy + 0.75 * s), (cx - 0.55 * s, cy - 0.1 * s)]
    draw.polygon(cr, outline=GOLD, width=2)
    draw.line([(cx, cy - 0.9 * s), (cx, cy + 0.75 * s)], fill=GOLD, width=1)
    draw.line([(cx - 0.55 * s, cy - 0.1 * s), (cx + 0.55 * s, cy - 0.1 * s)],
              fill=GOLD, width=1)
    # gull: two curved wings
    draw.arc([cx - 0.95 * s, cy - 1.7 * s, cx - 0.05 * s, cy - 0.7 * s],
             200, 340, fill=NAVY, width=2)
    draw.arc([cx + 0.05 * s, cy - 1.7 * s, cx + 0.95 * s, cy - 0.7 * s],
             200, 340, fill=NAVY, width=2)
    draw.ellipse([cx - 2, cy - 1.62 * s, cx + 2, cy - 1.58 * s], fill=NAVY)
    # waves under the crystal
    for k, yy in enumerate((0.95, 1.12)):
        draw.arc([cx - 0.7 * s, cy + yy * s, cx + 0.7 * s, cy + (yy + 0.35) * s],
                 0, 180, fill=NAVY, width=2)


def draw_portrait(draw, box):
    """Stylised bust portrait, drawn from shapes only."""
    x0, y0, x1, y1 = box
    # background: teal gradient bands + faint salt crystals
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0))
        c = tuple(int(a + (b - a) * t) for a, b in
                  zip((168, 196, 190), (96, 138, 142)))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    for (cx, cy, r) in [(x0 + 18, y0 + 26, 7), (x1 - 22, y0 + 40, 5),
                        (x0 + 30, y0 + 150, 5), (x1 - 16, y0 + 132, 6)]:
        draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                     outline=(235, 240, 238), width=1)
    # shoulders / coat
    draw.polygon([(x0 + 18, y1), (x0 + 48, y1 - 62), (x0 + 66, y1 - 66),
                  (x1 - 66, y1 - 66), (x1 - 48, y1 - 62), (x1 - 18, y1)],
                 fill=(52, 66, 84))
    draw.polygon([(x0 + 62, y1 - 64), (x0 + 75, y1), (x1 - 75, y1),
                  (x1 - 62, y1 - 64)], fill=(226, 224, 210))
    # neck and head
    draw.rectangle([x0 + 63, y1 - 88, x0 + 87, y1 - 58], fill=(198, 152, 118))
    draw.ellipse([x0 + 44, y0 + 26, x0 + 106, y0 + 108], fill=(206, 162, 128))
    # hair: dark swept shape over the head
    draw.pieslice([x0 + 40, y0 + 18, x0 + 110, y0 + 92], 180, 360,
                  fill=(46, 38, 34))
    draw.polygon([(x0 + 44, y0 + 58), (x0 + 62, y0 + 34), (x0 + 88, y0 + 30),
                  (x0 + 106, y0 + 52), (x0 + 100, y0 + 66), (x0 + 78, y0 + 48),
                  (x0 + 58, y0 + 52)], fill=(46, 38, 34))
    # simple features: eyes, brows, nose, mouth
    for ex in (x0 + 62, x0 + 88):
        draw.ellipse([ex - 5, y0 + 66, ex + 5, y0 + 71], fill=(38, 30, 26))
        draw.line([(ex - 7, y0 + 60), (ex + 7, y0 + 59)], fill=(46, 38, 34),
                  width=2)
    draw.line([(x0 + 75, y0 + 70), (x0 + 73, y0 + 86)], fill=(170, 128, 100),
              width=2)
    draw.arc([x0 + 66, y0 + 90, x0 + 84, y0 + 100], 20, 160,
             fill=(140, 84, 70), width=2)
    # earring + collar pin (salt crystal)
    draw.ellipse([x0 + 47, y0 + 88, x0 + 51, y0 + 92], fill=(232, 220, 160))
    draw.polygon([(x0 + 75, y1 - 40), (x0 + 79, y1 - 34), (x0 + 75, y1 - 28),
                  (x0 + 71, y1 - 34)], outline=GOLD, width=1)


def stamp_layer(text_lines, w, h, ink, angle, bold=13, small=10):
    """One entry/exit stamp on its own layer, slightly rotated."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + w, oy + h], radius=8, outline=ink,
                        width=3)
    d.rounded_rectangle([ox + 5, oy + 5, ox + w - 5, oy + h - 5], radius=6,
                        outline=ink, width=1)
    y = oy + 10
    for i, line in enumerate(text_lines):
        f = font(SANS_B, bold) if i == 0 else font(SANS, small)
        d.text((ox + w // 2, y), line, font=f, fill=ink, anchor="ma")
        y += bold + 4 if i == 0 else small + 5
    return layer.rotate(angle, resample=Image.BICUBIC, expand=False)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # page background + guilloche
    d.rectangle([0, 0, W - 1, H - 1], fill=PAPER)
    guilloche(d, 14, 14, 506, 666, (196, 186, 158))
    guilloche(d, 518, 14, 1010, 666, (196, 186, 158))
    # spine fold shading
    for i in range(14):
        d.line([(512 - 7 + i, 10), (512 - 7 + i, 670)],
               fill=(0, 0, 0, 10 + i))
    d.line([(512, 10), (512, 670)], fill=(120, 110, 88), width=2)
    # outer border
    d.rectangle([8, 8, W - 9, H - 9], outline=NAVY, width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=GOLD, width=1)

    # ---------------- LEFT PAGE: data page ----------------
    coat_of_arms(d, 58, 74, 18)
    text(d, (258, 26), "REPUBLIC OF KALVARA", font(SANS_B, 25), NAVY, "ma")
    text(d, (258, 56), "R E P U B L I K A   K A L V A R A", font(SANS, 10),
         GREY, "ma")
    text(d, (258, 76), "P A S S P O R T", font(SANS_B, 15), GOLD, "ma")
    d.line([(36, 100), (488, 100)], fill=NAVY, width=2)
    text(d, (36, 108), "TYPE  P", font(SANS, 10), GREY)
    text(d, (258, 108), "CODE  KLV", font(SANS, 10), GREY, "ma")
    text(d, (488, 108), "No. KLV 482 913", font(SANS_B, 10), NAVY, "ra")

    # portrait
    pbox = (36, 128, 186, 313)
    d.rectangle([pbox[0] - 2, pbox[1] - 2, pbox[2] + 2, pbox[3] + 2],
                outline=NAVY, width=2)
    draw_portrait(d, pbox)
    text(d, (111, 318), "PORTRAIT — HOLDER", font(SANS, 8), GREY, "ma")

    # data fields (label above value, two columns right of portrait)
    fields = [
        ("SURNAME", "VOSS", 206, 128),
        ("GIVEN NAMES", "MARA SELIN", 206, 168),
        ("NATIONALITY", "KALVARAN", 206, 208),
        ("DATE OF BIRTH", "15 JUL 1990", 206, 248),
        ("PLACE OF BIRTH", "PORT SALINE", 360, 128),
        ("SEX", "F", 360, 168),
        ("DATE OF ISSUE", "12 MAR 2023", 360, 208),
        ("DATE OF EXPIRY", "12 MAR 2033", 360, 248),
    ]
    for label, value, x, y in fields:
        text(d, (x, y), label, font(SANS, 9), GREY)
        text(d, (x, y + 13), value, font(SANS_B, 15), INK)
    d.line([(206, 292), (488, 292)], fill=LIGHT, width=1)

    # authority + signature
    text(d, (36, 340), "AUTHORITY", font(SANS, 9), GREY)
    text(d, (36, 353), "PORT SALINE — MINISTRY OF SALT", font(SANS_B, 13),
         INK)
    text(d, (36, 372), "HOLDER'S SIGNATURE", font(SANS, 9), GREY)
    sig = [(40, 402), (58, 388), (76, 400), (92, 386), (110, 398),
           (128, 388), (146, 400), (160, 392), (176, 402)]
    d.line(sig, fill=(40, 50, 80), width=2, joint="curve")
    d.line([(36, 408), (196, 408)], fill=GREY, width=1)
    text(d, (300, 340), "HEIGHT  168 cm", font(SANS, 11), INK)
    text(d, (300, 360), "EYES  BROWN", font(SANS, 11), INK)
    text(d, (300, 380), "OCCUPATION  SALT HARBOUR PILOT",
         font(SANS, 11), INK)
    text(d, (300, 400), "Kalvari:  SOLSUUDU PILOOT", font(SANS_O, 11), GREY)

    # small Kalvara entry stamp on the data page (issue stamp)
    st = stamp_layer(["KALVARA", "ISSUED · PORT SALINE", "12 MAR 2023"],
                     190, 74, (96, 60, 130, 235), -5)
    img.paste(st, (292, 440), st)

    # MRZ strip
    d.rectangle([28, 560, 496, 648], fill=(232, 224, 200),
                outline=NAVY, width=1)
    name = "VOSS<<MARA<SELIN"
    line1 = ("P<KLV" + name).ljust(44, "<")
    doc = "KLV482913"
    dob, exp = "900715", "330312"
    # ICAO composite check covers doc+check, dob+check, expiry+check and
    # the optional data only (nationality and sex are excluded).
    comp_src = (doc + mrz_check(doc) + dob + mrz_check(dob)
                + exp + mrz_check(exp) + "<" * 15)
    line2 = (doc + mrz_check(doc) + "KLV" + dob + mrz_check(dob)
             + "F" + exp + mrz_check(exp) + "<" * 15
             + mrz_check(comp_src))
    assert len(line1) == 44 and len(line2) == 44, (line1, line2)
    mf = font(MONO_B, 16)
    d.text((36, 574), line1, font=mf, fill=INK)
    d.text((36, 606), line2, font=mf, fill=INK)
    text(d, (36, 652), "MACHINE-READABLE ZONE — ICAO 9303", font(SANS, 8),
         GREY)

    # ---------------- RIGHT PAGE: visas & stamps ----------------
    text(d, (764, 26), "V I S A S", font(SANS_B, 20), NAVY, "ma")
    text(d, (764, 52), "STAMPS OF NEIGHBOURING STATES", font(SANS, 10),
         GREY, "ma")
    d.line([(528, 76), (988, 76)], fill=NAVY, width=2)

    stamps = [
        ("TARNOVIA", "ENTRY", "14 JUN 2024", "TRV-114", (96, 60, 130, 235),
         -4, (548, 96)),
        ("TARNOVIA", "EXIT", "28 JUN 2024", "TRV-114", (96, 60, 130, 235),
         3, (782, 96)),
        ("OSTARA", "ENTRY", "09 NOV 2024", "OST-207", (30, 90, 160, 235),
         4, (548, 226)),
        ("OSTARA", "EXIT", "21 NOV 2024", "OST-207", (30, 90, 160, 235),
         -3, (782, 226)),
        ("MERIDIAN FREE PORT", "ENTRY", "02 MAR 2026", "MFP-031",
         (150, 60, 40, 235), -5, (548, 356)),
    ]
    for name, kind, date, code, ink, ang, (sx, sy) in stamps:
        st = stamp_layer([name, kind + "  ·  " + date, code], 200, 78, ink,
                         ang)
        img.paste(st, (sx, sy), st)

    # telling paperwork detail: salt-flats visa condition
    d.rounded_rectangle([548, 486, 988, 596], radius=6,
                        outline=(150, 40, 40), width=3)
    d.rounded_rectangle([554, 492, 982, 590], radius=4,
                        outline=(150, 40, 40), width=1)
    text(d, (768, 502), "VISA CONDITION — ART. 7", font(SANS_B, 13),
         (150, 40, 40), "ma")
    text(d, (768, 524), "HOLDER MAY NOT ENTER THE SALT FLATS", font(SANS_B, 13),
         (150, 40, 40), "ma")
    text(d, (768, 542), "WITHOUT A GUIDE PERMIT", font(SANS_B, 13),
         (150, 40, 40), "ma")
    text(d, (768, 564), "PORT SALINE · 12 MAR 2023", font(SANS, 10),
         (150, 40, 40), "ma")

    text(d, (764, 616), "PAGES 12–13 · THIS SPREAD IS THE HOLDER'S",
         font(SANS, 9), GREY, "ma")
    text(d, (764, 632), "COMPLETE TRAVEL RECORD TO DATE",
         font(SANS, 9), GREY, "ma")

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
