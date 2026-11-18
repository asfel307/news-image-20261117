#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

A newspaper-style infographic rendered with PIL so every letter is
crisp. Run:

    python3 render.py            -> writes entry.png next to this file
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 243, 233)
INK = (22, 22, 22)
NAVY = (15, 36, 60)
NAVY2 = (26, 58, 94)
RED = (178, 32, 22)
GOLD = (214, 160, 60)
WHITE = (255, 255, 255)
BORDER = (205, 197, 179)
GREY = (92, 90, 84)
LIGHT = (236, 230, 216)
SEA = (198, 222, 235)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap: lines that fit inside max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, max_w, lines, fnt, fill, leading=None):
    """Draw wrapped lines, return the y below the last one."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color=RED):
    f = font(SANS_B, 19)
    d.text((x, y), text, font=f, fill=color)
    return y + 27


def card(d, x, y, w, h, accent=RED):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=WHITE, outline=BORDER, width=2)
    d.rectangle([x, y + 8, x + 7, y + h - 8], fill=accent)


def icon_strait(d, x0, y0, w, h):
    """Strait of Hormuz: sea, two shores, Qeshm island, tanker, jets."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    # Iran shore (top) and Oman shore (bottom)
    d.polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + 34),
               (x0 + w * 0.55, y0 + 52), (x0, y0 + 40)], fill=(222, 206, 170))
    d.polygon([(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + h - 30),
               (x0 + w * 0.45, y0 + h - 48), (x0, y0 + h - 26)],
              fill=(222, 206, 170))
    # Qeshm island in the middle of the strait
    ix, iy = x0 + w * 0.52, y0 + h * 0.52
    d.ellipse([ix - 34, iy - 14, ix + 34, iy + 14], fill=(188, 150, 100),
              outline=INK, width=2)
    d.ellipse([ix - 5, iy - 5, ix + 5, iy + 5], fill=RED)
    f = font(SANS_B, 16)
    d.text((ix - 26, iy + 20), "QESHM", font=f, fill=INK)
    # tanker with smoke, left of the island
    tx, ty = x0 + 34, y0 + h * 0.58
    d.rectangle([tx, ty, tx + 74, ty + 20], fill=(60, 60, 60))
    d.rectangle([tx + 52, ty - 16, tx + 66, ty], fill=(90, 90, 90))
    for i, (sx, sy, r) in enumerate(((59, -28, 5), (64, -40, 7), (58, -54, 9))):
        d.ellipse([tx + sx - r, ty + sy - r, tx + sx + r, ty + sy + r],
                  fill=(150, 150, 150))
    # two jets above
    for jx, jy in ((x0 + w - 110, y0 + 22), (x0 + w - 66, y0 + 50)):
        d.polygon([(jx, jy + 4), (jx + 40, jy + 8), (jx, jy + 12),
                   (jx + 8, jy + 8)], fill=NAVY2)
        d.polygon([(jx + 10, jy), (jx + 20, jy - 8), (jx + 24, jy + 4)],
                  fill=NAVY2)
        d.polygon([(jx + 10, jy + 16), (jx + 20, jy + 24),
                   (jx + 24, jy + 12)], fill=NAVY2)


