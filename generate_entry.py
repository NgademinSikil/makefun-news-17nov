#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a newspaper front page summing up
Tuesday 17 November 2026, painted with Pillow at 1024x1024.

Run:  python3 generate_entry.py  ->  entry.png (1024x1024, < 1 MiB)

The picture is deterministic: no randomness, no timestamps, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (28, 78, 140)
GRAY = (110, 110, 110)
LIGHT = (238, 238, 236)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def para(draw, x, y, text, fnt, max_width, leading=None, fill=INK):
    """Draw wrapped paragraph, left aligned; returns y below last line."""
    lh = leading if leading is not None else int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- masthead
def draw_masthead(draw):
    title = font(SERIF, 96)
    centred(draw, W // 2, 30, "THE WORLD", title)
    rule(draw, MARGIN, W - MARGIN, 140, width=5, fill=RED)
    rule(draw, MARGIN, W - MARGIN, 149, width=2)
    date = font(SANS_B, 30)
    centred(draw, W // 2, 160, "TUESDAY 17 NOVEMBER 2026", date)
    rule(draw, MARGIN, W - MARGIN, 200, width=2)


# ------------------------------------------------------------ main story
def draw_bridge(draw, x0, x1, y0, y1):
    """Flat bridge over a strait, its road arch broken in the middle."""
    # sky band
    draw.rectangle([x0, y0, x1, y0 + 26], fill=(214, 228, 240))
    # water band
    water_top = y1 - 30
    draw.rectangle([x0, water_top, x1, y1], fill=(168, 200, 228))
    for wy in (water_top + 9, water_top + 19):
        for wx in range(x0 + 6, x1 - 30, 60):
            draw.arc([wx, wy - 5, wx + 34, wy + 5], 180, 360, fill=BLUE, width=3)
    # piers
    deck_y = y0 + 52
    for px in (x0 + 120, x1 - 150):
        draw.rectangle([px, deck_y, px + 26, water_top + 4], fill=GRAY)
    # deck, broken in the middle
    gap = 46
    mid = (x0 + x1) // 2
    draw.line([(x0, deck_y), (mid - gap, deck_y)], fill=INK, width=7)
    draw.line([(mid + gap, deck_y), (x1, deck_y)], fill=INK, width=7)
    # arch below the deck on each side
    for (ax0, ax1) in ((x0 + 40, mid - gap - 8), (mid + gap + 8, x1 - 40)):
        draw.arc([ax0, deck_y - 6, ax1, deck_y + 66], 180, 360, fill=RED, width=6)
    # fallen arch piece, tilted into the water
    draw.line([(mid - 34, deck_y + 8), (mid + 22, water_top - 2)],
              fill=RED, width=6)
    draw.line([(mid - 22, deck_y + 12), (mid + 34, water_top - 6)],
              fill=RED, width=6)
    # smoke puffs above the gap
    for (sx, sy, sr) in ((mid - 26, y0 + 22, 13), (mid + 4, y0 + 12, 17),
                         (mid + 30, y0 + 24, 11)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 150, 150))
    # two small drones
    for (dx, dy) in ((x0 + 210, y0 + 8), (x1 - 230, y0 + 4)):
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)
        draw.line([(dx - 12, dy), (dx + 12, dy)], fill=INK, width=2)


