import os
import sys
import html
import numpy as np
from PIL import Image

RAMP = " .'`^,:;Il!i+_-?][1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
COLS = 84
ROWS = 44
CHAR_W = 4.0
CHAR_H = 8.2
PAD_X = 17
TOP_Y = 58

FALLBACK_ART = [
    "                                                                                    ",
    "                                      /\\                                            ",
    "                                     /  \\                                           ",
    "                                    / /\\ \\                                          ",
    "                                   / /  \\ \\                                         ",
    "                                  / /    \\ \\                                        ",
    "                                 / /  /\\  \\ \\                                       ",
    "                                / /  /  \\  \\ \\                                      ",
    "                               / /  / /\\ \\  \\ \\                                     ",
    "                              / /  / /  \\ \\  \\ \\                                    ",
    "                             / /  / /    \\ \\  \\ \\                                   ",
    "                            / /  / /  /\\  \\ \\  \\ \\                                  ",
    "                           / /  / /  /  \\  \\ \\  \\ \\                                 ",
    "                          / /__/ /__/ /\\ \\__\\ \\__\\ \\                                ",
    "                         /___________/  \\___________\\                               ",
    "                         \\           \\  /           /                               ",
    "                          \\___________\\/___________/                                ",
    "                                                                                    ",
    "                    ==============================================                  ",
    "                      A R Y A M E H R   //   S Y S - K E R N E L                    ",
    "                    ==============================================                  ",
    "                       [ ARCH: FULL-STACK & AEROSPACE ENG ]                         ",
    "                       [ CORE: LARAVEL / VUE 3 / PYTHON   ]                         ",
    "                       [ NODE: SHARIF UNIVERSITY (SUT)    ]                         ",
]

def image_to_ascii_rows(image_path: str):
    if not os.path.exists(image_path):
        rows = [" " * COLS for _ in range(ROWS)]
        start_r = (ROWS - len(FALLBACK_ART)) // 2
        for i, line in enumerate(FALLBACK_ART):
            if start_r + i < ROWS:
                rows[start_r + i] = line[:COLS].ljust(COLS)
        return rows

    img = Image.open(image_path).convert("L").resize((COLS, ROWS), Image.Resampling.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    rows = []
    for r in range(ROWS):
        line_chars = []
        for c in range(COLS):
            darkness = 1.0 - arr[r, c]
            if darkness < 0.08:
                line_chars.append(" ")
            else:
                idx = min(int(darkness * (len(RAMP) - 1)), len(RAMP) - 1)
                line_chars.append(RAMP[idx])
        rows.append("".join(line_chars).rstrip())
    return rows

def build_ascii_svg(rows, out_path="ascii-portrait.svg"):
    width, height = 370, 440
    row_dur = 0.040
    row_step = 0.028

    defs = []
    body = []

    for i, line in enumerate(rows):
        y = TOP_Y + (i + 1) * CHAR_H
        begin_s = f"{i * row_step:.3f}s"
        dur_s = f"{row_dur:.3f}s"
        line_w = max(len(line) * CHAR_W, 1)

        defs.append(f"""
    <clipPath id="r{i}">
      <rect x="{PAD_X}" y="{y - CHAR_H:.1f}" width="0" height="{CHAR_H + 2:.1f}">
        <animate attributeName="width" from="0" to="{line_w:.1f}" begin="{begin_s}" dur="{dur_s}" fill="freeze" />
      </rect>
    </clipPath>""")

        escaped = html.escape(line)
        body.append(
            f'    <text x="{PAD_X}" y="{y:.1f}" clip-path="url(#r{i})" xml:space="preserve">{escaped}</text>'
        )
        if line.strip():
            body.append(f"""    <rect x="{PAD_X}" y="{y - CHAR_H + 1:.1f}" width="{CHAR_W}" height="{CHAR_H - 1:.1f}" fill="#39d353" opacity="0">
      <animate attributeName="x" from="{PAD_X}" to="{PAD_X + line_w:.1f}" begin="{begin_s}" dur="{dur_s}" fill="freeze" />
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" begin="{begin_s}" dur="{dur_s}" fill="freeze" />
    </rect>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>{"".join(defs)}
  </defs>
  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2"/>
  <path d="M 1 10 Q 1 1 10 1 L {width-10} 1 Q {width-1} 1 {width-1} 10 L {width-1} 38 L 1 38 Z" fill="#161b22"/>
  <line x1="1" y1="38" x2="{width-1}" y2="38" stroke="#30363d" stroke-width="1"/>
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{width//2}" y="23" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" fill="#8b949e">portrait.sh — AryaMehr</text>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="6.6" fill="#c9d1d9">
{chr(10).join(body)}
  </g>
</svg>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[ok] Generated {out_path} ({width}x{height})")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "ascii-portrait.svg"
    rows = image_to_ascii_rows(src)
    build_ascii_svg(rows, out)
