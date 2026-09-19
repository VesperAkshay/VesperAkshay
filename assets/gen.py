#!/usr/bin/env python3
"""Generates the custom SVG asset set for VesperAkshay's GitHub profile README."""
import os, math

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- palette
BG      = "#070A0E"
PANEL   = "#0C1117"
PANEL2  = "#0F151C"
LINE    = "#1A222C"
TEXT    = "#E8EEF4"
MUTED   = "#78889A"
DIM     = "#4A5766"

MINT    = "#4DE8C2"
ORANGE  = "#FF8A3D"
VIOLET  = "#8B7BFF"
AMBER   = "#FFD166"
BLUE    = "#7CD8FF"
PINK    = "#FF7AA8"

MONO = "ui-monospace,'SF Mono','JetBrains Mono','Fira Code',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,Inter,'Helvetica Neue',Arial,sans-serif"

W = 1000


def cw(size):
    """approximate monospace advance width"""
    return size * 0.6


def sw(text, size, bold=True):
    """rough advance-width estimate for a bold sans face"""
    wide, narrow = set("mwMW@%"), set("iljtfr.,;:'!|I ")
    total = 0.0
    for c in text:
        if c in wide:
            total += 0.90
        elif c in narrow:
            total += 0.34
        elif c.isupper():
            total += 0.68
        else:
            total += 0.57
    return total * size * (1.04 if bold else 1.0)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name, len(body), "bytes")


def frame(p, w, h, radius=14, bg=BG, stroke=LINE, grid=True):
    """standard panel background: bg + grid + border"""
    out = []
    if grid:
        out.append(f'''<pattern id="{p}grid" width="26" height="26" patternUnits="userSpaceOnUse">
      <path d="M26 0H0V26" fill="none" stroke="#0F161E" stroke-width="1"/>
    </pattern>''')
    out_defs = "".join(out)
    body = f'<rect width="{w}" height="{h}" rx="{radius}" fill="{bg}"/>'
    if grid:
        body += f'<rect width="{w}" height="{h}" rx="{radius}" fill="url(#{p}grid)"/>'
    body += (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{radius}" '
             f'fill="none" stroke="{stroke}" stroke-width="1"/>')
    return out_defs, body


