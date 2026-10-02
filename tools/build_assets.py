#!/usr/bin/env python3
"""Generates every SVG asset used by README.md.
Edit the DATA section (skills, roadmap, statuses), then run:  python tools/build_assets.py
No dependencies beyond the Python standard library."""
import math, os, random, textwrap, zlib
from xml.sax.saxutils import escape

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
A = os.path.join(ROOT, "assets")
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"
INK, NAVY, ROYAL, BLUE, VIOLET, ROSE = "#060814", "#0B1033", "#1B2A9E", "#4F6BFF", "#8B5CF6", "#E879F9"
GOLD, CYAN, WHITE, MUTED, LINK = "#F5C451", "#22D3EE", "#F8FAFF", "#A9B4E0", "#9FB0FF"

def esc(t): return escape(t, {'"': "&quot;"})
def write(rel, s):
    p = os.path.join(A, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

# ------------------------------------------------------------------ DATA (edit me)
SKILL_TIERS = [
    ("Hands-on experience", "used in real projects or training", GOLD,
     "Robotics & automation projects · electronics prototyping · FANUC and ABB robot operation · teach pendant · pneumatics · PLC fundamentals"),
    ("Currently building with", "in active use right now", CYAN, "Python · Git & GitHub · MATLAB"),
    ("Currently learning", "foundations in progress", VIOLET,
     "Control systems · engineering mathematics · Simulink · ROS2 · OpenCV · data analysis"),
    ("Future direction", "where this is heading", ROSE,
     "Sensing & processing · communication technologies · robotics software · autonomous systems · space technologies"),
]
ROADMAP = [  # (line1, line2, status)  status: "active" | "planned" | "done"
    ("100 Days", "of Python", "active"), ("PicoSat", "write-up", "planned"),
    ("Arm & pick-place", "documentation", "planned"), ("Control project", "MATLAB · Simulink", "planned"),
    ("First ROS2", "project", "planned"), ("First OpenCV", "project", "planned"),
]
STATUS = "DOCS COMING SOON"

# ------------------------------------------------------------------ primitives
def defs(extra=""):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060814"/><stop offset=".55" stop-color="#101A5C"/><stop offset="1" stop-color="#2B1470"/></linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{ROSE}"/></linearGradient>
<linearGradient id="sub" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#67E8F9"/><stop offset=".5" stop-color="#A78BFA"/><stop offset="1" stop-color="#F0ABFC"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE9A8"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="#C98A1B"/></linearGradient>
<linearGradient id="frame" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GOLD}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="royal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3B4CE0"/><stop offset="1" stop-color="#1B2A9E"/></linearGradient>
<radialGradient id="earth" cx=".5" cy=".12" r=".55"><stop offset="0" stop-color="#7DE9FF"/><stop offset=".3" stop-color="#2F55F0"/><stop offset=".7" stop-color="#101A5C"/><stop offset="1" stop-color="#060814"/></radialGradient>
<radialGradient id="planet" cx=".32" cy=".3" r=".85"><stop offset="0" stop-color="#9BE7FF"/><stop offset=".35" stop-color="{BLUE}"/><stop offset=".75" stop-color="#1B2A9E"/><stop offset="1" stop-color="#0B1033"/></radialGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset=".4" stop-color="{BLUE}" stop-opacity=".45"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="moon" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#FFE3FB"/><stop offset="1" stop-color="{ROSE}"/></radialGradient>
<radialGradient id="aB"><stop offset="0" stop-color="{BLUE}" stop-opacity=".5"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="aV"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".5"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="aG"><stop offset="0" stop-color="{GOLD}" stop-opacity=".25"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="aR"><stop offset="0" stop-color="{ROSE}" stop-opacity=".45"/><stop offset="1" stop-color="{ROSE}" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#8FA2FF" stroke-opacity=".08"/></pattern>
{extra}</defs>'''

def svg(w, h, body, title, extra="", rounded=18, border=True):
    bd = f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{rounded}" fill="none" stroke="url(#frame)" stroke-opacity=".55" stroke-width="1.5"/>' if border else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
{defs(extra)}
<clipPath id="clip"><rect width="{w}" height="{h}" rx="{rounded}"/></clipPath>
<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="url(#bg)"/>
{body}</g>{bd}
</svg>'''

def rot(angles, dur, cx=0, cy=0, smooth=False, begin=0):
    n = len(angles); v = ";".join(f"{a} {cx} {cy}" for a in angles); s = ""
    if smooth:
        kt = ";".join(f"{i/(n-1):.4f}" for i in range(n)); ks = ";".join(["0.45 0 0.55 1"] * (n - 1))
        s = f' calcMode="spline" keyTimes="{kt}" keySplines="{ks}"'
    return f'<animateTransform attributeName="transform" type="rotate" values="{v}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"{s}/>'

def trans(pts, dur, kt=None, smooth=False):
    v = ";".join(f"{x} {y}" for x, y in pts); s = ""
    if kt: s += f' keyTimes="{";".join(str(k) for k in kt)}"'
    elif smooth:
        n = len(pts); s = f' calcMode="spline" keyTimes="{";".join(f"{i/(n-1):.4f}" for i in range(n))}" keySplines="{";".join(["0.45 0 0.55 1"]*(n-1))}"'
    return f'<animateTransform attributeName="transform" type="translate" values="{v}" dur="{dur}s" repeatCount="indefinite"{s}/>'

def scl(vals, dur, begin=0):
    return f'<animateTransform attributeName="transform" type="scale" values="{";".join(vals)}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'

def an(attr, vals, dur, begin=0, extra=""):
    return f'<animate attributeName="{attr}" values="{";".join(str(v) for v in vals)}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'

def stars(w, h, n, seed, tw=.45):
    r = random.Random(seed); o = []
    for _ in range(n):
        x, y, rad = r.uniform(0, w), r.uniform(0, h), r.choice([.6, .8, 1, 1.2, 1.6])
        c = r.choice([WHITE] * 5 + [GOLD, CYAN, "#C4B5FD"])
        if r.random() < tw:
            d = r.uniform(3, 9)
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="{c}"><animate attributeName="opacity" values=".12;1;.12" dur="{d:.1f}s" begin="-{r.uniform(0,d):.1f}s" repeatCount="indefinite"/></circle>')
        else:
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="{c}" opacity=".55"/>')
    return "".join(o)

def aurora(w, h):
    return f'''<g>
<ellipse cx="{w*.2}" cy="{h*.22}" rx="{w*.34}" ry="{h*.26}" fill="url(#aB)">{trans([(0,0),(50,26),(0,0)],16,smooth=True)}</ellipse>
<ellipse cx="{w*.82}" cy="{h*.78}" rx="{w*.36}" ry="{h*.3}" fill="url(#aV)">{trans([(0,0),(-46,-20),(0,0)],19,smooth=True)}</ellipse>
<ellipse cx="{w*.5}" cy="{h*1.02}" rx="{w*.3}" ry="{h*.14}" fill="url(#aG)">{trans([(0,0),(60,0),(0,0)],13,smooth=True)}</ellipse>
</g>'''

def sat(s=1.0, body=WHITE, panel=CYAN):
    return (f'<g transform="scale({s})"><rect x="-6" y="-4" width="12" height="8" rx="1.5" fill="{body}"/>'
            f'<rect x="-22" y="-2.5" width="14" height="5" fill="{panel}"/><rect x="8" y="-2.5" width="14" height="5" fill="{panel}"/>'
            f'<line y2="-9" stroke="{GOLD}"/><circle cy="-10" r="1.6" fill="{GOLD}"/></g>')

def ring(cx, cy, rx, ry, tilt, color, dash, dur, obj, rev=False, op=.55):
    sw = 1 if rev else 0
    path = f"M{cx-rx},{cy} a{rx},{ry} 0 1,{sw} {2*rx},0 a{rx},{ry} 0 1,{sw} {-2*rx},0"
    return (f'<g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.4" {dash}/>'
            f'<g>{obj}<animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/></g></g>')

