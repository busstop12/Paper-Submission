"""Builds the tile sheet for the hero background: a mosaic of the real-phone task executions.

Each run in static/cases/ is drawn as a phone in five states (the screen before step 1, a tap on that step's target, the
screen before step 2, a tap on its target, the final screen). The sheet has one row per run, in the order of cases.js,
and one column per state. The page draws the moving mosaic from it on a canvas (see "Background" in the page script).
Uses ImageMagick. Usage:

  python3 -I website/tools/build_bg_tiles.py website

Writes static/bg/tiles.webp.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCREEN_W = 170             # phone screen in the sheet, px (the case frames are 540x1187)
BEZEL = 7
INK, TAP = "#1c2130", "#E8893A"
QUALITY = 72

# The five states of a run: (frame index, tap on step k or None). Their durations are set in the page script.
STATES = [(0, None), (0, 0), (1, None), (1, 1), (2, None)]


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True, capture_output=True)


def load_cases(site):
    js = (site / "static" / "cases" / "cases.js").read_text()
    return json.loads(js[js.index("["):js.rindex("]") + 1])


def tile(site, case, frame, tap, out):
    """The screenshot in a phone bezel, with an orange tap mark on the step's target."""
    sw, sh = SCREEN_W, round(SCREEN_W * 1187 / 540)
    tw, th = sw + 2 * BEZEL, sh + 2 * BEZEL
    draw = []
    box = case["steps"][tap]["box"] if tap is not None and tap < len(case["steps"]) else None
    if box:
        cx, cy = (box[0] + box[2]) / 2000 * sw, (box[1] + box[3]) / 2000 * sh
        draw = ["-fill", "rgba(232,137,58,.35)", "-stroke", TAP, "-strokewidth", 3,
                "-draw", f"circle {cx:.1f},{cy:.1f} {cx + 17:.1f},{cy:.1f}",
                "-fill", TAP, "-stroke", "none", "-draw", f"circle {cx:.1f},{cy:.1f} {cx + 6:.1f},{cy:.1f}"]
    magick("-size", f"{tw}x{th}", "xc:none", "-fill", INK, "-draw", f"roundrectangle 0,0 {tw - 1},{th - 1} 24,24",
           "(", site / case["frames"][frame], "-resize", f"{sw}x{sh}!", *draw,
           "(", "-size", f"{sw}x{sh}", "xc:black", "-fill", "white", "-draw", f"roundrectangle 0,0 {sw - 1},{sh - 1} 17,17", ")",
           "-alpha", "off", "-compose", "CopyOpacity", "-composite", ")",
           "-compose", "over", "-geometry", f"+{BEZEL}+{BEZEL}", "-composite", out)


def build(site):
    cases = load_cases(site)
    out = site / "static" / "bg"
    out.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="bg_tiles_"))
    try:
        rows = []
        for c in cases:
            row = []
            for s, (frame, tap) in enumerate(STATES):
                row.append(work / f"{c['no']}_{s}.png")
                tile(site, c, frame, tap, row[-1])
            rows.append(["(", *row, "-background", "none", "+append", ")"])
        magick(*[a for r in rows for a in r], "-background", "none", "-append", "-strip",
               "-quality", QUALITY, "-define", "webp:method=6", "-define", "webp:alpha-quality=60", out / "tiles.webp")
    finally:
        shutil.rmtree(work)
    print(f"{out / 'tiles.webp'}: {(out / 'tiles.webp').stat().st_size / 1024:.0f} KiB, {len(cases)} runs x {len(STATES)} states")


if __name__ == "__main__":
    build(Path(sys.argv[1]))
