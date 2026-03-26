#!/usr/bin/env python3
"""Generate a social media OG image for claude-aliens-spinner-verbs."""

import random
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 640
OUT = "og-image.png"

# Color palette — dark space / green phosphor terminal
BG_TOP     = (8, 12, 20)
BG_BOTTOM  = (4, 8, 14)
STAR_COLOR = (200, 220, 255)
TERM_BG    = (10, 20, 16)
TERM_BORDER= (0, 180, 80)
GREEN_DIM  = (0, 160, 60)
GREEN_BRIGHT = (0, 255, 100)
GREEN_MID  = (0, 210, 80)
WHITE      = (230, 240, 235)
GRAY       = (120, 140, 130)
ACCENT     = (255, 200, 50)   # amber for the repo name

SPINNER_CHARS = ["|", "/", "-", "\\", "|", "/", "-", "\\"]

VERBS = [
    "Staying frosty",
    "Running a bypass",
    "Taking off and nuking the entire site from orbit",
    "Entering the pipe, five by five",
    "Discussing the bonus situation",
    "Mostly coming out at night",
    "Being an ultimate badass",
    "Eating cornbread",
]

def gradient_bg(draw, w, h):
    for y in range(h):
        t = y / h
        r = int(BG_TOP[0] * (1-t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1-t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1-t) + BG_BOTTOM[2] * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def draw_stars(draw, w, h, seed=42):
    rng = random.Random(seed)
    for _ in range(180):
        x = rng.randint(0, w)
        y = rng.randint(0, h)
        brightness = rng.randint(100, 255)
        size = rng.choice([1, 1, 1, 2])
        alpha = rng.randint(80, 200)
        col = (brightness, brightness, min(255, brightness + 30), alpha)
        draw.ellipse([x, y, x+size, y+size], fill=(brightness, brightness, min(255, brightness+20)))

def rounded_rect(draw, box, radius, fill, outline=None, outline_width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                            outline=outline, width=outline_width)

def try_font(names, size):
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

def main():
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    gradient_bg(draw, WIDTH, HEIGHT)
    draw_stars(draw, WIDTH, HEIGHT)

    # Subtle scanline texture
    for y in range(0, HEIGHT, 4):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, 20))

    # Fonts
    mono_paths = [
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    sans_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    bold_paths = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    font_title  = try_font(bold_paths, 60)
    font_sub    = try_font(sans_paths, 26)
    font_label  = try_font(sans_paths, 20)
    font_term   = try_font(mono_paths, 25)
    font_term_sm= try_font(mono_paths, 22)
    font_spin   = try_font(mono_paths, 28)

    # ── Left panel: title block ──────────────────────────────────────────
    left_x = 60
    title_y = 90

    # "claude code" small label
    draw.text((left_x, title_y), "Claude Code", font=font_label, fill=GRAY)

    # Repository name
    title_y += 42
    draw.text((left_x, title_y), "claude-aliens-", font=font_title, fill=WHITE)
    title_y += 62
    draw.text((left_x, title_y), "spinner-verbs", font=font_title, fill=ACCENT)

    # Divider
    title_y += 72
    draw.line([(left_x, title_y), (left_x + 380, title_y)], fill=GREEN_DIM, width=2)
    title_y += 16

    # Subtitle
    draw.text((left_x, title_y), "Custom spinner verbs for", font=font_sub, fill=GRAY)
    title_y += 36
    draw.text((left_x, title_y), "Claude Code from the", font=font_sub, fill=GRAY)
    title_y += 36
    draw.text((left_x, title_y), "Aliens movie franchise", font=font_sub, fill=GRAY)

    # URL at bottom left
    draw.text((left_x, HEIGHT - 52), "github.com/petenelson/claude-aliens-spinner-verbs",
              font=font_label, fill=GREEN_DIM)

    # ── Right panel: terminal window ─────────────────────────────────────
    term_x0 = 520
    term_y0 = 50
    term_x1 = WIDTH - 40
    term_y1 = HEIGHT - 50
    term_w  = term_x1 - term_x0

    # Terminal shadow
    rounded_rect(draw, [term_x0+6, term_y0+6, term_x1+6, term_y1+6],
                 radius=12, fill=(0, 30, 10))

    # Terminal body
    rounded_rect(draw, [term_x0, term_y0, term_x1, term_y1],
                 radius=12, fill=TERM_BG, outline=TERM_BORDER, outline_width=2)

    # Title bar
    bar_y1 = term_y0 + 42
    rounded_rect(draw, [term_x0, term_y0, term_x1, bar_y1],
                 radius=12, fill=(0, 40, 20))
    draw.rectangle([term_x0, term_y0+20, term_x1, bar_y1], fill=(0, 40, 20))

    # Traffic-light dots
    dot_y = term_y0 + 16
    for i, col in enumerate([(180, 60, 60), (180, 150, 40), (40, 160, 60)]):
        cx = term_x0 + 22 + i * 24
        draw.ellipse([cx-6, dot_y-6, cx+6, dot_y+6], fill=col)

    # Title bar label
    bar_label = "~ claude-aliens-spinner-verbs"
    draw.text((term_x0 + term_w//2, term_y0 + 8), bar_label,
              font=font_label, fill=GREEN_DIM, anchor="mt")

    # Prompt line
    prompt_y = bar_y1 + 22
    draw.text((term_x0 + 24, prompt_y), "$ claude", font=font_term, fill=GREEN_BRIGHT)

    # Spinner verb lines
    line_y = prompt_y + 50
    line_h  = 46

    for i, verb in enumerate(VERBS[:6]):
        spin = SPINNER_CHARS[i % len(SPINNER_CHARS)]
        if i == 0:
            color = GREEN_BRIGHT
        elif i < 3:
            color = GREEN_MID
        else:
            color = GREEN_DIM

        draw.text((term_x0 + 24, line_y), spin, font=font_spin, fill=color)
        draw.text((term_x0 + 58, line_y), verb, font=font_term_sm, fill=color)
        line_y += line_h

    # Blinking cursor block after last line
    cur_x = term_x0 + 24
    draw.rectangle([cur_x, line_y + 4, cur_x + 14, line_y + 30], fill=GREEN_BRIGHT)

    img.save(OUT)
    print(f"Saved {OUT}  ({WIDTH}×{HEIGHT})")

if __name__ == "__main__":
    main()