# =================================================================== HERO
def hero():
    p = "h_"
    w, h = W, 300
    defs, bg = frame(p, w, h)

    # ---- typing phrases
    phrases = [
        ("rust systems engineer", MINT),
        ("ai agent architect", VIOLET),
        ("developer-tools builder", ORANGE),
        ("open-source maintainer", BLUE),
    ]
    fs = 19
    ch = cw(fs)
    tx, ty = 48 + 24, 186          # text baseline (after "> " prefix)
    n = len(phrases)
    cycle = n * 4.0                 # seconds

    clips, texts = [], []
    caret_vals, caret_times = [], []
    for i, (txt, col) in enumerate(phrases):
        wpx = len(txt) * ch
        t0 = i * 4.0 / cycle
        t1 = (i * 4.0 + 1.5) / cycle     # finished typing
        t2 = (i * 4.0 + 3.3) / cycle     # start erase
        t3 = (i * 4.0 + 3.9) / cycle     # erased
        kt = f"0;{t0:.4f};{t1:.4f};{t2:.4f};{t3:.4f};1"
        clips.append(
            f'<clipPath id="{p}c{i}"><rect x="{tx}" y="{ty-20}" width="0" height="28">'
            f'<animate attributeName="width" values="0;0;{wpx:.1f};{wpx:.1f};0;0" '
            f'keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/></rect></clipPath>')
        texts.append(
            f'<text x="{tx}" y="{ty}" clip-path="url(#{p}c{i})" font-family="{MONO}" '
            f'font-size="{fs}" fill="{col}" letter-spacing="0.4" '
            f'textLength="{wpx:.1f}" lengthAdjust="spacing">{esc(txt)}</text>')
        caret_vals += [f"{tx}", f"{tx}", f"{tx+wpx:.1f}", f"{tx+wpx:.1f}", f"{tx}", f"{tx}"]
        caret_times += [f"{t0:.4f}", f"{t0:.4f}", f"{t1:.4f}", f"{t2:.4f}", f"{t3:.4f}", f"{t3:.4f}"]
    # normalise caret keyTimes to start at 0 / end at 1
    caret_times[0] = "0"
    caret_times[-1] = "1"

    # ---- agent mesh (right side)
    cx, cy, R = 795, 150, 84
    nodes = [(cx, cy, 7, MINT)]
    ring = []
    for k in range(6):
        a = math.radians(-90 + k * 60)
        ring.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    edges = []
    for (x, y) in ring:
        edges.append((cx, cy, x, y))
    for k in range(6):
        x1, y1 = ring[k]
        x2, y2 = ring[(k + 1) % 6]
        edges.append((x1, y1, x2, y2))

    mesh = []
    mesh.append(f'<circle cx="{cx}" cy="{cy}" r="{R+26}" fill="none" stroke="{LINE}" '
                f'stroke-width="1" stroke-dasharray="2 7" opacity=".85">'
                f'<animateTransform attributeName="transform" type="rotate" '
                f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="52s" repeatCount="indefinite"/></circle>')
    mesh.append(f'<circle cx="{cx}" cy="{cy}" r="{R+46}" fill="none" stroke="#131B24" stroke-width="1"/>')

    for i, (x1, y1, x2, y2) in enumerate(edges):
        spoke = i < 6
        col = MINT if spoke else "#1F3A3A"
        op = ".55" if spoke else ".5"
        mesh.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{col}" stroke-width="1" opacity="{op}" stroke-dasharray="4 5">'
                    f'<animate attributeName="stroke-dashoffset" values="27;0" dur="{2.4+i*0.18:.2f}s" '
                    f'repeatCount="indefinite"/></line>')

    for i, (x, y) in enumerate(ring):
        col = [MINT, VIOLET, ORANGE, BLUE, AMBER, PINK][i]
        d = i * 0.62
        mesh.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{PANEL}" stroke="{col}" '
                    f'stroke-width="1.4" opacity=".95"/>')
        mesh.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}">'
                    f'<animate attributeName="r" values="3;5.4;3" dur="3.2s" begin="{d:.2f}s" '
                    f'repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="1;.45;1" dur="3.2s" begin="{d:.2f}s" '
                    f'repeatCount="indefinite"/></circle>')
        mesh.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="none" stroke="{col}" stroke-width="1">'
                    f'<animate attributeName="r" values="13;26" dur="3.2s" begin="{d:.2f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values=".55;0" dur="3.2s" begin="{d:.2f}s" '
                    f'repeatCount="indefinite"/></circle>')
        # packet travelling to the hub
        mesh.append(f'<circle r="2.6" fill="{ORANGE}">'
                    f'<animateMotion dur="2.6s" begin="{d:.2f}s" repeatCount="indefinite" '
                    f'path="M{x:.1f},{y:.1f} L{cx},{cy}"/>'
                    f'<animate attributeName="opacity" values="0;1;1;0" dur="2.6s" begin="{d:.2f}s" '
                    f'repeatCount="indefinite"/></circle>')

    mesh.append(f'<circle cx="{cx}" cy="{cy}" r="24" fill="{PANEL}" stroke="{MINT}" stroke-width="1.6"/>')
    mesh.append(f'<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="{MINT}" stroke-width="1.6" opacity=".5">'
                f'<animate attributeName="r" values="24;44" dur="3s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values=".5;0" dur="3s" repeatCount="indefinite"/></circle>')
    mesh.append(f'<text x="{cx}" y="{cy+4.5}" text-anchor="middle" font-family="{MONO}" font-size="12" '
                f'font-weight="700" fill="{MINT}" letter-spacing="0.5">AP</text>')

    # ---- stat chips
    chips = [("62", "repositories", MINT), ("100+", "forks earned", ORANGE), ("6", "langs shipped", VIOLET)]
    chip_x = 48
    chip_svg = []
    for val, lab, col in chips:
        vw = len(val) * cw(13) * 1.08
        tw = vw + 12 + len(lab) * cw(10.5)
        bw = tw + 30
        chip_svg.append(f'<g><rect x="{chip_x}" y="212" width="{bw:.0f}" height="30" rx="8" '
                        f'fill="{PANEL2}" stroke="{LINE}"/>'
                        f'<rect x="{chip_x}" y="212" width="2.5" height="30" rx="1.2" fill="{col}"/>'
                        f'<text x="{chip_x+14}" y="232" font-family="{MONO}" font-size="13" '
                        f'font-weight="700" fill="{TEXT}">{val}</text>'
                        f'<text x="{chip_x+14+vw+11:.0f}" y="232" font-family="{MONO}" '
                        f'font-size="10.5" fill="{MUTED}">{lab}</text></g>')
        chip_x += bw + 12

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Akshay Patel — Rust systems engineer and AI agent architect">
  <defs>
    {defs}
    <linearGradient id="{p}name" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="{MINT}"/><stop offset="48%" stop-color="{BLUE}"/>
      <stop offset="100%" stop-color="{VIOLET}"/>
    </linearGradient>
    <radialGradient id="{p}g1" cx="0.18" cy="0.1" r="0.7">
      <stop offset="0%" stop-color="{MINT}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{MINT}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="{p}g2" cx="0.82" cy="0.55" r="0.55">
      <stop offset="0%" stop-color="{VIOLET}" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{MINT}" stop-opacity=".9"/>
      <stop offset="100%" stop-color="{MINT}" stop-opacity="0"/>
    </linearGradient>
    {''.join(clips)}
  </defs>

  {bg}
  <rect width="{w}" height="{h}" rx="14" fill="url(#{p}g1)"/>
  <rect width="{w}" height="{h}" rx="14" fill="url(#{p}g2)"/>

  <!-- corner ticks -->
  <path d="M24 46 V24 H46" fill="none" stroke="{MINT}" stroke-width="1.4" opacity=".6"/>
  <path d="M{w-46} 24 H{w-24} V46" fill="none" stroke="{VIOLET}" stroke-width="1.4" opacity=".6"/>
  <path d="M24 {h-46} V{h-24} H46" fill="none" stroke="{VIOLET}" stroke-width="1.4" opacity=".6"/>
  <path d="M{w-46} {h-24} H{w-24} V{h-46}" fill="none" stroke="{MINT}" stroke-width="1.4" opacity=".6"/>

  <g>{''.join(mesh)}</g>

  <!-- eyebrow -->
  <circle cx="52" cy="76" r="3.4" fill="{MINT}">
    <animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="66" y="80" font-family="{MONO}" font-size="12" fill="{MUTED}" letter-spacing="1.6">
    KANPUR, INDIA <tspan fill="{DIM}">//</tspan> B.TECH @ PSIT <tspan fill="{DIM}">//</tspan> OPEN TO WORK
  </text>

  <!-- name -->
  <text x="46" y="140" font-family="{SANS}" font-size="52" font-weight="800"
        fill="url(#{p}name)" letter-spacing="-1.2">Akshay Patel</text>
  <text x="48" y="140" font-family="{SANS}" font-size="52" font-weight="800"
        fill="{MINT}" letter-spacing="-1.2" opacity=".12">Akshay Patel</text>

  <rect x="48" y="154" width="300" height="1.5" fill="url(#{p}rule)"/>

  <!-- typing line -->
  <text x="48" y="186" font-family="{MONO}" font-size="19" fill="{DIM}">&gt;</text>
  {''.join(texts)}
  <rect x="{tx}" y="{ty-16}" width="9" height="21" rx="1" fill="{MINT}" opacity=".9">
    <animate attributeName="x" values="{';'.join(caret_vals)}" keyTimes="{';'.join(caret_times)}"
             dur="{cycle}s" repeatCount="indefinite"/>
    <animate attributeName="fill-opacity" values="1;1;0;0;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>

  {''.join(chip_svg)}
