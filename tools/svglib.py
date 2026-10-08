"""Generate the report's architecture and fund-flow diagrams as SVG.

Run: python3 report/figures/gen.py   (writes *.svg next to this file)

Each diagram is a list of boxes (id, x, y, w, h, label, kind) and arrows
(from, to, label, style). Coordinates are in px on a fixed canvas; the PDF
scales the SVG to the text width.
"""

from pathlib import Path
from xml.sax.saxutils import escape

BASE = Path(__file__).resolve().parent.parent / "outputs" / "figures"
OUT = BASE
LANG = "en"
VI = {}


def T(text):
    """Translate a label line by line when rendering the Vietnamese set."""
    if LANG != "vi" or text is None:
        return text
    return "\n".join(VI.get(line, line) for line in text.split("\n"))


FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK = "#1b2a41"
MUTED = "#5b6b7f"
KINDS = {
    # fill, stroke
    "buy": ("#e6f0f5", "#1f6f8b"),      # purchased / third-party component
    "build": ("#fdf3e3", "#b7791f"),    # Cyclone-built
    "member": ("#eef0f3", "#5b6b7f"),   # Member / external party
    "chain": ("#eaf5ec", "#2f855a"),    # on-chain asset location
    "risk": ("#fbeaea", "#c53030"),     # high-risk / excluded element
    "group": ("none", "#9aa7b6"),       # boundary
}


def box(b):
    _id, x, y, w, h, label, kind = b
    label = T(label)
    fill, stroke = KINDS[kind]
    dash = ' stroke-dasharray="5 4"' if kind == "group" else ""
    rx = 4 if kind != "group" else 8
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"{dash}/>']
    lines = label.split("\n")
    if kind == "group":
        out.append(f'<text x="{x + 8}" y="{y + 15}" font-size="11.5" '
                   f'fill="{MUTED}" font-weight="bold">{escape(lines[0])}</text>')
        return "\n".join(out)
    lh = 14
    y0 = y + h / 2 - (len(lines) - 1) * lh / 2 + 4
    for i, line in enumerate(lines):
        weight = "bold" if i == 0 else "normal"
        size = 12.5 if i == 0 else 10.5
        color = INK if i == 0 else MUTED
        out.append(f'<text x="{x + w / 2}" y="{y0 + i * lh}" font-size="{size}" '
                   f'text-anchor="middle" fill="{color}" font-weight="{weight}">'
                   f'{escape(line)}</text>')
    return "\n".join(out)


def anchor(b, side):
    _id, x, y, w, h, *_ = b
    return {
        "l": (x, y + h / 2), "r": (x + w, y + h / 2),
        "t": (x + w / 2, y), "b": (x + w / 2, y + h),
    }[side]


def arrow(boxes, a):
    src, dst, label, style = (a + (None,))[:4] if len(a) == 3 else a
    s_id, s_side = src.split(".")
    d_id, d_side = dst.split(".")
    x1, y1 = anchor(boxes[s_id], s_side)
    x2, y2 = anchor(boxes[d_id], d_side)
    color = {"money": "#2f855a", "data": "#1f6f8b", "ctrl": "#b7791f",
             "risk": "#c53030"}.get(style or "data")
    dash = ' stroke-dasharray="4 3"' if style == "data" else ""
    marker = f"url(#m-{style or 'data'})"
    # Orthogonal path: horizontal-first when leaving left/right, else vertical-first.
    if s_side in "lr" and d_side in "lr":
        mx = (x1 + x2) / 2
        d = f"M{x1},{y1} L{mx},{y1} L{mx},{y2} L{x2},{y2}"
        lx, ly = mx, (y1 + y2) / 2
    elif s_side in "tb" and d_side in "tb":
        my = (y1 + y2) / 2
        d = f"M{x1},{y1} L{x1},{my} L{x2},{my} L{x2},{y2}"
        lx, ly = (x1 + x2) / 2, my
    elif s_side in "lr":
        d = f"M{x1},{y1} L{x2},{y1} L{x2},{y2}"
        lx, ly = (x1 + x2) / 2, y1
    else:
        d = f"M{x1},{y1} L{x1},{y2} L{x2},{y2}"
        lx, ly = x1, (y1 + y2) / 2
    out = [f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{dash} '
           f'marker-end="{marker}"/>']
    label = T(label)
    if label:
        parts = label.split("\n")
        width = max(len(p) for p in parts) * 6.0 + 8
        height = 13 * len(parts) + 4
        out.append(f'<rect x="{lx - width / 2}" y="{ly - height / 2}" width="{width}" '
                   f'height="{height}" fill="white" opacity="0.92" rx="2"/>')
        for i, p in enumerate(parts):
            out.append(f'<text x="{lx}" y="{ly - height / 2 + 13 + i * 13}" '
                       f'font-size="10" text-anchor="middle" fill="{color}">{escape(p)}</text>')
    return "\n".join(out)


