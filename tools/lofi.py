#!/usr/bin/env python3
"""
neveralways — the rot filter.
takes the model's pretty pictures and does to them what the internet does to everything:
shrinks them, crushes the colours, dithers, fries. output: assets/img/lofi/

    python3 tools/lofi.py
"""
import glob
import io
import os

from PIL import Image, ImageEnhance, ImageFilter

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
SRC = os.path.join(ROOT, "anime")
OUT = os.path.join(ROOT, "lofi")
os.makedirs(OUT, exist_ok=True)

# width in real pixels after the rot. css blows them back up with image-rendering: pixelated.
WIDTH = {"ever": 96, "pfp": 96, "smug": 128, "stickers": 240, "rot": 200, "bed": 120, "flat97": 220, "rave96": 220}
DEFAULT = 192


def crush(im, colors):
    return im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")


def jpeg(im, q):
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q)
    b.seek(0)
    return Image.open(b).convert("RGB")


def width_for(name):
    for k, w in WIDTH.items():
        if name.startswith(k):
            return w
    return DEFAULT


def rot(path):
    name = os.path.splitext(os.path.basename(path))[0]
    im = Image.open(path).convert("RGB")
    w = width_for(name)
    h = round(im.height * w / im.width)
    small = im.resize((w, h), Image.BOX)
    small = ImageEnhance.Color(small).enhance(1.35)
    small = ImageEnhance.Contrast(small).enhance(1.15)
    lo = crush(small, 20)
    lo.save(os.path.join(OUT, name + ".png"), optimize=True)
    # deep-fried twin: oversaturated, oversharpened, jpeg'd to death, then pixelated again
    fr = ImageEnhance.Color(small).enhance(2.6)
    fr = ImageEnhance.Contrast(fr).enhance(1.7)
    fr = fr.filter(ImageFilter.UnsharpMask(2, 250, 0))
    for q in (12, 8, 5):
        fr = jpeg(fr, q)
    fr = crush(fr, 12)
    fr.save(os.path.join(OUT, name + "-fried.png"), optimize=True)
    print(name, lo.size)
    return name, lo


def stickers(sheet):
    """cut the 3x3 sticker sheet into nine stickers."""
    w, h = sheet.size
    cw, ch = w // 3, h // 3
    for i in range(9):
        x, y = i % 3, i // 3
        s = sheet.crop((x * cw, y * ch, (x + 1) * cw, (y + 1) * ch))
        s.save(os.path.join(OUT, "sticker-%d.png" % i), optimize=True)
    print("stickers: 9")


def flowers():
    """the homepage flowers, shrunk until you can count the pixels."""
    for i in range(3):
        im = Image.open(os.path.join(ROOT, "flower%d.png" % i)).convert("RGB")
        lo = crush(im.resize((180, 180), Image.BOX), 14)
        lo.save(os.path.join(OUT, "flower%d.png" % i), optimize=True)
    print("flowers: 3")


def main():
    flowers()
    for p in sorted(glob.glob(os.path.join(SRC, "*.jpg"))):
        name, lo = rot(p)
        if name == "stickers":
            stickers(lo)


if __name__ == "__main__":
    main()
