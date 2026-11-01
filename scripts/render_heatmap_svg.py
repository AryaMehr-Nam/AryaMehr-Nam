import json
import sys
import os
import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render_heatmap(json_path="data/contributions.json", out_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"[error] {json_path} does not exist. Run fetch_contributions.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])[-371:]
    total = data.get("total", 0)
    cur_streak = data.get("current_streak", 0)
    max_streak = data.get("longest_streak", 0)
    active_days = data.get("active_days", 0)
    username = data.get("username", "aryamehr")

    width, height = 868, 212
    cell, gap = 11.5, 3.2
    step = cell + gap
    start_x, start_y = 48, 68

    rects = []
    month_labels = []
    last_month = None

    for idx, d in enumerate(days):
        week = idx // 7
        dow = idx % 7
        x = start_x + week * step
        y = start_y + dow * step
        lvl = min(max(int(d.get("level", 0)), 0), 4)
        color = PALETTE[lvl]
        delay = (week + dow) * 0.012
        glow = ' filter="url(#glow)"' if lvl == 4 else ""
        rects.append(
            f'    <rect class="c" x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2.6" '
            f'fill="{color}"{glow} style="animation-delay:{delay:.3f}s"/>'
        )
        if dow == 0 and d.get("date"):
            try:
                m_idx = int(d["date"].split("-")[1]) - 1
                if m_idx != last_month and week < 51:
                    month_labels.append(f'    <text x="{x:.1f}" y="58" class="lbl">{MONTHS[m_idx]}</text>')
                    last_month = m_idx
            except Exception:
                pass

    legend = "".join(
        f'<rect x="{744 + i * 15}" y="180" width="11" height="11" rx="2.2" fill="{c}"/>'
        for i, c in enumerate(PALETTE)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="0" stdDeviation="1.8" flood-color="#39d353" flood-opacity="0.55"/>
    </filter>
  </defs>
  <style>
    .m {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .lbl {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10px; fill: #8b949e; }}
    .c {{ opacity: 0; transform: translateY(-5px); animation: drop 0.26s ease-out forwards; }}
    @keyframes drop {{ to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2"/>
  <path d="M 1 10 Q 1 1 10 1 L {width-10} 1 Q {width-1} 1 {width-1} 10 L {width-1} 36 L 1 36 Z" fill="#161b22"/>
  <line x1="1" y1="36" x2="{width-1}" y2="36" stroke="#30363d" stroke-width="1"/>
  <circle cx="20" cy="18" r="5.5" fill="#ff5f56"/>
  <circle cx="38" cy="18" r="5.5" fill="#ffbd2e"/>
  <circle cx="56" cy="18" r="5.5" fill="#27c93f"/>
  <text x="82" y="22" class="m" font-size="11" fill="#8b949e">{username.lower()}@github ~ $ ./telemetry-heatmap.sh</text>
  <text x="846" y="22" text-anchor="end" class="m" font-size="11" fill="#39d353">● LIVE CRON</text>

  <text x="20" y="92" class="lbl">Mon</text>
  <text x="20" y="121" class="lbl">Wed</text>
  <text x="20" y="151" class="lbl">Fri</text>
{chr(10).join(month_labels)}
  <g>
{chr(10).join(rects)}
  </g>

  <text x="48" y="190" class="m" font-size="11.5" fill="#c9d1d9" font-weight="600">{total:,} contributions</text>
  <text x="195" y="190" class="m" font-size="11.5" fill="#8b949e">· Streak: <tspan fill="#39d353" font-weight="600">{cur_streak}d</tspan> · Max: <tspan fill="#58a6ff" font-weight="600">{max_streak}d</tspan> · Active: <tspan fill="#d2a8ff">{active_days}d</tspan></text>
  <text x="710" y="190" class="lbl">Less</text>
  {legend}
  <text x="824" y="190" class="lbl">More</text>
</svg>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[ok] Generated {out_path} ({width}x{height})")

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap(inp, out)