def pill(x, y, text, color, font=14, h=30):
    w = len(text) * font * (.68 if text.isupper() or '·' in text and text.split(' · ')[0].isupper() else .56) + 34
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{NAVY}" fill-opacity=".8" stroke="{color}" stroke-opacity=".85"/>'
            f'<circle cx="{x+15}" cy="{y+h/2}" r="3" fill="{color}">{an("opacity",[1,.3,1],2.4)}</circle>'
            f'<text x="{x+27}" y="{y+h/2+font*.35:.1f}" font-family="{SANS}" font-size="{font}" fill="{WHITE}">{esc(text)}</text>'), w

# ------------------------------------------------------------------ hero
def hero():
    W, H, cx, cy = 900, 520, 655, 262
    ex = f'''<linearGradient id="namefill" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="900" y2="0">
<stop offset="0" stop-color="{WHITE}"/><stop offset=".43" stop-color="{WHITE}"/><stop offset=".5" stop-color="#FFD978"/><stop offset=".57" stop-color="{WHITE}"/><stop offset="1" stop-color="{WHITE}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-640 0;-640 0;160 0" keyTimes="0;.3;1" dur="7s" repeatCount="indefinite"/></linearGradient>
<clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="64"/></clipPath>'''
    b = [aurora(W, H), f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', stars(W, H, 80, 7),
         f'<rect width="{W}" height="2" fill="{CYAN}" opacity=".13">{an("y",[-4,H],9)}</rect>']
    b.append(f'<circle cx="{cx}" cy="{cy}" r="160" fill="url(#halo)"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="100" fill="none" stroke="{ROSE}" stroke-opacity=".28" stroke-dasharray="2 7"/>')
    b.append(ring(cx, cy, 235, 66, -20, GOLD, "", 22, sat(1.2, WHITE, CYAN), op=.6))
    b.append(ring(cx, cy, 178, 48, 24, CYAN, 'stroke-dasharray="3 6"', 13,
                  '', rev=True, op=.5))
    # comet (head + fading tail) on the cyan ring
    sw = 1; rx, ry = 178, 48
    path = f"M{cx-rx},{cy} a{rx},{ry} 0 1,{sw} {2*rx},0 a{rx},{ry} 0 1,{sw} {-2*rx},0"
    comet = "".join(f'<g transform="rotate(24 {cx} {cy})"><circle r="{r}" fill="{CYAN}" opacity="{o}" filter="url(#glow)"><animateMotion dur="13s" begin="{bg}s" repeatCount="indefinite" path="{path}"/></circle></g>'
                    for r, o, bg in [(4, 1, -.6), (3, .55, -.3), (2, .3, 0)])
    b.append(comet)
    b.append(f'<g clip-path="url(#pc)"><circle cx="{cx}" cy="{cy}" r="64" fill="url(#planet)"/>' + "".join(
        f'<path d="M{cx-190},{cy+dy} q32,-9 64,0 t64,0 t64,0 t64,0 t64,0 t64,0 t64,0" fill="none" stroke="#CFE9FF" stroke-opacity=".16" stroke-width="7">{trans([(0,0),(128,0)],14)}</path>'
        for dy in (-30, 2, 32)) + f'<circle cx="{cx+22}" cy="{cy+20}" r="66" fill="#060814" opacity=".35"/></g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="64" fill="none" stroke="{CYAN}" stroke-opacity=".55" stroke-width="1.5"/>')
    b.append(f'<g><circle r="8" fill="url(#moon)" filter="url(#glow)"/><animateMotion dur="11s" repeatCount="indefinite" path="M{cx-100},{cy} a100,100 0 1,1 200,0 a100,100 0 1,1 -200,0"/></g>')
    # identity
    b.append(f'<circle cx="52" cy="66" r="4" fill="{CYAN}">{an("opacity",[1,.2,1],2.2)}</circle><text x="66" y="71" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{MUTED}">NM-001 · ONLINE</text>')
    b.append(f'<text x="44" y="172" font-family="{SANS}" font-size="86" font-weight="800" letter-spacing="2" fill="url(#namefill)">NARESH</text>')
    b.append(f'<text x="44" y="256" font-family="{SANS}" font-size="86" font-weight="800" letter-spacing="2" fill="url(#gold)">MURTHY</text>')
    b.append(f'<text x="48" y="300" font-family="{SANS}" font-size="21" font-weight="700" letter-spacing="3" fill="url(#sub)">ROBOTICS → SPACE SYSTEMS</text>')
    b.append(f'<line x1="48" y1="316" x2="400" y2="316" stroke="url(#frame)" stroke-width="1.5" stroke-dasharray="352" stroke-dashoffset="352"><animate attributeName="stroke-dashoffset" values="352;0" dur="2s" fill="freeze"/></line>')
    # typing
    phr = ["SPACE SYSTEMS", "ROBOTICS & AUTOMATION", "CONTROL & AUTONOMY", "SOFTWARE FOR MACHINES"]
    T, cw, x0, ty = 16, 13.4, 74, 354
    clips = texts = ""
    for i, p in enumerate(phr):
        s = i / 4; Wd = round(len(p) * cw + 3, 1)
        kt = f"0;{s:.3f};{s+.055:.3f};{s+.2:.3f};{s+.235:.3f};1"
        clips += f'<clipPath id="tc{i}"><rect x="{x0}" y="{ty-24}" width="0" height="34"><animate attributeName="width" values="0;0;{Wd};{Wd};0;0" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>'
        texts += (f'<text x="{x0}" y="{ty}" font-family="{MONO}" font-size="22" font-weight="600" fill="{CYAN}" clip-path="url(#tc{i})">{esc(p)}</text>'
                  f'<g><animate attributeName="opacity" values="1;0" keyTimes="0;.5" calcMode="discrete" dur="1s" repeatCount="indefinite"/>'
                  f'<rect y="{ty-20}" width="9" height="24" fill="{GOLD}" x="{x0}"><animate attributeName="x" values="{x0};{x0};{x0+Wd};{x0+Wd};{x0};{x0}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="visibility" values="hidden;visible;hidden;hidden" keyTimes="0;{s:.3f};{s+.235:.3f};1" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/></rect></g>')
    b.append(f'<defs>{clips}</defs><text x="46" y="{ty}" font-family="{MONO}" font-size="22" fill="{GOLD}">&gt;</text>{texts}')
    p1, w1 = pill(44, 384, "M.Sc. Space Science & Technology · University of Bremen", GOLD, 13)
    p2, w2 = pill(44, 424, "B.Tech Robotics & Automation · Lovely Professional University", CYAN, 13)
    b += [p1, p2]
    b.append(f'<text x="46" y="492" font-family="{MONO}" font-size="12.5" letter-spacing="4" fill="{MUTED}">SPACE · ROBOTICS · SOFTWARE · CONTROL</text>')
    b.append(f'<text x="{W-44}" y="492" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}" opacity=".7">ORBIT 01 · LOCKED</text>')
    b.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="16" fill="none" stroke="url(#frame)" stroke-opacity=".7" stroke-width="2"/>')
    b.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="16" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-dasharray="150 2680" filter="url(#glow)"><animate attributeName="stroke-dashoffset" values="0;-2830" dur="11s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "".join(b), "Naresh Murthy. Robotics to Space Systems. M.Sc. Space Science and Technology, University of Bremen.", ex, 20, border=False)

# ------------------------------------------------------------------ banners
def gear(ro=19, ri=14, n=8):
    pts = []
    for i in range(n):
        a, w = 2 * math.pi * i / n, math.pi / n
        for ang, r in [(a - w * .55, ri), (a - w * .3, ro), (a + w * .3, ro), (a + w * .55, ri)]:
            pts.append(f"{r*math.cos(ang):.1f},{r*math.sin(ang):.1f}")
    return " ".join(pts)

