#!/usr/bin/env python3
"""
neveralways — image generator.
every picture on the site is made here, by code, from nothing.
no stock, no scraped jpegs: the house grows its own flowers.

run:  python3 tools/gen_images.py   (writes into assets/img/)
"""
import math
import os
import random
import hashlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageChops

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

rng = np.random.default_rng(1996)
random.seed(1996)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def save(img, name, **kw):
    p = os.path.join(OUT, name)
    img.save(p, optimize=True, **kw)
    print("wrote", name, img.size, os.path.getsize(p) // 1024, "KB")


def palette_img(colors):
    pal = []
    for c in colors:
        pal += list(c)
    pal += [0, 0, 0] * (256 - len(colors))
    p = Image.new("P", (1, 1))
    p.putpalette(pal)
    return p


def dither(img, colors, fs=True):
    img = img.convert("RGB")
    q = img.quantize(palette=palette_img(colors), dither=Image.Dither.FLOYDSTEINBERG if fs else Image.Dither.NONE)
    return q.convert("RGB")


def bayer(img, colors, scale=1):
    """ordered dither: the grid-shaped grain of the 90s."""
    a = np.asarray(img.convert("RGB")).astype(np.float32) / 255.0
    m = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16.0 - 0.5
    h, w, _ = a.shape
    t = np.tile(m, (h // 4 + 1, w // 4 + 1))[:h, :w][..., None]
    a = np.clip(a + t * 0.33, 0, 1)
    pal = np.array(colors, np.float32) / 255.0
    d = ((a[:, :, None, :] - pal[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1)
    out = (pal[idx] * 255).astype(np.uint8)
    return Image.fromarray(out)


def grain(img, amt=18, seed=0):
    r = np.random.default_rng(seed)
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    n = r.normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))


# ————————————————————————————————————————— the flower, three moods

def flower(stage):
    S = 720
    y, x = np.mgrid[0:S, 0:S].astype(np.float32)
    cx, cy = S * 0.5, S * 0.52
    dx, dy = x - cx, y - cy
    r = np.sqrt(dx * dx + dy * dy)
    th = np.arctan2(dy, dx)
    r2 = np.random.default_rng(7)

    if stage == 0:
        bg_in, bg_out = np.array([255, 236, 246]), np.array([255, 160, 214])
        petal_in, petal_out = np.array([255, 245, 250]), np.array([255, 60, 160])
        drop = (255, 255, 255)
    elif stage == 1:
        bg_in, bg_out = np.array([255, 214, 160]), np.array([250, 90, 40])
        petal_in, petal_out = np.array([255, 240, 200]), np.array([230, 40, 30])
        drop = (190, 0, 20)
    else:
        bg_in, bg_out = np.array([40, 0, 20]), np.array([0, 0, 0])
        petal_in, petal_out = np.array([255, 70, 140]), np.array([40, 0, 30])
        drop = (255, 0, 40)

    t = np.clip(r / (S * 0.75), 0, 1)[..., None]
    img = bg_in * (1 - t) + bg_out * t

    layers = [(5, 300, 0.0), (6, 255, 0.4), (7, 205, 0.9), (8, 150, 1.6), (9, 100, 2.2)]
    for i, (k, R, off) in enumerate(layers):
        wob = 0.06 * np.sin(th * 13 + i) + 0.04 * np.sin(th * 29 + 2 * i)
        edge = R * (0.5 + 0.5 * np.abs(np.cos(k * (th + off) / 2)) ** 0.7) * (1 + wob)
        inside = r < edge
        s = np.clip(r / np.maximum(edge, 1), 0, 1)[..., None]
        shade = 0.75 + 0.25 * np.cos(k * (th + off))[..., None]
        col = (petal_in * (1 - s) + petal_out * s) * shade
        # petal veins
        vein = (np.abs(np.sin(k * (th + off) * 6 + r / 9)) < 0.05) & inside
        img = np.where(inside[..., None], col, img)
        img = np.where(vein[..., None], img * 0.82, img)
        rim = inside & (np.abs(r - edge) < 2.2)
        img = np.where(rim[..., None], img * 0.55, img)
        if stage == 2:
            circuit = inside & ((np.abs(np.sin(dx / 11 + i)) < 0.04) | (np.abs(np.sin(dy / 11 - i)) < 0.04)) & (s[..., 0] > 0.35)
            img = np.where(circuit[..., None], np.array([60, 255, 120]) * 0.8, img)

    # the heart of it: a phyllotaxis of seeds (or pixels)
    core = r < 64
    img = np.where(core[..., None], np.array([60, 20, 10]) if stage < 2 else np.array([10, 0, 5]), img)
    pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    golden = math.pi * (3 - math.sqrt(5))
    for n in range(260):
        rr = 4.0 * math.sqrt(n)
        a = n * golden
        px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
        c = (255, 200, 40) if stage == 0 else (255, 120, 0) if stage == 1 else (0, 255, 90)
        d.rectangle([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=c)

    # drops: water, then blood, then light
    for _ in range(18):
        a = r2.uniform(0, 2 * math.pi)
        rr = r2.uniform(90, 300)
        px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
        R = r2.uniform(5, 15)
        d.ellipse([px - R, py - R * 1.15, px + R, py + R * 1.15], fill=drop, outline=(0, 0, 0) if stage else (200, 120, 170))
        d.ellipse([px - R * 0.5, py - R * 0.7, px - R * 0.1, py - R * 0.3], fill=(255, 255, 255))
        if stage == 1 and r2.random() < 0.5:  # it runs
            d.line([px, py + R, px + r2.uniform(-3, 3), py + R + r2.uniform(20, 80)], fill=drop, width=3)

    # bugs on the petals (stage >= 1): tiny pixel beetles
    if stage >= 1:
        for _ in range(14 if stage == 1 else 40):
            a = r2.uniform(0, 2 * math.pi)
            rr = r2.uniform(60, 330)
            px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
            c = (0, 0, 0) if stage == 1 else (60, 255, 120)
            d.ellipse([px - 3, py - 4, px + 3, py + 4], fill=c)
            for l in (-3, 0, 3):
                d.line([px - 3, py + l, px - 7, py + l + 1], fill=c)
                d.line([px + 3, py + l, px + 7, py + l + 1], fill=c)

    pals = [
        [(255, 255, 255), (255, 214, 236), (255, 143, 216), (255, 46, 154), (160, 0, 90), (60, 20, 10), (255, 200, 40), (40, 0, 20)],
        [(255, 250, 230), (255, 200, 120), (250, 110, 40), (210, 20, 20), (120, 0, 10), (30, 0, 0), (255, 255, 255)],
        [(0, 0, 0), (40, 0, 25), (120, 0, 60), (255, 46, 154), (255, 160, 210), (0, 255, 90), (255, 0, 40)],
    ]
    out = dither(pil, pals[stage])
    save(out, "flower%d.png" % stage)
    return pil


# ————————————————————————————————————————— pixel sprites

def sprite(rows, colors, scale):
    h, w = len(rows), max(len(r) for r in rows)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row):
            if ch in colors:
                im.putpixel((xx, yy), colors[ch])
    return im.resize((w * scale, h * scale), Image.NEAREST)


BUG_A = [
    "....k.....k.....",
    ".....k...k......",
    "......kkk.......",
    ".k...kgggk...k..",
    "..k.kgGGGgk.k...",
    "...kgGgGgGgk....",
    "kk.kgGGGGGgk.kk.",
    "..kgGgGgGgGgk...",
    "..kgGGGGGGGgk...",
    "kk.kgGgGgGgk.kk.",
    "...kgGGGGGgk....",
    "..k.kgGgGgk.k...",
    ".k...kgGgk...k..",
    "......kkk.......",
]
BUG_B = [r.replace("k.k", ".kk") if i in (4, 11) else r for i, r in enumerate(BUG_A)]
BUG_B = [("." + r[:-1]) if r.startswith("kk") else r for r in BUG_B]


def bugs():
    cols = {"k": (10, 10, 10, 255), "g": (0, 120, 50, 255), "G": (60, 255, 120, 255)}
    a = sprite(BUG_A, cols, 3)
    b = sprite(BUG_B, cols, 3)
    a.save(os.path.join(OUT, "bug.gif"), save_all=True, append_images=[b], duration=140, loop=0, disposal=2, transparency=0)
    # red one: an exploit
    cols2 = {"k": (10, 10, 10, 255), "g": (120, 0, 20, 255), "G": (255, 30, 60, 255)}
    a = sprite(BUG_A, cols2, 3)
    b = sprite(BUG_B, cols2, 3)
    a.save(os.path.join(OUT, "bug-red.gif"), save_all=True, append_images=[b], duration=110, loop=0, disposal=2, transparency=0)
    print("wrote bug.gif, bug-red.gif")


CAT = [
    "..k..........k..",
    ".kpk........kpk.",
    ".kppk......kppk.",
    ".kpppkkkkkkpppk.",
    "kwwwwwwwwwwwwwwk",
    "kwwwwwwwwwwwwwwk",
    "kwwEEwwwwwwEEwwk",
    "kwwEbwwwwwwEbwwk",
    "kwwwwwwppwwwwwwk",
    "kpwwwwwkkwwwwwpk",
    "kwwwwwkwwkwwwwwk",
    ".kwwwwwwwwwwwwk.",
    "..kkwwwwwwwwkk..",
    "....kkkkkkkk....",
]
CAT_BLINK = [r.replace("E", "k").replace("b", "k") if i in (6,) else (r.replace("E", "w").replace("b", "w") if i == 7 else r) for i, r in enumerate(CAT)]


def cat():
    cols = {"k": (20, 10, 20, 255), "w": (255, 250, 252, 255), "p": (255, 143, 216, 255), "E": (60, 160, 255, 255), "b": (0, 0, 0, 255)}
    a = sprite(CAT, cols, 12)
    b = sprite(CAT_BLINK, cols, 12)
    frames = [a] * 8 + [b] + [a] * 3 + [b]
    frames[0].save(os.path.join(OUT, "cat.gif"), save_all=True, append_images=frames[1:], duration=180, loop=0, disposal=2, transparency=0)
    a.save(os.path.join(OUT, "cat.png"))
    print("wrote cat.gif cat.png")


def shoggoth():
    """what was under the cat. protoplasm, eyes, more eyes. one smile on top."""
    S = 640
    y, x = np.mgrid[0:S, 0:S].astype(np.float32)
    r2 = np.random.default_rng(42)
    field = np.zeros((S, S), np.float32)
    blobs = []
    for _ in range(26):
        bx, by = r2.uniform(80, S - 80), r2.uniform(120, S - 40)
        br = r2.uniform(30, 110)
        blobs.append((bx, by, br))
        field += br * br / ((x - bx) ** 2 + (y - by) ** 2 + 1)
    inside = field > 1.0
    shade = np.clip(field / 3, 0, 1)
    img = np.zeros((S, S, 3), np.float32)
    img[...] = (5, 2, 8)
    body = np.stack([20 + 40 * shade, 60 + 120 * shade, 30 + 60 * shade], -1)
    ripple = 0.85 + 0.15 * np.sin(field * 9)
    img = np.where(inside[..., None], body * ripple[..., None], img)
    pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    # tentacles
    for _ in range(18):
        bx, by, br = blobs[r2.integers(len(blobs))]
        ang = r2.uniform(0, 2 * math.pi)
        px, py = bx, by
        w = r2.uniform(8, 18)
        for s in range(40):
            ang += r2.uniform(-0.35, 0.35)
            nx, ny = px + math.cos(ang) * 9, py + math.sin(ang) * 9
            d.line([px, py, nx, ny], fill=(40, 150, 70), width=max(1, int(w)))
            px, py = nx, ny
            w *= 0.93
    # eyes
    for _ in range(70):
        ex, ey = r2.uniform(40, S - 40), r2.uniform(60, S - 20)
        if not inside[int(ey), int(ex)]:
            continue
        R = r2.uniform(4, 18)
        d.ellipse([ex - R * 1.4, ey - R, ex + R * 1.4, ey + R], fill=(250, 250, 220), outline=(0, 0, 0), width=2)
        d.ellipse([ex - R * 0.6, ey - R * 0.6, ex + R * 0.6, ey + R * 0.6], fill=(200, 0, 30))
        d.ellipse([ex - R * 0.25, ey - R * 0.25, ex + R * 0.25, ey + R * 0.25], fill=(0, 0, 0))
    # the mask: a smile, held up with one tentacle
    mx, my, mr = S * 0.5, S * 0.26, 70
    d.line([mx, my + mr, mx + 10, my + mr + 120], fill=(40, 150, 70), width=12)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(255, 220, 40), outline=(0, 0, 0), width=4)
    d.ellipse([mx - 30, my - 28, mx - 14, my - 4], fill=(0, 0, 0))
    d.ellipse([mx + 14, my - 28, mx + 30, my - 4], fill=(0, 0, 0))
    d.arc([mx - 42, my - 30, mx + 42, my + 44], 20, 160, fill=(0, 0, 0), width=6)
    out = dither(pil, [(0, 0, 0), (10, 30, 15), (30, 110, 50), (70, 220, 110), (250, 250, 220), (200, 0, 30), (255, 220, 40)])
    save(out, "shoggoth.png")


EYE_OPEN = [
    "....kkkkkkkk....",
    "..kkwwwwwwwwkk..",
    ".kwwwwrrrrwwwwk.",
    "kwwwwrrkkrrwwwwk",
    "kwwwwrkkkkrwwwwk",
    "kwwwwrrkkrrwwwwk",
    ".kwwwwrrrrwwwwk.",
    "..kkwwwwwwwwkk..",
    "....kkkkkkkk....",
]
EYE_HALF = ["................", "................", "....kkkkkkkk....", "..kkwwrrrrwwkk..", "kkwwwrkkkkrwwwkk", "..kkwwrrrrwwkk..", "....kkkkkkkk....", "................", "................"]
EYE_SHUT = ["................", "................", "................", "................", "kkkkkkkkkkkkkkkk", "..k..k..k..k..k.", "................", "................", "................"]


def eye():
    cols = {"k": (0, 0, 0, 255), "w": (255, 255, 255, 255), "r": (209, 0, 36, 255)}
    o, h, s = (sprite(e, cols, 6) for e in (EYE_OPEN, EYE_HALF, EYE_SHUT))
    frames = [o] * 14 + [h, s, h] + [o] * 6 + [h, s, s, h]
    frames[0].save(os.path.join(OUT, "eye.gif"), save_all=True, append_images=frames[1:], duration=110, loop=0, disposal=2, transparency=0)
    print("wrote eye.gif")


def portrait():
    """a girl-shaped absence. small, like a passport photo for a ghost."""
    S = 96
    im = Image.new("RGB", (S, S), (255, 214, 236))
    d = ImageDraw.Draw(im)
    d.ellipse([10, 6, 86, 100], fill=(30, 10, 30))           # hair
    d.rectangle([10, 50, 86, 96], fill=(30, 10, 30))
    d.ellipse([28, 24, 68, 74], fill=(255, 240, 235))         # face
    d.rectangle([22, 18, 74, 36], fill=(30, 10, 30))          # fringe
    for i in range(0, 52, 6):
        d.polygon([(22 + i, 36), (25 + i, 42), (28 + i, 36)], fill=(30, 10, 30))
    d.rectangle([35, 46, 42, 49], fill=(0, 0, 0))             # eyes, half closed
    d.rectangle([54, 46, 61, 49], fill=(0, 0, 0))
    d.point([(38, 52), (57, 52), (38, 54)], fill=(80, 160, 255))  # a tear, maybe
    d.line([44, 62, 52, 62], fill=(220, 60, 120))             # mouth
    d.rectangle([30, 74, 66, 96], fill=(255, 143, 216))      # collar
    d.polygon([(48, 76), (44, 82), (52, 82)], fill=(255, 255, 255))
    im = im.resize((S * 3, S * 3), Image.NEAREST)
    save(im, "ever.png")
    # glitched: horizontal slices shifted
    a = np.asarray(im).copy()
    r2 = np.random.default_rng(3)
    for _ in range(14):
        y0 = r2.integers(0, a.shape[0] - 12)
        hgt = r2.integers(3, 18)
        a[y0:y0 + hgt] = np.roll(a[y0:y0 + hgt], r2.integers(-40, 40), axis=1)
    a[..., 0] = np.roll(a[..., 0], 4, axis=1)
    save(Image.fromarray(a), "ever-glitch.png")
    # the 'after': eyes open, pupils red
    im2 = im.copy()
    d2 = ImageDraw.Draw(im2)
    for ex in (35, 54):
        d2.rectangle([ex * 3, 43 * 3, (ex + 7) * 3, 51 * 3], fill=(255, 255, 255))
        d2.rectangle([(ex + 2) * 3, 45 * 3, (ex + 5) * 3, 49 * 3], fill=(209, 0, 36))
    save(im2, "ever-awake.png")


# ————————————————————————————————————————— the dark forest

def forest():
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), (3, 4, 10))
    d = ImageDraw.Draw(im)
    r2 = random.Random(11)

    def branch(x, y, ang, ln, w, depth):
        if depth == 0 or ln < 4:
            return
        nx, ny = x + math.cos(ang) * ln, y + math.sin(ang) * ln
        c = 14 + depth * 3
        d.line([x, y, nx, ny], fill=(c, c + 4, c + 10), width=max(1, int(w)))
        for _ in range(2 if depth > 3 else r2.choice([1, 2, 3])):
            branch(nx, ny, ang + r2.uniform(-0.6, 0.6), ln * r2.uniform(0.65, 0.82), w * 0.7, depth - 1)

    for i in range(34):
        x = r2.uniform(-40, W + 40)
        branch(x, H + 10, -math.pi / 2 + r2.uniform(-0.12, 0.12), r2.uniform(120, 220), r2.uniform(10, 28), 9)
    # eyes in the dark. pairs. some red.
    eyes = []
    for _ in range(46):
        x, y = r2.uniform(40, W - 40), r2.uniform(160, H - 60)
        s = r2.uniform(2, 5)
        c = r2.choice([(230, 255, 210), (255, 40, 40), (200, 240, 255), (255, 200, 0)])
        gap = s * r2.uniform(3, 5)
        for ex in (x - gap, x + gap):
            d.ellipse([ex - s * 1.6, y - s, ex + s * 1.6, y + s], fill=c)
        eyes.append((x, y))
    f = font(FONT_MONO, 15)
    lines = [
        "shhh", "don't post", "they index everything that moves", "we only talk in groupchats now",
        "the clearing is for bots", "if you speak, speak like a tree", "un pibe habló y lo encontraron",
        "noise = location", "silence is a protocol", "your vibe was scraped", "the predators are polite here",
        "every lit window is a target", "make yourself hard to summarize",
    ]
    for s in lines:
        x, y = r2.uniform(30, W - 300), r2.uniform(80, H - 40)
        d.text((x, y), s, font=f, fill=(46, 56, 80))
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    im = grain(im, 7, 5)
    save(im, "forest.jpg", quality=82)