def draw_main_story(draw):
    label = font(SANS_B, 21)
    draw.text((MARGIN, 214), "TOP STORY", font=label, fill=RED)
    head = font(SERIF, 58)
    centred(draw, W // 2, 240, "KERCH BRIDGE FALLS", head)
    body = font(SANS, 25)
    para(draw, MARGIN + 8, 312,
         "Ukrainian drones and missiles drop the road arch into the strait; "
         "two killed; rail back on one track \u2014 as Russia hits Kyiv's "
         "bridges in reply.",
         body, W - 2 * MARGIN - 16, leading=33)
    draw_bridge(draw, MARGIN, W - MARGIN, 388, 492)
    rule(draw, MARGIN, W - MARGIN, 506, width=4, fill=RED)


# ------------------------------------------------------------- four panels
def draw_jet_icon(draw, x, y, s):
    """Small flat jet, nose up-right, with a burst behind it."""
    draw.polygon([(x + 6 * s, y + 52 * s), (x + 58 * s, y + 6 * s),
                  (x + 52 * s, y + 26 * s), (x + 30 * s, y + 40 * s),
                  (x + 34 * s, y + 58 * s)], fill=(70, 70, 70))
    draw.polygon([(x + 34 * s, y + 34 * s), (x + 62 * s, y + 30 * s),
                  (x + 60 * s, y + 42 * s), (x + 40 * s, y + 46 * s)],
                 fill=(70, 70, 70))
    for ang in range(0, 360, 45):
        import math
        r0, r1 = 4 * s, 12 * s
        cx, cy = x + 8 * s, y + 8 * s
        draw.line([(cx + r0 * math.cos(math.radians(ang)),
                    cy + r0 * math.sin(math.radians(ang))),
                   (cx + r1 * math.cos(math.radians(ang)),
                    cy + r1 * math.sin(math.radians(ang)))],
                  fill=RED, width=3)


def draw_tents_icon(draw, x, y, s):
    """Row of tents with rain slanting down."""
    for i, tx in enumerate((0, 22, 44)):
        col = (200, 120, 40) if i % 2 == 0 else (60, 110, 80)
        draw.polygon([(x + tx * s, y + 52 * s), (x + (tx + 11) * s, y + 22 * s),
                      (x + (tx + 22) * s, y + 52 * s)], fill=col)
    for rx in range(4, 64, 12):
        draw.line([(x + rx * s, y + 2 * s), (x + (rx - 4) * s, y + 14 * s)],
                  fill=BLUE, width=2)


def draw_arrow_icon(draw, x, y, s):
    """Coastline with a bold arrow pushing down toward it."""
    draw.line([(x + 2 * s, y + 52 * s), (x + 20 * s, y + 44 * s),
               (x + 38 * s, y + 54 * s), (x + 62 * s, y + 46 * s)],
              fill=BLUE, width=4)
    draw.line([(x + 12 * s, y + 6 * s), (x + 44 * s, y + 40 * s)],
              fill=RED, width=6)
    draw.polygon([(x + 30 * s, y + 34 * s), (x + 58 * s, y + 34 * s),
                  (x + 44 * s, y + 56 * s)], fill=RED)


def draw_crowd_icon(draw, x, y, s):
    """Rows of heads and one placard."""
    for row, ry in enumerate((14, 32, 50)):
        for cx in range(6 + (row % 2) * 8, 62, 14):
            draw.ellipse([x + (cx - 4) * s, y + (ry - 4) * s,
                          x + (cx + 4) * s, y + (ry + 4) * s],
                         fill=(40, 40, 40))
    draw.rectangle([x + 34 * s, y + 2 * s, x + 60 * s, y + 16 * s],
                   outline=RED, width=3)
    draw.line([(x + 47 * s, y + 16 * s), (x + 47 * s, y + 30 * s)],
              fill=RED, width=3)


PANELS = [
    ("US JETS HIT IRAN",
     "US jets strike a Revolutionary Guard missile site on Qeshm Island; "
     "Iran fires drones at US bases in Bahrain and Kuwait.",
     draw_jet_icon),
    ("FOUR NATIONS PLEAD FOR GAZA",
     "UK, Australia, Canada and Italy urge Israel to open crossings; "
     "150,000 tents held at the border as floods hit; situation \u201cdire\u201d.",
     draw_tents_icon),
    ("HOUTHIS PUSH ON ADEN",
     "Houthi forces advance toward Aden and seize the Bab el-Mandeb "
     "coast; Saudi pipeline strike claimed.",
     draw_arrow_icon),
    ("FRANCE MARCHES",
     "146,000 march nationwide over pay and the cost of living "
     "(official count; unions say 500,000+).",
     draw_crowd_icon),
]


def draw_panels(draw):
    grid_x0, grid_y0 = MARGIN, 522
    col_w, row_h = 468, 168
    gap_x, gap_y = 4, 8
    head_f = font(SERIF, 27)
    body_f = font(SANS, 20)
    for i, (headline, body, icon) in enumerate(PANELS):
        px = grid_x0 + (i % 2) * (col_w + gap_x)
        py = grid_y0 + (i // 2) * (row_h + gap_y)
        # headline, up to two lines, icon tucked top-right
        icon(draw, px + col_w - 66, py + 2, 1.0)
        para(draw, px, py + 2, headline, head_f, col_w - 76, leading=32)
        para(draw, px, py + 74, body, body_f, col_w - 8, leading=25)
    # grid dividers
    rule(draw, MARGIN, W - MARGIN, grid_y0 + row_h + gap_y // 2, width=1, fill=GRAY)
    draw.line([(W // 2, grid_y0), (W // 2, grid_y0 + 2 * row_h + gap_y)],
              fill=GRAY, width=1)


# ------------------------------------------------------------ bottom strip
BOTTOM = [
    ("US LOSES MEASLES-FREE STATUS",
     "After 26 years; 5,400+ cases, 10 deaths."),
    ("19 KILLED IN SIBERIA PLANE CRASH",
     "Russian military An-12 crashes near Kemerovo."),
    ("RECORD DRONE NIGHT",
     "Russia says it shot down 1,441 Ukrainian drones, a record."),
]


def draw_bottom(draw):
    y0 = 890
    rule(draw, MARGIN, W - MARGIN, y0 - 12, width=4, fill=RED)
    label = font(SANS_B, 19)
    draw.text((MARGIN, y0 - 4), "ALSO TODAY", font=label, fill=RED)
    head_f = font(SANS_B, 21)
    body_f = font(SANS, 18)
    col_w = 304
    for i, (headline, body) in enumerate(BOTTOM):
        cx = MARGIN + i * (col_w + 12)
        para(draw, cx, y0 + 20, headline, head_f, col_w, leading=24)
        para(draw, cx, y0 + 70, body, body_f, col_w, leading=21)


# ------------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # thin black frame
    draw.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    draw_masthead(draw)
    draw_main_story(draw)
    draw_panels(draw)
    draw_bottom(draw)
    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
