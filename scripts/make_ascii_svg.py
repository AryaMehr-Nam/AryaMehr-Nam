import os
import sys
import html

EMBLEM_LINES = [
    ("                    /\\                    ", "#58a6ff"),
    ("                   /  \\                   ", "#58a6ff"),
    ("                  / /\\ \\                  ", "#58a6ff"),
    ("                 / /  \\ \\                 ", "#58a6ff"),
    ("                / / /\\ \\ \\                ", "#79c0ff"),
    ("               / / /  \\ \\ \\               ", "#79c0ff"),
    ("              / / / /\\ \\ \\ \\              ", "#79c0ff"),
    ("             / / / /  \\ \\ \\ \\             ", "#39d353"),
    ("            / / / / /\\ \\ \\ \\ \\            ", "#39d353"),
    ("           / / / / /__\\ \\ \\ \\ \\           ", "#39d353"),
    ("          / /_/ /______\\ \\_\\ \\ \\          ", "#39d353"),
    ("         /______________________\\         ", "#39d353"),
    ("         \\                      /         ", "#2ea043"),
    ("          \\____________________/          ", "#2ea043"),
    ("                                          ", "#8b949e"),
    ("   ┌──────────────────────────────────┐   ", "#30363d"),
    ("   │   A R Y A M E H R  N A M D A R Y │   ", "#58a6ff"),
    ("   │   Sharif Univ. of Technology     │   ", "#79c0ff"),
    ("   │   Aerospace & Computer Engineer  │   ", "#39d353"),
    ("   │   Kernel // System Architecture  │   ", "#d2a8ff"),
    ("   └──────────────────────────────────┘   ", "#30363d"),
    ("                                          ", "#8b949e"),
    ("   [●] STATUS     : ONLINE                ", "#39d353"),
    ("   [●] NODE       : SUT.TEHRAN            ", "#58a6ff"),
    ("   [●] ENVIRONMENT: PRODUCTION            ", "#ffa657"),
]

def build_ascii_svg(out_path="ascii-portrait.svg"):
    width, height = 370, 440
    row_h = 13.5
    top_y = 62
    font_size = 9.2
    char_w = 5.5

    defs = []
    body = []

    for i, (line, color) in enumerate(EMBLEM_LINES):
        y = top_y + i * row_h
        line_w = len(line) * char_w
        begin_s = f"{i * 0.055:.3f}s"
        dur_s = "0.080s"

        defs.append(f"""
    <clipPath id="c{i}">
      <rect x="20" y="{y - row_h + 3:.1f}" width="0" height="{row_h + 1:.1f}">
        <animate attributeName="width" from="0" to="{line_w:.1f}" begin="{begin_s}" dur="{dur_s}" fill="freeze" />
      </rect>
    </clipPath>""")

        escaped = html.escape(line)
        body.append(
            f'    <text x="20" y="{y:.1f}" fill="{color}" clip-path="url(#c{i})" xml:space="preserve">{escaped}</text>'
        )
        if line.strip():
            body.append(f"""    <rect x="20" y="{y - row_h + 4:.1f}" width="6" height="{row_h - 2:.1f}" fill="#39d353" opacity="0">
      <animate attributeName="x" from="20" to="{20 + line_w:.1f}" begin="{begin_s}" dur="{dur_s}" fill="freeze" />
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
  <text x="{width//2}" y="23" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" fill="#8b949e">terminal.sh — aryamehr@sut</text>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="{font_size}" font-weight="600">
{chr(10).join(body)}
  </g>
</svg>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[ok] Generated {out_path} ({width}x{height})")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "ascii-portrait.svg"
    build_ascii_svg(out)
