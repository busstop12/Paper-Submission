#!/usr/bin/env python3
"""Draw the method walkthrough SVGs and write them into ../index.html.

The page redraws the paper's overview figure as one SVG per stage (overview, (a), (b), (c)) plus the
Action Sharing / Variant Preservation example of the first figure. Each SVG sits between
<!-- svg:NAME --> and <!-- /svg:NAME --> in index.html. After editing a drawing here, run

    python3 tools/build_method_svgs.py

Hooks the page CSS/JS relies on:
  <g class="a" style="--d:1.2s">    enters 1.2 s after its step starts ("pop" adds an overshoot)
  <g ... style="--d2:1.8s" class="dim">  fades to the background at 1.8 s
  <path class="ln" pathLength="1">  is drawn from start to end; its arrowhead appears when it is done
  data-go="k"                       clicking the group opens stage k of the walkthrough
  data-layer="k" (concept figure)   the group is step k of the step-by-step player
The examples (contacts, report files) are illustrative, following the examples used in the paper.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
ICON = "static/icons/{}.png"

INK, STROKE, MUTED = "#1c2130", "#222", "#5d6677"
BLUE, BLUE_DEEP, RED, GREEN, ORANGE = "#5b8fd6", "#2b5fae", "#d6443a", "#23854c", "#d9742c"
# stage colours, from the paper's overview figure: (a) green, (b) blue, (c) orange
A_BOX, A_PANEL, A_TAB = "#e2f0df", "#eef6ec", "#c3e1be"
B_BOX, B_PANEL, B_TAB = "#d9e9f8", "#edf4fb", "#bcd6ef"
C_BOX, C_PANEL, C_TAB = "#fde0c2", "#fdf3e8", "#f8cfa2"
# record colours: task (yellow), action (blue), variant (lilac); lilac is also used for agents
T_FILL, T_INK = "#fff3cc", "#c99a1c"
A_FILL, A_INK = "#d6e7f7", "#4f86c9"
V_FILL, V_INK = "#ead9f2", "#9a5bb0"
L_FILL, L_INK = "#efe4f5", "#a46cbc"
TAP = "#e0457b"
# Smallest text, in SVG units (the figures are drawn at about 1 unit per pixel on a desktop screen): labels, and the
# text inside the mock phone screens. Smaller sizes passed to T are raised to these.
LABEL_MIN, SCREEN_MIN = 13, 9
_in_screen = False


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def num(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def R(x, y, w, h, fill="#fff", stroke=STROKE, sw=2.2, rx=10, dash=None, extra=""):
    st = "" if stroke == "none" else f' stroke="{stroke}" stroke-width="{sw}"'
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{rx}" fill="{fill}"{st}{ds}{extra}/>'


def T(x, y, s, size=15, w=400, anchor="middle", fill=INK, it=False, sans=False, raw=False, extra="", sub=False):
    if not sub:   # subscripts keep their own size
        size = max(size, SCREEN_MIN if _in_screen else LABEL_MIN)
    cls = ' class="sans"' if sans else ""
    fs = ' font-style="italic"' if it else ""
    body = s if raw else esc(s)
    return (f'<text x="{num(x)}" y="{num(y)}" dominant-baseline="central" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}"{fs}{cls}{extra}>{body}</text>')


def ML(x, y, lines, size=15, lh=None, **kw):
    """Several lines centred vertically on y."""
    lh = lh or max(size, SCREEN_MIN if _in_screen else LABEL_MIN) * 1.25
    y0 = y - lh * (len(lines) - 1) / 2
    return "".join(T(x, y0 + i * lh, s, size, **kw) for i, s in enumerate(lines))


def C(cx, cy, r, fill="#fff", stroke=STROKE, sw=2, extra=""):
    st = "" if stroke == "none" else f' stroke="{stroke}" stroke-width="{sw}"'
    return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}" fill="{fill}"{st}{extra}/>'


def IMG(name, x, y, w, h):
    return f'<image href="{ICON.format(name)}" x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}"/>'


def badge(cx, cy, n, r=12):
    return C(cx, cy, r, fill=INK, stroke="none") + T(cx, cy + 0.5, str(n), r * 1.15, 700, fill="#fff")


def check(cx, cy, r=10, color=GREEN):
    return (C(cx, cy, r, fill=color, stroke="none") +
            f'<path d="M{num(cx - r * .45)} {num(cy + r * .02)} l{num(r * .32)} {num(r * .32)} l{num(r * .58)} {num(-r * .62)}" '
            f'fill="none" stroke="#fff" stroke-width="{num(r * .26)}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r=10, color=RED):
    k = r * .38
    return (C(cx, cy, r, fill=color, stroke="none") +
            f'<path d="M{num(cx - k)} {num(cy - k)} L{num(cx + k)} {num(cy + k)} M{num(cx + k)} {num(cy - k)} L{num(cx - k)} {num(cy + k)}" '
            f'stroke="#fff" stroke-width="{num(r * .26)}" stroke-linecap="round"/>')


def loop_glyph(fig, cx, cy, r=6.5, color=INK):
    """The clockwise circular arrow that marks "for each candidate step" in the paper figure: a 270-degree arc
    open at the top, with a filled arrowhead at its upper-left end pointing along the arc."""
    import math
    rad = math.radians
    sx, sy = cx + r * math.cos(rad(300)), cy + r * math.sin(rad(300))
    a = rad(210)
    ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)          # direction of travel (clockwise on screen)
    nx, ny = math.cos(a), math.sin(a)           # outward normal
    tip = (ex + tx * 4.2, ey + ty * 4.2)
    b1 = (ex - tx * 1.0 + nx * 3.4, ey - ty * 1.0 + ny * 3.4)
    b2 = (ex - tx * 1.0 - nx * 3.4, ey - ty * 1.0 - ny * 3.4)
    head = " ".join(f"{x:.1f},{y:.1f}" for x, y in (tip, b1, b2))
    return (f'<path d="M{sx:.1f} {sy:.1f} A{r} {r} 0 1 1 {ex:.1f} {ey:.1f}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<polygon points="{head}" fill="{color}"/>')


def block_arrow(x, y):
    """Thick black arrow between panels (as in the paper figure), pointing right, starting at x."""
    return (f'<path d="M{x} {y - 8} h10 v-8 l13 16 l-13 16 v-8 h-10z" fill="{INK}"/>')


def chip(x, y, w, h, label, fill, stroke, size=13, it=False, w8=700, sans=False, sw=2):
    return R(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=7) + T(x + w / 2, y + h / 2, label, size, w8, it=it, sans=sans)


class Fig:
    """One inline SVG; arrowhead markers are collected per figure so their ids stay unique."""

    def __init__(self, prefix, w, h, label):
        self.p, self.w, self.h, self.label = prefix, w, h, label
        self.parts, self.cols = [], []

    def add(self, *s):
        self.parts.extend(s)

    def g(self, d, *body, cls="a", extra=""):
        self.parts.append(f'<g class="{cls}" style="--d:{d:.2f}s"{extra}>{"".join(body)}</g>')

    def mk(self, color):
        if color not in self.cols:
            self.cols.append(color)
        return f"url(#{self.p}-{color.lstrip('#')})"

    def P(self, d, color=STROKE, sw=2.4, arrow=True, dash=None, draw=True, extra=""):
        cls = ' class="ln" pathLength="1"' if draw and not dash else ""
        me = f' marker-end="{self.mk(color)}"' if arrow else ""
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<path{cls} d="{d}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linejoin="round" '
                f'stroke-linecap="round"{ds}{me}{extra}/>')

    def svg(self, inner_only=False):
        defs = "".join(
            f'<marker id="{self.p}-{c.lstrip("#")}" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="5.5" '
            f'markerHeight="5.5" orient="auto"><path d="M0 0.5 L10 5 L0 9.5z" fill="{c}"/></marker>' for c in self.cols)
        return (f'<svg class="pfig" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{self.label}">'
                f'<defs>{defs}</defs>{"".join(self.parts)}</svg>')


# ---------------------------------------------------------------- phone screens (local coordinates)

def phone(x, y, w, h, screen, side=4, top=10, bottom=8):
    global _in_screen
    sw, sh = w - 2 * side, h - top - bottom
    _in_screen = True
    try:
        body = screen(sw, sh)
    finally:
        _in_screen = False
    return (R(x, y, w, h, fill=INK, stroke="none", rx=round(w * .15, 1)) +
            R(x + side, y + top, sw, sh, fill="#fff", stroke="none", rx=3) +
            R(x + w / 2 - 9, y + 3.5, 18, 2.6, fill="#59606d", stroke="none", rx=1.3) +
            f'<svg x="{num(x + side)}" y="{num(y + top)}" width="{num(sw)}" height="{num(sh)}" viewBox="0 0 {num(sw)} {num(sh)}">'
            f'{body}</svg>')


def tapmark(cx, cy, color=TAP):
    return C(cx, cy, 5.6, fill="none", stroke=color, sw=1.4) + C(cx, cy, 2.3, fill=color, stroke="none")


def crosshair(cx, cy, color):
    return (C(cx, cy, 6.5, fill="none", stroke=color, sw=1.6) +
            f'<path d="M{cx - 10} {cy} h6 M{cx + 4} {cy} h6 M{cx} {cy - 10} v6 M{cx} {cy + 4} v6" stroke="{color}" stroke-width="1.6"/>' +
            C(cx, cy, 1.8, fill=color, stroke="none"))


def appbar(w, title, right=""):
    return (R(0, 0, w, 18, fill="#e6effa", stroke="none", rx=0) + T(6, 9.5, "‹", 13, 700, fill=BLUE_DEEP) +
            T(15, 9.5, title, 9.5, 700, "start", sans=True) + right)


def files_screen(order, hl=None, tap=None, marks=()):
    def draw(w, h):
        s = [appbar(w, "Files", T(w - 5, 9.5, "⋮", 10, 700, fill=MUTED)),
             R(5, 23, w - 10, 9, fill="#fff", stroke="#c9d3df", sw=.8, rx=4.5)]
        for i, name in enumerate(order):
            cy = 48 + 23 * i
            if name == hl:
                s.append(R(2, cy - 10.5, w - 4, 21, fill="#fbe3f3", stroke="#d07fc0", sw=1, rx=4))
            s.append(f'<path d="M6 {cy - 5.5} h5 l2.4 2.4 v8.6 h-7.4z" fill="#fff" stroke="{BLUE}" stroke-width="1.1"/>')
            s.append(T(17, cy - 1.8, name, 9, 700, "start", sans=True))
            s.append(R(17, cy + 4, 22, 1.8, fill="#cfd6e0", stroke="none", rx=.9))
            if name == tap:
                s.append(tapmark(w - 13, cy))
        for name, color in marks:
            s.append(crosshair(w - 13, 48 + 23 * order.index(name), color))
        return "".join(s)
    return draw


def report_screen(icon):
    def draw(w, h):
        if icon == "share":
            ic = (C(w - 14, 9.5, 1.6, fill=BLUE_DEEP, stroke="none") + C(w - 8, 6, 1.6, fill=BLUE_DEEP, stroke="none") +
                  C(w - 8, 13, 1.6, fill=BLUE_DEEP, stroke="none") +
                  f'<path d="M{w - 14} 9.5 L{w - 8} 6 M{w - 14} 9.5 L{w - 8} 13" stroke="{BLUE_DEEP}" stroke-width=".9"/>')
        else:
            ic = (R(w - 15, 5, 9, 9, fill="#fff", stroke=BLUE_DEEP, sw=1.1, rx=1.2) + R(w - 13, 5, 5, 3, fill=BLUE_DEEP, stroke="none", rx=.4))
        s = [appbar(w, "Report", ic + tapmark(w - 11, 9.5)),
             R(6, 25, w - 12, h - 34, fill="#fff", stroke="#d3dbe6", sw=1, rx=3),
             T(11, 33, "Report", 7.5, 700, "start", sans=True)]
        for i, (bh, col) in enumerate([(16, "#c9b8e6"), (24, "#a9c6ee"), (12, "#c9b8e6"), (30, "#6fa3e6")]):
            s.append(R(14 + i * 12, 70 - bh, 8, bh, fill=col, stroke="none", rx=1))
        s.append(f'<path d="M11 70.5 H{w - 11}" stroke="#9aa3b2" stroke-width=".8"/>')
        for i in range(4):
            s.append(R(11, 80 + i * 8, (w - 22) * (.9 if i % 2 == 0 else .7), 2.4, fill="#d9dfe8", stroke="none", rx=1.2))
        return "".join(s)
    return draw


def share_sheet(x, y):
    s = [R(x, y, 112, 92, fill="#fff", stroke="#b9c3d0", sw=1.6, rx=12),
         R(x + 46, y + 7, 20, 3, fill="#c9d0da", stroke="none", rx=1.5),
         T(x + 56, y + 24, "Share Report", 11.5, 700, sans=True)]
    for i, col in enumerate(["#9fb8e6", "#d6a6e0", "#f2b071"]):
        cx = x + 26 + i * 30
        s += [C(cx, y + 52, 10, fill=col, stroke="none"), C(cx, y + 49, 3.4, fill="#fff", stroke="none"),
              R(cx - 6, y + 53, 12, 6, fill="#fff", stroke="none", rx=3), R(cx - 8, y + 68, 16, 2.6, fill="#cfd6e0", stroke="none", rx=1.3)]
    s.append(R(x + 36, y + 80, 40, 3, fill="#c9d0da", stroke="none", rx=1.5))
    return "".join(s)


def save_sheet(x, y):
    s = [R(x, y, 112, 92, fill="#fff", stroke="#b9c3d0", sw=1.6, rx=12),
         R(x + 46, y + 7, 20, 3, fill="#c9d0da", stroke="none", rx=1.5),
         T(x + 56, y + 24, "Save a copy", 11.5, 700, sans=True)]
    for i, (name, sel) in enumerate([("Documents", False), ("Archive", True)]):
        yy = y + 36 + i * 20
        if sel:
            s.append(R(x + 6, yy - 1, 100, 18, fill="#dbe9f8", stroke=BLUE, sw=1, rx=4))
        s.append(f'<path d="M{x + 12} {yy + 4} h4 l1.5 2 h6 v8 h-11.5z" fill="#fff" stroke="{BLUE_DEEP}" stroke-width="1"/>')
        s.append(T(x + 29, yy + 8, name, 9, 700 if sel else 500, "start", sans=True))
    s.append(R(x + 72, y + 78, 32, 9, fill=BLUE_DEEP, stroke="none", rx=4.5))
    return "".join(s)


# contacts app for the online reuse stage; screen size about 116 x 206
def home_screen(w, h):
    s = [R(0, 0, w, h, fill="#e9f0fa", stroke="none", rx=0), T(10, 8, "9:41", 7.5, 700, "start", sans=True)]
    apps = [("Clock", "#9aa3b2"), ("Files", "#6fa3e6"), ("Mail", "#f2b071"), ("Contacts", "#5b8fd6"), ("Maps", "#7cc4a0"),
            ("Notes", "#f3d36b"), ("Photos", "#e79ab8"), ("Camera", "#8c93a0"), ("Music", "#c9a2e6")]
    for i, (name, col) in enumerate(apps):
        cx, cy = 22 + (i % 3) * 36, 36 + (i // 3) * 44
        s.append(R(cx - 13, cy - 13, 26, 26, fill=col, stroke="none", rx=7))
        if name == "Contacts":
            s += [C(cx, cy - 3, 4.5, fill="#fff", stroke="none"), R(cx - 7.5, cy + 2.5, 15, 7, fill="#fff", stroke="none", rx=3.5)]
        s.append(T(cx, cy + 19, name, 7, 500, sans=True))
    s.append(tapmark(58, 77))
    return "".join(s)


def contacts_screen(w, h):
    s = [R(0, 0, w, 20, fill="#e6effa", stroke="none", rx=0), T(8, 10.5, "Contacts", 10, 700, "start", sans=True),
         R(6, 25, w - 12, 10, fill="#fff", stroke="#c9d3df", sw=.8, rx=5),
         T(10, 47, "+  Create contact", 9.5, 700, "start", fill=BLUE_DEEP, sans=True), tapmark(88, 47)]
    for i, (name, col) in enumerate([("Alice", "#f2b071"), ("Carol", "#7cc4a0"), ("Dan", "#9fb8e6"), ("Eve", "#e79ab8")]):
        cy = 70 + i * 24
        s += [C(16, cy, 8, fill=col, stroke="none"), T(16, cy + .5, name[0], 8, 700, fill="#fff", sans=True),
              T(30, cy, name, 9.5, 500, "start", sans=True), f'<path d="M30 {cy + 11} H{w - 8}" stroke="#e3e8ef" stroke-width=".8"/>']
    return "".join(s)


def form_screen(name):
    def draw(w, h):
        s = [R(0, 0, w, 20, fill="#e6effa", stroke="none", rx=0), T(8, 10.5, "Create contact", 9.5, 700, "start", sans=True),
             R(w - 30, 4, 26, 12, fill=BLUE_DEEP, stroke="none", rx=6), T(w - 17, 10.5, "Save", 7.5, 700, fill="#fff", sans=True),
             C(w / 2, 44, 15, fill="#dbe5f2", stroke="none"), C(w / 2, 40, 5, fill="#fff", stroke="none"),
             R(w / 2 - 8, 46, 16, 8, fill="#fff", stroke="none", rx=4),
             T(8, 72, "Name", 7.5, 500, "start", fill=MUTED, sans=True),
             R(6, 78, w - 12, 18, fill="#fff", stroke=BLUE if not name else "#c9d3df", sw=1.3, rx=4),
             T(8, 112, "Phone", 7.5, 500, "start", fill=MUTED, sans=True),
             R(6, 118, w - 12, 18, fill="#fff", stroke="#c9d3df", sw=1, rx=4)]
        if name:
            s += [T(11, 87.5, name, 10, 700, "start", sans=True), tapmark(w - 17, 10)]
        else:
            s.append(f'<path d="M11 82 v10" stroke="{BLUE_DEEP}" stroke-width="1.2"/>')
            s.append(R(0, h - 58, w, 58, fill="#dfe4ec", stroke="none", rx=0))
            for r, n in enumerate([10, 9, 7]):
                for k in range(n):
                    kw = (w - 8) / 10
                    s.append(R(4 + (10 - n) * kw / 2 + k * kw + 1, h - 54 + r * 17, kw - 2, 13, fill="#fff", stroke="none", rx=2))
        return "".join(s)
    return draw


def saved_screen(w, h):
    return "".join([
        R(0, 0, w, h, fill="#fff", stroke="none", rx=0), R(0, 0, w, 20, fill="#e6effa", stroke="none", rx=0),
        T(6, 10.5, "‹", 13, 700, fill=BLUE_DEEP), T(15, 10.5, "Contact", 9.5, 700, "start", sans=True),
        C(w / 2, 56, 21, fill="#c9b3e6", stroke="none"), T(w / 2, 57, "B", 18, 700, fill="#fff", sans=True),
        T(w / 2, 92, "Bob", 13, 700, sans=True),
        R(10, 108, w - 20, 16, fill="#f3f5f8", stroke="none", rx=4), R(10, 130, w - 20, 16, fill="#f3f5f8", stroke="none", rx=4),
        R(12, h - 32, w - 24, 18, fill=INK, stroke="none", rx=9), T(w / 2, h - 23, "Contact saved", 8, 700, fill="#fff", sans=True)])


# ---------------------------------------------------------------- overview

def overview():
    f = Fig("ov", 1100, 540, "TAVMem overview: memory construction on the cloud, task retrieval and reuse on the phone")
    f.add(R(3, 3, 1094, 534, fill="#fff", stroke=STROKE, sw=2.4, rx=24),
          R(16, 16, 1068, 216, fill="#f5faf4", stroke="none", rx=16),
          R(16, 244, 1068, 280, fill="#fdf7f3", stroke="none", rx=16))
    f.g(.05, IMG("cloud", 926, 24, 46, 46), T(978, 47, "On-Cloud", 19, 700, "start"))
    # trajectories
    hist = (R(60, 50, 120, 92, fill="#fff", stroke="#d38fc4", sw=1.8, rx=6) +
            R(52, 57, 120, 92, fill="#fff", stroke="#d38fc4", sw=1.8, rx=6) +
            R(44, 64, 120, 92, fill="#fff", stroke=STROKE, sw=2, rx=6) +
            T(104, 86, "(q₁, S₁)", 15) + T(104, 109, "(q₂, S₂)", 15) + T(104, 134, "⋯   H", 15, it=True))
    f.g(.10, hist, ML(104, 190, ["historical", "trajectories"], 17, 21, it=True, fill="#333"))
    f.g(.35, f.P("M164 110 L230 110"))
    f.g(.50, R(230, 60, 210, 100, fill=A_BOX, sw=2.2, dash="8 5"), T(259, 110, "(a)", 20, 700),
        ML(356, 110, ["Memory", "Construction"], 18, 24, w=700), cls="a pop", extra=' data-go="1" role="button" tabindex="0" aria-label="Open stage (a): memory construction"')
    f.g(.75, f.P("M440 110 L494 110"))
    graph = (chip(504, 68, 46, 28, "T₁", T_FILL, T_INK, 14, it=True) + chip(504, 124, 46, 28, "T₂", T_FILL, T_INK, 14, it=True) +
             chip(582, 92, 46, 36, "A", A_FILL, A_INK, 16, it=True) +
             chip(660, 68, 46, 28, "V₁", V_FILL, V_INK, 14, it=True) + chip(660, 124, 46, 28, "V₂", V_FILL, V_INK, 14, it=True) +
             f'<path d="M550 82 L582 104 M550 138 L582 116 M628 104 L660 82 M628 116 L660 138" stroke="{STROKE}" stroke-width="1.8" fill="none"/>')
    f.g(.90, graph, cls="a pop")
    f.g(.95, T(605, 186, "full memory library", 17, it=True, fill="#333"))
    f.g(1.15, f.P("M706 110 L774 110"), T(740, 95, "export", 16, it=True, fill="#333"))
    f.g(1.30, IMG("box_export", 776, 76, 68, 68), ML(852, 110, ["runtime", "export"], 17, 21, anchor="start", it=True, fill="#333"))
    # cloud -> phone
    f.g(1.45, f'<path d="M16 238 H1084" stroke="#9aa3b2" stroke-width="1.6" stroke-dasharray="7 6"/>')
    f.g(1.55, f.P("M810 146 L810 282"))
    f.g(1.60, IMG("smartphone", 934, 244, 38, 38), T(974, 264, "On-Device", 19, 700, "start"))
    lib = [R(40, 284, 1020, 50, fill="#eef4fb", stroke=BLUE, sw=2.2, rx=10), IMG("database", 48, 289, 40, 40),
           T(94, 309, "Runtime memory library", 15, 700, "start")]
    f.g(1.75, *lib, cls="a wipe")
    for i, (x, w, label, fill, stroke, dash) in enumerate([
            (306, 136, "retrieval index", "#fff", "#9aa3b2", "5 4"), (453, 112, "task records", T_FILL, T_INK, None),
            (577, 128, "action records", A_FILL, A_INK, None), (716, 82, "variants", V_FILL, V_INK, None)]):
        f.g(1.95 + i * .1, R(x, 294, w, 30, fill=fill, stroke=stroke, sw=1.6, rx=8, dash=dash), T(x + w / 2, 309, label, 13), cls="a pop")
    f.g(2.35, T(1048, 309, "0.95–4.07 MiB, no screenshots", 13.8, it=True, anchor="end", fill="#333"))
    f.g(2.45, f.P("M281 334 L281 368"), f.P("M595 334 L595 360"))
    # online reuse
    f.g(2.40, IMG("person_chat", 40, 378, 64, 64), ML(92, 472, ["new", "instruction q"], 16, 20, it=True, fill="#333"))
    f.g(2.55, f.P("M108 414 L174 414"))
    f.g(2.65, R(174, 370, 212, 88, fill=B_BOX, sw=2.2, dash="8 5"), T(203, 414, "(b)", 20, 700),
        ML(298, 414, ["Task", "Retrieval"], 18, 24, w=700), cls="a pop", extra=' data-go="2" role="button" tabindex="0" aria-label="Open stage (b): task retrieval"')
    f.g(2.85, f.P("M386 414 L468 414"), ML(427, 390, ["task", "record"], 15, 17, it=True, fill="#333"))
    f.g(3.00, R(468, 362, 252, 104, fill=C_BOX, sw=2.2, dash="8 5"), T(497, 414, "(c)", 20, 700),
        ML(612, 414, ["Reuse &", "Applicability", "Checking"], 18, 24, w=700), cls="a pop",
        extra=' data-go="3" role="button" tabindex="0" aria-label="Open stage (c): reuse and applicability checking"')
    f.g(3.15, loop_glyph(f, 498, 487), T(514, 487, "for each candidate step", 15, it=True, anchor="start", fill="#333"))
    f.g(3.30, f.P("M720 392 L968 392", GREEN), T(840, 379, "✓ accepted: reuse the stored action", 13, 700, fill=GREEN, sans=True))
    f.g(3.45, IMG("smartphone", 950, 362, 100, 100), T(1000, 476, "current UI", 16.5, it=True, fill="#333"))
    f.g(3.60, f.P("M720 446 L758 446 L758 486 L788 486", RED, dash="6 5", draw=False),
        T(752, 508, "✗ cannot reuse", 14.5, 700, "end", fill=RED, sans=True))
    f.g(3.75, R(788, 458, 124, 56, fill=L_FILL, stroke=L_INK, sw=2, rx=10), IMG("robot", 794, 462, 46, 46),
        ML(876, 486, ["base", "agent"], 15, 18, w=700), cls="a pop")
    f.g(3.95, f.P("M912 486 L940 486 L940 440 L968 440"), T(948, 506, "VLM call", 14, it=True, anchor="start", fill=MUTED))
    return f.svg()


# ---------------------------------------------------------------- (a) memory construction

def construct():
    f = Fig("pa", 1100, 470, "Stage (a): memory construction")
    title = "(a) Memory Construction on the Cloud"
    tw = len(title) * 11.4 + 40
    cols = [(20, 210), (254, 370), (648, 214), (886, 194)]
    f.g(.05, R(3, 3, 1094, 464, fill=A_PANEL, stroke=STROKE, sw=2.4, rx=26),
        R(550 - tw / 2, 13, tw, 32, fill=A_TAB, stroke="none", rx=9), T(550, 29, title, 19, 700),
        *[R(x, 58, w, 396, fill="#fbfdfa", stroke="none", rx=18) for x, w in cols])
    heads = ["Trajectories", "Step matching & merging", "Full memory library", "Runtime export"]
    for i, ((x, w), h) in enumerate(zip(cols, heads)):
        f.g([.15, 1.05, 3.05, 4.25][i], badge(x + 22, 82, i + 1), T(x + 42, 82, h, 15, 700, "start", sans=True))
    for i, x in enumerate([231, 625, 863]):
        f.g([.95, 2.95, 4.15][i], block_arrow(x, 255))
    # 1. trajectories
    card = [R(32, 102, 186, 160, fill="#fff", stroke="#d38fc4", sw=1.8, rx=10),
            T(46, 122, "q₁", 14, 700, "start", it=True), T(70, 122, "Share Report", 13, 700, "start", sans=True), check(204, 122, 8)]
    f.g(.25, *card)
    for i, (purpose, act) in enumerate([("open the report", "click (x,y₁)"), ("tap share", "click (x′,y′)"), ("pick a contact", "click (x″,y″)")]):
        cy = 156 + i * 34
        f.g(.4 + i * .1, C(48, cy, 9, fill="#fbe3f3", stroke="#d07fc0", sw=1.4), T(48, cy + .5, str(i + 1), 10.5, 700, sans=True),
            T(64, cy - 7, purpose, 12, 700, "start", sans=True), T(64, cy + 9, act, 11, 400, "start", fill=MUTED),
            R(166, cy - 8, 20, 16, fill=A_FILL, stroke=A_INK, sw=1, rx=3), T(176, cy, "UI", 8.5, 700),
            R(192, cy - 10, 13, 20, fill="#fff", stroke=INK, sw=1.2, rx=2.5), R(194.5, cy - 6.5, 8, 11, fill="#dbe7f5", stroke="none", rx=1))
    f.g(.75, R(32, 274, 186, 56, fill="#fff", stroke="#d38fc4", sw=1.8, rx=10), T(46, 292, "q₂", 14, 700, "start", it=True),
        T(70, 292, "Save Report", 13, 700, "start", sans=True), check(204, 292, 8),
        T(46, 314, "steps, UI info, screenshots", 11, 400, "start", fill=MUTED, sans=True))
    f.g(.85, T(125, 352, "⋯", 18, 700, fill=MUTED),
        ML(125, 388, ["keep the shortest", "successful run of", "each instruction"], 12, 16, it=True, fill=MUTED, sans=True))
    # 2. step matching and merging
    f.g(1.15, R(268, 100, 342, 32, fill="#fff", stroke=STROKE, sw=1.8, rx=8, dash="6 4"),
        T(439, 116, "new step from q₂: open the report, click (x, y₂)", 12.5, 700, sans=True), cls="a pop")
    f.g(1.30, f.P("M314 132 L314 150"))
    boxes = [(264, "Candidates", ["app", "action type", "description"]), (380, "Match action", ["parameters", "UI context", "VLM if unclear"]),
             (496, "Match variant", ["click target", "input text", "swipe path"])]
    for i, (x, head, rows) in enumerate(boxes):
        body = [R(x, 150, 100, 104, fill=A_FILL, stroke=A_INK, sw=2, rx=10), T(x + 50, 167, head, 13, 700, sans=True)]
        for k, r in enumerate(rows):
            body += [R(x + 5, 180 + k * 23, 90, 19, fill="#fff", stroke=A_INK, sw=1, rx=5), T(x + 50, 189.5 + k * 23, r, 11, 500, sans=True)]
        f.g(1.40 + i * .25, *body, cls="a pop")
    f.g(1.55, f.P("M364 202 L380 202"), T(372, 191, "C", 12, 700, it=True))
    f.g(1.80, f.P("M480 202 L496 202"), T(488, 191, "A", 12, 700, it=True))

    def decision(cx, d, yes, no):
        f.g(d, f.P(f"M{cx} 254 L{cx} 270", arrow=False))
        f.g(d + .05, f'<path d="M{cx} 270 l34 20 l-34 20 l-34 -20z" fill="#ffe9a8" stroke="{T_INK}" stroke-width="1.8"/>',
            T(cx, 290, "match?", 11.5, 400, it=True, sans=True), cls="a pop")
        f.g(d + .15, f'<path d="M{cx} 310 V318 M{cx - 27} 318 H{cx + 27} M{cx - 27} 318 V338 M{cx + 27} 318 V338" stroke="{STROKE}" stroke-width="1.8" fill="none"/>',
            check(cx - 27, 328, 7), cross(cx + 27, 328, 7))
        f.g(d + .25, R(cx - 52, 338, 50, 22, fill="#fbe3f3", stroke="#d07fc0", sw=1.4, rx=6), T(cx - 27, 349, yes, 11, 400, it=True, sans=True),
            R(cx + 2, 338, 50, 22, fill="#fbe3f3", stroke="#d07fc0", sw=1.4, rx=6), T(cx + 27, 349, no, 11, 400, it=True, sans=True))
    decision(430, 2.05, "reuse A", "create A")
    decision(546, 2.35, "link V", "add V")
    # the example: the action matches, the variant does not
    f.g(2.70, R(430 - 56, 334, 58, 30, fill="none", stroke=GREEN, sw=2.6, rx=8), cls="a pop")
    f.g(2.80, R(546 - 2, 334, 58, 30, fill="none", stroke=GREEN, sw=2.6, rx=8), cls="a pop")
    f.g(2.85, ML(439, 408, ["Example: the step matches action A, “Open Report”,", "but its tap (x, y₂) differs from variant V₁,",
                             "so a new variant V₂ is added to A."], 12.5, 17, sans=True, fill="#333"))
    # 3. full memory library
    f.g(3.15, chip(664, 106, 48, 28, "T₁", T_FILL, T_INK, 14, it=True), cls="a pop")
    f.g(3.25, chip(734, 128, 42, 46, "A", A_FILL, A_INK, 18, it=True), cls="a pop")
    f.g(3.30, f.P("M712 120 L734 142", sw=1.8))
    f.g(3.40, chip(664, 168, 48, 28, "T₂", T_FILL, T_INK, 14, it=True), cls="a pop")
    f.g(3.45, f.P("M712 182 L734 160", sw=1.8))
    f.g(3.60, chip(798, 106, 48, 28, "V₁", V_FILL, V_INK, 14, it=True), f.P("M776 142 L798 120", sw=1.8), cls="a pop")
    f.g(3.70, chip(798, 168, 48, 28, "V₂", V_FILL, V_INK, 14, it=True), f.P("M776 160 L798 182", sw=1.8),
        R(794, 164, 56, 36, fill="none", stroke=GREEN, sw=2.4, rx=9), cls="a pop")
    f.g(3.55, T(755, 222, "Action Sharing", 12.5, 700, sans=True))
    f.g(3.80, T(755, 240, "Variant Preservation", 12.5, 700, sans=True))
    f.g(3.90, T(755, 272, "retrieval index", 12, it=True, fill=MUTED, sans=True),
        R(660, 284, 190, 44, fill=A_FILL, stroke=A_INK, sw=1.8, rx=10), IMG("embeddings", 668, 290, 32, 32),
        ML(778, 306, ["instruction", "embeddings"], 12.5, 16, w=700, sans=True))
    f.g(4.00, R(660, 340, 190, 76, fill=V_FILL, stroke=V_INK, sw=1.8, rx=10), IMG("knowledge", 667, 362, 33, 33),
        T(778, 357, "knowledge layer", 12.5, 700, sans=True),
        ML(778, 389, ["task summaries", "action descriptions", "topic pages"], 11, 16.5, sans=True, fill="#333"))
    # 4. runtime export: sizes on the 50-task AndroidWorld set (ablation study)
    bars = [("full library", "68.4 MiB", 68.374), ("runtime export", "6.80 MiB", 6.799), ("runtime library", "2.83 MiB", 2.832)]
    steps = [("keep_shots", ["screenshots stay", "on the cloud"], 36, 31, 942), ("compaction", ["compact UI", "records"], 58, 25, 962)]
    for i, (label, val, mib) in enumerate(bars):
        y = 104 + i * 104
        d = 4.35 + i * .45
        f.g(d, T(898, y + 8, label, 12.5, 700, "start", sans=True), T(1068, y + 8, val, 12, 700, "end", fill=RED if i == 2 else INK))
        f.g(d + .05, R(898, y + 22, max(4, 170 * mib / 68.374), 16, fill="#c3cad5" if i < 2 else "#f0a093", stroke=STROKE, sw=1.4, rx=3),
            cls="a draw")
        f.g(d + .05, R(898, y + 22, 170, 16, fill="none", stroke="#b9c1cc", sw=1, rx=3, dash="3 3"))
        if i < 2:
            ic, lines, iw, ih, tx = steps[i]
            f.g(d + .25, IMG(ic, 900, y + 67 - ih / 2, iw, ih), ML(tx, y + 67, lines, 11.5, 15.5, anchor="start", sans=True, fill="#333"))
    f.g(5.75, R(898, 382, 170, 52, fill="#fff", stroke=STROKE, sw=1.8, rx=10), IMG("smartphone", 900, 388, 40, 40),
        ML(1004, 408, ["−95.9% storage", "on the phone"], 12.5, 16, w=700, sans=True), cls="a pop")
    f.g(5.80, T(983, 446, "50-task AndroidWorld set", 10.5, it=True, fill=MUTED, sans=True))
    return f.svg()


# ---------------------------------------------------------------- (b) task retrieval

def retrieve():
    f = Fig("pb", 1100, 450, "Stage (b): task retrieval")
    title = "(b) Task Retrieval on the Phone"
    tw = len(title) * 11.4 + 40
    f.g(.05, R(3, 3, 1094, 444, fill=B_PANEL, stroke=STROKE, sw=2.4, rx=26),
        R(550 - tw / 2, 13, tw, 32, fill=B_TAB, stroke="none", rx=9), T(550, 29, title, 19, 700))
    # new instruction
    f.g(.15, R(22, 70, 156, 148, fill=L_FILL, stroke=L_INK, sw=2, rx=14), IMG("person_chat", 74, 78, 52, 52),
        T(100, 142, "new instruction q", 11.5, it=True, fill="#333"),
        R(32, 156, 136, 50, fill="#fff", stroke=L_INK, sw=1.4, rx=8), ML(100, 181, ["Create a contact", "named Bob"], 13, 17, w=700, sans=True),
        cls="a pop")
    f.g(.40, f.P("M178 144 L200 144"))
    # instruction retrieval
    f.g(.50, R(200, 60, 500, 270, fill="#fff", stroke=BLUE, sw=2.2, rx=14, dash="8 5"),
        badge(222, 84, 1), IMG("document_search", 238, 70, 28, 28), T(272, 84, "Instruction retrieval", 15, 700, "start", sans=True),
        T(686, 84, 's = α s<tspan dy="4" font-size="10">sem</tspan><tspan dy="-4"> + (1−α) s</tspan><tspan dy="4" font-size="10">lex</tspan>',
          13, anchor="end", raw=True),
        T(222, 112, "historical instruction", 11.5, it=True, anchor="start", fill=MUTED, sans=True),
        T(540, 112, "score s(q, qᵢ)", 11.5, it=True, anchor="start", fill=MUTED))
    rows = [("Create a contact named Alice", .92), ("Delete the contact named Bob", .84), ("Edit the contact named Alice", .76),
            ("Create a new calendar event", .57), ("Turn on airplane mode", None)]
    for i, (q, s) in enumerate(rows):
        cy = 140 + i * 36
        d = .65 + i * .1
        row = (f'<g class="a" style="--d:{d:.2f}s">{R(214, cy - 15, 442, 30, fill="#f6f9fd", stroke="#c9d6e6", sw=1.2, rx=8)}'
               f'{T(226, cy, q, 13, 500, "start", sans=True)}</g>')
        if s is not None:
            row += f'<g class="a draw" style="--d:{d + .25:.2f}s">{R(540, cy - 6, 110 * s, 12, fill=BLUE if i == 0 else "#9cc0ea", stroke="none", rx=3)}</g>'
        # the fourth instruction passes the threshold but ranks below the top K, so it fades out
        f.add(f'<g class="dim" style="--d2:1.75s">{row}</g>' if i == 3 else row)
        if s is None:
            f.g(1.45, f'<path d="M222 {cy} H380" stroke="{RED}" stroke-width="2.4"/>',
                T(540, cy, "s", 12, 700, "start", fill=RED, it=True), T(548.5, cy + 4.5, "sem", 10.5, 700, "start", fill=RED, sub=True),
                T(575, cy, "< τ: filtered", 12, 700, "start", fill=RED, sans=True))
    f.g(1.75, f'<path d="M664 127 h8 v98 h-8" stroke="{STROKE}" stroke-width="2" fill="none"/>',
        T(686, 176, "top K", 12.5, 700, extra=' transform="rotate(-90 686 176)"'))
    f.g(1.95, f.P("M700 176 L722 176"))
    f.g(2.05, R(722, 130, 96, 92, fill=L_FILL, stroke=L_INK, sw=2, rx=12), IMG("robot", 746, 136, 48, 48), T(770, 202, "Selector", 13, 700, sans=True),
        cls="a pop")
    f.g(2.10, T(770, 238, "model call", 11, it=True, fill=MUTED, sans=True))
    f.g(2.35, R(210, 121, 450, 38, fill="none", stroke=GREEN, sw=2.8, rx=10), check(658, 122, 9), cls="a pop")
    f.g(2.50, f.P("M818 176 L838 176"))
    # task record
    f.g(2.60, R(838, 62, 240, 284, fill=T_FILL, stroke=T_INK, sw=2.2, rx=14), T(852, 84, "Task record", 14, 700, "start", sans=True),
        chip(1046, 72, 22, 22, "T", "#fff", T_INK, 12, it=True, sw=1.4),
        T(852, 108, "q′ = Create a contact named Alice", 11.5, 500, "start", sans=True), cls="a pop")
    steps = [("Open Contacts", "1", "1"), ("Tap “Create contact”", "2", "1"), ("Type “Alice”", "3", "1"), ("Tap “Save”", "4", "2")]
    for i, (s, a, v) in enumerate(steps):
        cy = 146 + i * 46
        f.g(2.75 + i * .1, R(848, cy - 19, 220, 38, fill="#fff", stroke="#e1c977", sw=1.4, rx=8), badge(866, cy, i + 1, 9),
            T(882, cy, s, 12, 700, "start", sans=True),
            chip(1018, cy - 9, 20, 18, "A", A_FILL, A_INK, 10, it=True, sw=1.2), chip(1042, cy - 9, 20, 18, "V", V_FILL, V_INK, 10, it=True, sw=1.2))
    f.g(3.20, T(958, 334, "steps → action records & variants", 10.5, it=True, fill=MUTED, sans=True))
    # fallback
    f.g(3.35, f.P("M450 330 L450 352", dash="5 4", draw=False), T(458, 341, "nothing passes τ", 11, it=True, anchor="start", fill=MUTED, sans=True))
    f.g(3.45, R(200, 352, 500, 80, fill="#fbfcfe", stroke="#9aa3b2", sw=1.6, rx=14, dash="6 5"), IMG("book_knowledge", 212, 362, 58, 58),
        T(282, 374, "Knowledge retrieval", 13.5, 700, "start", sans=True),
        T(282, 394, "task summaries, action descriptions and topic pages", 12, 500, "start", sans=True, fill="#333"),
        T(282, 414, "no match → the base agent handles the instruction", 12, 500, "start", sans=True, fill=MUTED))
    f.g(3.60, f.P("M700 392 L958 392 L958 348", dash="5 4", draw=False), T(830, 380, "task record", 11, it=True, fill=MUTED, sans=True))
    return f.svg()


# ---------------------------------------------------------------- (c) reuse and applicability checking

def reuse():
    f = Fig("pc", 1100, 480, "Stage (c): reuse and applicability checking")
    title = "(c) Reuse & Applicability Checking for Each Candidate Step"
    tw = len(title) * 11.4 + 40
    f.g(.05, R(3, 3, 1094, 474, fill=C_PANEL, stroke=STROKE, sw=2.4, rx=26),
        R(550 - tw / 2, 13, tw, 32, fill=C_TAB, stroke="none", rx=9), T(550, 29, title, 19, 700),
        R(20, 58, 280, 404, fill="#fffaf4", stroke="none", rx=18))
    # phone: the current UI after each step
    px, py, pw, ph = 940, 96, 128, 228
    f.g(.10, T(px + pw / 2, 82, "current UI", 13.5, it=True, fill="#333"), phone(px, py, pw, ph, home_screen, 6, 12, 10))
    # 2. candidate step selection
    f.g(.15, badge(42, 82, 2), IMG("checklist", 58, 68, 28, 28), T(92, 82, "Candidate steps", 15, 700, "start", sans=True), IMG("robot", 262, 66, 30, 30))
    f.g(.30, R(32, 100, 256, 64, fill="#fff", stroke="#dcc6b0", sw=1.4, rx=10),
        T(42, 120, "q′", 12, 700, "start", it=True), T(62, 120, "Create a contact named", 12, 500, "start", sans=True),
        chip(222, 109, 56, 22, "Alice", "#fff", RED, 12, sans=True, sw=1.4),
        T(42, 146, "q", 12, 700, "start", it=True), T(62, 146, "Create a contact named", 12, 500, "start", sans=True),
        chip(222, 135, 56, 22, "Bob", "#e3eefb", BLUE_DEEP, 12, sans=True, sw=1.4))
    f.g(.55, f.P("M226 120 L274 120", RED, sw=2.2, arrow=False))
    f.g(.65, T(32, 186, "steps of the retrieved task record", 11, it=True, anchor="start", fill=MUTED, sans=True))
    rows = [("Open Contacts", True), ("Tap “Create contact”", True), ("Type “Alice”", False), ("Tap “Save”", True)]
    for i, (s, keep) in enumerate(rows):
        cy = 216 + i * 44
        f.g(.75 + i * .1, R(32, cy - 18, 256, 36, fill="#fff", stroke="#e1c977", sw=1.4, rx=8), badge(50, cy, i + 1, 9),
            T(66, cy, s, 12, 700, "start", sans=True))
        if keep:
            f.g(1.25, R(226, cy - 10, 54, 20, fill="#e7f4ec", stroke=GREEN, sw=1.2, rx=10), T(253, cy, "reuse?", 10.5, 700, fill=GREEN, sans=True))
        else:
            f.g(1.35, R(222, cy - 10, 58, 20, fill="#fbe5e2", stroke=RED, sw=1.2, rx=10), T(251, cy, "change", 10.5, 700, fill=RED, sans=True),
                cls="a pop")
    f.g(1.45, ML(160, 410, ["A model marks the steps that", "must change for q; the others", "become candidate steps."],
                 11.5, 17, sans=True, fill="#333"))
    # 3-4. per-step lane
    f.g(1.50, loop_glyph(f, 330, 76), T(346, 76, "for each candidate step: check, then reuse", 13, it=True, anchor="start", fill="#333"))
    cols = [318, 468, 618, 768]
    steps = [("Open", "Contacts"), ("Tap", "Create contact"), ("Type", "“Alice”"), ("Tap", "Save")]
    t0 = [1.60, 2.40, 3.20, 4.10]
    screens = [contacts_screen, form_screen(""), form_screen("Bob"), saved_screen]
    for i, x in enumerate(cols):
        cx, d = x + 66, t0[i]
        f.g(d, R(x, 92, 132, 48, fill=T_FILL, stroke=T_INK, sw=1.8, rx=9), badge(x + 15, 106, i + 1, 9),
            T(x + 30, 106, steps[i][0], 12.5, 700, "start", sans=True), T(cx, 126, steps[i][1], 12.5, 700, sans=True), cls="a pop")
        if i == 2:
            f.g(d + .05, f'<path d="M{cx - 22} 126 H{cx + 22}" stroke="{RED}" stroke-width="2"/>')
        f.g(d + .12, f.P(f"M{cx} 140 L{cx} 156", sw=2))
        if i == 2:
            f.g(d + .22, R(x, 158, 132, 48, fill="#f4f5f7", stroke="#9aa3b2", sw=1.4, rx=9, dash="5 4"),
                ML(cx, 182, ["not a candidate:", "needs a new value"], 11, 15.5, sans=True, fill=MUTED))
        else:
            f.g(d + .22, R(x, 158, 132, 48, fill="#fff", stroke=ORANGE, sw=1.8, rx=9, dash="6 4"), IMG("shield_check", x + 6, 164, 36, 36),
                T(x + 46, 175, "applicable", 11.5, 500, "start", fill=MUTED, sans=True), T(x + 46, 192, "✓ accept", 13, 700, "start", fill=GREEN, sans=True),
                cls="a pop")
        f.g(d + .36, f.P(f"M{cx} 206 L{cx} 222", sw=2))
        if i == 2:
            f.g(d + .46, R(x, 224, 132, 48, fill="#fff", stroke=L_INK, sw=1.8, rx=9), IMG("robot", x + 5, 229, 38, 38),
                T(x + 46, 241, "base agent", 12, 700, "start", sans=True), T(x + 46, 258, "types “Bob”", 11.5, 500, "start", sans=True), cls="a pop")
        else:
            f.g(d + .46, R(x, 224, 132, 48, fill=L_FILL, stroke=L_INK, sw=1.8, rx=9), IMG("replay", x + 6, 230, 36, 36),
                T(x + 46, 241, "reuse", 13, 700, "start", sans=True), T(x + 46, 258, "stored action", 11, 500, "start", fill=MUTED, sans=True),
                cls="a pop")
        f.g(d + .62, phone(px, py, pw, ph, screens[i], 6, 12, 10), cls="a fade")
    f.g(3.85, f.P("M700 292 L822 292", ORANGE), T(694, 292, "locate the next step, resume reuse", 12, 700, "end", fill=ORANGE, sans=True))
    # what the check compares, for step 4
    f.g(4.30, R(318, 316, 582, 146, fill="#fff", stroke=ORANGE, sw=2, rx=14), IMG("shield_check", 330, 324, 32, 32),
        T(370, 340, "Applicability check for step 4", 13.5, 700, "start", sans=True))
    f.g(4.45, T(457, 368, "stored variant of “Tap Save”", 11.5, it=True, fill=MUTED, sans=True),
        R(330, 378, 254, 32, fill=V_FILL, stroke=V_INK, sw=1.6, rx=8), T(457, 394, "tap (x, y) → Button “Save”, enabled", 12, 700, sans=True))
    f.g(4.60, T(758, 368, "current UI, hit-test at (x, y)", 11.5, it=True, fill=MUTED, sans=True),
        R(632, 378, 254, 32, fill="#fff", stroke=STROKE, sw=1.6, rx=8), T(759, 394, "Button “Save”, enabled", 12, 700, sans=True))
    f.g(4.75, T(608, 394, "=", 20, 700, fill=GREEN), cls="a pop")
    f.g(4.85, T(609, 434, "Key UI evidence matches (control type, text, bounds, state) → accept and reuse the tap.", 12, 700, fill=GREEN, sans=True))
    return f.svg()


# ---------------------------------------------------------------- Action Sharing and Variant Preservation (paper Figure 1)

def concept():
    f = Fig("cs", 1100, 436, "Action Sharing and Variant Preservation example")
    f.add(R(14, 14, 442, 408, fill="#f2f8f1", stroke="none", rx=18), R(468, 14, 308, 408, fill="#f2f8f1", stroke="none", rx=18),
          R(788, 14, 298, 408, fill="#fbf1ec", stroke="none", rx=18))
    s = []

    def layer(k, cap, parts):
        s.append(f'<g data-layer="{k}" data-cap="{esc(cap)}">{"".join(parts)}</g>')

    def g(d, *body, cls="a"):
        return f'<g class="{cls}" style="--d:{d:.2f}s">{"".join(body)}</g>'

    # step 1: two tasks share their first step
    p = []
    for r, (tag, name, order, tail, sheet) in enumerate([
            ("T₁", "Share Report", ["Report", "Notes", "Plan"], ["Share"], share_sheet),
            ("T₂", "Save Report", ["Notes", "Plan", "Report"], ["Save a", "copy"], save_sheet)]):
        y0, d0 = 26 + r * 196, .1 + r * 1.3
        cy = y0 + 30 + 75
        p.append(g(d0, chip(28, y0, 30, 22, tag, T_FILL, T_INK, 13, it=True, sw=1.6), T(66, y0 + 11, name, 14, 700, "start", sans=True)))
        p.append(g(d0 + .1, phone(28, y0 + 30, 86, 150, files_screen(order, hl="Report", tap="Report"))))
        # the label sits on the side the dashed "share" line does not use (row 1 above, row 2 below the arrow)
        p.append(g(d0 + .4, f.P(f"M114 {cy} L194 {cy}", BLUE_DEEP), T(154, cy - 12 if r == 0 else cy + 13, "Open Report", 12, 700, fill=BLUE_DEEP, sans=True)))
        p.append(g(d0 + .6, phone(194, y0 + 30, 86, 150, report_screen("share" if r == 0 else "save"))))
        p.append(g(d0 + .8, f.P(f"M280 {cy} L326 {cy}"), ML(303, cy - 16 if len(tail) == 1 else cy - 20, tail, 11.5, 13, w=700, sans=True)))
        p.append(g(d0 + .95, sheet(332, cy - 46), cls="a pop"))
    layer(0, "<b>Two tasks, one shared step.</b> Sharing a report and saving a copy are different tasks, but both begin by opening the "
             "report. Task 2 ran after the file list changed, so Report sat in the bottom row. (Illustrative example, following Figure 1 of the paper.)", p)

    # step 2: both Open Report steps point to one action record; it keeps one variant per execution
    def mini_list(x, y, hl_row):
        rows = "".join(R(x + 4, y + 5 + i * 13, 44, 10, fill="#fbe3f3" if i == hl_row else "#fff",
                         stroke="#d07fc0" if i == hl_row else "#d3dbe6", sw=1, rx=2) for i in range(3))
        return R(x, y, 52, 46, fill="#fff", stroke=STROKE, sw=1.4, rx=5) + rows + tapmark(x + 41, y + 10 + hl_row * 13, TAP)

    cy1, cy2 = 131, 327
    p = [g(.10, C(154, cy1, 4, fill=BLUE_DEEP, stroke="none"), C(154, cy2, 4, fill=BLUE_DEEP, stroke="none"),
           f.P(f"M154 {cy1} V216 M154 {cy2} V216 H462 V118 H478", BLUE_DEEP, sw=2, dash="6 5", draw=False),
           T(360, 205, "share one action record", 11.5, 700, fill=BLUE_DEEP, it=True, sans=True)),
         g(.45, R(480, 30, 284, 176, fill="#e9f2fb", stroke=BLUE, sw=2.4, rx=12), chip(492, 40, 22, 22, "A", "#fff", BLUE, 12, it=True, sw=1.4),
           T(522, 51, "Shared action record", 12.5, 400, "start", it=True, sans=True),
           IMG("doc_tap", 600, 62, 44, 47), T(622, 126, "Open Report", 20, 700, sans=True), cls="a pop"),
         g(.70, R(494, 144, 256, 24, fill="#fff", stroke="#b9cde6", sw=1.2, rx=6), T(504, 156, "Action type:", 12, 500, "start", sans=True),
           T(740, 156, "click", 12.5, 700, "end", sans=True)),
         g(.85, R(494, 174, 256, 24, fill="#fff", stroke="#b9cde6", sw=1.2, rx=6), T(504, 186, "Target:", 12, 500, "start", sans=True),
           T(740, 186, "Report", 12.5, 700, "end", sans=True)),
         g(1.05, f'<path d="M622 206 V224 H488 V362" stroke="{STROKE}" stroke-width="2" fill="none"/>',
           f.P("M488 284 L498 284", sw=2), f.P("M488 362 L498 362", sw=2))]
    for k, (vy, sub, label, row) in enumerate([(252, "₁", "Report in top row", 0), (330, "₂", "Report in bottom row", 2)]):
        p.append(g(1.20 + k * .2, R(500, vy, 264, 64, fill=V_FILL, stroke=V_INK, sw=2, rx=10),
                   chip(510, vy + 18, 40, 28, "V" + sub, "#fff", V_INK, 14, it=True, sw=1.6),
                   T(562, vy + 22, f"tap (x, y{sub})", 12, 700, "start"), T(562, vy + 42, label, 11.5, 500, "start", sans=True, fill="#333"),
                   mini_list(702, vy + 9, row), cls="a pop"))
    p.append(g(1.65, T(632, 408, "Variant Preservation", 12.5, 700, sans=True)))
    layer(1, "<b>Action Sharing and Variant Preservation.</b> The shared step of both tasks is stored once, as action record A “Open Report” "
             "(a click on Report). A keeps one variant per distinct execution: V₁ taps (x, y₁), where Report was in the top row; V₂ taps (x, y₂), "
             "where it was in the bottom row.", p)
    # step 3: check the stored variants on the current UI
    order = ["Notes", "Plan", "Report"]
    p = [g(.10, T(937, 32, "Current UI", 13.5, 700, sans=True), phone(894, 46, 86, 150, files_screen(order))),
         g(.80, f.P("M764 284 L798 284", V_INK, sw=2.2), cls="a fade"),
         g(1.60, f.P("M764 362 L798 362", V_INK, sw=2.2), cls="a fade"),
         g(.55, phone(894, 46, 86, 150, files_screen(order, marks=[("Notes", RED)])), T(992, 104, "V₁", 13, 700, "start", it=True, fill=RED), cross(1024, 104, 7),
           cls="a fade"),
         g(.75, R(862, 206, 150, 24, fill=C_BOX, stroke=ORANGE, sw=1.8, rx=12), T(937, 218, "Applicability check", 12, 700, sans=True)),
         g(.80, T(852, 242, "stored", 11, 500, it=True, fill=MUTED, sans=True), T(968, 242, "current UI", 11, 500, it=True, fill=MUTED, sans=True)),
         g(.95, R(800, 250, 274, 68, fill="#fff", stroke=STROKE, sw=1.6, rx=10, dash="6 4"),
           chip(812, 258, 80, 24, "Report", V_FILL, V_INK, 12, sans=True, sw=1.4), T(911, 270, "≠", 18, 700, fill=RED),
           chip(930, 258, 80, 24, "Notes", "#fff", STROKE, 12, sans=True, sw=1.4), cross(1048, 270, 9)),
         g(1.20, T(937, 302, "Reject: the tap would hit Notes", 12, 700, fill=RED, it=True, sans=True)),
         g(1.55, phone(894, 46, 86, 150, files_screen(order, hl="Report", marks=[("Notes", RED), ("Report", GREEN)])),
           T(992, 104, "V₁", 13, 700, "start", it=True, fill=RED), cross(1024, 104, 7),
           T(992, 150, "V₂", 13, 700, "start", it=True, fill=GREEN), check(1024, 150, 7), cls="a fade"),
         g(1.75, R(800, 328, 274, 68, fill="#fff", stroke=STROKE, sw=1.6, rx=10, dash="6 4"),
           chip(812, 336, 80, 24, "Report", V_FILL, V_INK, 12, sans=True, sw=1.4), T(911, 348, "=", 18, 700, fill=GREEN),
           chip(930, 336, 80, 24, "Report", "#fff", STROKE, 12, sans=True, sw=1.4), check(1048, 348, 9)),
         g(2.00, T(937, 380, "Accept: same target", 12, 700, fill=GREEN, it=True, sans=True)),
         g(2.30, R(866, 398, 142, 22, fill=GREEN, stroke="none", rx=11), T(937, 409, "Reuse V₂", 12.5, 700, fill="#fff", sans=True), cls="a pop")]
    layer(2, "<b>Applicability checking.</b> A new task retrieves Task 1, whose step points to V₁. Each variant of A is checked against the "
             "current UI: V₁’s tap would land on Notes, so it is rejected; V₂’s tap hits Report, so V₂ is reused.", p)
    f.add(*s)
    return f.svg()


FIGS = {"overview": overview, "construct": construct, "retrieve": retrieve, "reuse": reuse, "concept": concept}


def main():
    html = INDEX.read_text(encoding="utf-8")
    for name, fn in FIGS.items():
        pat = re.compile(rf"(<!-- svg:{name} -->).*?(<!-- /svg:{name} -->)", re.S)
        if not pat.search(html):
            raise SystemExit(f"marker <!-- svg:{name} --> not found in index.html")
        html = pat.sub(lambda m: m.group(1) + fn() + m.group(2), html)
    INDEX.write_text(html, encoding="utf-8")
    print("wrote", ", ".join(FIGS), "into", INDEX)


if __name__ == "__main__":
    main()
