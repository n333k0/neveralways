#!/usr/bin/env python3
"""
neveralways — the desktop. pixel file icons and 88x31 badges for the homepage.
    python3 tools/gen_desktop.py   ->  assets/img/desk/
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
OUT = os.path.join(ROOT, "desk")
os.makedirs(OUT, exist_ok=True)
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

K, W, G1, G2 = (0, 0, 0, 255), (255, 255, 255, 255), (192, 192, 192, 255), (128, 128, 128, 255)
PINK, HOT, RED, GRN, YEL, BLU, CYA, VIO = (255, 143, 216, 255), (255, 46, 154, 255), (209, 0, 36, 255), (57, 255, 106, 255), (255, 230, 0, 255), (0, 0, 160, 255), (0, 229, 255, 255), (176, 75, 255, 255)


def canvas():
    return Image.new("RGBA", (32, 32), (0, 0, 0, 0))


def page(d, band=None):
    d.polygon([(6, 2), (21, 2), (27, 8), (27, 30), (6, 30)], fill=W, outline=K)
    d.polygon([(21, 2), (21, 8), (27, 8)], fill=G1, outline=K)
    if band:
        d.rectangle([7, 22, 26, 28], fill=band)
    for y in (12, 15, 18):
        d.line([9, y, 24, y], fill=G2)


def save(im, name, scale=1):
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(os.path.join(OUT, name + ".png"))


def icons():
    im = canvas(); d = ImageDraw.Draw(im); page(d); save(im, "txt")
    im = canvas(); d = ImageDraw.Draw(im); page(d, RED); d.text((9, 22), "PDF", fill=W, font=ImageFont.load_default()); save(im, "pdf")
    im = canvas(); d = ImageDraw.Draw(im); page(d, BLU); save(im, "doc")
    im = canvas(); d = ImageDraw.Draw(im)  # exe: a tiny window
    d.rectangle([2, 5, 29, 27], fill=G1, outline=K); d.rectangle([3, 6, 28, 10], fill=BLU); d.rectangle([25, 7, 27, 9], fill=G1)
    d.rectangle([5, 12, 26, 25], fill=K); d.line([7, 15, 10, 15], fill=GRN); d.line([7, 18, 14, 18], fill=GRN); d.point((7, 21), fill=GRN)
    save(im, "exe")
    im = canvas(); d = ImageDraw.Draw(im)  # zip: folder with a zipper
    d.polygon([(2, 8), (12, 8), (14, 11), (29, 11), (29, 28), (2, 28)], fill=YEL, outline=K)
    for y in range(12, 28, 2):
        d.rectangle([14, y, 17, y], fill=K if y % 4 else G2)
    save(im, "zip")
    im = canvas(); d = ImageDraw.Draw(im); page(d)  # img
    d.rectangle([8, 11, 25, 27], fill=PINK); d.polygon([(8, 27), (14, 18), (19, 24), (22, 20), (25, 27)], fill=HOT); d.ellipse([19, 12, 23, 16], fill=YEL)
    save(im, "img")
    im = canvas(); d = ImageDraw.Draw(im); page(d)  # mp3
    d.line([16, 12, 16, 24], fill=K, width=2); d.line([16, 12, 22, 14], fill=K, width=2); d.ellipse([11, 22, 17, 27], fill=VIO)
    save(im, "mp3")
    im = canvas(); d = ImageDraw.Draw(im)  # eml: envelope
    d.rectangle([2, 8, 29, 26], fill=W, outline=K); d.line([2, 8, 15, 18, 29, 8], fill=K); d.line([2, 26, 12, 16], fill=G2); d.line([29, 26, 19, 16], fill=G2)
    save(im, "eml")
    im = canvas(); d = ImageDraw.Draw(im)  # computer
    d.rectangle([4, 3, 27, 21], fill=G1, outline=K); d.rectangle([7, 6, 24, 18], fill=(10, 0, 30, 255)); d.point([(9, 8), (10, 8), (11, 8)], fill=GRN)
    d.rectangle([11, 22, 20, 24], fill=G2); d.rectangle([5, 25, 26, 29], fill=G1, outline=K)
    save(im, "computer")
    im = canvas(); d = ImageDraw.Draw(im)  # recycle bin
    d.polygon([(8, 9), (24, 9), (22, 29), (10, 29)], fill=G1, outline=K); d.rectangle([6, 6, 26, 9], fill=G2, outline=K)
    for x in (12, 16, 20):
        d.line([x, 12, x - (1 if x < 16 else -1 if x > 16 else 0), 26], fill=G2)
    save(im, "bin")
    im = canvas(); d = ImageDraw.Draw(im)  # globe (webring)
    d.ellipse([3, 3, 28, 28], fill=CYA, outline=K); d.polygon([(8, 9), (14, 7), (16, 13), (11, 17)], fill=GRN); d.polygon([(18, 16), (25, 15), (23, 24), (17, 22)], fill=GRN)
    d.arc([3, 3, 28, 28], 0, 360, fill=K); d.line([3, 15, 28, 15], fill=(0, 120, 140, 255)); d.arc([10, 3, 21, 28], 0, 360, fill=(0, 120, 140, 255))
    save(im, "globe")
    im = canvas(); d = ImageDraw.Draw(im)  # book (guestbook)
    d.rectangle([5, 4, 26, 28], fill=HOT, outline=K); d.rectangle([7, 4, 8, 28], fill=RED); d.rectangle([11, 9, 23, 13], fill=W)
    save(im, "book")
    # the kitty face, from the house cat
    cat = Image.open(os.path.join(ROOT, "cat.png")).convert("RGBA")
    k = cat.resize((32, 28), Image.NEAREST)
    im = canvas(); im.paste(k, (0, 2), k); save(im, "kitty")
    print("icons ok")


def badge(text, bg, fg, name, deco=None):
    im = Image.new("RGB", (88, 31), bg)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    if deco == "stripes":
        for x in range(-31, 88, 6):
            d.line([x, 31, x + 31, 0], fill=tuple(min(255, c + 30) for c in bg))
    if deco == "grid":
        for x in range(0, 88, 4):
            d.line([x, 0, x, 31], fill=tuple(min(255, c + 25) for c in bg))
    d.rectangle([0, 0, 87, 30], outline=fg)
    d.rectangle([2, 2, 85, 28], outline=tuple(c // 2 for c in fg))
    f = ImageFont.truetype(MONO_B, 9)
    lines = text.split("\n")
    y = 15 - len(lines) * 5
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((88 - w) / 2 + 1, y + 1), ln, fill=(0, 0, 0), font=f)
        d.text(((88 - w) / 2, y), ln, fill=fg, font=f)
        y += 10
    im.save(os.path.join(OUT, "b-" + name + ".png"))


def badges():
    badge("BEST VIEWED\nAT 3AM", (20, 0, 40), (255, 143, 216), "3am", "grid")
    badge("ZONE 5\nMEMBERS ONLY", (0, 0, 0), (255, 0, 40), "zone5")
    badge("NO HANDS\nJUST VIBES", (255, 46, 154), (255, 255, 255), "nohands", "stripes")
    badge("UNIT\n'95-'03", (230, 225, 210), (20, 20, 20), "unit")
    badge("MADE WITH\nNOTEPAD.EXE", (0, 0, 160), (255, 255, 255), "notepad")
    badge("I ♥ SYZYGY", (0, 0, 0), (57, 255, 106), "syzygy", "grid")
    badge("POST-\nAUTHORED", (176, 75, 255), (255, 255, 255), "post", "stripes")
    badge("COZYWEB\nONLY", (10, 20, 10), (159, 230, 255), "cozy")
    badge("ANTI-INDEX\nCOMPLIANT", (255, 230, 0), (0, 0, 0), "anti", "stripes")
    print("badges ok")


if __name__ == "__main__":
    icons()
    badges()