def legend(x, y, items):
    out = []
    for i, (kind, text) in enumerate(items):
        fill, stroke = KINDS[kind]
        xi = x + i * 150
        out.append(f'<rect x="{xi}" y="{y}" width="14" height="10" fill="{fill}" '
                   f'stroke="{stroke}" stroke-width="1.2"/>')
        out.append(f'<text x="{xi + 20}" y="{y + 9}" font-size="10.5" fill="{MUTED}">'
                   f'{escape(T(text))}</text>')
    return "\n".join(out)


def line_legend(x, y):
    items = [("money", "Funds movement"), ("data", "Data / events"), ("ctrl", "Control / approval")]
    out = []
    for i, (style, text) in enumerate(items):
        color = {"money": "#2f855a", "data": "#1f6f8b", "ctrl": "#b7791f"}[style]
        dash = ' stroke-dasharray="4 3"' if style == "data" else ""
        xi = x + i * 150
        out.append(f'<line x1="{xi}" y1="{y + 5}" x2="{xi + 22}" y2="{y + 5}" '
                   f'stroke="{color}" stroke-width="1.5"{dash}/>')
        out.append(f'<text x="{xi + 28}" y="{y + 9}" font-size="10.5" fill="{MUTED}">'
                   f'{escape(T(text))}</text>')
    return "\n".join(out)


def render(name, width, height, boxes, arrows, legend_items, lines=True):
    by_id = {b[0]: b for b in boxes}
    defs = "".join(
        f'<marker id="m-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for k, c in {"money": "#2f855a", "data": "#1f6f8b", "ctrl": "#b7791f", "risk": "#c53030"}.items()
    )
    groups = [b for b in boxes if b[6] == "group"]
    others = [b for b in boxes if b[6] != "group"]
    body = [box(b) for b in groups]
    body += [arrow(by_id, a) for a in arrows]
    body += [box(b) for b in others]
    body.append(legend(10, height - 34, legend_items))
    if lines:
        body.append(line_legend(10, height - 16))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'width="{width}" height="{height}" font-family="{FONT}">'
           f'<defs>{defs}</defs><rect width="100%" height="100%" fill="white"/>'
           + "\n".join(body) + "</svg>")
    (OUT / f"{name}.svg").write_text(svg)