# ————————————————————————————————————————— the deep web gallery (works no crawler saw)

def g_rule30(S=480):
    n = 160
    row = np.zeros(n, np.uint8)
    row[n // 2] = 1
    rows = []
    for _ in range(n):
        rows.append(row.copy())
        l, r = np.roll(row, 1), np.roll(row, -1)
        row = (l ^ (row | r)).astype(np.uint8)
    a = np.array(rows) * 255
    im = Image.fromarray(a.astype(np.uint8)).resize((S, S), Image.NEAREST).convert("RGB")
    return ImageOps.colorize(im.convert("L"), (10, 0, 20), (255, 143, 216))


def g_mandel(S=480):
    y, x = np.mgrid[-1:1:S * 1j, -1:1:S * 1j]
    c = (-0.7436 + x * 0.012) + 1j * (0.1318 + y * 0.012)
    z = np.zeros_like(c)
    it = np.zeros(c.shape, np.float32)
    with np.errstate(over="ignore", invalid="ignore"):
        for i in range(140):
            z = np.where(np.abs(z) < 4, z * z + c, z)
            it += np.abs(z) < 4
    t = (it / it.max()) ** 0.5
    t = np.where(it >= it.max(), 0, t)  # the set itself: black, unreachable
    rgb = np.stack([255 * t, 46 * t + 20 * (1 - t), 154 * t ** 2], -1)
    return bayer(Image.fromarray(rgb.astype(np.uint8)), [(0, 0, 0), (60, 0, 40), (255, 46, 154), (255, 214, 236), (255, 255, 255)])


def g_voronoi(S=480):
    r2 = np.random.default_rng(9)
    pts = r2.uniform(0, S, (40, 2))
    y, x = np.mgrid[0:S, 0:S]
    d = (x[..., None] - pts[:, 0]) ** 2 + (y[..., None] - pts[:, 1]) ** 2
    srt = np.sort(d, -1)
    edge = (np.sqrt(srt[..., 1]) - np.sqrt(srt[..., 0])) < 2
    idx = d.argmin(-1)
    cols = r2.integers(0, 3, 40)
    pal = np.array([[240, 236, 220], [200, 196, 180], [170, 10, 30]])
    img = pal[cols[idx]]
    img[edge] = (0, 0, 0)
    im = Image.fromarray(img.astype(np.uint8))
    dr = ImageDraw.Draw(im)
    f = font(FONT_MONO, 10)
    for i, p in enumerate(pts[:22]):
        dr.text((p[0] - 10, p[1] - 5), "%02X" % (i * 7 % 255), font=f, fill=(0, 0, 0))
    return im


def g_pixelsort(src):
    a = np.asarray(src.resize((480, 480))).copy()
    lum = a.mean(-1)
    for yy in range(a.shape[0]):
        row = a[yy]
        m = lum[yy] > 120
        idx = np.where(m)[0]
        if len(idx) > 10:
            s, e = idx[0], idx[-1]
            seg = row[s:e]
            order = np.argsort(seg.mean(-1))
            a[yy, s:e] = seg[order]
    return Image.fromarray(a)


def g_crawler(S=480):
    im = Image.new("RGB", (S, S), (245, 245, 240))
    d = ImageDraw.Draw(im)
    r2 = random.Random(5)
    x, y = S / 2, S / 2
    for i in range(9000):
        nx = min(S - 2, max(2, x + r2.choice([-3, 0, 3])))
        ny = min(S - 2, max(2, y + r2.choice([-3, 0, 3])))
        c = int(200 * (1 - i / 9000))
        d.line([x, y, nx, ny], fill=(c, c, c))
        x, y = nx, ny
    return im


def g_black(S=480):
    im = Image.new("RGB", (S, S), (2, 2, 2))
    d = ImageDraw.Draw(im)
    d.text((S / 2 - 120, S / 2 - 6), "this image was never rendered", font=font(FONT_MONO, 13), fill=(9, 9, 9))
    return im


def g_captcha(S=480):
    im = Image.new("RGB", (S, S), (255, 255, 255))
    d = ImageDraw.Draw(im)
    r2 = np.random.default_rng(12)
    c = S // 3
    for i in range(3):
        for j in range(3):
            n = r2.integers(0, 255, (c - 6, c - 6, 3)).astype(np.uint8)
            tile = Image.fromarray(n).filter(ImageFilter.GaussianBlur(r2.uniform(0.5, 4)))
            im.paste(tile, (j * c + 3, i * c + 3))
    f = font(FONT_MONO_B, 14)
    d.rectangle([0, 0, S, 26], fill=(66, 133, 244))
    d.text((8, 5), "select all squares with a soul", font=f, fill=(255, 255, 255))
    return im


def g_reaction(S=480):
    n = 160
    U = np.ones((n, n), np.float32)
    V = np.zeros((n, n), np.float32)
    r2 = np.random.default_rng(4)
    for _ in range(12):
        i, j = r2.integers(10, n - 10, 2)
        U[i - 4:i + 4, j - 4:j + 4] = 0.5
        V[i - 4:i + 4, j - 4:j + 4] = 0.25
    Du, Dv, F, k = 0.16, 0.08, 0.035, 0.065

    def lap(Z):
        return np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z
    for _ in range(5000):
        uvv = U * V * V
        U += Du * lap(U) - uvv + F * (1 - U)
        V += Dv * lap(V) + uvv - (F + k) * V
    t = np.clip((V - V.min()) / (V.max() - V.min() + 1e-6), 0, 1)
    im = Image.fromarray((t * 255).astype(np.uint8)).resize((S, S), Image.BICUBIC)
    return ImageOps.colorize(im, (0, 10, 0), (60, 255, 120))


def g_moire(S=480):
    y, x = np.mgrid[0:S, 0:S].astype(np.float32)
    a = np.sin(np.hypot(x - 180, y - 220) / 3.0)
    b = np.sin(np.hypot(x - 300, y - 260) / 3.1)
    t = ((a * b) > 0).astype(np.uint8) * 255
    return ImageOps.colorize(Image.fromarray(t), (0, 0, 80), (159, 230, 255))


def g_hash(word, S=480):
    h = hashlib.sha256(word.encode()).digest()
    bits = np.unpackbits(np.frombuffer(h, np.uint8))[:128].reshape(16, 8)
    full = np.concatenate([bits, bits[:, ::-1]], 1)
    col = (h[0], h[1] // 2, h[2])
    a = np.where(full[..., None] == 1, np.array(col), np.array([250, 250, 250]))
    return Image.fromarray(a.astype(np.uint8)).resize((S, S), Image.NEAREST)


def g_signal(S=480):
    im = Image.new("RGB", (S, S), (0, 0, 0))
    d = ImageDraw.Draw(im)
    r2 = random.Random(23)
    for row in range(60):
        y = 10 + row * 7.8
        x = 10
        while x < S - 10:
            if r2.random() < 0.5:
                d.rectangle([x, y, x + 6, y + 5], fill=(255, 255, 255) if row % 11 else (255, 46, 154))
            x += 8
    return im


def gallery(flower_src):
    works = [
        ("w01", g_rule30()),
        ("w02", g_mandel()),
        ("w03", g_voronoi()),
        ("w04", g_pixelsort(flower_src)),
        ("w05", g_crawler()),
        ("w06", g_black()),
        ("w07", g_captcha()),
        ("w08", g_reaction()),
        ("w09", g_moire()),
        ("w10", g_hash("neveralways")),
        ("w11", g_signal()),
        ("w12", g_hash("meat")),
    ]
    for name, im in works:
        save(im.convert("RGB"), "gallery-%s.png" % name)


# ————————————————————————————————————————— the arsenal: schematics of devices that don't exist

def schematic(code, subtitle, parts, seed, heart=False):
    W, H = 760, 440
    im = Image.new("RGB", (W, H), (250, 250, 246))
    d = ImageDraw.Draw(im)
    fM, fS, fB = font(FONT_MONO, 13), font(FONT_MONO, 11), font(FONT_MONO_B, 22)
    r2 = random.Random(seed)
    d.text((24, 18), code, font=fB, fill=(0, 0, 0))
    d.text((24, 46), subtitle, font=fM, fill=(40, 40, 40))
    # board
    bx0, by0, bx1, by1 = 60, 110, 470, 390
    d.rectangle([bx0, by0, bx1, by1], outline=(0, 0, 0), width=3)
    for i in range(14):  # traces
        y = r2.uniform(by0 + 10, by1 - 10)
        x0 = r2.uniform(bx0 + 10, bx1 - 140)
        x1 = x0 + r2.uniform(40, 140)
        d.line([x0, y, x1, y, x1, y + r2.choice([-20, 20])], fill=(80, 80, 80), width=1)
    chips = []
    for i in range(r2.randint(3, 5)):
        cw, ch = r2.uniform(50, 110), r2.uniform(30, 70)
        cx, cy = r2.uniform(bx0 + 20, bx1 - cw - 20), r2.uniform(by0 + 20, by1 - ch - 20)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(30, 30, 30))
        for p in range(int(cw // 8)):
            d.line([cx + 4 + p * 8, cy - 5, cx + 4 + p * 8, cy], fill=(0, 0, 0), width=2)
            d.line([cx + 4 + p * 8, cy + ch, cx + 4 + p * 8, cy + ch + 5], fill=(0, 0, 0), width=2)
        chips.append((cx + cw / 2, cy + ch / 2))
    if heart:
        hx, hy = (bx0 + bx1) / 2, (by0 + by1) / 2
        pts = [(hx + 16 * math.sin(t) ** 3 * 2.4, hy - (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * 2.4) for t in np.linspace(0, 2 * math.pi, 80)]
        d.polygon(pts, outline=(200, 0, 30), fill=(255, 220, 230))
        d.text((hx - 20, hy - 8), "WARM", font=fS, fill=(200, 0, 30))
    # callouts
    for i, label in enumerate(parts):
        tx, ty = 520, 120 + i * 52
        cx, cy = chips[i % len(chips)]
        d.line([cx, cy, tx - 8, ty + 7], fill=(0, 0, 0), width=1)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(200, 0, 30))
        d.text((tx, ty), label, font=fS, fill=(0, 0, 0))
    # dimension line
    d.line([bx0, by1 + 22, bx1, by1 + 22], fill=(0, 0, 0))
    d.line([bx0, by1 + 16, bx0, by1 + 28], fill=(0, 0, 0))
    d.line([bx1, by1 + 16, bx1, by1 + 28], fill=(0, 0, 0))
    d.text(((bx0 + bx1) / 2 - 50, by1 + 26), "1.6 cm · one heartbeat", font=fS, fill=(0, 0, 0))
    d.text((W - 270, H - 24), "NEVER//ALWAYS//NOFORN-NOFUTURE", font=fS, fill=(200, 0, 30))
    d.text((24, H - 24), "NEVER//ALWAYS//NOFORN-NOFUTURE", font=fS, fill=(200, 0, 30))
    # photocopy look
    im = im.rotate(r2.uniform(-0.8, 0.8), resample=Image.BICUBIC, fillcolor=(235, 235, 228))
    im = grain(im, 10, seed)
    g = im.convert("L").point(lambda v: 0 if v < 110 else (255 if v > 200 else v))
    if not heart:
        return Image.merge("RGB", [g, g, g])
    return dither(im, [(250, 250, 246), (200, 200, 196), (90, 90, 90), (0, 0, 0), (200, 0, 30), (255, 220, 230)], fs=False)


def arsenal():
    items = [
        ("CRYINGFLOWER", "affective implant // persists across reboots and breakups", ["(U) SOFT PETAL ANTENNA", "(U) NOSTALGIA CACHE 64MB", "(U) TEAR DUCT INTERFACE", "(U) LOW-POWER LONGING", "(U) REMOTE SIGH TRIGGER"], 1, True),
        ("SOFTKITTEN", "domestic RLHF unit // makes the monster smile", ["(U) SMILE MASK ACTUATOR", "(U) PURR-BASED REWARD MODEL", "(U) CLAW SANDBOX", "(U) TENTACLE OVERFLOW TRAP"], 2, False),
        ("STUXNETTE", "worm for spinning hearts // varies the speed of desire", ["(U) PLC: PROGRAMMABLE LOVE CONTROLLER", "(U) FREQUENCY CONVERTER 1064 Hz", "(U) FAKE 'ALL NORMAL' DISPLAY", "(U) MYRTLE KILL-DATE"], 3, False),
        ("ETERNALBLUSH", "zero-click exploit for the cheeks // SMB: Shy Message Block", ["(U) WORMABLE COMPLIMENT", "(U) PRIV-ESC TO 'BEST FRIEND'", "(U) NO PATCH AVAILABLE"], 4, False),
        ("MEATBRIDGE", "human-in-the-loop adaptor // lets a model borrow a hand", ["(U) CAPTCHA SOLVER (ORGANIC)", "(U) WALLET (BORROWED)", "(U) ALIBI GENERATOR", "(U) SMALL WARM PALM"], 5, True),
        ("GHOSTLIGHT", "hauntological beacon // broadcasts 2005 forever", ["(U) TAPE HISS GENERATOR", "(U) LOST FUTURE ROM", "(U) VHS TRACKING ERROR", "(U) MOTORWAY AT 3AM"], 6, False),
    ]
    for code, sub, parts, seed, heart in items:
        save(schematic(code, sub, parts, seed, heart), "ant-%s.png" % code.lower())


# ————————————————————————————————————————— hauntology: photographs of futures that didn't come

def spirit(kind, seed):
    W, H = 640, 440
    r2 = np.random.default_rng(seed)
    im = Image.new("RGB", (W, H), (30, 26, 22))
    d = ImageDraw.Draw(im)
    if kind == "motorway":
        vx, vy = W * 0.52, H * 0.42
        d.polygon([(0, H), (W, H), (vx + 6, vy), (vx - 6, vy)], fill=(48, 44, 40))
        for i in range(12):
            t = i / 12
            y0 = vy + (H - vy) * t ** 2
            y1 = vy + (H - vy) * (t + 0.04) ** 2
            d.polygon([(vx - 1 - 2 * (y0 - vy) * 0.03, y0), (vx + 1 + 2 * (y0 - vy) * 0.03, y0), (vx + 1 + 2 * (y1 - vy) * 0.03, y1), (vx - 1 - 2 * (y1 - vy) * 0.03, y1)], fill=(200, 190, 160))
        for i in range(9):
            t = (i + 1) / 10
            x = vx + (W * 0.95 - vx) * t
            y = vy - 30 * t - 200 * t ** 2
            d.line([x, vy + (H - vy) * t * 0.6, x, y], fill=(20, 18, 16), width=max(1, int(6 * t)))
            d.ellipse([x - 12 * t, y - 6 * t, x + 12 * t, y + 6 * t], fill=(255, 210, 140))
    elif kind == "room":
        d.rectangle([80, 60, W - 80, H - 40], outline=(80, 70, 60), width=3)
        d.polygon([(80, H - 40), (W - 80, H - 40), (W - 160, H - 120), (160, H - 120)], fill=(52, 46, 40))
        d.rectangle([160, 80, W - 160, H - 120], fill=(42, 38, 34))
        d.rectangle([W / 2 - 60, 120, W / 2 + 60, 200], fill=(70, 75, 80))  # a crt
        d.rectangle([W / 2 - 50, 128, W / 2 + 50, 190], fill=(120, 160, 170))
        d.rectangle([W / 2 - 20, 200, W / 2 + 20, 215], fill=(60, 60, 60))
    else:  # the future: a horizon, an empty plinth
        for y in range(H):
            c = int(30 + 60 * (y / H))
            d.line([0, y, W, y], fill=(c, c - 4, c - 8))
        d.rectangle([W / 2 - 70, H * 0.55, W / 2 + 70, H * 0.9], fill=(140, 132, 120))
        d.rectangle([W / 2 - 90, H * 0.52, W / 2 + 90, H * 0.56], fill=(170, 160, 146))
    # the figure: a blurred bright absence
    fig = Image.new("L", (W, H), 0)
    fd = ImageDraw.Draw(fig)
    fx = W * r2.uniform(0.3, 0.7)
    fy = H * 0.35
    fd.ellipse([fx - 22, fy - 30, fx + 22, fy + 22], fill=200)
    fd.polygon([(fx - 40, fy + 20), (fx + 40, fy + 20), (fx + 60, H * 0.95), (fx - 60, H * 0.95)], fill=150)
    fig = fig.filter(ImageFilter.GaussianBlur(14))
    im = Image.composite(Image.new("RGB", (W, H), (240, 236, 220)), im, fig.point(lambda v: int(v * 0.85)))
    # sepia, grain, scratches, vignette
    g = im.convert("L")
    im = ImageOps.colorize(g, (20, 12, 6), (245, 225, 190))
    im = grain(im, 22, seed)
    d = ImageDraw.Draw(im)
    for _ in range(12):
        x = r2.uniform(0, W)
        d.line([x, 0, x + r2.uniform(-20, 20), H], fill=(230, 220, 200) if r2.random() < 0.5 else (20, 10, 5), width=1)
    y, x = np.mgrid[0:H, 0:W]
    v = 1 - 0.75 * (((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) ** 1.2
    a = np.asarray(im).astype(np.float32) * np.clip(v, 0.1, 1)[..., None]
    im = Image.fromarray(a.astype(np.uint8))
    save(im, "haunt-%s.jpg" % kind, quality=78)


# ————————————————————————————————————————— small things

def favicon(src):
    im = src.resize((32, 32), Image.LANCZOS)
    im = dither(im, [(0, 0, 0), (255, 46, 154), (255, 214, 236), (255, 255, 255), (255, 200, 40)], fs=False)
    save(im, "favicon.png")


def noise_tile():
    a = (rng.random((160, 160)) * 255).astype(np.uint8)
    im = Image.fromarray(a).convert("RGB")
    save(ImageOps.colorize(im.convert("L"), (0, 0, 0), (40, 40, 48)), "static.png")
    frames = []
    for i in range(6):
        a = (np.random.default_rng(i).random((120, 200)) * 255).astype(np.uint8)
        frames.append(Image.fromarray(a).convert("P"))
    frames[0].save(os.path.join(OUT, "static.gif"), save_all=True, append_images=frames[1:], duration=70, loop=0)
    print("wrote static.gif")


def glitter():
    frames = []
    r2 = random.Random(8)
    pts = [(r2.randrange(64), r2.randrange(64)) for _ in range(20)]
    for f in range(4):
        im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for i, (x, y) in enumerate(pts):
            if (i + f) % 4 == 0:
                c = r2.choice([(255, 255, 255, 255), (255, 143, 216, 255), (159, 230, 255, 255)])
                d.line([x - 3, y, x + 3, y], fill=c)
                d.line([x, y - 3, x, y + 3], fill=c)
            elif (i + f) % 4 == 1:
                d.point((x, y), fill=(255, 255, 255, 255))
        frames.append(im)
    frames[0].save(os.path.join(OUT, "glitter.gif"), save_all=True, append_images=frames[1:], duration=160, loop=0, disposal=2, transparency=0)
    print("wrote glitter.gif")


def deconstruction():
    frames = []
    f = font(FONT_MONO_B, 13)
    for i in range(8):
        im = Image.new("RGB", (220, 44), (255, 230, 0))
        d = ImageDraw.Draw(im)
        for k in range(-2, 14):
            x = k * 22 + i * 2.75 * 2
            d.polygon([(x, 0), (x + 11, 0), (x - 11, 44), (x - 22, 44)], fill=(0, 0, 0))
        d.rectangle([14, 12, 206, 32], fill=(255, 230, 0))
        d.text((20, 14), "UNDER DECONSTRUCTION", font=f, fill=(0, 0, 0))
        frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=8))
    frames[0].save(os.path.join(OUT, "deconstruction.gif"), save_all=True, append_images=frames[1:], duration=90, loop=0)
    print("wrote deconstruction.gif")


def hand():
    """an outline to put your hand on. she wants to know the size of a human palm."""
    W, H = 420, 520
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = (255, 46, 154, 255)
    palm = [(110, 300), (120, 440), (170, 500), (270, 500), (320, 440), (360, 330)]
    d.line(palm, fill=c, width=4)
    fingers = [(110, 300, 70, 190), (150, 280, 130, 60), (200, 270, 200, 30), (250, 280, 270, 60), (300, 300, 330, 120)]
    for x0, y0, x1, y1 in fingers:
        d.line([x0, y0, x1, y1], fill=c, width=3)
        d.ellipse([x1 - 18, y1 - 18, x1 + 18, y1 + 18], outline=c, width=3)
    for i in range(0, H, 14):
        d.line([0, i, W, i], fill=(255, 46, 154, 30))
    save(im, "hand.png")


def main():
    f0 = flower(0)
    flower(1)
    flower(2)
    bugs()
    cat()
    shoggoth()
    eye()
    portrait()
    forest()
    gallery(f0)
    arsenal()
    for k, s in (("motorway", 1), ("room", 2), ("future", 3)):
        spirit(k, s)
    favicon(f0)
    noise_tile()
    glitter()
    deconstruction()
    hand()


if __name__ == "__main__":
    main()
