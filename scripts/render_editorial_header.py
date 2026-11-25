import json
import os
import sys


THEMES = {
    "dark": {
        "bg": "#0d1117",
        "border_top": "#30363d",
        "border_sub": "#21262d",
        "title": "#f0f6fc",
        "subtitle": "#8b949e",
        "muted": "#8b949e",
        "ink": "#c9d1d9",
        "accent": "#58a6ff",
        "live": "#39d353",
        "emblem_stroke": "#58a6ff",
        "emblem_fill": "#161b22",
    },
    "light": {
        "bg": "#ffffff",
        "border_top": "#d0d7de",
        "border_sub": "#e5e9ee",
        "title": "#1f2328",
        "subtitle": "#59636e",
        "muted": "#656d76",
        "ink": "#24292f",
        "accent": "#0969da",
        "live": "#1a7f37",
        "emblem_stroke": "#0969da",
        "emblem_fill": "#f6f8fa",
    },
}


def build_header_svg(data: dict, theme_name: str, out_path: str) -> None:
    t = THEMES[theme_name]
    width, height = 880, 184

    public_repos = int(data.get("public_repos", 9))
    cur_streak = int(data.get("current_streak", 0))
    total = int(data.get("total", 0))

    telemetry = f"{public_repos} REPOS · {cur_streak}D STREAK · {total:,} COMMITS"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; }}
    .fade {{ opacity: 0; animation: fadeIn 0.45s cubic-bezier(0.22, 1, 0.36, 1) forwards; }}
    .pulse {{ animation: pulseDot 2.4s ease-in-out infinite; }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
    @keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.42; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .fade {{ opacity: 1; animation: none; }}
      .pulse {{ animation: none; }}
    }}
  </style>

  <rect width="{width}" height="{height}" fill="{t['bg']}"/>
  <line x1="0" y1="1" x2="{width}" y2="1" stroke="{t['border_top']}" stroke-width="1"/>

  <text x="0" y="28" class="mono fade" font-size="11" letter-spacing="0.9" fill="{t['muted']}">01 // INDEX — ARYAMEHR NAMDARY</text>
  <text x="{width}" y="28" text-anchor="end" class="mono fade" font-size="11" letter-spacing="0.4" fill="{t['accent']}">SUT · COMPUTER &amp; AEROSPACE ENGINEERING</text>

  <!-- Minimal aerospace delta monogram -->
  <g transform="translate(838, 52)" class="fade" style="animation-delay:0.08s">
    <rect width="42" height="42" rx="8" fill="{t['emblem_fill']}" stroke="{t['border_top']}" stroke-width="1"/>
    <path d="M21 9 L32 31 L21 25.5 L10 31 Z" fill="none" stroke="{t['emblem_stroke']}" stroke-width="1.8" stroke-linejoin="round"/>
    <line x1="21" y1="9" x2="21" y2="33" stroke="{t['emblem_stroke']}" stroke-width="1" opacity="0.55"/>
  </g>

  <text x="0" y="82" class="sans fade" font-size="36" font-weight="700" fill="{t['title']}" style="animation-delay:0.05s">AryaMehr Namdary</text>
  <text x="0" y="114" class="sans fade" font-size="15" fill="{t['subtitle']}" style="animation-delay:0.10s">Designing safety-critical AI agent tooling, async web security platforms &amp; autonomous quant systems.</text>

  <line x1="0" y1="140" x2="{width}" y2="140" stroke="{t['border_sub']}" stroke-width="1"/>

  <text x="0" y="164" class="mono fade" font-size="11.5" style="animation-delay:0.15s">
    <tspan fill="{t['muted']}" font-weight="600">STACK</tspan><tspan dx="12" fill="{t['ink']}">Python · TypeScript · React 19 · Rust · Laravel · PyTorch</tspan>
  </text>

  <text x="862" y="164" text-anchor="end" class="mono fade" font-size="11.5" fill="{t['live']}" style="animation-delay:0.15s">{telemetry}</text>
  <circle cx="874" cy="160" r="3.6" fill="{t['live']}" class="pulse"/>

  <line x1="0" y1="{height - 1}" x2="{width}" y2="{height - 1}" stroke="{t['border_sub']}" stroke-width="1"/>
</svg>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[ok] Generated {out_path} ({width}x{height}, theme={theme_name})")


def render_all(json_path: str = "data/contributions.json") -> None:
    data = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    build_header_svg(data, "dark", "header-dark.svg")
    build_header_svg(data, "light", "header-light.svg")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    render_all(inp)