</svg>
'''
    write("hero.svg", svg)


def main():
    hero()
    terminal()
    stack()
    achievements()
    divider()
    section("sec-about.svg",   "01", "whoami",   "// the short version",        MINT)
    section("sec-stack.svg",   "02", "toolbox",  "// what I build with",        VIOLET)
    section("sec-work.svg",    "03", "selected work", "// things I actually shipped", ORANGE)
    section("sec-signals.svg", "04", "signals",  "// activity & contribution",  BLUE)
    section("sec-contact.svg", "05", "say hello","// inbox is open",            AMBER)
    button("btn-linkedin.svg", "LINKEDIN", "link",  BLUE)
    button("btn-dropwire.svg", "DROPWIRE DOCS", "bolt", ORANGE)
    button("btn-devto.svg",    "DEV.TO", "pen",   VIOLET)
    button("btn-holopin.svg",  "HOLOPIN", "star", AMBER)
    button("btn-email.svg",    "EMAIL ME", "mail", MINT)
    button("btn-repos.svg",    "ALL 62 REPOS", "code", PINK)


# ============================================================ SECTION HEAD
def section(name, num, title, sub, accent):
    p = f"s{num}_"
    w, h = W, 52
    tw = sw(title, 21)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <defs>
    <linearGradient id="{p}r" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}" stop-opacity=".55"/>
      <stop offset="70%" stop-color="{accent}" stop-opacity=".08"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="{BG}" rx="8"/>
  <rect x="0" y="10" width="4" height="32" rx="2" fill="{accent}"/>
  <text x="20" y="32" font-family="{MONO}" font-size="12" font-weight="700" fill="{accent}"
        letter-spacing="1.2" opacity=".85">{num}</text>
  <text x="50" y="33" font-family="{SANS}" font-size="21" font-weight="800" fill="{TEXT}"
        letter-spacing="-0.2">{esc(title)}</text>
  <text x="{50+tw+18:.0f}" y="32" font-family="{MONO}" font-size="11.5" fill="{MUTED}"
        letter-spacing=".3">{esc(sub)}</text>
  <rect x="0" y="47" width="{w}" height="1.6" fill="url(#{p}r)"/>
  <circle cy="47.8" r="3.2" fill="{accent}">
    <animate attributeName="cx" values="4;{w-60};4" dur="9s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" dur="9s" repeatCount="indefinite"/>
  </circle>
</svg>
'''
    write(name, svg)