ICONS = {
 "mission": lambda c: f'<circle r="18" fill="none" stroke="{c}" stroke-opacity=".5"/><circle r="9" fill="none" stroke="{c}" stroke-opacity=".8"/><circle r="3.5" fill="{GOLD}"/><g><circle cx="18" r="3.5" fill="{WHITE}"/>{rot([0,360],6)}</g>',
 "journey": lambda c: f'<path id="jp" d="M-20,14 C-8,14 -4,-6 6,-8 S16,-16 20,-18" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round"/><circle r="3.5" fill="{WHITE}" filter="url(#glow)"><animateMotion dur="3s" repeatCount="indefinite" path="M-20,14 C-8,14 -4,-6 6,-8 S16,-16 20,-18"/></circle>',
 "projects": lambda c: "".join(f'<rect x="{x}" y="{y}" width="15" height="15" rx="3" fill="{c}">{an("opacity",[.3,1,.3],2.4,-i*.6)}</rect>' for i, (x, y) in enumerate([(-17,-17),(2,-17),(2,2),(-17,2)])),
 "skills": lambda c: f'<circle r="21" fill="none" stroke="{c}" stroke-opacity=".5">{an("r",[19,22,19],2.5)}</circle><text y="7" text-anchor="middle" font-family="{MONO}" font-weight="700" font-size="19" fill="{WHITE}">&lt;/&gt;</text>',
 "industrial": lambda c: f'<g><polygon points="{gear()}" fill="{c}"/><circle r="6" fill="{NAVY}"/>{rot([0,360],12)}</g>',
 "international": lambda c: f'<circle r="18" fill="none" stroke="{c}"/><line x1="-18" x2="18" stroke="{c}" stroke-opacity=".6"/><line x1="-15.6" x2="15.6" y1="-9" y2="-9" stroke="{c}" stroke-opacity=".4"/><line x1="-15.6" x2="15.6" y1="9" y2="9" stroke="{c}" stroke-opacity=".4"/><ellipse ry="18" rx="16" fill="none" stroke="{c}" stroke-opacity=".8">{an("rx",[16,0,16],6)}</ellipse><ellipse ry="18" rx="0" fill="none" stroke="{GOLD}" stroke-opacity=".8">{an("rx",[0,16,0],6)}</ellipse>',
 "foundations": lambda c: f'<text x="-19" y="8" font-family="{MONO}" font-weight="700" font-size="24" fill="{c}">&gt;</text><rect x="-3" y="7" width="15" height="3.5" fill="{WHITE}">{an("opacity",[1,0,1],1.2)}</rect>',
 "roadmap": lambda c: f'<path d="M0,-21 C9,-12 9,4 6,11 L-6,11 C-9,4 -9,-12 0,-21 Z" fill="{WHITE}" stroke="{c}"/><circle cy="-7" r="3.2" fill="{c}"/><polygon points="-6,4 -13,15 -6,11" fill="{c}"/><polygon points="6,4 13,15 6,11" fill="{c}"/><g transform="translate(0,11)"><g>{scl(["1 1","1 1.5","1 .8","1 1.3","1 1"],.5)}<polygon points="-4,0 0,13 4,0" fill="{GOLD}"/></g></g>',
 "contact": lambda c: f'<circle r="3.5" fill="{GOLD}"/>' + "".join(f'<circle r="4" fill="none" stroke="{c}" stroke-width="1.6">{an("r",[4,22],2.7,-i*.9)}{an("opacity",[.9,0],2.7,-i*.9)}</circle>' for i in range(3)),
}

def banner(key, title, sub, c1, c2):
    W, H = 900, 92
    ex = f'<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}" stop-opacity=".4"/><stop offset=".55" stop-color="{c1}" stop-opacity="0"/></linearGradient><linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}" stop-opacity="0"/><stop offset=".5" stop-color="{WHITE}"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></linearGradient>'
    chev = "".join(f'<path d="M{826+i*16},34 l10,12 l-10,12" fill="none" stroke="{c2}" stroke-width="3" stroke-linecap="round">{an("opacity",[.15,1,.15],1.8,-i*.35)}</path>' for i in range(3))
    b = (f'<rect width="{W}" height="{H}" fill="url(#gl)"/>{stars(W,H,22,zlib.crc32(key.encode())%999,.6)}'
         f'<circle cx="58" cy="46" r="31" fill="{NAVY}" stroke="{c1}" stroke-width="1.5"/>'
         f'<circle cx="58" cy="46" r="38" fill="none" stroke="{c2}" stroke-opacity=".6" stroke-dasharray="3 8"><animateTransform attributeName="transform" type="rotate" values="0 58 46;360 58 46" dur="18s" repeatCount="indefinite"/></circle>'
         f'<g transform="translate(58,46)">{ICONS[key](c1)}</g>'
         f'<text x="112" y="46" font-family="{SANS}" font-size="31" font-weight="800" letter-spacing=".5" fill="{WHITE}">{esc(title)}</text>'
         f'<text x="114" y="68" font-family="{MONO}" font-size="13" letter-spacing="1" fill="{MUTED}">{esc(sub)}</text>{chev}'
         f'<rect y="{H-3}" width="{W}" height="3" fill="{c1}" opacity=".35"/><rect y="{H-3}" width="220" height="3" fill="url(#ln)">{an("x",[-220,W],4.5)}</rect>')
    return svg(W, H, b, title, ex, 16)

