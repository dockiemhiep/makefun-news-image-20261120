from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = (1024, 1024)
PAPER = "#F7F3E8"
INK = "#111111"
RED = "#A31621"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")


def wrap_text(draw, text, font, width):
    lines = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}" if current else word
        left, _, right, _ = draw.textbbox((0, 0), candidate, font=font)
        if right - left <= width:
            current = candidate
            continue
        left, _, right, _ = draw.textbbox((0, 0), word, font=font)
        if right - left > width:
            raise ValueError(f"Word exceeds the available width: {word!r}")
        lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(
    draw, text, font, x, top, width, *, line_step=None, fill=INK, centered=False
):
    lines = wrap_text(draw, text, font, width)
    boxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    step = font.size + 3 if line_step is None else line_step
    y = top - min(box[1] for box in boxes)
    bottom = top
    for line, (left, _, right, lower) in zip(lines, boxes):
        offset = (width - (right - left)) // 2 if centered else 0
        draw.text((x + offset - left, y), line, font=font, fill=fill)
        bottom = max(bottom, y + lower)
        y += step
    return bottom


def draw_scales(draw, x, y):
    draw.line((x, y - 27, x, y + 24), fill=INK, width=5)
    draw.line((x - 69, y - 19, x + 69, y - 19), fill=INK, width=4)
    draw.line((x - 35, y + 24, x + 35, y + 24), fill=INK, width=5)
    for hanger in (x - 64, x + 64):
        draw.line(
            [(hanger - 24, y + 10), (hanger, y - 19), (hanger + 24, y + 10)],
            fill=INK,
            width=2,
        )
        draw.polygon(
            [
                (hanger - 25, y + 10),
                (hanger + 25, y + 10),
                (hanger + 16, y + 18),
                (hanger - 16, y + 18),
            ],
            fill=RED,
        )


def draw_circles(draw, x, y):
    radius = 53
    for center in (x - 77, x, x + 77):
        draw.ellipse(
            (center - radius, y - radius, center + radius, y + radius),
            outline=INK,
            width=4,
        )


def draw_chart(draw, x, y):
    points = [
        (x - 156, y - 51),
        (x - 119, y - 32),
        (x - 88, y - 42),
        (x - 43, y - 7),
        (x - 15, y - 18),
        (x + 30, y + 23),
        (x + 58, y + 9),
        (x + 93, y + 37),
        (x + 117, y + 27),
        (x + 147, y + 51),
    ]
    draw.line(points, fill=RED, width=6, joint="curve")
    draw.polygon(
        [(x + 155, y + 57), (x + 126, y + 53), (x + 144, y + 29)], fill=RED
    )


def draw_tower(draw, x, y):
    draw.rectangle((x - 57, y - 61, x + 38, y + 61), fill=INK)
    for window_y in range(y - 45, y + 53, 15):
        for window_x in range(x - 43, x + 31, 17):
            draw.ellipse(
                (window_x, window_y, window_x + 3, window_y + 3), fill=PAPER
            )

    impact = (x + 36, y - 40)
    for end in (
        (x + 26, y - 69),
        (x + 48, y - 70),
        (x + 64, y - 59),
        (x + 74, y - 39),
        (x + 65, y - 20),
        (x + 49, y - 10),
        (x + 30, y - 14),
        (x + 12, y - 30),
        (x + 12, y - 53),
    ):
        draw.line((impact, end), fill=RED, width=3)
    draw.ellipse((x + 32, y - 44, x + 40, y - 36), fill=RED)


PANELS = (
    (
        "JUSTICE",
        "ICJ RULES MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA",
        "First such ruling against a state by the world court",
        draw_scales,
        56,
    ),
    (
        "SUMMIT",
        "TRUMP, XI AND PUTIN HOLD FIRST THREE-WAY SUMMIT",
        "Shenzhen meeting ends with a joint peace declaration",
        draw_circles,
        108,
    ),
    (
        "MARKETS",
        "AI SELL-OFF ROCKS GLOBAL MARKETS",
        "Nikkei falls 4.8% after Anthropic's Nasdaq debut",
        draw_chart,
        118,
    ),
    (
        "CONFLICT",
        "HOUTHI MISSILE DAMAGES RIYADH SKYSCRAPER",
        "Financial district tower hit for the second time this month",
        draw_tower,
        142,
    ),
)

FOOTER = (
    "ALSO TODAY — KENYA DISCHARGES ITS LAST EBOLA PATIENT · "
    "RUSSIAN BARRAGE DAMAGES EMBASSIES IN KYIV · "
    "COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT"
)


def main():
    image = Image.new("RGB", SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    bold = FONT_DIR / "Arial Bold.ttf"
    regular = FONT_DIR / "Arial.ttf"
    masthead = ImageFont.truetype(bold, 64)
    date = ImageFont.truetype(regular, 30)
    tag_font = ImageFont.truetype(bold, 17)
    headline_font = ImageFont.truetype(bold, 44)
    subline_font = ImageFont.truetype(regular, 25)
    footer_font = ImageFont.truetype(regular, 23)

    margin = 28
    page_width = SIZE[0] - 2 * margin
    draw_text_block(
        draw,
        "THE WORLD IN ONE PICTURE",
        masthead,
        margin,
        22,
        page_width,
        centered=True,
    )
    draw.rectangle((margin, 84, SIZE[0] - margin - 1, 88), fill=RED)
    draw_text_block(
        draw,
        "FRIDAY · 20 NOVEMBER 2026",
        date,
        margin,
        102,
        page_width,
        centered=True,
    )

    grid_top = 146
    grid_bottom = 924
    gutter = 16
    panel_width = (page_width - gutter) // 2
    panel_height = (grid_bottom - grid_top - gutter) // 2
    padding = 14
    content_width = panel_width - 2 * padding

    for index, (tag, headline, subline, motif, motif_height) in enumerate(PANELS):
        row, column = divmod(index, 2)
        left = margin + column * (panel_width + gutter)
        top = grid_top + row * (panel_height + gutter)
        right = left + panel_width
        bottom = top + panel_height
        draw.rectangle((left, top, right - 1, bottom - 1), outline=INK, width=2)

        x = left + padding
        tag_bottom = draw_text_block(
            draw, tag, tag_font, x, top + 16, content_width, fill=RED
        )
        headline_bottom = draw_text_block(
            draw,
            headline,
            headline_font,
            x,
            tag_bottom + 11,
            content_width,
            line_step=43,
        )
        subline_bottom = draw_text_block(
            draw,
            subline,
            subline_font,
            x,
            headline_bottom + 12,
            content_width,
            line_step=28,
        )
        motif_top = subline_bottom + 10
        motif_bottom = bottom - padding
        if motif_bottom - motif_top < motif_height:
            raise ValueError(f"Text and motif exceed the panel height for {tag}")
        motif(draw, (left + right) // 2, (motif_top + motif_bottom) // 2)

    draw.line((margin, 940, SIZE[0] - margin - 1, 940), fill=INK, width=2)
    footer_bottom = draw_text_block(
        draw,
        FOOTER,
        footer_font,
        margin,
        954,
        page_width,
        line_step=26,
        centered=True,
    )
    if footer_bottom > SIZE[1] - 20:
        raise ValueError("Footer exceeds the available height")

    if image.size != (1024, 1024):
        raise ValueError(f"Unexpected image dimensions: {image.size}")
    image.save(Path(__file__).with_name("entry.png"), optimize=True)


if __name__ == "__main__":
    main()