# ================================================================ TERMINAL
def terminal():
    p = "t_"
    rows = [
        ("name",      "Akshay Patel  ·  @VesperAkshay", TEXT),
        ("based",     "Kanpur, Uttar Pradesh, India  ·  B.Tech @ PSIT", MUTED),
        ("focus",     "Rust systems  ·  AI agents & MCP  ·  developer tooling", MINT),
        ("shipping",  "DropWire — zero-cloud P2P encrypted transfer engine", ORANGE),
        ("open_src",  "GSSoC '23 & '24  ·  Hacktoberfest '24  ·  100+ forks", VIOLET),
        ("wants",     "hard problems, ambitious collaborators, real users", BLUE),
    ]
    w = W
    top = 46
    rh = 27
    h = top + 46 + len(rows) * rh + 24

    defs, bg = frame(p, w, h, grid=False, bg=PANEL)
    lines = []
    for i, (k, v, col) in enumerate(rows):
        y = top + 48 + i * rh
        b = i * 0.42 + 0.9
        T = len(rows) * 0.42 + 1.9
        k1, k2 = b / T, (b + 0.32) / T
        lines.append(f'''<g opacity="1">
      <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{k1:.3f};{k2:.3f};1" dur="{T:.2f}s" fill="freeze"/>
      <text x="34" y="{y}" font-family="{MONO}" font-size="13" fill="{DIM}">&#9656;</text>
      <text x="52" y="{y}" font-family="{MONO}" font-size="13" fill="{MUTED}">{k}</text>
      <text x="{52 + 10 * cw(13):.0f}" y="{y}" font-family="{MONO}" font-size="13" fill="{DIM}">:</text>
      <text x="{52 + 12 * cw(13):.0f}" y="{y}" font-family="{MONO}" font-size="13" fill="{col}">{esc(v)}</text>
    </g>''')

    end = len(rows) * 0.42 + 1.3
    dots = "".join(
        f'<circle cx="{26+i*17}" cy="24" r="5" fill="{c}" opacity=".9"/>'
        for i, c in enumerate([ORANGE, AMBER, MINT]))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="whoami">
  <defs>{defs}</defs>
  {bg}
  <path d="M0 14 a14 14 0 0 1 14-14 h{w-28} a14 14 0 0 1 14 14 v34 h-{w} z" fill="{PANEL2}"/>
  <line x1="0" y1="48" x2="{w}" y2="48" stroke="{LINE}"/>
  {dots}
  <text x="{w/2}" y="29" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{MUTED}"
        letter-spacing=".6">akshay@vesper — ~/profile</text>
  <text x="34" y="{top+20}" font-family="{MONO}" font-size="13.5" fill="{MINT}">$</text>
  <text x="52" y="{top+20}" font-family="{MONO}" font-size="13.5" fill="{TEXT}">whoami --verbose</text>
  {''.join(lines)}
  <g opacity="1"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{end/(end+0.6):.3f};{(end+0.3)/(end+0.6):.3f};1" dur="{end+0.6:.2f}s" fill="freeze"/>
    <text x="34" y="{h-22}" font-family="{MONO}" font-size="13.5" fill="{MINT}">$</text>
    <rect x="52" y="{h-34}" width="9" height="16" fill="{MINT}">
      <animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>
  </g>