def sequence(name, participants, steps, width=640, lane_top=16, step_h=30):
    """Render a sequence diagram.

    participants: [(id, label, kind)]
    steps: (src, dst, label, style) messages; src == dst draws a self-step;
           ("note", text) draws a full-width note; ("phase", text) a divider.
    """
    n = len(participants)
    margin = 20
    col_w = (width - 2 * margin) / n
    xs = {p[0]: margin + col_w * (i + 0.5) for i, p in enumerate(participants)}
    head_h = 36
    y = lane_top + head_h + 18
    body = []
    rows = []
    for st in steps:
        if st[0] in ("note", "phase"):
            rows.append((st, y))
            y += step_h
        else:
            rows.append((st, y))
            y += step_h + (8 if st[0] == st[1] else 0)
    bottom = y + 6
    height = bottom + 20
    defs = "".join(
        f'<marker id="s-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for k, c in {"money": "#2f855a", "data": "#1f6f8b", "ctrl": "#b7791f", "risk": "#c53030"}.items())
    colors = {"money": "#2f855a", "data": "#1f6f8b", "ctrl": "#b7791f", "risk": "#c53030"}
    # lifelines and heads
    for pid, label, kind in participants:
        x = xs[pid]
        fill, stroke = KINDS[kind]
        bw = min(col_w - 8, 150)
        body.append(f'<line x1="{x}" y1="{lane_top + head_h}" x2="{x}" y2="{bottom}" stroke="#c3ccd6" '
                    f'stroke-width="1" stroke-dasharray="3 3"/>')
        lines = T(label).split("\n")
        body.append(f'<rect x="{x - bw / 2}" y="{lane_top}" width="{bw}" height="{head_h}" rx="4" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        y0 = lane_top + head_h / 2 - (len(lines) - 1) * 6 + 4
        for i, line in enumerate(lines):
            body.append(f'<text x="{x}" y="{y0 + i * 12}" font-size="{12 if i == 0 else 10}" '
                        f'text-anchor="middle" fill="{INK if i == 0 else MUTED}" '
                        f'font-weight="{"bold" if i == 0 else "normal"}">{escape(line)}</text>')
    for st, yy in rows:
        if st[0] == "phase":
            body.append(f'<line x1="{margin}" y1="{yy}" x2="{width - margin}" y2="{yy}" stroke="#9aa7b6" '
                        f'stroke-width="0.8"/>')
            body.append(f'<rect x="{margin}" y="{yy - 8}" width="{len(st[1]) * 5.6 + 12}" height="15" fill="#eef3f7"/>')
            body.append(f'<text x="{margin + 6}" y="{yy + 3}" font-size="9.5" font-weight="bold" '
                        f'fill="{MUTED}">{escape(T(st[1]))}</text>')
            continue
        if st[0] == "note":
            body.append(f'<rect x="{margin + 20}" y="{yy - 10}" width="{width - 2 * margin - 40}" height="18" '
                        f'rx="3" fill="#fdf3e3" stroke="#e2c58f" stroke-width="0.8"/>')
            body.append(f'<text x="{width / 2}" y="{yy + 3}" font-size="9" text-anchor="middle" '
                        f'fill="{INK}">{escape(T(st[1]))}</text>')
            continue
        src, dst, label, style = (list(st) + [None])[:4]
        style = style or "data"
        color = colors[style]
        dash = ' stroke-dasharray="4 3"' if style == "data" else ""
        x1, x2 = xs[src], xs[dst]
        label = T(label) or ""
        if src == dst:
            body.append(f'<path d="M{x1},{yy - 4} h28 v12 h-26" fill="none" stroke="{color}" '
                        f'stroke-width="1.3"{dash} marker-end="url(#s-{style})"/>')
            # Labels for right-hand lifelines go on the left so they are not clipped.
            if x1 + 34 + len(label) * 5.9 > width - 4:
                body.append(f'<text x="{x1 - 6}" y="{yy + 6}" font-size="10.5" text-anchor="end" '
                            f'fill="{color}">{escape(label)}</text>')
            else:
                body.append(f'<text x="{x1 + 34}" y="{yy + 6}" font-size="10.5" fill="{color}">{escape(label)}</text>')
            continue
        body.append(f'<line x1="{x1}" y1="{yy}" x2="{x2 + (-3 if x2 > x1 else 3)}" y2="{yy}" stroke="{color}" '
                    f'stroke-width="1.4"{dash} marker-end="url(#s-{style})"/>')
        mx = (x1 + x2) / 2
        tw = len(label) * 5.9 + 8
        body.append(f'<rect x="{mx - tw / 2}" y="{yy - 15}" width="{tw}" height="13" fill="white" opacity="0.9"/>')
        body.append(f'<text x="{mx}" y="{yy - 4}" font-size="10.5" text-anchor="middle" fill="{color}">'
                    f'{escape(label)}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
           f'height="{height}" font-family="{FONT}"><defs>{defs}</defs>'
           f'<rect width="100%" height="100%" fill="white"/>' + "\n".join(body) + "</svg>")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(svg)
