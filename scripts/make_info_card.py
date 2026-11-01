import os
import sys
import html

INFO_LINES = [
    ("Identity", "AryaMehr Namdary", "#58a6ff"),
    ("Role", "Full-Stack Software Architect", "#58a6ff"),
    ("Education", "Computer & Aerospace Eng @ SUT", "#79c0ff"),
    ("Backend", "PHP, Laravel 11, Python, Django", "#d2a8ff"),
    ("Frontend", "Vue 3, Inertia.js, Livewire, TALL", "#d2a8ff"),
    ("R&D", "Solar UAV Modeling & Biomimetics", "#ffa657"),
    ("Flagship", "Yasouj Amlak (Filament + Neshan)", "#ffa657"),
    ("Toolchain", "Antigravity · Claude Code · Obsidian", "#39d353"),
    ("Soundtrack", "Pink Floyd · Mogwai · GY!BE · Sorena", "#7ee787"),
]

def build_info_card(out_path="info-card.svg"):
    width, height = 490, 440
    static = os.environ.get("STATIC") == "1"

    rows_svg = []
    for idx, (key, val, color) in enumerate(INFO_LINES):
        y = 108 + idx * 29
        delay = 0.15 + idx * 0.10
        cls = "" if static else f'class="r" style="animation-delay:{delay:.2f}s"'
        rows_svg.append(
            f'    <g {cls}>'
            f'<text x="26" y="{y}" fill="{color}" font-weight="600">{html.escape(key)}</text>'
            f'<text x="128" y="{y}" fill="#484f58">::</text>'
            f'<text x="150" y="{y}" fill="#e6edf3">{html.escape(val)}</text>'
            f'</g>'
        )

    swatches = "".join(
        f'<rect x="{26 + i * 24}" y="396" width="16" height="12" rx="3" fill="{c}"/>'
        for i, c in enumerate(["#21262d", "#ff7b72", "#39d353", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#f0f6fc"])
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .m {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 12.5px; }}
    .r {{ opacity: 0; transform: translateX(-8px); animation: s 0.35s cubic-bezier(0.22, 1, 0.36, 1) forwards; }}
    .blink {{ animation: b 1.1s step-end infinite; }}
    @keyframes s {{ to {{ opacity: 1; transform: translateX(0); }} }}
    @keyframes b {{ 50% {{ opacity: 0; }} }}
  </style>
  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2"/>
  <path d="M 1 10 Q 1 1 10 1 L {width-10} 1 Q {width-1} 1 {width-1} 10 L {width-1} 38 L 1 38 Z" fill="#161b22"/>
  <line x1="1" y1="38" x2="{width-1}" y2="38" stroke="#30363d" stroke-width="1"/>
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{width//2}" y="23" text-anchor="middle" class="m" font-size="11" fill="#8b949e">neofetch — aryamehr@sut</text>

  <g class="m">
    <text x="26" y="68" fill="#39d353" font-weight="700">aryamehr@github</text>
    <text x="152" y="68" fill="#8b949e">~ $</text>
    <text x="184" y="68" fill="#f0f6fc">fastfetch --profile</text>
    <line x1="26" y1="80" x2="464" y2="80" stroke="#21262d" stroke-width="1"/>
{chr(10).join(rows_svg)}
    <line x1="26" y1="376" x2="464" y2="376" stroke="#21262d" stroke-width="1"/>
  </g>
  {swatches}
  <text x="246" y="406" class="m" font-size="11.5" fill="#8b949e">SYS: ONLINE</text>
  <rect x="332" y="396" width="8" height="12" fill="#39d353" class="blink"/>
</svg>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[ok] Generated {out_path} ({width}x{height})")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "info-card.svg"
    build_info_card(out)