</svg>
'''
    write("about.svg", svg)


# =================================================================== STACK
def stack():
    p = "k_"
    cats = [
        ("SYSTEMS & LANGUAGES", ORANGE, ["Rust", "Go", "Python", "C++", "C", "TypeScript", "JavaScript"]),
        ("AI · AGENTS · LLM", VIOLET, ["Multi-Agent Systems", "MCP", "Agentic Workflows", "RAG",
                                        "Gemini API", "TensorFlow", "OpenCV"]),
        ("WEB & INTERFACES", MINT, ["React", "Next.js", "Tailwind", "Framer Motion", "HTML5", "CSS3"]),
        ("BACKEND & DATA", BLUE, ["Node.js", "Express", "FastAPI", "PostgreSQL", "MySQL", "Firebase"]),
        ("DEVTOOLS & CLI", AMBER, ["TUI / Ratatui", "Shell", "Git", "GitHub Actions", "Homebrew", "Scoop"]),
        ("DESIGN & MOTION", PINK, ["Figma", "After Effects", "Canva", "SVG Motion"]),
    ]
    cols, margin, gap = 3, 20, 20
    cwid = (W - margin * 2 - gap * (cols - 1)) // cols
    pad, fs = 14, 10.5
    inner = cwid - pad * 2

    laid = []
    for title, col, tags in cats:
        rows, cur, curw = [], [], 0.0
        for t in tags:
            tw = len(t) * cw(fs) + 20
            if cur and curw + tw + 7 > inner:
                rows.append(cur); cur, curw = [], 0.0
            cur.append((t, tw)); curw += tw + 7
        if cur:
            rows.append(cur)
        laid.append((title, col, rows))

    rowh = 25
    chH = max(44 + len(r) * rowh + 8 for _, _, r in laid)
    h = margin + (chH + gap) * 2 - gap + margin

    cards = []
    for i, (title, col, rows) in enumerate(laid):
        x = margin + (i % cols) * (cwid + gap)
        y = margin + (i // cols) * (chH + gap)
        g = [f'<rect x="{x}" y="{y}" width="{cwid}" height="{chH}" rx="11" fill="{PANEL}" stroke="{LINE}"/>',
             f'<rect x="{x+12}" y="{y}" width="{cwid-24}" height="2.5" rx="1.2" fill="{col}" opacity=".9"/>',
             f'<circle cx="{x+pad+4}" cy="{y+26}" r="3.6" fill="{col}">'
             f'<animate attributeName="opacity" values="1;.3;1" dur="{2.6+i*0.3:.1f}s" repeatCount="indefinite"/></circle>',
             f'<text x="{x+pad+16}" y="{y+30}" font-family="{MONO}" font-size="10.5" font-weight="700" '
             f'fill="{MUTED}" letter-spacing="1.1">{esc(title)}</text>']
        for ri, row in enumerate(rows):
            px = x + pad
            py = y + 46 + ri * rowh
            for t, tw in row:
                g.append(f'<rect x="{px:.1f}" y="{py}" width="{tw:.1f}" height="19" rx="9.5" '
                         f'fill="{PANEL2}" stroke="{LINE}"/>')
                g.append(f'<text x="{px+tw/2:.1f}" y="{py+13.2}" text-anchor="middle" font-family="{MONO}" '
                         f'font-size="{fs}" fill="{TEXT}" opacity=".92">{esc(t)}</text>')
                px += tw + 7
        cards.append("".join(g))

    defs, bg = frame(p, W, h, grid=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="Tech stack">
  <defs>{defs}</defs>
  {bg}
  {''.join(cards)}
</svg>
'''
    write("stack.svg", svg)


