#!/usr/bin/env python3
"""Builds the animated SVGs in ../assets. Needs: pip install chess"""
import os
import chess
from html import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SANS = "'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
SYM = "'Segoe UI Symbol','Apple Symbols','Noto Sans Symbols 2','DejaVu Sans','Arial Unicode MS',sans-serif"

BORDER = '''<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#2dd4bf"/>
<animateTransform attributeName="gradientTransform" type="rotate" from="0 .5 .5" to="360 .5 .5" dur="12s" repeatCount="indefinite"/></linearGradient>'''


def write(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)
    print(name, len(s) // 1024, "KB")


# ---------------------------------------------------------------- keyframe helper
def kf(points, D, init, final=None, ease=True):
    """points: [(t_seconds, value)] -> (keyTimes, values, keySplines) over duration D."""
    final = init if final is None else final
    pts = sorted(points, key=lambda p: p[0])
    if not pts or pts[0][0] > 0:
        pts.insert(0, (0.0, init))
    pts.append((D, final))
    fixed, last = [], -1
    for t, v in pts:
        t = max(t, last + 0.001) if fixed else 0.0
        t = min(t, D)
        fixed.append((t, v))
        last = t
    fixed[-1] = (D, fixed[-1][1])
    kt = ";".join(f"{t / D:.5f}" for t, _ in fixed)
    vals = ";".join(str(v) for _, v in fixed)
    spl = ";".join(("0.45 0 0.2 1" if (ease and fixed[i][1] != fixed[i + 1][1]) else "0 0 1 1")
                   for i in range(len(fixed) - 1))
    return kt, vals, spl


def anim(attr, pts, D, init, final=None, tag="animate", extra="", ease=True):
    kt, vals, spl = kf(pts, D, init, final, ease)
    return (f'<{tag} attributeName="{attr}" {extra} values="{vals}" keyTimes="{kt}" '
            f'calcMode="spline" keySplines="{spl}" dur="{D}s" repeatCount="indefinite"/>')


# ================================================================== BANNER
def banner():
    W, H = 900, 240
    lines = ["Building AI that ships, one hackathon at a time.",
             "Team lead @ BinaryV2  |  AI models + LLMs",
             "AgroNova: smart farming for Indian farmers.",
             "B.Tech CSE @ Kalvium  |  NSS volunteer",
             "Next: a top product company. Then my own."]
    P, T = 4.4, 4.4 * len(lines)
    CW = 10.2  # mono char width at 17px (forced with textLength)
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Jagadish Naik banner">
<defs>{BORDER}
<filter id="blur"><feGaussianBlur stdDeviation="38"/></filter>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#99f6e4"/><stop offset="1" stop-color="#fff"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<clipPath id="card"><rect x="8" y="8" width="{W-16}" height="{H-16}" rx="24"/></clipPath>''']
    for i in range(len(lines)):
        out.append(f'<clipPath id="c{i}"><rect x="188" y="124" width="0" height="30">'
                   + anim("width", [(i * P, 0), (i * P + 1.9, len(lines[i]) * CW), ((i + 1) * P - 0.45, len(lines[i]) * CW), ((i + 1) * P - 0.3, 0)], T, 0, ease=False)
                   + '</rect></clipPath>')
    out.append('</defs>')
    out.append(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" rx="24" fill="#0b1214"/>')
    out.append('<g clip-path="url(#card)">'
               '<circle cx="180" cy="40" r="110" fill="#7c3aed" opacity=".35" filter="url(#blur)"><animate attributeName="cx" values="180;300;180" dur="9s" repeatCount="indefinite"/></circle>'
               '<circle cx="760" cy="210" r="120" fill="#14b8a6" opacity=".35" filter="url(#blur)"><animate attributeName="cx" values="760;640;760" dur="11s" repeatCount="indefinite"/></circle>'
               '<circle cx="450" cy="250" r="90" fill="#3b82f6" opacity=".22" filter="url(#blur)"><animate attributeName="cy" values="250;200;250" dur="7s" repeatCount="indefinite"/></circle></g>')
    out.append(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" rx="24" fill="none" stroke="url(#bd)" stroke-width="1.8"/>')
    # avatar monogram
    out.append('''<g transform="translate(104 110)">
<circle r="58" fill="none" stroke="#2dd4bf" stroke-opacity=".25" stroke-width="3"/>
<circle r="58" fill="none" stroke="url(#bd)" stroke-width="4" stroke-linecap="round" stroke-dasharray="110 260"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="5s" repeatCount="indefinite"/></circle>
<circle r="46" fill="#10201f"/>
<text y="14" text-anchor="middle" font-family="%s" font-size="40" font-weight="800" fill="#99f6e4">JN</text>
<circle cx="41" cy="-41" r="6" fill="#22c55e"><animate attributeName="r" values="6;8;6" dur="2s" repeatCount="indefinite"/></circle></g>''' % SANS)
    out.append(f'<text x="188" y="52" font-family="{MONO}" font-size="14" letter-spacing="4" fill="#7fb8b0" opacity="0">@jagadish-s-naik<animate attributeName="opacity" from="0" to="1" begin=".2s" dur=".6s" fill="freeze"/></text>')
    out.append(f'<text x="188" y="108" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#nm)" opacity="0">Jagadish Naik'
               '<animate attributeName="opacity" from="0" to="1" begin=".35s" dur=".8s" fill="freeze"/>'
               '<animate attributeName="y" from="124" to="108" begin=".35s" dur=".8s" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1" fill="freeze"/></text>')
    # typewriter lines
    for i, ln in enumerate(lines):
        w = len(ln) * CW
        out.append(f'<text x="188" y="145" clip-path="url(#c{i})" font-family="{MONO}" font-size="17" fill="#9ddfd6" textLength="{w:.1f}" lengthAdjust="spacing">{escape(ln)}</text>')
        out.append(f'<rect y="128" width="2" height="22" fill="#5eead4" opacity="0">'
                   + anim("x", [(i * P, 188), (i * P + 1.9, 188 + w), ((i + 1) * P - 0.45, 188 + w), ((i + 1) * P - 0.3, 188)], T, 188, ease=False)
                   + anim("opacity", [(i * P, 0), (i * P + 0.01, 1), ((i + 1) * P - 0.3, 1), ((i + 1) * P - 0.29, 0)], T, 0, ease=False)
                   + '</rect>')
    # pills
    x = 188
    for k, (lab, wd) in enumerate([("Jupyter Notebook", 152), ("Python", 84), ("TypeScript", 108), ("HTML", 70), ("LLMs", 70)]):
        out.append(f'<g><rect x="{x}" y="176" width="{wd}" height="32" rx="16" fill="#0f1f20" stroke="#2dd4bf" stroke-opacity=".6">'
                   f'<animate attributeName="stroke-opacity" values=".25;.95;.25" dur="3.5s" begin="{k*0.5}s" repeatCount="indefinite"/></rect>'
                   f'<text x="{x+wd/2}" y="197" text-anchor="middle" font-family="{SANS}" font-size="13.5" font-weight="700" fill="#e2f5f2">{lab}</text></g>')
        x += wd + 12
    out.append(f'''<g transform="translate(790 98)" text-anchor="middle">
<text font-family="{SANS}" font-size="52" font-weight="800" fill="#a78bfa">10+<animate attributeName="opacity" values="1;.65;1" dur="3s" repeatCount="indefinite"/></text>
<text y="28" font-family="{MONO}" font-size="11" letter-spacing="3" fill="#8fb3ae">HACKATHONS</text></g>''')
    out.append('</svg>')
    write("banner.svg", "\n".join(out))


# ================================================================== NAME (dot matrix)
FONT = {
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
}


def name_svg():
    word = "JAGADISH"
    cell, r = 16, 5.6
    cols = len(word) * 6 - 1
    mw = cols * cell
    W, H = 860, 300
    ox, oy = (W - mw) // 2 + cell // 2, 112
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="JAGADISH animated wordmark">
<defs>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#99f6e4" stop-opacity=".30"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="prompt"><rect x="30" y="44" width="0" height="22">{anim("width", [(0.3, 0), (2.0, 400)], 40, 0, final=400, ease=False)}</rect></clipPath>
<clipPath id="mx"><rect x="{ox-12}" y="{oy-12}" width="{mw+8}" height="{7*cell+8}"/></clipPath>
</defs>
<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="14" fill="#0b1214" stroke="#1d3a3a"/>
<rect x="4" y="4" width="{W-8}" height="32" rx="14" fill="#101c1e"/><rect x="4" y="22" width="{W-8}" height="14" fill="#101c1e"/>
<circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>
<text x="{W/2}" y="24" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#6b8f8a">jagadish-s-naik@github: ~ $ ./wordmark.sh --name</text>
<text x="30" y="62" font-family="{MONO}" font-size="14" clip-path="url(#prompt)"><tspan fill="#2dd4bf">jagadish-s-naik@github</tspan><tspan fill="#8fb3ae">:~$ </tspan><tspan fill="#e2f5f2">./wordmark.sh --name</tspan></text>''']
    # faint grid
    for c in range(cols):
        for rr in range(7):
            out.append(f'<circle cx="{ox+c*cell}" cy="{oy+rr*cell}" r="1.8" fill="#2dd4bf" opacity=".12"/>')
    for li, ch in enumerate(word):
        for rr, row in enumerate(FONT[ch]):
            for cc, bit in enumerate(row):
                if bit != "1":
                    continue
                col = li * 6 + cc
                cx, cy = ox + col * cell, oy + rr * cell
                reveal = 2.4 + col * 0.045 + rr * 0.01
                wave = 5.2 + col * 0.06
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#5eead4" opacity="0">'
                           f'<animate attributeName="opacity" from="0" to="1" begin="{reveal:.2f}s" dur=".25s" fill="freeze"/>'
                           f'<animate attributeName="r" values="{r};{r+2.2};{r}" dur="3.2s" begin="{wave:.2f}s" repeatCount="indefinite"/>'
                           f'<animate attributeName="fill" values="#5eead4;#a78bfa;#60a5fa;#5eead4" dur="3.2s" begin="{wave:.2f}s" repeatCount="indefinite"/></circle>')
    out.append(f'<g clip-path="url(#mx)"><rect x="{ox-60}" y="{oy-14}" width="70" height="{7*cell+10}" fill="url(#sweep)">'
               f'<animate attributeName="x" values="{ox-60};{ox+mw}" dur="3.2s" begin="5.2s" repeatCount="indefinite"/></rect></g>')
    out.append(f'<text x="30" y="{H-24}" font-family="{MONO}" font-size="12" fill="#4f7f79">[ok] wordmark rendered<tspan fill="#2dd4bf"> &#9608;<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>')
    out.append(f'<text x="{W-30}" y="{H-24}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#4f7f79">AI &#183; agri-tech &#183; social impact</text>')
    out.append('</svg>')
    write("name.svg", "\n".join(out))


# ================================================================== CHESS
GAME = ("e4 e5 Nf3 d6 d4 Bg4 dxe5 Bxf3 Qxf3 dxe5 Bc4 Nf6 Qb3 Qe7 Nc3 c6 Bg5 b5 Nxb5 cxb5 Bxb5+ Nbd7 "
        "O-O-O Rd8 Rxd7 Rxd7 Rd1 Qe6 Bxd7+ Nxd7 Qb8+ Nxb8 Rd8#").split()
GLYPH = {"P": "\u265f\ufe0e", "N": "\u265e", "B": "\u265d", "R": "\u265c", "Q": "\u265b", "K": "\u265a"}


def chess_svg():
    S, BX, BY = 60, 80, 96
    W, H = 640, 690
    START, SLOT, MOVE = 1.8, 1.25, 0.7
    D = round(START + len(GAME) * SLOT + 4.2, 2)
    TR = D - 2.0                      # reset instant (board is invisible then)

    def cx(sq):
        return BX + chess.square_file(sq) * S + S / 2

    def cy(sq):
        return BY + (7 - chess.square_rank(sq)) * S + S / 2

    board = chess.Board()
    pieces, at = {}, {}
    for sq, p in board.piece_map().items():
        pid = f"p{sq}"
        pieces[pid] = {"type": p.symbol().upper(), "white": p.color, "sq": sq, "path": [], "cap": None}
        at[sq] = pid
    ticks, highs = [], []

    for i, san in enumerate(GAME):
        mv = board.parse_san(san)
        tS = START + i * SLOT
        tE = tS + MOVE
        white = board.turn
        num = i // 2 + 1
        moves = [(mv.from_square, mv.to_square)]
        if board.is_castling(mv):
            rank = chess.square_rank(mv.from_square)
            if chess.square_file(mv.to_square) == 2:
                moves.append((chess.square(0, rank), chess.square(3, rank)))
            else:
                moves.append((chess.square(7, rank), chess.square(5, rank)))
        if board.is_capture(mv) and not board.is_en_passant(mv):
            pieces[at[mv.to_square]]["cap"] = tE
            del at[mv.to_square]
        for fr, to in moves:
            pid = at.pop(fr)
            at[to] = pid
            pieces[pid]["path"].append((tS, tE, fr, to))
            pieces[pid]["sq"] = to
        highs.append((tS, tE, mv.from_square, mv.to_square, i == len(GAME) - 1, san.endswith("#")))
        ticks.append((tS, f"{num}{'.' if white else '...'} {san}", i == len(GAME) - 1))
        board.push(mv)

    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated chess game: The Opera Game, Morphy 1858">
<defs>{BORDER}
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="pg"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="22" fill="#0b1214"/>
<text x="{W/2}" y="40" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="800" fill="#e8fffb">Play the next move</text>
<text x="{W/2}" y="62" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="2" fill="#5eead4">THE OPERA GAME &#183; PARIS 1858 &#183; LIVE REPLAY</text>
<rect x="{BX-14}" y="{BY-14}" width="{8*S+28}" height="{8*S+28}" rx="22" fill="#14b8a6" opacity=".35" filter="url(#glow)"><animate attributeName="opacity" values=".25;.5;.25" dur="4s" repeatCount="indefinite"/></rect>
<rect x="{BX-12}" y="{BY-12}" width="{8*S+24}" height="{8*S+24}" rx="20" fill="#0d2d2f" stroke="url(#bd)" stroke-width="2"/>''']
    for r in range(8):
        for f in range(8):
            light = (r + f) % 2 == 0
            out.append(f'<rect x="{BX+f*S}" y="{BY+r*S}" width="{S}" height="{S}" fill="{"#1c7a70" if light else "#07504f"}"/>')
    for f in range(8):
        out.append(f'<text x="{BX+f*S+S/2}" y="{BY+8*S+26}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="#5eead4">{"abcdefgh"[f]}</text>')
    for r in range(8):
        out.append(f'<text x="{BX-26}" y="{BY+r*S+S/2+4}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="#5eead4">{8-r}</text>')

    out.append(f'<g>{anim("opacity", [(D-3.0, 1), (D-2.4, 0), (D-1.2, 0)], D, 1, ease=False)}')
    # last-move highlights
    for tS, tE, fr, to, last, mate in highs:
        for sq, a in ((fr, .22), (to, .5)):
            col = "#f43f5e" if (mate and sq == to) else "#5eead4"
            pts = [(tS, 0), (tE, a)] + ([] if last else [(tS + SLOT, a), (tS + SLOT + 0.5, 0)]) + [(TR, 0)]
            out.append(f'<rect x="{BX+chess.square_file(sq)*S}" y="{BY+(7-chess.square_rank(sq))*S}" width="{S}" height="{S}" fill="{col}" opacity="0">'
                       + anim("opacity", pts, D, 0, ease=False) + '</rect>')
    # king check pulse on e8 at the end
    last_t = START + (len(GAME) - 1) * SLOT + MOVE
    out.append(f'<rect x="{BX+4*S}" y="{BY}" width="{S}" height="{S}" fill="none" stroke="#f43f5e" stroke-width="3" opacity="0">'
               + anim("opacity", [(last_t, 0), (last_t + 0.2, 1), (last_t + 0.6, .2), (last_t + 1.0, 1), (last_t + 1.4, .2), (TR - 0.2, 1), (TR, 0)], D, 0, ease=False) + '</rect>')
    # pieces
    for pid, p in pieces.items():
        start = int(pid[1:])
        x, y = cx(start), cy(start)
        pts, cur = [], (0, 0)
        for tS, tE, fr, to in p["path"]:
            new = (cx(to) - x, cy(to) - y)
            pts += [(tS, f"{cur[0]:g} {cur[1]:g}"), (tE, f"{new[0]:g} {new[1]:g}")]
            cur = new
        pts += [(TR, f"{cur[0]:g} {cur[1]:g}"), (TR + 0.1, "0 0")]
        fill, stroke = ("#c9fff6", "#2dd4bf") if p["white"] else ("#2a1a63", "#a78bfa")
        body = f'<text x="{x}" y="{y+16}" text-anchor="middle" font-family="{SYM}" font-size="50" fill="{fill}" stroke="{stroke}" stroke-width="1.6" filter="url(#pg)">{GLYPH[p["type"]]}'
        if p["path"]:
            body += anim("transform", pts, D, "0 0", tag="animateTransform", extra='type="translate"')
        if p["cap"]:
            body += anim("opacity", [(p["cap"] - 0.05, 1), (p["cap"] + 0.25, 0), (TR, 0), (TR + 0.1, 1)], D, 1, ease=False)
        out.append(body + "</text>")
    out.append("</g>")
    # labels + ticker
    out.append(f'<text x="{BX-12}" y="{BY-22}" font-family="{MONO}" font-size="12" fill="#a78bfa">&#9818; Black: Duke of Brunswick &amp; Count Isouard</text>')
    out.append(f'<text x="{BX-12}" y="{BY+8*S+52}" font-family="{MONO}" font-size="12" fill="#99f6e4">&#9812; White: Paul Morphy</text>')
    out.append(f'<text x="{BX+8*S+12}" y="{BY+8*S+52}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#4f7f79">looping replay</text>')
    for t, txt, last in ticks:
        pts = [(t - 0.01, 0), (t, 1)] + ([(TR - 0.3, 1), (TR, 0)] if last else [(t + SLOT - 0.01, 1), (t + SLOT, 0)])
        out.append(f'<text x="{W/2}" y="{H-24}" text-anchor="middle" font-family="{MONO}" font-size="19" font-weight="700" fill="#e8fffb" opacity="0">{escape(txt)}'
                   + anim("opacity", pts, D, 0, ease=False) + '</text>')
    out.append("</svg>")
    write("chess.svg", "\n".join(out))


# ================================================================== PODIUM
def podium():
    W, H = 900, 250
    cards = [("2ND PRIZE", "Build for Billions", "OpenVyapar | Reinvent DPI", "#c0c8d4"),
             ("RUNNER-UP", "Srinathon 2.0", "International hackathon", "#5eead4"),
             ("2ND PRIZE", "NSD Science Day", "Hackathon", "#a78bfa"),
             ("2ND RUNNER-UP", "Hackwise 2.0", "Hackathon", "#fbbf24")]
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hackathon podium finishes">
<defs>{BORDER}<filter id="g"><feGaussianBlur stdDeviation="14"/></filter></defs>
<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="20" fill="#0b1214" stroke="url(#bd)" stroke-width="1.6"/>
<text x="34" y="42" font-family="{MONO}" font-size="13" letter-spacing="3" fill="#2dd4bf">&gt; podium.list --team BinaryV2</text>''']
    for i, (rank, ev, sub, col) in enumerate(cards):
        x, b = 34 + i * 208, 0.25 * i
        out.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b}s" dur=".6s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="0 30" to="0 0" begin="{b}s" dur=".6s" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1" fill="freeze"/>
<circle cx="{x+95}" cy="120" r="46" fill="{col}" opacity=".25" filter="url(#g)"><animate attributeName="opacity" values=".15;.4;.15" dur="3s" begin="{b}s" repeatCount="indefinite"/></circle>
<rect x="{x}" y="62" width="190" height="160" rx="14" fill="#0f1b1d" stroke="{col}" stroke-opacity=".5"/>
<g transform="translate({x+95} 112)"><animateTransform attributeName="transform" type="translate" values="{x+95} 112;{x+95} 106;{x+95} 112" dur="3s" begin="{b}s" repeatCount="indefinite"/>
<circle r="26" fill="none" stroke="{col}" stroke-width="3"/><circle r="19" fill="{col}" opacity=".18"/>
<path d="M-9 -9 H9 V-2 C9 6 3 10 0 10 C-3 10 -9 6 -9 -2 Z" fill="{col}"/><rect x="-5" y="10" width="10" height="4" fill="{col}"/><rect x="-9" y="14" width="18" height="3" rx="1.5" fill="{col}"/></g>
<text x="{x+95}" y="168" text-anchor="middle" font-family="{MONO}" font-size="11.5" letter-spacing="2.5" fill="{col}">{rank}</text>
<text x="{x+95}" y="193" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="#f1f5f9">{escape(ev)}</text>
<text x="{x+95}" y="212" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="#8fb3ae">{escape(sub)}</text></g>''')
    for k in range(14):  # confetti
        cx = 60 + k * 58
        col = ["#5eead4", "#a78bfa", "#fbbf24", "#60a5fa"][k % 4]
        out.append(f'<rect x="{cx}" y="52" width="5" height="5" rx="1" fill="{col}" opacity="0"><animate attributeName="y" values="52;230" dur="{4+k%4}s" begin="{k*0.7}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;.8;0" dur="{4+k%4}s" begin="{k*0.7}s" repeatCount="indefinite"/>'
                   f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} 52" to="360 {cx} 52" dur="3s" begin="{k*0.7}s" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    write("podium.svg", "\n".join(out))


# ================================================================== ORBIT
def orbit():
    W, H = 900, 400
    cx, cy = W / 2, H / 2
    rings = [(80, 22, "#5eead4", ["Python", "LLMs", "RAG"]),
             (130, 34, "#a78bfa", ["TypeScript", "React", "Node.js", "Supabase"]),
             (178, 48, "#60a5fa", ["GCP", "Firebase", "Flutter", "Docker", "scikit-learn"])]
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack in orbit">
<defs><radialGradient id="core"><stop offset="0" stop-color="#5eead4" stop-opacity=".55"/><stop offset="1" stop-color="#5eead4" stop-opacity="0"/></radialGradient></defs>
<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="20" fill="#0b1214" stroke="#1d3a3a"/>
<circle cx="{cx}" cy="{cy}" r="70" fill="url(#core)"><animate attributeName="r" values="60;78;60" dur="4s" repeatCount="indefinite"/></circle>''']
    for ri, (rad, dur, col, items) in enumerate(rings):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{col}" stroke-opacity=".28" stroke-dasharray="3 7"/>')
        direction = (0, 360) if ri % 2 == 0 else (360, 0)
        out.append(f'<g transform="translate({cx} {cy})"><g>'
                   f'<animateTransform attributeName="transform" type="rotate" from="{direction[0]}" to="{direction[1]}" dur="{dur*1.6}s" repeatCount="indefinite"/>')
        n = len(items)
        for k, it in enumerate(items):
            ang = 360 / n * k
            w = 14 + len(it) * 7.6
            out.append(f'<g transform="rotate({ang}) translate({rad} 0)"><g>'
                       f'<animateTransform attributeName="transform" type="rotate" from="{-ang - direction[0]}" to="{-ang - direction[1]}" dur="{dur*1.6}s" repeatCount="indefinite"/>'
                       f'<rect x="{-w/2}" y="-13" width="{w}" height="26" rx="13" fill="#0f1b1d" stroke="{col}"/>'
                       f'<text y="5" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="700" fill="#e8fffb">{escape(it)}</text></g></g>')
        out.append("</g></g>")
    out.append(f'<text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="800" fill="#e8fffb">JN</text>')
    out.append(f'<text x="34" y="46" font-family="{MONO}" font-size="13" letter-spacing="3" fill="#2dd4bf">&gt; stack.orbit</text>')
    out.append(f'<text x="{W-34}" y="{H-26}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#4f7f79">tools chosen for the work, not the trend</text>')
    out.append("</svg>")
    write("orbit.svg", "\n".join(out))


# ================================================================== FOOTER
def footer():
    W, H = 900, 140
    def wave(amp, off):
        d = f"M0 {70+off}"
        for i in range(0, 1801, 150):
            d += f" Q{i+75} {70+off-amp} {i+150} {70+off}" if (i // 150) % 2 == 0 else f" Q{i+75} {70+off+amp} {i+150} {70+off}"
        return d + f" V{H} H0 Z"
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Footer wave">
<defs><clipPath id="f"><rect width="{W}" height="{H}"/></clipPath></defs><g clip-path="url(#f)">
<path d="{wave(18, 6)}" fill="#14b8a6" opacity=".25"><animateTransform attributeName="transform" type="translate" from="0 0" to="-300 0" dur="9s" repeatCount="indefinite"/></path>
<path d="{wave(14, 16)}" fill="#a78bfa" opacity=".25"><animateTransform attributeName="transform" type="translate" from="-300 0" to="0 0" dur="12s" repeatCount="indefinite"/></path>
<path d="{wave(10, 28)}" fill="#0b2a2b"><animateTransform attributeName="transform" type="translate" from="0 0" to="-300 0" dur="6s" repeatCount="indefinite"/></path></g>
<text x="{W/2}" y="92" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" fill="#e8fffb">Keep the story moving.<animate attributeName="opacity" values=".7;1;.7" dur="3s" repeatCount="indefinite"/></text>
<text x="{W/2}" y="118" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="3" fill="#7fb8b0">SHIP &#183; LEARN &#183; REPEAT</text></svg>''']
    write("footer.svg", "\n".join(out))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner(); name_svg(); chess_svg(); podium(); orbit(); footer()