# ------------------------------------------------------------------ identity (constellation)
def identity():
    W, H = 900, 400
    nodes = [(150, "ROBOTICS", "where I start", BLUE, "Arms · pick-and-place · drones · AGV · industrial robot exposure"),
             (450, "SOFTWARE & CONTROL", "the bridge", VIOLET, "Python · control systems · MATLAB / Simulink · ROS2"),
             (750, "SPACE", "where I'm heading", ROSE, "Satellite systems · sensing · processing · communication")]
    icons = {0: f'<g transform="translate(-14,16)"><g>{rot([-10,30,-10],4,smooth=True)}<rect x="-3" y="-30" width="6" height="32" rx="3" fill="{WHITE}"/><g transform="translate(0,-28)"><g>{rot([50,100,50],4,smooth=True)}<rect x="-3" y="-26" width="6" height="28" rx="3" fill="{GOLD}"/></g></g></g></g>',
             1: f'<text y="9" text-anchor="middle" font-family="{MONO}" font-weight="700" font-size="26" fill="{WHITE}">&lt;/&gt;</text>',
             2: f'<circle r="15" fill="url(#planet)"/><g transform="rotate(-22)"><ellipse rx="30" ry="8" fill="none" stroke="{GOLD}" stroke-width="2"/><g><circle cx="30" r="3" fill="{WHITE}"/><animateMotion dur="4s" repeatCount="indefinite" path="M-30,0 a30,8 0 1,0 60,0 a30,8 0 1,0 -60,0"/></g></g>'}
    b = [aurora(W, H), f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', stars(W, H, 50, 3)]
    for i in range(2):
        x1, x2 = nodes[i][0] + 58, nodes[i + 1][0] - 58
        b.append(f'<line x1="{x1}" y1="150" x2="{x2}" y2="150" stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="8 8" stroke-opacity=".9">{an("stroke-dashoffset",[0,-32],1.2)}</line>'
                 f'<polygon points="{x2},150 {x2-12},143 {x2-12},157" fill="{GOLD}"/>')
    for x, t, tag, c, desc in nodes:
        b.append(f'<circle cx="{x}" cy="150" r="90" fill="url(#{ {BLUE:"aB",VIOLET:"aV",ROSE:"aR"}[c] })"/>')
        b.append(f'<circle cx="{x}" cy="150" r="52" fill="{NAVY}" stroke="{c}" stroke-width="2"/>')
        b.append(f'<circle cx="{x}" cy="150" r="52" fill="none" stroke="{c}" stroke-width="1.5">{an("r",[52,66],3)}{an("opacity",[.8,0],3)}</circle>')
        b.append(f'<g transform="translate({x},150)">{icons[nodes.index((x,t,tag,c,desc))]}</g>')
        b.append(f'<text x="{x}" y="58" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{c}">{tag.upper()}</text>')
        b.append(f'<text x="{x}" y="244" text-anchor="middle" font-family="{SANS}" font-size="21" font-weight="800" fill="{WHITE}">{esc(t)}</text>')
        for k, ln in enumerate(textwrap.wrap(desc, 32 if x != 150 else 36)):
            b.append(f'<text x="{x}" y="{268+k*19}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{MUTED}">{esc(ln)}</text>')
    b.append(f'<rect x="40" y="326" width="820" height="52" rx="26" fill="{NAVY}" fill-opacity=".85" stroke="url(#frame)" stroke-opacity=".8"/>')
    for x, _, _, c, _ in nodes:
        b.append(f'<line x1="{x}" y1="326" x2="{x}" y2="300" stroke="{c}" stroke-opacity=".7" stroke-dasharray="3 5">{an("stroke-dashoffset",[0,-16],1.4)}</line>')
    b.append(f'<circle cx="76" cy="352" r="4" fill="{GOLD}">{an("opacity",[1,.3,1],2)}</circle>')
    b.append(f'<text x="94" y="357" font-family="{SANS}" font-size="15" fill="{WHITE}"><tspan font-weight="800" fill="{GOLD}">International experience</tspan>  ·  governance and audit across teams in Europe and the Americas</text>')
    return svg(W, H, "".join(b), "Identity map: Robotics, then Software and Control, then Space, all supported by international experience.", rounded=18)

# ------------------------------------------------------------------ journey
def journey():
    W, H = 900, 470
    segs = [((100, 380), (250, 380), (310, 290), (430, 262)), ((430, 262), (560, 234), (650, 150), (810, 104))]
    def bez(s, t):
        a, b_, c, d = s; u = 1 - t
        return tuple(u**3*a[i] + 3*u*u*t*b_[i] + 3*u*t*t*c[i] + t**3*d[i] for i in range(2))
    pts = [bez(s, k / 120) for s in segs for k in range(121)]
    cum = [0]
    for i in range(1, len(pts)): cum.append(cum[-1] + math.dist(pts[i], pts[i-1]))
    def at(f):
        tgt = f * cum[-1]
        for i, c in enumerate(cum):
            if c >= tgt: return pts[i]
    d = f"M100,380 C250,380 310,290 430,262 C560,234 650,150 810,104"
    nodes = [("School", ["NASA Space Settlement", "project (school-level)"], BLUE, "up", 0),
             ("B.Tech", ["Robotics & Automation", "Lovely Professional Univ."], CYAN, "down", .2),
             ("Projects", ["PicoSat · arm · drone", "AGV · RC car · more"], VIOLET, "up", .4),
             ("DIFACTO", ["Industrial robotics", "training, Bangalore"], GOLD, "down", .6),
             ("M.Sc.", ["Space Science & Tech", "University of Bremen"], ROSE, "up", .8),
             ("Next", ["Autonomous & intelligent", "space systems"], WHITE, "down", 1.0)]
    b = [aurora(W, H), f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', stars(W, H, 60, 11)]
    b.append(f'<path d="{d}" fill="none" stroke="url(#brand)" stroke-width="10" stroke-opacity=".18" stroke-linecap="round"/>')
    b.append(f'<path d="{d}" fill="none" stroke="url(#sub)" stroke-width="3" stroke-linecap="round" stroke-dasharray="1500" stroke-dashoffset="1500"><animate attributeName="stroke-dashoffset" values="1500;0" dur="3s" fill="freeze"/></path>')
    b.append(f'<circle r="6" fill="{WHITE}" filter="url(#glow)"><animateMotion dur="9s" repeatCount="indefinite" path="{d}"/></circle>')
    for i, (t, lines, c, side, f) in enumerate(nodes):
        x, y = at(f)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{NAVY}" stroke="{c}" stroke-width="2.5"{" stroke-dasharray=&quot;3 3&quot;" if t=="Next" else ""}/>'.replace("&quot;", '"'))
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="none" stroke="{c}">{an("r",[13,28],3,-i*.5)}{an("opacity",[.8,0],3,-i*.5)}</circle><circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="{c}"/>')
        ty = y - 70 if side == "up" else y + 50
        if i == 0: ty = y - 86
        anc, tx = "middle", x
        if i == 0: anc, tx = "start", x - 40
        if i == 5: anc, tx = "end", x + 40
        b.append(f'<line x1="{x:.0f}" y1="{y + (-14 if side=="up" else 14):.0f}" x2="{x:.0f}" y2="{(y - 56 if side=="up" else y + 34) if i else y - 70:.0f}" stroke="{c}" stroke-opacity=".6"/>')
        b.append(f'<text x="{tx:.0f}" y="{ty:.0f}" text-anchor="{anc}" font-family="{SANS}" font-size="20" font-weight="800" fill="{c}">{esc(t)}</text>')
        for k, ln in enumerate(lines):
            b.append(f'<text x="{tx:.0f}" y="{ty+22+k*18:.0f}" text-anchor="{anc}" font-family="{SANS}" font-size="14" fill="{MUTED}">{esc(ln)}</text>')
    return svg(W, H, "".join(b), "Engineering journey: school space project, B.Tech Robotics and Automation, engineering projects, DIFACTO industrial robotics training, M.Sc. Space Science and Technology in Bremen, then autonomous and intelligent space systems.")

# ------------------------------------------------------------------ project illustrations (440 x 170 box)
def link(l, w, fill="#2A3BC8"):
    return f'<rect x="{-w/2}" y="{-l-w/2}" width="{w}" height="{l+w}" rx="{w/2}" fill="{fill}" stroke="{LINK}" stroke-width="1.5"/>'

def ill_picosat():
    panel = lambda sx: (f'<g transform="scale({sx},1)"><rect x="22" y="-11" width="56" height="22" fill="#1B2A9E" stroke="{CYAN}"/>'
                        + "".join(f'<line x1="{x}" y1="-11" x2="{x}" y2="11" stroke="{CYAN}" stroke-opacity=".6"/>' for x in (36, 50, 64))
                        + f'<line x1="22" x2="78" stroke="{CYAN}" stroke-opacity=".6"/></g>')
    sig = "".join(f'<circle cy="-31" r="3" fill="none" stroke="{ROSE}" stroke-width="1.6">{an("r",[3,28],2.7,-i*.9)}{an("opacity",[.9,0],2.7,-i*.9)}</circle>' for i in range(3))
    return (f'<circle cx="220" cy="330" r="226" fill="url(#earth)"/><circle cx="220" cy="330" r="226" fill="none" stroke="{CYAN}" stroke-opacity=".6" stroke-width="2"/>'
            f'<path d="M30,126 Q220,-14 410,126" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-dasharray="3 6"/>'
            f'<g><circle r="3" fill="{GOLD}"/><animateMotion dur="9s" repeatCount="indefinite" path="M30,126 Q220,-14 410,126"/></g>'
            f'<g>{trans([(220,72),(220,64),(220,72)],5,smooth=True)}<g>{rot([-5,5,-5],7,smooth=True)}'
            f'{panel(1)}{panel(-1)}<rect x="-17" y="-17" width="34" height="34" rx="3" fill="url(#gold)" stroke="{WHITE}" stroke-opacity=".7"/>'
            f'<line x1="-17" y1="0" x2="17" y2="0" stroke="#7A5200" stroke-opacity=".6"/><line y1="-17" y2="17" stroke="#7A5200" stroke-opacity=".6"/>'
            f'<line y1="-17" y2="-30" stroke="{LINK}"/><circle cy="-31" r="3" fill="{ROSE}"/>{sig}</g></g>')

def ill_arm():
    return (f'<rect x="96" y="148" width="76" height="12" rx="4" fill="#1B2A9E" stroke="{CYAN}" stroke-opacity=".7"/>'
            f'<path d="M116,148 L124,134 H144 L152,148 Z" fill="#101A5C" stroke="{CYAN}" stroke-opacity=".6"/>'
            f'<rect x="334" y="112" width="16" height="48" fill="#101A5C" stroke="{CYAN}" stroke-opacity=".5"/><circle cx="342" cy="104" r="9" fill="url(#moon)">{an("opacity",[1,.6,1],2)}</circle>'
            f'<g transform="translate(134,134)"><g>{rot([22,48,22],6,smooth=True)}{link(78,15)}'
            f'<g transform="translate(0,-78)"><g>{rot([58,92,58],6,smooth=True)}{link(78,13)}'
            f'<g transform="translate(0,-78)"><g>{rot([-8,22,-8],6,smooth=True)}<rect x="-9" y="-8" width="18" height="12" rx="3" fill="{GOLD}"/>'
            f'<rect x="-9" y="-24" width="4" height="18" fill="{WHITE}">{an("x",[-9,-6,-9],3)}</rect><rect x="5" y="-24" width="4" height="18" fill="{WHITE}">{an("x",[5,2,5],3)}</rect></g></g>'
            f'<circle r="8" fill="{GOLD}"/></g></g><circle r="9" fill="{GOLD}"/></g></g>')

def ill_pick():
    K = [0, .28, .36, .42, .52, .68, .76, .82, .92, 1.0]
    G = [(190,44),(190,44),(190,88),(190,88),(190,44),(340,44),(340,88),(340,88),(340,44),(190,44)]
    B = [(36,110),(190,110),(190,110),(190,110),(190,66),(340,66),(340,110),(340,110),(340,110),(340,110)]
    return (f'<clipPath id="rail"><rect x="0" y="24" width="440" height="146"/></clipPath>'
            f'<rect x="10" y="22" width="420" height="4" rx="2" fill="{GOLD}" opacity=".8"/>'
            f'<rect x="14" y="122" width="214" height="12" rx="6" fill="#1B2A9E" stroke="{CYAN}" stroke-opacity=".7"/>'
            f'<line x1="26" y1="128" x2="216" y2="128" stroke="{WHITE}" stroke-opacity=".5" stroke-dasharray="8 10">{an("stroke-dashoffset",[0,-36],1)}</line>'
            f'<rect x="286" y="122" width="116" height="12" rx="4" fill="{GOLD}" opacity=".85"/><rect x="296" y="134" width="8" height="26" fill="#101A5C"/><rect x="384" y="134" width="8" height="26" fill="#101A5C"/>'
            f'<g clip-path="url(#rail)"><g>{trans(G,6,K)}<rect x="-2.5" y="-300" width="5" height="300" fill="{LINK}"/><rect x="-14" y="-6" width="28" height="12" rx="3" fill="{GOLD}"/>'
            f'<rect x="-14" y="4" width="5" height="14" rx="1.5" fill="{WHITE}"/><rect x="9" y="4" width="5" height="14" rx="1.5" fill="{WHITE}"/></g></g>'
            f'<g><animate attributeName="opacity" values="0;1;1;1;0;0" keyTimes="0;.03;.88;.92;.97;1" dur="6s" repeatCount="indefinite"/><g>{trans(B,6,K)}<rect x="-12" y="-12" width="24" height="24" rx="3" fill="url(#moon)" stroke="{WHITE}" stroke-opacity=".7"/></g></g>')

def ill_quad():
    rotors = [(-66, -30), (66, -30), (-66, 30), (66, 30)]
    s = "".join(f'<line x2="{x}" y2="{y}" stroke="{LINK}" stroke-width="5" stroke-linecap="round"/>' for x, y in rotors)
    for i, (x, y) in enumerate(rotors):
        s += (f'<g transform="translate({x},{y})"><circle r="27" fill="{CYAN}" fill-opacity=".1" stroke="{CYAN}" stroke-opacity=".5"/><g>{rot([0,360] if i%2 else [360,0],.45)}'
              f'<line x1="-25" x2="25" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/><line y1="-25" y2="25" stroke="{WHITE}" stroke-opacity=".7" stroke-width="3" stroke-linecap="round"/></g>'
              f'<circle r="4" fill="{GOLD}"/><circle cx="{-16 if x<0 else 16}" cy="{-16 if y<0 else 16}" r="2.4" fill="{ROSE if i<2 else CYAN}">{an("opacity",[1,.1,1],1.1,-i*.3)}</circle></g>')
    s += (f'<rect x="-17" y="-17" width="34" height="34" rx="9" fill="#1B2A9E" stroke="{GOLD}" stroke-width="1.5" transform="rotate(45)"/><circle r="7" fill="{NAVY}" stroke="{CYAN}"/><circle r="2.5" fill="{CYAN}"/>'
          f'<polygon points="-5,-24 5,-24 0,-34" fill="{GOLD}">{an("opacity",[1,.3,1],1.4)}</polygon>')
    return (f'<ellipse cx="220" cy="156" rx="64" ry="8" fill="#000" opacity=".35">{an("rx",[64,52,64],3.2)}</ellipse>'
            f'<g transform="translate(220,82)"><g>{trans([(0,0),(0,-6),(0,0)],3.2,smooth=True)}<g>{rot([-3,3,-3],4.4,smooth=True)}{s}</g></g></g>')

TRACK = "M30,128 C100,40 170,160 232,96 S360,40 414,112"
def ill_agv():
    return (f'<path d="{TRACK}" fill="none" stroke="{GOLD}" stroke-opacity=".28" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="{TRACK}" fill="none" stroke="{WHITE}" stroke-opacity=".55" stroke-width="2" stroke-dasharray="6 8">{an("stroke-dashoffset",[0,-28],1.4)}</path>'
            + "".join(f'<rect x="{x-6}" y="{y-6}" width="12" height="12" rx="2" fill="{NAVY}" stroke="{c}" stroke-width="2"/>' for x, y, c in [(30,128,CYAN),(232,96,ROSE),(414,112,GOLD)])
            + f'<g><polygon points="16,-4 56,-18 56,18 16,4" fill="{GOLD}" opacity=".18">{an("opacity",[.1,.3,.1],1.6)}</polygon>'
            f'<rect x="-18" y="-11" width="36" height="22" rx="6" fill="url(#royal)" stroke="{CYAN}" stroke-width="1.5"/>'
            f'<rect x="-14" y="-14" width="9" height="4" rx="1" fill="{WHITE}"/><rect x="5" y="-14" width="9" height="4" rx="1" fill="{WHITE}"/><rect x="-14" y="10" width="9" height="4" rx="1" fill="{WHITE}"/><rect x="5" y="10" width="9" height="4" rx="1" fill="{WHITE}"/>'
            f'<rect x="-8" y="-6" width="14" height="12" rx="2" fill="{GOLD}"/><circle cx="18" r="3" fill="{ROSE}">{an("opacity",[1,.2,1],.9)}</circle>'
            f'<animateMotion dur="10s" rotate="auto" repeatCount="indefinite" path="{TRACK}"/></g>')

def ill_cosmo():
    return (f'<line x1="14" y1="148" x2="426" y2="148" stroke="{CYAN}" stroke-opacity=".4"/>'
            f'<g>{trans([(130,0),(310,0),(130,0)],9,smooth=True)}<g>{trans([(0,0),(0,-3),(0,0)],.9)}'
            f'<line y1="58" y2="44" x1="0" x2="0" stroke="{LINK}" stroke-width="2"/><circle cy="40" r="4.5" fill="{GOLD}" filter="url(#glow)">{an("opacity",[1,.3,1],1.3)}</circle>'
            f'<rect x="-27" y="58" width="54" height="34" rx="15" fill="url(#royal)" stroke="{LINK}" stroke-width="1.5"/>'
            f'<ellipse cx="-10" cy="75" rx="5" ry="5" fill="{CYAN}">{an("ry",[5,5,.6,5],4)}</ellipse><ellipse cx="10" cy="75" rx="5" ry="5" fill="{CYAN}">{an("ry",[5,5,.6,5],4)}</ellipse>'
            f'<rect x="-36" y="94" width="72" height="42" rx="12" fill="url(#royal)" stroke="{LINK}" stroke-width="1.5"/><rect x="-22" y="104" width="44" height="6" rx="3" fill="{NAVY}"/><circle cy="122" r="6" fill="{ROSE}">{an("opacity",[1,.35,1],1.8)}</circle>'
            f'<rect x="-44" y="100" width="8" height="26" rx="4" fill="{GOLD}"/><rect x="36" y="100" width="8" height="26" rx="4" fill="{GOLD}"/>'
            + "".join(f'<g transform="translate({x},140)"><circle r="9" fill="{NAVY}" stroke="{WHITE}"/><g>{rot([0,360],1.2)}<line x1="-8" x2="8" stroke="{WHITE}"/><line y1="-8" y2="8" stroke="{WHITE}"/></g></g>' for x in (-20, 20))
            + '</g></g>')

def ill_rc():
    wheel = lambda x: f'<g transform="translate({x},4)"><circle r="15" fill="{NAVY}" stroke="{WHITE}" stroke-width="2"/><g>{rot([0,360],.7)}<line x1="-11" x2="11" stroke="{GOLD}" stroke-width="2"/><line y1="-11" y2="11" stroke="{GOLD}" stroke-width="2"/></g><circle r="3" fill="{GOLD}"/></g>'
    sig = "".join(f'<circle cx="62" cy="40" r="4" fill="none" stroke="{ROSE}" stroke-width="1.6">{an("r",[4,34],2.4,-i*.8)}{an("opacity",[.9,0],2.4,-i*.8)}</circle>' for i in range(3))
    return (f'<line x1="0" y1="140" x2="440" y2="140" stroke="{CYAN}" stroke-opacity=".4"/><line x1="0" y1="152" x2="440" y2="152" stroke="{WHITE}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="22 18">{an("stroke-dashoffset",[0,40],.7)}</line>'
            f'<rect x="40" y="44" width="34" height="22" rx="5" fill="{NAVY}" stroke="{GOLD}"/><circle cx="50" cy="55" r="4" fill="{GOLD}"/><circle cx="64" cy="55" r="2.5" fill="{CYAN}"/><line x1="62" y1="44" x2="62" y2="30" stroke="{LINK}" stroke-width="2"/><circle cx="62" cy="28" r="3" fill="{ROSE}"/>{sig}'
            f'<g transform="translate(240,126)"><g>{trans([(0,0),(0,-2.5),(0,0)],.5)}'
            f'<path d="M-72,6 L-72,-12 Q-56,-18 -38,-24 L-16,-42 L30,-42 L52,-24 Q72,-18 76,-6 L76,6 Z" fill="url(#royal)" stroke="{LINK}" stroke-width="1.5"/>'
            f'<polygon points="-14,-38 -28,-24 22,-24 20,-38" fill="{CYAN}" fill-opacity=".45"/><path d="M-72,-4 H76" stroke="{GOLD}" stroke-width="3"/>{wheel(-40)}{wheel(44)}</g></g>')

def hexpts(cx, cy, r): return " ".join(f"{cx + r*math.cos(math.radians(90+60*k)):.1f},{cy + r*math.sin(math.radians(90+60*k)):.1f}" for k in range(6))
def ill_easybee():
    r = 25; d = r * math.sqrt(3); s = ""
    for k in range(6):
        a = math.radians(60 * k); s += f'<polygon points="{hexpts(220 + d*math.cos(a), 85 + d*math.sin(a), r-2)}" fill="{GOLD}" stroke="{GOLD}" stroke-width="1.5">{an("fill-opacity",[.08,.6,.08],3.6,-k*.6)}</polygon>'
    s += f'<polygon points="{hexpts(220,85,r-2)}" fill="url(#royal)" stroke="{GOLD}" stroke-width="2"/><circle cx="220" cy="85" r="5" fill="{GOLD}" filter="url(#glow)">{an("r",[4,7,4],2)}</circle>'
    s += f'<circle cx="220" cy="85" r="82" fill="none" stroke="{VIOLET}" stroke-opacity=".5" stroke-dasharray="3 7"/><g><circle r="4" fill="{WHITE}"/><animateMotion dur="8s" repeatCount="indefinite" path="M138,85 a82,82 0 1,1 164,0 a82,82 0 1,1 -164,0"/></g>'
    return s

PROJECTS = {  # file: (title, subtitle, tag, tag colour, illustration)
    "picosat": ("PicoSat", "Satellite project", "SPACE", ROSE, ill_picosat),
    "robotic-arm": ("Robotic arm", "Built as a project · not the industrial robots", "ROBOTICS · MANIPULATION", CYAN, ill_arm),
    "pick-and-place": ("Pick-and-place robot", "Robotic manipulation and automation", "AUTOMATION", GOLD, ill_pick),
    "quadcopter": ("Quadcopter drone", "Drone engineering project", "AERIAL ROBOTICS", BLUE, ill_quad),
    "agv": ("AGV prototype", "Automated guided vehicle prototype", "AUTONOMOUS SYSTEMS", VIOLET, ill_agv),
    "cosmo-cleanse-bot": ("Cosmo Cleanse Bot", "Robotics project", "ROBOTICS", CYAN, ill_cosmo),
    "rc-car": ("RC car", "Remote-controlled vehicle", "ELECTRONICS · ROBOTICS", GOLD, ill_rc),
    "easybee": ("EasyBee prototype", "Engineering prototype", "PROTOTYPE", VIOLET, ill_easybee),
}

def card(key, w):
    title, subtitle, tag, tc, illu = PROJECTS[key]
    s = w / 440; ih = 170 * s; f = .85 if w < 400 else 1; H = round(ih + 100 * f)
    tg, tw = pill(12, 12, tag, tc, 11 if w < 400 else 12, 26)
    b = (f'{stars(w, ih, 14, zlib.crc32(key.encode()) % 99, .6)}<rect width="{w}" height="{ih}" fill="url(#grid)" opacity=".8"/>'
         f'<g transform="translate({22*s:.1f},{26*s:.1f}) scale({s*.88:.3f})">{illu()}</g>'
         f'<rect y="{ih:.0f}" width="{w}" height="1.5" fill="url(#frame)" opacity=".6"/>{tg}'
         f'<text x="18" y="{ih+36*f:.0f}" font-family="{SANS}" font-size="{25*f:.0f}" font-weight="800" fill="{WHITE}">{esc(title)}</text>'
         f'<text x="18" y="{ih+58*f:.0f}" font-family="{SANS}" font-size="{14*f:.0f}" fill="{MUTED}">{esc(subtitle)}</text>'
         f'<text x="{w-16}" y="{H-14}" text-anchor="end" font-family="{MONO}" font-size="{11*f:.0f}" letter-spacing="1.5" fill="{GOLD}" opacity=".85">{STATUS}</text>')
    return svg(w, H, b, f"{title}. {subtitle}.", rounded=18)

def card_wide():
    W, H = 900, 250
    tg, _ = pill(28, 28, "SPACE · FEATURED", ROSE, 12, 28)
    b = (f'{aurora(W,H)}<rect width="{W}" height="{H}" fill="url(#grid)"/>{stars(W,H,40,5)}<g transform="translate(450,38)">{ill_picosat()}</g>{tg}'
         f'<text x="28" y="118" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#gold)">PicoSat</text>'
         f'<text x="30" y="152" font-family="{SANS}" font-size="18" fill="{WHITE}">Satellite project</text>'
         f'<text x="30" y="178" font-family="{SANS}" font-size="15" fill="{MUTED}">The bridge between my robotics background</text>'
         f'<text x="30" y="198" font-family="{SANS}" font-size="15" fill="{MUTED}">and my M.Sc. direction in space technology.</text>'
         f'<text x="30" y="228" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{GOLD}">{STATUS}</text>')
    return svg(W, H, b, "PicoSat. Satellite project, the bridge between robotics and space technology.", rounded=20)

# ------------------------------------------------------------------ skills orbit
def skills():
    W, H, cx, cy = 900, 520, 225, 258
    b = [aurora(W, H), f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', stars(W, H, 40, 21)]
    radii = [62, 112, 162, 212]; durs = [16, 26, 38, 52]
    for i, ((t, sub, c, txt), r) in enumerate(zip(SKILL_TIERS, radii)):
        dash = 'stroke-dasharray="4 7"' if i == 3 else ""
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity=".55" stroke-width="1.5" {dash}/>')
        n = len(txt.split(" · ")) if i != 0 else 4
        n = min(n, 5)
        for k in range(n):
            ph = k * 360 / n + i * 40
            sgn = [0, 360] if i % 2 == 0 else [360, 0]
            b.append(f'<g transform="rotate({ph:.0f} {cx} {cy})"><g>{rot(sgn, durs[i], cx, cy)}<circle cx="{cx+r}" cy="{cy}" r="{5 if i==0 else 4.2}" fill="{c}" filter="url(#glow)"/></g></g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="url(#gold)" filter="url(#glow)"/><circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{GOLD}">{an("r",[34,48],3)}{an("opacity",[.8,0],3)}</circle>')
    b.append(f'<text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="26" fill="{NAVY}">NM</text>')
    y = 62
    for t, sub, c, txt in SKILL_TIERS:
        b.append(f'<circle cx="480" cy="{y-5}" r="6" fill="{c}"/><text x="496" y="{y}" font-family="{SANS}" font-size="19" font-weight="800" fill="{WHITE}">{esc(t)}</text>'
                 f'<text x="496" y="{y+19}" font-family="{MONO}" font-size="12" letter-spacing=".5" fill="{c}">{esc(sub)}</text>')
        lines = textwrap.wrap(txt, 46)
        for k, ln in enumerate(lines):
            b.append(f'<text x="496" y="{y+42+k*19}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{esc(ln)}</text>')
        y += 44 + len(lines) * 19 + 24
    b.append(f'<text x="{cx}" y="{H-12}" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}" opacity=".8">closer to the centre = more hands-on experience</text>')
    alt = "Skill orbit, from most to least hands-on experience. " + " ".join(f"{t}: {x}." for t, _, _, x in SKILL_TIERS)
    return svg(W, H, "".join(b), alt)

# ------------------------------------------------------------------ industrial
def industrial():
    W, H = 900, 390
    b = [aurora(W, H), f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', stars(W, H, 30, 31)]
    b.append(f'<g transform="translate(0,44)"><rect x="20" y="288" width="330" height="3" fill="{CYAN}" opacity=".4"/><rect x="110" y="268" width="90" height="22" rx="4" fill="#1B2A9E" stroke="{CYAN}" stroke-opacity=".7"/><rect x="132" y="244" width="46" height="26" fill="#101A5C" stroke="{CYAN}" stroke-opacity=".6"/>')
    b.append(f'<g transform="translate(155,244)"><g>{rot([-24,-6,-24],7,smooth=True)}{link(100,20,"#C98A1B")}'
             f'<g transform="translate(0,-100)"><g>{rot([78,112,78],7,smooth=True)}{link(88,17,"#E3A92B")}'
             f'<g transform="translate(0,-88)"><g>{rot([-35,5,-35],7,smooth=True)}{link(32,12,"#F5C451")}<rect x="-12" y="-44" width="24" height="8" rx="2" fill="{WHITE}"/>'
             f'<rect x="-12" y="-58" width="5" height="16" fill="{WHITE}">{an("x",[-12,-8,-12],2.4)}</rect><rect x="7" y="-58" width="5" height="16" fill="{WHITE}">{an("x",[7,3,7],2.4)}</rect></g></g>'
             f'<circle r="9" fill="{NAVY}" stroke="{GOLD}" stroke-width="2.5"/></g></g><circle r="12" fill="{NAVY}" stroke="{GOLD}" stroke-width="2.5"/></g></g></g>')
    b.append(f'<circle cx="430" cy="52" r="5" fill="{GOLD}">{an("opacity",[1,.3,1],2)}</circle><text x="446" y="57" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{GOLD}">TRAINING · HANDS-ON EXPOSURE</text>')
    b.append(f'<text x="410" y="104" font-family="{SANS}" font-size="30" font-weight="800" fill="{WHITE}">DIFACTO</text><text x="410" y="132" font-family="{SANS}" font-size="17" fill="{WHITE}">Robotics and Automation · Bangalore, India</text>'
             f'<text x="410" y="156" font-family="{SANS}" font-size="14" fill="{MUTED}">Industrial robotics and automation training</text>')
    chips = [("FANUC", GOLD), ("ABB", CYAN), ("Teach pendant", ROSE), ("Robot operation & control", VIOLET), ("Industrial robotic arms", BLUE), ("Automation", GOLD), ("Pneumatics", CYAN), ("PLC fundamentals", ROSE)]
    x, y = 410, 190
    for t, c in chips:
        w = len(t) * 8.3 + 34
        if x + w > 870: x, y = 410, y + 40
        p, w = pill(x, y, t, c, 14, 30); b.append(p); x += w + 10
    return svg(W, H, "".join(b), "Industrial robotics training at DIFACTO Robotics and Automation, Bangalore: FANUC and ABB robots, teach pendant, automation, pneumatics, PLC fundamentals.")

# ------------------------------------------------------------------ international
def international():
    W, H = 900, 420
    lon0, lon1, lat0, lat1, mx, my, mw, mh = -120, 160, -45, 75, 30, 40, 560, 300
    P = lambda lo, la: (mx + (lo - lon0) / (lon1 - lon0) * mw, my + (lat1 - la) / (lat1 - lat0) * mh)
    ex = f'<pattern id="dots" x="{mx}" y="{my}" width="{mw/28:.2f}" height="{mh/12:.2f}" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1.1" fill="{LINK}" fill-opacity=".35"/></pattern>'
    b = [aurora(W, H), stars(W, H, 24, 41), f'<rect x="20" y="24" width="580" height="340" rx="14" fill="{NAVY}" fill-opacity=".6" stroke="{LINK}" stroke-opacity=".3"/><rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="url(#dots)"/>']
    ax, ay = P(-75, 5); ex_, ey = P(15, 55)
    b.append(f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="72" ry="128" fill="{VIOLET}" fill-opacity=".14" stroke="{VIOLET}" stroke-dasharray="4 5"><animate attributeName="stroke-opacity" values=".4;1;.4" dur="4s" repeatCount="indefinite"/></ellipse><text x="{ax:.0f}" y="{ay:.0f}" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="2" fill="#C4B5FD">THE AMERICAS</text>')
    b.append(f'<ellipse cx="{ex_:.0f}" cy="{ey:.0f}" rx="66" ry="36" fill="{VIOLET}" fill-opacity=".14" stroke="{VIOLET}" stroke-dasharray="4 5"><animate attributeName="stroke-opacity" values=".4;1;.4" dur="4s" begin="-2s" repeatCount="indefinite"/></ellipse><text x="{ex_:.0f}" y="{ey-42:.0f}" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="2" fill="#C4B5FD">EUROPE</text>')
    de = P(10, 51)
    places = [("Norway", 8, 61, "end", -10, -4), ("Finland", 25, 62, "start", 10, -4), ("India", 78, 21, "start", 12, 4), ("Ethiopia", 40, 9, "end", -12, 4), ("Australia", 134, -25, "end", -12, 4)]
    for i, (n, lo, la, anc, dx, dy) in enumerate(places):
        x, y = P(lo, la); dist = math.dist((x, y), de); lift = .28 * dist
        d = f"M{de[0]:.0f},{de[1]:.0f} Q{(x+de[0])/2:.0f},{(y+de[1])/2-lift:.0f} {x:.0f},{y:.0f}"
        b.append(f'<path d="{d}" fill="none" stroke="url(#sub)" stroke-width="1.6" stroke-dasharray="5 6" stroke-opacity=".9">{an("stroke-dashoffset",[0,-22],1.5)}</path>')
        b.append(f'<circle r="2.6" fill="{WHITE}" filter="url(#glow)"><animateMotion dur="{4+i*.7:.1f}s" begin="-{i}s" repeatCount="indefinite" path="{d}"/></circle>')
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="none" stroke="{GOLD}">{an("r",[4,17],2.6,-i*.5)}{an("opacity",[.9,0],2.6,-i*.5)}</circle><circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="{GOLD}"/>')
        b.append(f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{anc}" font-family="{SANS}" font-size="13" font-weight="600" fill="{WHITE}">{n}</text>')
    b.append(f'<circle cx="{de[0]:.0f}" cy="{de[1]:.0f}" r="7" fill="{CYAN}" filter="url(#glow)"/><text x="{de[0]-12:.0f}" y="{de[1]+5:.0f}" text-anchor="end" font-family="{SANS}" font-size="13" font-weight="700" fill="{WHITE}">Germany</text>')
    b.append(f'<circle cx="40" cy="388" r="5" fill="none" stroke="{VIOLET}" stroke-dasharray="2 2"/><text x="52" y="392" font-family="{MONO}" font-size="12" fill="{MUTED}">audit scope (ICB)</text><circle cx="200" cy="388" r="4" fill="{GOLD}"/><text x="212" y="392" font-family="{MONO}" font-size="12" fill="{MUTED}">teams and responsibilities I worked with</text>')
    b.append(f'<text x="640" y="62" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{GOLD}">AIESEC · ICB</text>')
    b.append(f'<text x="636" y="140" font-family="{SANS}" font-size="78" font-weight="800" fill="url(#gold)">≈70</text>')
    b.append(f'<text x="640" y="170" font-family="{SANS}" font-size="16" font-weight="700" fill="{WHITE}">countries in audit scope</text><text x="640" y="192" font-family="{SANS}" font-size="15" fill="{CYAN}">Europe and the Americas</text>')
    b.append(f'<line x1="640" y1="214" x2="860" y2="214" stroke="url(#frame)"/>')
    for k, ln in enumerate(["International Control", "Board Auditor"]):
        b.append(f'<text x="640" y="{244+k*22}" font-family="{SANS}" font-size="18" font-weight="800" fill="{WHITE}">{ln}</text>')
    for k, ln in enumerate(["Governance · audit", "compliance · accountability", "cross-cultural teamwork"]):
        b.append(f'<text x="640" y="{298+k*20}" font-family="{SANS}" font-size="14" fill="{MUTED}">{ln}</text>')
    return svg(W, H, "".join(b), "International experience: International Control Board auditor with an audit scope of about 70 countries in Europe and the Americas, and work connected to India, Australia, Ethiopia, Norway, Finland and Germany.", ex)

# ------------------------------------------------------------------ roadmap
def roadmap():
    W, H, y = 900, 270, 112
    b = [aurora(W, H), f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', stars(W, H, 36, 51)]
    xs = [80 + i * 148 for i in range(len(ROADMAP))]
    b.append(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{LINK}" stroke-opacity=".35" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>')
    b.append(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[1]}" y2="{y}" stroke="url(#sub)" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'<circle cy="{y}" r="5" fill="{WHITE}" filter="url(#glow)"><animateMotion dur="3.4s" repeatCount="indefinite" path="M{xs[0]},0 L{xs[1]},0"/></circle>')
    for i, ((l1, l2, st), x) in enumerate(zip(ROADMAP, xs)):
        c = GOLD if st == "active" else (CYAN if st == "done" else LINK)
        b.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{NAVY}" stroke="{c}" stroke-width="{3 if st!="planned" else 2}"/>')
        if st == "active": b.append(f'<circle cx="{x}" cy="{y}" r="17" fill="none" stroke="{GOLD}" stroke-width="2">{an("r",[17,34],2.4)}{an("opacity",[.9,0],2.4)}</circle><circle cx="{x}" cy="{y}" r="7" fill="{GOLD}"/>')
        else: b.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{c}">{i+1:02d}</text>')
        b.append(f'<text x="{x}" y="{y+58}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="{WHITE}">{esc(l1)}</text><text x="{x}" y="{y+78}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{MUTED}">{esc(l2)}</text>')
        lab = {"active": "IN PROGRESS", "planned": "PLANNED", "done": "DONE"}[st]
        b.append(f'<text x="{x}" y="{y-34}" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{c}">{lab}</text>')
    return svg(W, H, "".join(b), "Roadmap: " + ", ".join(f"{a} {b_}" for a, b_, _ in ROADMAP) + ".")

# ------------------------------------------------------------------ small pieces
def divider():
    W = 900
    ex = f'<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>'
    b = (f'<rect y="11" width="{W}" height="2" fill="url(#fade)"/><rect x="438" y="3" width="18" height="18" fill="none" stroke="{GOLD}" stroke-width="2" transform="rotate(45 447 12)"/>'
         f'<rect x="443" y="8" width="8" height="8" fill="{GOLD}" transform="rotate(45 447 12)">{an("opacity",[1,.3,1],2.4)}</rect>'
         f'<circle cy="12" r="3" fill="{WHITE}" filter="url(#glow)">{an("cx",[0,W],7)}</circle>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 24" width="{W}" height="24" role="presentation">{defs(ex)}{b}</svg>'

def footer():
    W, H = 900, 250
    wv = lambda y, a: f"M0,{y} Q112.5,{y+a} 225,{y} T450,{y} T675,{y} T900,{y} V{H} H0 Z"
    b = [aurora(W, H), f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', stars(W, H, 60, 61)]
    b.append(f'<g><animateMotion dur="20s" repeatCount="indefinite" path="M-30,70 Q450,-10 930,70"/>{sat(1.3)}</g>')
    for y, a, c, o, d in [(176, 26, BLUE, .35, 7), (192, -22, VIOLET, .4, 9), (210, 18, ROSE, .35, 11)]:
        b.append(f'<path d="{wv(y,a)}" fill="{c}" opacity="{o}"><animate attributeName="d" values="{wv(y,a)};{wv(y,-a)};{wv(y,a)}" dur="{d}s" repeatCount="indefinite"/></path>')
    b.append(f'<text x="450" y="104" text-anchor="middle" font-family="{SANS}" font-size="29" font-weight="800" fill="{WHITE}">Learn → Build → Break → Understand → Build Better</text>')
    b.append(f'<text x="450" y="138" text-anchor="middle" font-family="{SANS}" font-size="16" letter-spacing="3" fill="url(#gold)">NARESH MURTHY · ROBOTICS → SPACE SYSTEMS</text>')
    return svg(W, H, "".join(b), "Learn, build, break, understand, build better. Naresh Murthy, Robotics to Space Systems.", rounded=20)

def navpill(label):
    w = round(len(label) * 8.8 + 40); h = 38
    b = f'<circle cx="18" cy="19" r="3.5" fill="{GOLD}">{an("opacity",[1,.3,1],2.2)}</circle><text x="30" y="24.5" font-family="{SANS}" font-size="14.5" font-weight="700" letter-spacing=".4" fill="{WHITE}">{esc(label)}</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">{defs()}<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{h/2-.75}" fill="url(#royal)" fill-opacity=".55" stroke="url(#frame)" stroke-width="1.5"/>{b}</svg>'

def button(label, glyph, c):
    w, h = 176, 52
    b = (f'<rect width="{w}" height="{h}" fill="{NAVY}"/><circle cx="29" cy="26" r="16" fill="{c}"/><text x="29" y="31.5" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="800" fill="{NAVY}">{esc(glyph)}</text>'
         f'<text x="55" y="31" font-family="{SANS}" font-size="17" font-weight="700" fill="{WHITE}">{label}</text><rect y="{h-3}" width="70" height="3" fill="{c}">{an("x",[-70,w],3)}</rect>')
    return svg(w, h, b, label, rounded=26)

# ------------------------------------------------------------------ build
if __name__ == "__main__":
    write("hero.svg", hero()); write("divider.svg", divider()); write("footer.svg", footer())
    write("identity.svg", identity()); write("journey.svg", journey()); write("skills.svg", skills())
    write("industrial.svg", industrial()); write("international.svg", international()); write("roadmap.svg", roadmap())
    for k, t, s, c1, c2 in [("mission", "Mission", "what I'm building toward", BLUE, VIOLET), ("journey", "Engineering journey", "from school to space systems", CYAN, BLUE),
                            ("projects", "Featured projects", "what I built · why · with what", GOLD, ROSE), ("skills", "Technical profile", "honest tiers, no percentages", VIOLET, CYAN),
                            ("industrial", "Industrial robotics", "FANUC · ABB · DIFACTO training", GOLD, "#FFE9A8"), ("international", "International experience", "AIESEC · International Control Board", ROSE, VIOLET),
                            ("foundations", "Software foundations", "100 days of Python, on purpose", CYAN, VIOLET), ("roadmap", "Roadmap", "next milestones", GOLD, ROSE), ("contact", "Contact", "open to conversations", CYAN, GOLD)]:
        write(f"banners/{k}.svg", banner(k, t, s, c1, c2))
    write("projects/picosat.svg", card_wide())
    for k in PROJECTS:
        if k != "picosat": write(f"projects/{k}.svg", card(k, 440 if k in ("robotic-arm", "pick-and-place", "quadcopter", "agv") else 288))
    for k, l in [("projects", "Projects"), ("skills", "Skills"), ("journey", "Journey"), ("international", "International"), ("roadmap", "Roadmap"), ("contact", "Contact")]:
        write(f"nav/{k}.svg", navpill(l))
    for k, l, g, c in [("github", "GitHub", "{}", GOLD), ("linkedin", "LinkedIn", "in", CYAN), ("email", "Email", "@", ROSE)]:
        write(f"buttons/{k}.svg", button(l, g, c))
    print("assets written to", A)