# ============================================================ ACHIEVEMENTS
def achievements():
    p = "a_"
    items = [
        ("GSSoC", "'23 & '24", MINT),
        ("HACKTOBER", "2024", ORANGE),
        ("PULL SHARK", "x2", VIOLET),
        ("STARSTRUCK", "github", AMBER),
        ("PAIR EXTRA.", "github", BLUE),
        ("QUICKDRAW", "github", PINK),
        ("YOLO", "github", MINT),
    ]
    w = W
    h = 132
    defs, bg = frame(p, w, h, grid=True)
    n = len(items)
    margin, gap = 20, 12
    bw = (w - margin * 2 - gap * (n - 1)) / n

    cards = []
    for i, (title, sub, col) in enumerate(items):
        x = margin + i * (bw + gap)
        cxm = x + bw / 2
        d = i * 0.28
        hexpts = " ".join(
            f"{cxm + 20*math.cos(math.radians(a)):.1f},{54 + 20*math.sin(math.radians(a)):.1f}"
            for a in range(-90, 270, 60))
        cards.append(f'''<g>
      <rect x="{x:.1f}" y="18" width="{bw:.1f}" height="{h-36}" rx="11" fill="{PANEL}" stroke="{LINE}"/>
      <polygon points="{hexpts}" fill="none" stroke="{col}" stroke-width="1.4" opacity=".8"/>
      <polygon points="{hexpts}" fill="{col}" opacity=".08"/>
      <circle cx="{cxm:.1f}" cy="54" r="5" fill="{col}">
        <animate attributeName="r" values="4;6.6;4" dur="3s" begin="{d:.2f}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="1;.45;1" dur="3s" begin="{d:.2f}s" repeatCount="indefinite"/>
      </circle>
      <polygon points="{hexpts}" fill="none" stroke="{col}" stroke-width="1" opacity=".5">
        <animateTransform attributeName="transform" type="rotate"
          from="0 {cxm:.1f} 54" to="360 {cxm:.1f} 54" dur="{16+i*2}s" repeatCount="indefinite"/>
      </polygon>
      <text x="{cxm:.1f}" y="95" text-anchor="middle" font-family="{MONO}" font-size="9.2"
            font-weight="700" fill="{TEXT}" letter-spacing=".5">{title}</text>
      <text x="{cxm:.1f}" y="108" text-anchor="middle" font-family="{MONO}" font-size="8.4"
            fill="{MUTED}" letter-spacing=".4">{esc(sub)}</text>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Achievements">
  <defs>{defs}</defs>
  {bg}
  {''.join(cards)}
</svg>
'''
    write("achievements.svg", svg)


# ================================================================= DIVIDER
def divider():
    p = "d_"
    h = 26
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-hidden="true">
  <defs>
    <linearGradient id="{p}g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{MINT}" stop-opacity="0"/>
      <stop offset="22%" stop-color="{MINT}" stop-opacity=".5"/>
      <stop offset="50%" stop-color="{VIOLET}" stop-opacity=".55"/>
      <stop offset="78%" stop-color="{ORANGE}" stop-opacity=".5"/>
      <stop offset="100%" stop-color="{ORANGE}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{h}" fill="{BG}"/>
  <line x1="0" y1="13" x2="{W}" y2="13" stroke="url(#{p}g)" stroke-width="1.4"/>
  <line x1="0" y1="13" x2="{W}" y2="13" stroke="{BG}" stroke-width="4" stroke-dasharray="3 9" opacity=".8"/>
  <circle cy="13" r="3" fill="{MINT}">
    <animate attributeName="cx" values="0;{W};0" dur="11s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" dur="11s" repeatCount="indefinite"/>
  </circle>
  <circle cy="13" r="2" fill="{ORANGE}">
    <animate attributeName="cx" values="{W};0;{W}" dur="14s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;.9;.9;0" dur="14s" repeatCount="indefinite"/>
  </circle>
  <polygon points="{W/2-7},13 {W/2},7 {W/2+7},13 {W/2},19" fill="{BG}" stroke="{VIOLET}" stroke-width="1.2"/>
</svg>
'''
    write("divider.svg", svg)


# ================================================================= BUTTONS
GLYPHS = {
    "link":  'M-5,-1 a4,4 0 0 1 4,-4 h2 M5,1 a4,4 0 0 1 -4,4 h-2 M-2,0 h4',
    "code":  'M-5,-4 L-9,0 L-5,4 M5,-4 L9,0 L5,4 M2,-6 L-2,6',
    "star":  'M0,-7 L2,-2 L7,-2 L3,1 L5,6 L0,3 L-5,6 L-3,1 L-7,-2 L-2,-2 Z',
    "pen":   'M-7,7 L-5,1 L3,-7 L7,-3 L-1,5 Z M-5,1 L-1,5',
    "bolt":  'M1,-8 L-5,1 L-1,1 L-1,8 L5,-1 L1,-1 Z',
    "mail":  'M-8,-5 h16 v10 h-16 z M-8,-5 L0,2 L8,-5',
}


def button(name, label, glyph, accent):
    p = f"b{abs(hash(name)) % 9999}_"
    fs = 11.5
    tw = len(label) * cw(fs) * 1.02
    w = int(tw + 68)
    h = 40
    gpath = GLYPHS[glyph]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
  <defs>
    <linearGradient id="{p}g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{accent}" stop-opacity=".16"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity=".03"/>
    </linearGradient>
  </defs>
  <rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="10" fill="{PANEL}" stroke="{accent}"
        stroke-width="1.5" stroke-opacity=".55"/>
  <rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="10" fill="url(#{p}g)"/>
  <rect x="0" y="12" width="2.5" height="16" rx="1.2" fill="{accent}"/>
  <g transform="translate(26,20)" stroke="{accent}" stroke-width="1.6" fill="none"
     stroke-linecap="round" stroke-linejoin="round">
    <path d="{gpath}"/>
  </g>
  <text x="44" y="24.5" font-family="{MONO}" font-size="{fs}" font-weight="700" fill="{TEXT}"
        letter-spacing="1">{esc(label)}</text>
  <circle cx="{w-14}" cy="20" r="2.4" fill="{accent}">
    <animate attributeName="opacity" values=".25;1;.25" dur="2.4s" repeatCount="indefinite"/>
  </circle>
</svg>
'''
    write(name, svg)


main()