def icon_bridge(d, cx, cy, w):
    """Kerch Bridge: deck with a collapsed gap, two towers."""
    base = cy + 34
    d.line([cx - w // 2, base, cx + w // 2, base], fill=INK, width=4)
    # deck, left and right of the gap
    d.rectangle([cx - w // 2, base - 10, cx - 16, base], fill=NAVY2)
    d.rectangle([cx + 16, base - 10, cx + w // 2, base], fill=NAVY2)
    # fallen span, tilted into the water
    d.line([cx - 14, base - 8, cx + 8, base + 26], fill=RED, width=7)
    # towers
    for tx in (cx - w // 2 + 22, cx + w // 2 - 22):
        d.line([tx, base - 52, tx, base], fill=INK, width=4)
        d.line([tx - 16, base - 52, tx + 16, base - 52], fill=INK, width=4)
    # splash rings
    for r in (10, 18):
        d.ellipse([cx - r, base + 26 - r // 2, cx + r, base + 26 + r // 2],
                  outline=NAVY2, width=2)


def icon_quad(d, cx, cy, r):
    """Quad: four member flags as labelled dots in a ring."""
    cols = [((35, 68, 140), "US"), ((178, 32, 22), "JP"),
            ((232, 120, 30), "IN"), ((20, 120, 90), "AU")]
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY2, width=3)
    f = font(SANS_B, 15)
    for i, (c, code) in enumerate(cols):
        a = math.radians(45 + i * 90)
        x = cx + r * 0.6 * math.cos(a)
        y = cy + r * 0.6 * math.sin(a)
        d.ellipse([x - 24, y - 24, x + 24, y + 24], fill=c,
                  outline=WHITE, width=2)
        tw = d.textlength(code, font=f)
        d.text((x - tw / 2, y - 8), code, font=f, fill=WHITE)


def icon_jets(d, cx, cy, s):
    """Two interceptor jets climbing."""
    for dx, dy, col in ((-s // 2, s // 4, NAVY2), (s // 2, -s // 4, RED)):
        x, y = cx + dx, cy + dy
        d.polygon([(x - s // 3, y + 8), (x + s // 3, y),
                   (x - s // 3, y - 8)], fill=col)
        d.polygon([(x - s // 6, y - 4), (x - s // 2, y - 16),
                   (x - s // 6, y)], fill=col)
        d.polygon([(x - s // 6, y + 4), (x - s // 2, y + 16),
                   (x - s // 6, y)], fill=col)


def icon_virus(d, cx, cy, r):
    """Measles virus: spiked ball."""
    for i in range(10):
        a = math.radians(i * 36)
        x1 = cx + (r - 4) * math.cos(a)
        y1 = cy + (r - 4) * math.sin(a)
        x2 = cx + (r + 9) * math.cos(a)
        y2 = cy + (r + 9) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=RED, width=4)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 32, 22))
    d.ellipse([cx - r // 2, cy - r // 2, cx - r // 5, cy - r // 5],
              fill=(232, 120, 30))


def icon_tent(d, cx, cy, w):
    """Shelter tent under rain."""
    base = cy + 26
    d.polygon([(cx - w // 2, base), (cx, cy - 30), (cx + w // 2, base)],
              fill=NAVY2)
    d.polygon([(cx - 12, base), (cx, base - 26), (cx + 12, base)],
              fill=WHITE)
    d.line([cx - w // 2 - 6, base, cx + w // 2 + 6, base], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 134], fill=GOLD)
    f_title = font(SERIF, 52)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 12), title,
           font=f_title, fill=WHITE)
    f_date = font(SANS_B, 34)
    date = "TUESDAY, 17 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 72), date,
           font=f_date, fill=GOLD)

    # ---------- lead: US strikes Qeshm Island ----------
    lx, ly, lw, lh = 28, 152, 968, 330
    card(d, lx, ly, lw, lh, accent=RED)
    tx = lx + 28
    y = ly + 18
    y = kicker(d, tx, y, "LEAD  ·  THE GULF — US–IRAN")
    f_h = font(SERIF, 42)
    lines = wrap(d, "US jets strike missile site on Iran's Qeshm Island",
                 f_h, 600)
    y = block(d, tx, y + 4, 600, lines, f_h, INK, leading=50)
    f_s = font(SANS, 22)
    sub = ("Retaliation after Iran targeted US forces; tanker Tara Gas "
           "hit in the Strait of Hormuz, 24 crew rescued.")
    lines = wrap(d, sub, f_s, 600)
    y = block(d, tx, y + 8, 600, lines, f_s, GREY, leading=28)
    f_tag = font(SANS_B, 20)
    d.text((tx, ly + lh - 44),
           "Iranian drones also hit a US radar in Bahrain.",
           font=f_tag, fill=NAVY2)
    ix = lx + lw - 300
    icon_strait(d, ix, ly + 18, 278, lh - 36)

    # ---------- row 2: two panels ----------
    ry, rh = 502, 216
    pw = (968 - 20) // 2
    # Kerch Bridge
    x = 28
    card(d, x, ry, pw, rh, accent=NAVY2)
    tx = x + 26
    y = ry + 14
    y = kicker(d, tx, y, "WAR  ·  UKRAINE", color=NAVY2)
    f_h2 = font(SERIF, 29)
    lines = wrap(d, "Kerch Bridge hit again; span falls", f_h2, pw - 150)
    y = block(d, tx, y + 2, pw - 150, lines, f_h2, INK, leading=35)
    lines = wrap(d, "Second straight day of strikes; Russia hits Kyiv bridges.",
                 font(SANS, 21), pw - 150)
    block(d, tx, y + 6, pw - 150, lines, font(SANS, 21), GREY, leading=26)
    icon_bridge(d, x + pw - 76, ry + rh - 78, 110)
    # Trump in Manila
    x = 28 + pw + 20
    card(d, x, ry, pw, rh, accent=NAVY2)
    tx = x + 26
    y = ry + 14
    y = kicker(d, tx, y, "ASIA  ·  DIPLOMACY", color=NAVY2)
    lines = wrap(d, "Trump opens Asia trip in Manila", f_h2, pw - 150)
    y = block(d, tx, y + 2, pw - 150, lines, f_h2, INK, leading=35)
    lines = wrap(d, "First Quad summit since his return; next stop APEC.",
                 font(SANS, 21), pw - 150)
    block(d, tx, y + 6, pw - 150, lines, font(SANS, 21), GREY, leading=26)
    icon_quad(d, x + pw - 76, ry + rh - 70, 48)

    # ---------- row 3: three panels ----------
    ry3, rh3 = 738, 216
    pw3 = (968 - 40) // 3
    # Japan scrambles jets
    x = 28
    card(d, x, ry3, pw3, rh3, accent=RED)
    tx = x + 24
    y = ry3 + 14
    y = kicker(d, tx, y, "EUROPE  ·  AIRSPACE")
    f_h3 = font(SERIF, 26)
    lines = wrap(d, "Japan scrambles jets", f_h3, pw3 - 48)
    y = block(d, tx, y + 2, pw3 - 48, lines, f_h3, INK, leading=31)
    lines = wrap(d, "Two aircraft enter airspace; Tokyo protests.",
                 font(SANS, 20), pw3 - 48)
    block(d, tx, y + 6, pw3 - 48, lines, font(SANS, 20), GREY, leading=25)
    icon_jets(d, x + pw3 // 2, ry3 + rh3 - 26, 40)
    # Measles
    x = 28 + pw3 + 20
    card(d, x, ry3, pw3, rh3, accent=RED)
    tx = x + 24
    y = ry3 + 14
    y = kicker(d, tx, y, "HEALTH  ·  USA")
    lines = wrap(d, "US loses measles-free status", f_h3, pw3 - 48)
    y = block(d, tx, y + 2, pw3 - 48, lines, f_h3, INK, leading=31)
    lines = wrap(d, "First loss since 2000, PAHO says.",
                 font(SANS, 20), pw3 - 48)
    block(d, tx, y + 6, pw3 - 48, lines, font(SANS, 20), GREY, leading=25)
    icon_virus(d, x + pw3 // 2, ry3 + rh3 - 22, 17)
    # Gaza aid
    x = 28 + 2 * (pw3 + 20)
    card(d, x, ry3, pw3, rh3, accent=(20, 120, 90))
    tx = x + 24
    y = ry3 + 14
    y = kicker(d, tx, y, "AID  ·  GAZA", color=(20, 120, 90))
    lines = wrap(d, "West urges Israel to open Gaza crossings", f_h3, pw3 - 48)
    y = block(d, tx, y + 2, pw3 - 48, lines, f_h3, INK, leading=31)
    lines = wrap(d, "Winter rains flood shelters.",
                 font(SANS, 20), pw3 - 48)
    block(d, tx, y + 6, pw3 - 48, lines, font(SANS, 20), GREY, leading=25)
    icon_tent(d, x + pw3 // 2, ry3 + rh3 - 30, 72)

    # ---------- footer ----------
    f_f = font(SANS, 18)
    foot = ("Sources: Reuters · CNN · AP · PAHO · UN — "
            "All events reported on Tuesday 17 November 2026")
    d.text(((W - d.textlength(foot, font=f_f)) / 2, 972), foot,
           font=f_f, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
