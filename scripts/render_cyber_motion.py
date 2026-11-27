import json
import math
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def resolve_font(paths: list[str], size: int):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


SANS_BOLD_PATHS = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

MONO_BOLD_PATHS = [
    r"C:\Windows\Fonts\consolab.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
]

MONO_REG_PATHS = [
    r"C:\Windows\Fonts\consola.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]


def render_cyber_hero_gif(data: dict, out_gif: str = "assets/cyber-hero.gif", n_frames: int = 36) -> None:
    os.makedirs(os.path.dirname(out_gif) or ".", exist_ok=True)
    W, H = 880, 272

    repos_count = int(data.get("public_repos", 12))
    streak = int(data.get("current_streak", 26))
    commits = int(data.get("total", 41))

    # Outer icosahedron vertices & edges
    phi = (1 + math.sqrt(5)) / 2
    raw_v = [
        (-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0),
        (0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
        (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1),
    ]
    verts = [(x / 1.85, y / 1.85, z / 1.85) for x, y, z in raw_v]
    edges = [
        (0, 11), (0, 5), (0, 1), (0, 7), (0, 10), (1, 5), (5, 11), (11, 10), (10, 7), (7, 1),
        (3, 9), (3, 4), (3, 2), (3, 6), (3, 8), (4, 9), (9, 8), (8, 6), (6, 2), (2, 4),
        (1, 9), (5, 4), (11, 2), (10, 6), (7, 8),
    ]

    # Inner counter-rotating aerospace octahedron core
    inner_v = [(0.52, 0, 0), (-0.52, 0, 0), (0, 0.58, 0), (0, -0.58, 0), (0, 0, 0.52), (0, 0, -0.52)]
    inner_e = [
        (2, 0), (2, 1), (2, 4), (2, 5),
        (3, 0), (3, 1), (3, 4), (3, 5),
        (0, 4), (4, 1), (1, 5), (5, 0),
    ]

    particles = [((i * 79) % W, (i * 149) % H, 0.7 + (i % 4) * 0.45) for i in range(54)]

    font_title = resolve_font(SANS_BOLD_PATHS, 33)
    font_sub = resolve_font(MONO_BOLD_PATHS, 12)
    font_sm = resolve_font(MONO_REG_PATHS, 11)
    font_big = resolve_font(MONO_BOLD_PATHS, 19)

    prompt_full = ">_ AI GUARDRAILS · STATIC AST · WAF · QUANT RL"
    frames = []

    for f in range(n_frames):
        t = (f / n_frames) * 2 * math.pi
        img = Image.new("RGB", (W, H), (7, 9, 18))
        draw = ImageDraw.Draw(img)

        # Perspective cyber horizon floor scrolling toward camera
        horizon_y = 196
        for gx in range(-10, 11):
            x1 = W // 2 + gx * 42
            x2 = W // 2 + gx * 185
            draw.line([(x1, horizon_y), (x2, H)], fill=(20, 32, 58), width=1)
        for row in range(5):
            phase = ((row + (f / n_frames) * 2.0) % 5) / 5.0
            ry = int(horizon_y + (phase ** 1.55) * (H - horizon_y))
            draw.line([(0, ry), (W, ry)], fill=(24, 44, 78), width=1)

        # Drifting particles
        for px, py, spd in particles:
            nx = int((px + f * spd * 3.2) % W)
            col = (56, 189, 248) if px % 3 == 0 else ((52, 211, 153) if px % 3 == 1 else (167, 139, 250))
            draw.ellipse([nx - 1, py - 1, nx + 1, py + 1], fill=col)

        # Outer 3D Icosahedron
        cx, cy = 114, 134
        ay, ax = t, t * 0.5
        cy_a, sy_a = math.cos(ay), math.sin(ay)
        cx_a, sx_a = math.cos(ax), math.sin(ax)
        proj = []
        for x, y, z in verts:
            x1 = x * cy_a - z * sy_a
            z1 = x * sy_a + z * cy_a
            y2 = y * cx_a - z1 * sx_a
            z2 = y * sx_a + z1 * cx_a
            scale = 186 / (3.35 + z2)
            proj.append((cx + x1 * scale, cy + y2 * scale, z2))

        for a, b in edges:
            x1, y1, z1 = proj[a]
            x2, y2, z2 = proj[b]
            depth = (z1 + z2) / 2
            col = (56, 210, 255) if depth < 0 else (112, 68, 188)
            draw.line([(x1, y1), (x2, y2)], fill=col, width=2 if depth < 0 else 1)

        for x1, y1, z1 in proj:
            r = 3 if z1 < 0 else 2
            col = (52, 211, 153) if z1 < -0.15 else (167, 139, 250)
            draw.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=col)

        # Inner counter-rotating core
        i_ay, i_ax = -t * 2, t
        icy_a, isy_a = math.cos(i_ay), math.sin(i_ay)
        icx_a, isx_a = math.cos(i_ax), math.sin(i_ax)
        i_proj = []
        for x, y, z in inner_v:
            x1 = x * icy_a - z * isy_a
            z1 = x * isy_a + z * icy_a
            y2 = y * icx_a - z1 * isx_a
            z2 = y * isx_a + z1 * icx_a
            scale = 186 / (3.35 + z2)
            i_proj.append((cx + x1 * scale, cy + y2 * scale))
        for a, b in inner_e:
            draw.line([i_proj[a], i_proj[b]], fill=(52, 211, 153), width=1)

        # Neon border + sweeping laser scanner line
        draw.rounded_rectangle([1, 1, W - 2, H - 2], radius=14, outline=(49, 46, 129), width=2)
        scan_x = int(((f / n_frames) * (W + 160)) - 80)
        if 2 <= scan_x < W - 2:
            draw.line([(scan_x, 2), (scan_x, H - 3)], fill=(56, 189, 248), width=2)

        # Corner HUD ticks
        draw.line([(18, 18), (38, 18)], fill=(34, 211, 238), width=2)
        draw.line([(18, 18), (18, 38)], fill=(34, 211, 238), width=2)
        draw.line([(W - 38, H - 18), (W - 18, H - 18)], fill=(167, 139, 250), width=2)
        draw.line([(W - 18, H - 38), (W - 18, H - 18)], fill=(167, 139, 250), width=2)

        # Typography strictly within x=216..642
        draw.text((216, 32), "CYBER.SYNTH // ARYAMEHR-NAM · SUT.TEHRAN", font=font_sm, fill=(167, 139, 250))
        draw.text((218, 56), "ARYAMEHR NAMDARY", font=font_title, fill=(236, 72, 153))
        draw.text((215, 56), "ARYAMEHR NAMDARY", font=font_title, fill=(34, 211, 238))
        draw.text((216, 56), "ARYAMEHR NAMDARY", font=font_title, fill=(248, 250, 252))

        cursor = "_" if (f % 8) < 4 else " "
        draw.text((216, 108), f"{prompt_full} {cursor}", font=font_sub, fill=(52, 211, 153))
        draw.text((216, 136), "Building verifiable AI agent defenses, AST X-Ray", font=font_sm, fill=(148, 163, 184))
        draw.text((216, 154), "studios, async WAFs & trading ML @ Sharif Univ.", font=font_sm, fill=(148, 163, 184))

        # Live Telemetry Box (x=662..858)
        draw.rounded_rectangle([662, 30, 858, 176], radius=10, fill=(13, 18, 36), outline=(56, 189, 248), width=1)
        draw.text((680, 46), "SYS.TELEMETRY", font=font_sm, fill=(148, 163, 184))
        pulse_col = (52, 211, 153) if (f % 12) < 7 else (16, 85, 58)
        draw.ellipse([834, 47, 842, 55], fill=pulse_col)

        draw.text((680, 74), f"{repos_count} REPOS", font=font_big, fill=(248, 250, 252))
        draw.text((680, 104), f"{streak}D STREAK", font=font_big, fill=(52, 211, 153))
        draw.text((680, 134), f"{commits} COMMITS", font=font_big, fill=(34, 211, 238))

        # Bottom Ticker Bar
        draw.rounded_rectangle([216, 204, 858, 238], radius=6, fill=(11, 16, 32), outline=(30, 41, 59), width=1)
        draw.text(
            (232, 215),
            f"STACK: PYTHON · RUST · TS · REACT 19 · PYTORCH · LARAVEL   //   {repos_count} SYSTEMS ONLINE",
            font=font_sm,
            fill=(203, 213, 225),
        )

        frames.append(img.quantize(colors=128))

    frames[0].save(out_gif, save_all=True, append_images=frames[1:], duration=55, loop=0, optimize=True)
    print(f"[ok] Generated {out_gif} ({os.path.getsize(out_gif)} bytes)")


def render_telemetry_wave_svg(data: dict, out_path: str = "assets/telemetry-wave.svg") -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    days = data.get("days", [])[-35:]
    streak = int(data.get("current_streak", 26))
    commits = int(data.get("total", 41))
    active_days = int(data.get("active_days", 27))

    bars = []
    pts = []
    n = max(1, len(days))
    x0, w_span, base_y = 26, 488, 150
    for i, d in enumerate(days):
        cnt = int(d.get("count", 0))
        lvl = int(d.get("level", 0))
        bx = x0 + i * (w_span / n)
        bh = max(4, min(72, cnt * 14 + lvl * 4))
        by = base_y - bh
        col = "#34d399" if lvl >= 3 else ("#22d3ee" if lvl >= 1 else "#1e293b")
        op = "0.85" if lvl > 0 else "0.45"
        bars.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="9" height="{bh:.1f}" rx="2" fill="{col}" opacity="{op}">'
            f'<animate attributeName="opacity" values="{op};1;{op}" dur="2.6s" begin="{(i*0.07):.2f}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
        pts.append(f"{bx + 4.5:.1f},{by - 4:.1f}")

    poly = " ".join(pts)
    last_x, last_y = (pts[-1].split(",") if pts else ("514", "146"))

    # Verified GitHub language ratios across public repos (Python 73.6%, JS/TS 14.9%, Rust 5.3%, Web/Shell 6.2%)
    langs = [
        ("PYTHON", "73.6%", 110, "#38bdf8"),
        ("JS / TS", "14.9%", 24, "#a78bfa"),
        ("RUST", "5.3%", 10, "#fb923c"),
        ("CSS / HTML", "6.2%", 12, "#34d399"),
    ]
    lang_rows = []
    for idx, (name, pct, bw, col) in enumerate(langs):
        ly = 68 + idx * 28
        lang_rows.append(
            f'<text x="564" y="{ly}" font-size="10.5" fill="#94a3b8" font-weight="600">{name}</text>'
            f'<rect x="640" y="{ly - 9}" width="150" height="8" rx="4" fill="#111827"/>'
            f'<rect x="640" y="{ly - 9}" width="{bw}" height="8" rx="4" fill="{col}" filter="url(#tGlow)">'
            f'<animate attributeName="opacity" values="0.78;1;0.78" dur="2.2s" begin="{0.35*idx:.2f}s" repeatCount="indefinite"/>'
            f'</rect>'
            f'<text x="854" y="{ly}" text-anchor="end" font-size="10.5" fill="{col}" font-weight="700">{pct}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 184" width="880" height="184">
  <defs>
    <filter id="tGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="tScan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22d3ee" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="tClip"><rect width="880" height="184" rx="12"/></clipPath>
  </defs>

  <g clip-path="url(#tClip)" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
    <rect width="880" height="184" rx="12" fill="#070b14" stroke="#1e293b" stroke-width="1.2"/>
    <rect x="-80" y="0" width="80" height="184" fill="url(#tScan)">
      <animate attributeName="x" from="-80" to="900" dur="5.2s" repeatCount="indefinite"/>
    </rect>

    <!-- Left Telemetry Header -->
    <text x="26" y="32" font-size="11" font-weight="700" fill="#22d3ee">35-DAY VELOCITY SPECTRUM // {commits} COMMITS · {active_days}D ACTIVE</text>
    <text x="518" y="32" text-anchor="end" font-size="11" font-weight="700" fill="#34d399">{streak}D STREAK ●</text>
    <line x1="26" y1="44" x2="518" y2="44" stroke="#162238" stroke-width="1"/>
    <line x1="26" y1="150" x2="518" y2="150" stroke="#1e293b" stroke-width="1"/>

    {''.join(bars)}
    <polyline points="{poly}" fill="none" stroke="#34d399" stroke-width="1.8" stroke-linejoin="round" filter="url(#tGlow)"/>
    <circle cx="{last_x}" cy="{last_y}" r="3.8" fill="#34d399" filter="url(#tGlow)">
      <animate attributeName="r" values="3;5.5;3" dur="1.4s" repeatCount="indefinite"/>
    </circle>

    <!-- Divider -->
    <line x1="540" y1="18" x2="540" y2="166" stroke="#1e293b" stroke-width="1.2"/>

    <!-- Right Language DNA -->
    <text x="564" y="32" font-size="11" font-weight="700" fill="#a78bfa">CODEBASE DNA // 12 REPOS</text>
    <line x1="564" y1="44" x2="854" y2="44" stroke="#162238" stroke-width="1"/>
    {''.join(lang_rows)}
  </g>
</svg>'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[ok] Generated {out_path}")


def render_static_motion_modules() -> None:
    os.makedirs("assets", exist_ok=True)

    # 1. Animated Domains Circuit Bus (880x148)
    domains_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 148" width="880" height="148">
  <defs>
    <filter id="dGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="sweep" x1="-1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
      <animate attributeName="x1" from="-1" to="2" dur="3.2s" repeatCount="indefinite"/>
      <animate attributeName="x2" from="0" to="3" dur="3.2s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect width="880" height="148" fill="#0d1117"/>

  <!-- Top Hub Label -->
  <rect x="330" y="2" width="220" height="20" rx="10" fill="#0b1022" stroke="#312e81"/>
  <text x="440" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#a78bfa">CORE // ENGINEERING MATRIX</text>

  <!-- Circuit Traces -->
  <path id="tr1" d="M 440 22 L 440 34 L 104 34 L 104 48" fill="none" stroke="#1e3a5f" stroke-width="1.5"/>
  <path id="tr2" d="M 440 22 L 440 34 L 328 34 L 328 48" fill="none" stroke="#4c1d4b" stroke-width="1.5"/>
  <path id="tr3" d="M 440 22 L 440 34 L 552 34 L 552 48" fill="none" stroke="#2d1f47" stroke-width="1.5"/>
  <path id="tr4" d="M 440 22 L 440 34 L 776 34 L 776 48" fill="none" stroke="#133d2e" stroke-width="1.5"/>

  <!-- Moving Packets -->
  <circle r="3.3" fill="#22d3ee" filter="url(#dGlow)"><animateMotion dur="1.9s" repeatCount="indefinite"><mpath href="#tr1"/></animateMotion></circle>
  <circle r="3.3" fill="#ec4899" filter="url(#dGlow)"><animateMotion dur="1.6s" repeatCount="indefinite" begin="0.3s"><mpath href="#tr2"/></animateMotion></circle>
  <circle r="3.3" fill="#a78bfa" filter="url(#dGlow)"><animateMotion dur="1.8s" repeatCount="indefinite" begin="0.6s"><mpath href="#tr3"/></animateMotion></circle>
  <circle r="3.3" fill="#34d399" filter="url(#dGlow)"><animateMotion dur="2.1s" repeatCount="indefinite" begin="0.9s"><mpath href="#tr4"/></animateMotion></circle>

  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
    <rect x="0" y="48" width="208" height="96" rx="10" fill="#0b1022" stroke="#1e3a5f" stroke-width="1.2"/>
    <rect x="0" y="48" width="208" height="3" rx="1.5" fill="#22d3ee"/>
    <rect x="0" y="48" width="208" height="3" rx="1.5" fill="url(#sweep)"/>
    <text x="14" y="72" font-size="10.5" font-weight="700" fill="#22d3ee">01 // AGENT SECURITY</text>
    <text x="14" y="96" font-size="12.5" font-weight="700" fill="#f8fafc">mcp-guard · redline</text>
    <text x="14" y="116" font-size="10.5" fill="#94a3b8">8-layer MCP proxy</text>
    <text x="14" y="132" font-size="10.5" fill="#94a3b8">100% recall AST hooks</text>

    <rect x="224" y="48" width="208" height="96" rx="10" fill="#0b1022" stroke="#4c1d4b" stroke-width="1.2"/>
    <rect x="224" y="48" width="208" height="3" rx="1.5" fill="#ec4899"/>
    <rect x="224" y="48" width="208" height="3" rx="1.5" fill="url(#sweep)"/>
    <text x="238" y="72" font-size="10.5" font-weight="700" fill="#ec4899">02 // X-RAY &amp; AST STUDIOS</text>
    <text x="238" y="96" font-size="12.5" font-weight="700" fill="#f8fafc">CodeAtlas · A11yPilot</text>
    <text x="238" y="116" font-size="10.5" fill="#94a3b8">Tree-sitter + 60fps UIA</text>
    <text x="238" y="132" font-size="10.5" fill="#94a3b8">laravel-spec-skill</text>

    <rect x="448" y="48" width="208" height="96" rx="10" fill="#0b1022" stroke="#2d1f47" stroke-width="1.2"/>
    <rect x="448" y="48" width="208" height="3" rx="1.5" fill="#a78bfa"/>
    <rect x="448" y="48" width="208" height="3" rx="1.5" fill="url(#sweep)"/>
    <text x="462" y="72" font-size="10.5" font-weight="700" fill="#a78bfa">03 // APPSEC &amp; WAF</text>
    <text x="462" y="96" font-size="12.5" font-weight="700" fill="#f8fafc">SentinelX-Platform</text>
    <text x="462" y="116" font-size="10.5" fill="#94a3b8">Async WAF · React 19 UI</text>
    <text x="462" y="132" font-size="10.5" fill="#94a3b8">Chrome MV3 SecureLens</text>

    <rect x="672" y="48" width="208" height="96" rx="10" fill="#0b1022" stroke="#133d2e" stroke-width="1.2"/>
    <rect x="672" y="48" width="208" height="3" rx="1.5" fill="#34d399"/>
    <rect x="672" y="48" width="208" height="3" rx="1.5" fill="url(#sweep)"/>
    <text x="686" y="72" font-size="10.5" font-weight="700" fill="#34d399">04 // QUANT ML &amp; RUST</text>
    <text x="686" y="96" font-size="12.5" font-weight="700" fill="#f8fafc">TradeAgent · Aether</text>
    <text x="686" y="116" font-size="10.5" fill="#94a3b8">PyTorch DRL · FinBERT</text>
    <text x="686" y="132" font-size="10.5" fill="#94a3b8">Rust SOCKS5 · Solar UAV</text>
  </g>
</svg>'''
    Path("assets/cyber-domains.svg").write_text(domains_svg, encoding="utf-8")

    # 2. Animated Section Dividers
    def section_svg(code: str, title: str, accent: str, out: str):
        s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 38" width="880" height="38">
  <defs>
    <linearGradient id="ls" x1="-0.4" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{accent}" stop-opacity="1"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
      <animate attributeName="x1" from="-0.4" to="1.2" dur="2.8s" repeatCount="indefinite"/>
      <animate attributeName="x2" from="0" to="1.6" dur="2.8s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect width="880" height="38" fill="#0d1117"/>
  <rect x="0" y="6" width="6" height="20" rx="2" fill="{accent}"/>
  <text x="16" y="21" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13" font-weight="700" letter-spacing="1.2" fill="{accent}">{code}</text>
  <text x="42" y="21" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13" font-weight="700" letter-spacing="1" fill="#f0f6fc">// {title}</text>
  <line x1="0" y1="34" x2="880" y2="34" stroke="#21262d" stroke-width="1.5"/>
  <line x1="0" y1="34" x2="880" y2="34" stroke="url(#ls)" stroke-width="2"/>
  <rect x="854" y="13" width="6" height="8" fill="{accent}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></rect>
  <rect x="864" y="9" width="6" height="12" fill="{accent}"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.4s" repeatCount="indefinite"/></rect>
  <rect x="874" y="15" width="6" height="6" fill="{accent}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" begin="0.3s" repeatCount="indefinite"/></rect>
</svg>'''
        Path(out).write_text(s, encoding="utf-8")

    section_svg("02", "LIVE MOTION STUDIOS &amp; REPOSITORIES", "#22d3ee", "assets/sec-studios.svg")
    section_svg("03", "ANIMATED ARCHITECTURE SCHEMATICS", "#ec4899", "assets/sec-schematics.svg")
    section_svg("04", "REAL-TIME TELEMETRY &amp; CODEBASE DNA", "#34d399", "assets/sec-telemetry.svg")

    # 3. Animated 415x82 HUD Footer Strips beneath top 4 GIF Repo Cards
    repo_hud_specs = [
        ("CodeAtlas", "AST · 60fps Canvas", "Polyglot Tree-sitter dependency mapper &amp; blast-radius studio", "#22d3ee", "assets/card-codeatlas.svg"),
        ("A11yPilot", "UIA X-Ray · -89% Tokens", "Screenshot-free desktop automation &amp; HITL MCP server", "#34d399", "assets/card-a11ypilot.svg"),
        ("SentinelX-Platform", "WAF + SOC · CI Pass", "Async ASGI firewall, AI threat analyzer, React 19 UI &amp; MV3", "#a78bfa", "assets/card-sentinelx.svg"),
        ("agent-redline", "100% Recall · 0.82ms", "Deterministic PreToolUse AST firewall (335-cmd eval)", "#ec4899", "assets/card-redline.svg"),
    ]
    for title, pill, desc, col, path in repo_hud_specs:
        card = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 416 82" width="416" height="82">
  <defs>
    <linearGradient id="cScan" x1="-0.5" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="{col}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{col}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{col}" stop-opacity="0"/>
      <animate attributeName="x1" from="-0.5" to="1.3" dur="3.0s" repeatCount="indefinite"/>
      <animate attributeName="x2" from="0" to="1.8" dur="3.0s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect width="416" height="82" rx="8" fill="#0b1022" stroke="#1e293b" stroke-width="1.2"/>
  <line x1="0" y1="1.5" x2="416" y2="1.5" stroke="url(#cScan)" stroke-width="2"/>
  <circle cx="16" cy="24" r="3.6" fill="{col}">
    <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="27" y="29" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="15.5" font-weight="700" fill="#f8fafc">{title}</text>
  <rect x="260" y="13" width="142" height="20" rx="10" fill="#0f172a" stroke="{col}" stroke-opacity="0.55"/>
  <text x="331" y="27" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="{col}">{pill}</text>
  <text x="16" y="54" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="11.5" fill="#94a3b8">{desc}</text>
  <!-- Bottom signal pulse bar -->
  <rect x="16" y="68" width="384" height="2.5" rx="1.2" fill="#162238"/>
  <rect x="16" y="68" width="76" height="2.5" rx="1.2" fill="{col}">
    <animate attributeName="x" values="16;324;16" dur="3.6s" repeatCount="indefinite"/>
  </rect>
</svg>'''
        Path(path).write_text(card, encoding="utf-8")

    # 4. Second-Row Animated Architecture Schematic Cards (mcp-guard, TradeAgent, laravel-spec-skill, Aether-Tray)
    # mcp-guard: Animated 8-layer proxy packet inspection schematic (424x142)
    Path("assets/schem-mcpguard.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 424 142" width="424" height="142">
  <defs><filter id="mg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="424" height="142" rx="10" fill="#0b1022" stroke="#1e3a5f" stroke-width="1.2"/>
  <text x="16" y="28" font-family="-apple-system, system-ui, sans-serif" font-size="15" font-weight="700" fill="#f8fafc">mcp-guard</text>
  <rect x="272" y="13" width="136" height="20" rx="10" fill="#0f172a" stroke="#22d3ee" stroke-opacity="0.5"/>
  <text x="340" y="27" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#22d3ee">ZERO-TRUST PROXY</text>
  <text x="16" y="50" font-family="-apple-system, system-ui, sans-serif" font-size="11.5" fill="#94a3b8">8-layer MCP security scanner, schema pinning &amp; SARIF 2.1.0</text>
  <!-- Animated JSON-RPC flow -->
  <rect x="18" y="72" width="84" height="44" rx="6" fill="#070b14" stroke="#30363d"/>
  <text x="60" y="98" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#cbd5e1">AI CLIENT</text>
  <rect x="150" y="68" width="124" height="52" rx="6" fill="#0f172a" stroke="#22d3ee" stroke-width="1.3"/>
  <text x="212" y="90" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#22d3ee">8-LAYER ENGINE</text>
  <text x="212" y="106" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#34d399">ENFORCE · REDACT</text>
  <rect x="322" y="72" width="84" height="44" rx="6" fill="#070b14" stroke="#30363d"/>
  <text x="364" y="98" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#cbd5e1">MCP SERVER</text>
  <path id="mp1" d="M 102 94 L 150 94" stroke="#22d3ee" stroke-width="1.5"/>
  <path id="mp2" d="M 274 94 L 322 94" stroke="#34d399" stroke-width="1.5"/>
  <circle r="3.2" fill="#22d3ee" filter="url(#mg)"><animateMotion dur="1.1s" repeatCount="indefinite"><mpath href="#mp1"/></animateMotion></circle>
  <circle r="3.2" fill="#34d399" filter="url(#mg)"><animateMotion dur="1.1s" repeatCount="indefinite" begin="0.5s"><mpath href="#mp2"/></animateMotion></circle>
</svg>''', encoding="utf-8")

    # Autonomous-Trading-Framework: Animated equity curve & DRL pulse (424x142)
    Path("assets/schem-tradeagent.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 424 142" width="424" height="142">
  <defs><filter id="tg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="424" height="142" rx="10" fill="#0b1022" stroke="#3b2618" stroke-width="1.2"/>
  <text x="16" y="28" font-family="-apple-system, system-ui, sans-serif" font-size="14.5" font-weight="700" fill="#f8fafc">TradeAgent · Quant ML</text>
  <rect x="266" y="13" width="142" height="20" rx="10" fill="#0f172a" stroke="#fb923c" stroke-opacity="0.55"/>
  <text x="337" y="27" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#fb923c">+19.45% · SHARPE 9.24</text>
  <text x="16" y="50" font-family="-apple-system, system-ui, sans-serif" font-size="11.5" fill="#94a3b8">Multi-agent PyTorch Deep RL, XGBoost, FinBERT &amp; MT5 engine</text>
  <rect x="16" y="66" width="392" height="58" rx="6" fill="#070b14" stroke="#162238"/>
  <line x1="24" y1="110" x2="398" y2="110" stroke="#1e293b" stroke-dasharray="3 3"/>
  <polyline points="24,108 62,104 94,109 130,96 168,99 206,86 244,91 284,78 326,82 368,74 394,72"
            fill="none" stroke="#133d2e" stroke-width="2"/>
  <polyline points="24,108 62,104 94,109 130,96 168,99 206,86 244,91 284,78 326,82 368,74 394,72"
            fill="none" stroke="#34d399" stroke-width="2.2" filter="url(#tg)" stroke-dasharray="430">
    <animate attributeName="stroke-dashoffset" values="430;0;0" keyTimes="0;0.55;1" dur="4s" repeatCount="indefinite"/>
  </polyline>
  <circle cx="394" cy="72" r="4" fill="#34d399" filter="url(#tg)"><animate attributeName="r" values="3;5.5;3" dur="1.3s" repeatCount="indefinite"/></circle>
</svg>''', encoding="utf-8")

    # laravel-spec-skill: Animated spec verification checklist (424x142)
    Path("assets/schem-laravelspec.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 424 142" width="424" height="142">
  <rect width="424" height="142" rx="10" fill="#0b1022" stroke="#2d1f47" stroke-width="1.2"/>
  <text x="16" y="28" font-family="-apple-system, system-ui, sans-serif" font-size="15" font-weight="700" fill="#f8fafc">laravel-spec-skill</text>
  <rect x="272" y="13" width="136" height="20" rx="10" fill="#0f172a" stroke="#a78bfa" stroke-opacity="0.55"/>
  <text x="340" y="27" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#a78bfa">29 SPEC RULES · CI</text>
  <text x="16" y="50" font-family="-apple-system, system-ui, sans-serif" font-size="11.5" fill="#94a3b8">Spec-driven AI workflow compiling specs for Laravel &amp; Filament</text>
  <rect x="16" y="66" width="392" height="58" rx="6" fill="#070b14" stroke="#162238"/>
  <g font-family="ui-monospace, monospace" font-size="10.5">
    <text x="28" y="85" fill="#34d399">[✓] Schema &amp; Relations<animate attributeName="opacity" values="0.3;1;1" dur="3s" repeatCount="indefinite"/></text>
    <text x="224" y="85" fill="#34d399">[✓] RBAC Policy Matrix<animate attributeName="opacity" values="0.3;1;1" dur="3s" begin="0.4s" repeatCount="indefinite"/></text>
    <text x="28" y="109" fill="#38bdf8">[✓] Milestone DAG (0 cyc)<animate attributeName="opacity" values="0.3;1;1" dur="3s" begin="0.8s" repeatCount="indefinite"/></text>
    <text x="224" y="109" fill="#a78bfa">[✓] 0 Errors · TDD Ready<animate attributeName="opacity" values="0.3;1;1" dur="3s" begin="1.2s" repeatCount="indefinite"/></text>
  </g>
</svg>''', encoding="utf-8")

    # Aether-Tray: Animated Rust SOCKS5 encrypted tunnel pulse (424x142)
    Path("assets/schem-aether.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 424 142" width="424" height="142">
  <defs><filter id="ag" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="424" height="142" rx="10" fill="#0b1022" stroke="#133d2e" stroke-width="1.2"/>
  <text x="16" y="28" font-family="-apple-system, system-ui, sans-serif" font-size="15" font-weight="700" fill="#f8fafc">Aether-Tray</text>
  <rect x="272" y="13" width="136" height="20" rx="10" fill="#0f172a" stroke="#34d399" stroke-opacity="0.55"/>
  <text x="340" y="27" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#34d399">RUST · MULTI-OS</text>
  <text x="16" y="50" font-family="-apple-system, system-ui, sans-serif" font-size="11.5" fill="#94a3b8">Native Cloudflare WARP system tray over local SOCKS5</text>
  <rect x="16" y="66" width="392" height="58" rx="6" fill="#070b14" stroke="#162238"/>
  <path id="at1" d="M 32 95 L 392 95" stroke="#1e293b" stroke-width="3" stroke-dasharray="6 4"/>
  <circle r="4" fill="#34d399" filter="url(#ag)"><animateMotion dur="1.7s" repeatCount="indefinite"><mpath href="#at1"/></animateMotion></circle>
  <circle r="3.5" fill="#22d3ee" filter="url(#ag)"><animateMotion dur="1.7s" repeatCount="indefinite" begin="0.85s"><mpath href="#at1"/></animateMotion></circle>
  <rect x="26" y="81" width="76" height="28" rx="5" fill="#0f172a" stroke="#30363d"/><text x="64" y="99" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#f8fafc">SOCKS5</text>
  <rect x="158" y="81" width="108" height="28" rx="5" fill="#0f172a" stroke="#34d399"/><text x="212" y="99" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#34d399">127.0.0.1:1819</text>
  <rect x="316" y="81" width="82" height="28" rx="5" fill="#0f172a" stroke="#22d3ee"/><text x="357" y="99" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#22d3ee">WARP EDGE</text>
</svg>''', encoding="utf-8")

    # 5. Cyber Status Footer Bar (880x56)
    footer_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 56" width="880" height="56">
  <rect width="880" height="56" rx="10" fill="#070b14" stroke="#1e293b" stroke-width="1.2"/>
  <circle cx="24" cy="28" r="4" fill="#34d399"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
  <text x="38" y="32" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" fill="#94a3b8">
    R&amp;D: <tspan fill="#e2e8f0">Solar UAV Modeling &amp; Biomimetics @ SUT</tspan>  ·  STATUS: <tspan fill="#34d399" font-weight="700">ONLINE</tspan>
  </text>
  <text x="858" y="32" text-anchor="end" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" fill="#22d3ee">ARYAMEHR-NAM // 35.70°N 51.35°E</text>
</svg>'''
    Path("assets/cyber-footer.svg").write_text(footer_svg, encoding="utf-8")
    print("[ok] Generated all cyber SVG motion modules in assets/")


def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    data = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    render_cyber_hero_gif(data, "assets/cyber-hero.gif")
    render_telemetry_wave_svg(data, "assets/telemetry-wave.svg")
    render_static_motion_modules()


if __name__ == "__main__":
    main()
