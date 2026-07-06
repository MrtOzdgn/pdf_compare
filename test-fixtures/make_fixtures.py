import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pdfgen import Page

OUT = os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 840
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']
LETTER_YFRACS = [0.10 + i * 0.14 for i in range(6)]  # 0.10..0.80
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8']
NUMBER_XFRACS = [0.08 + j * 0.12 for j in range(8)]  # 0.08..0.92

FRAME = dict(x0=50, y0=50, x1=1150, y1=790)  # pdf coords, y up


def draw_frame(p):
    p.rect(FRAME['x0'], FRAME['y0'], FRAME['x1'] - FRAME['x0'], FRAME['y1'] - FRAME['y0'])


def draw_grid(p, orientation='letters_vertical'):
    """orientation: 'letters_vertical' -> letters on left/right edges, numbers
    on top/bottom. 'letters_horizontal' -> swapped (numbers on left/right,
    letters on top/bottom) to test axis-orientation independence."""
    left_x, right_x = 20, 1180
    top_y, bottom_y = p.yfrac_to_pdf(0.0238), p.yfrac_to_pdf(0.976)
    if orientation == 'letters_vertical':
        for ch, yf in zip(LETTERS, LETTER_YFRACS):
            y = p.yfrac_to_pdf(yf)
            p.text(left_x, y, 10, ch)
            p.text(right_x, y, 10, ch)
        for ch, xf in zip(NUMBERS, NUMBER_XFRACS):
            x = p.xfrac_to_pdf(xf)
            p.text(x, top_y, 10, ch)
            p.text(x, bottom_y, 10, ch)
    else:
        for ch, yf in zip(NUMBERS[:6], LETTER_YFRACS):
            y = p.yfrac_to_pdf(yf)
            p.text(left_x, y, 10, ch)
            p.text(right_x, y, 10, ch)
        for ch, xf in zip(LETTERS[:8] if len(LETTERS) >= 8 else LETTERS, NUMBER_XFRACS):
            x = p.xfrac_to_pdf(xf)
            p.text(x, top_y, 10, ch)
            p.text(x, bottom_y, 10, ch)


TB_BOX = dict(x=820, y=60, w=320, h=215)  # covers title block + revision table


def draw_title_block(p, rev, date, shuffle=False):
    x, y, w, h = TB_BOX['x'], TB_BOX['y'], TB_BOX['w'], TB_BOX['h']
    p.rect(x, y, w, h)
    p.line(x, y + 150, x + w, y + 150)  # separates revision table (top) from title fields
    p.text(x + 10, y + 255 - 180, 8, "REV")
    p.text(x + 60, y + 255 - 180, 8, "DATE")
    p.text(x + 150, y + 255 - 180, 8, "DESCRIPTION")
    p.text(x + 10, y + 255 - 195, 8, rev)
    p.text(x + 60, y + 255 - 195, 8, date)
    p.text(x + 150, y + 255 - 195, 8, "SEE NOTES")
    if rev == 'C':
        p.text(x + 10, y + 255 - 208, 8, "B")
        p.text(x + 60, y + 255 - 208, 8, "2025-11-03")
        p.text(x + 150, y + 255 - 208, 8, "INITIAL RELEASE")

    if not shuffle:
        fields = [
            (12, "ACME ENGINEERING CO."),
            (11, "BRACKET MOUNT ASSY"),
            (8, "DWG NO: 4471-A"),
            (8, "SCALE: 1:2"),
            (8, f"DATE: {date}"),
            (8, "DRAWN BY: J. SMITH"),
            (8, "CHECKED BY: R. LEE"),
        ]
        yy = y + 130
        for size, txt in fields:
            p.text(x + 10, yy, size, txt)
            yy -= 18
        p.text(x + 180, y + 130 - 18 * 2, 8, "SIZE: A2")
        p.text(x + 180, y + 130 - 18 * 3, 8, f"REV: {rev}")
    else:
        # Same information, deliberately different relative positions/order —
        # simulates an antet redesign between revisions.
        p.text(x + 10, y + 130, 12, "ACME ENGINEERING CO.")
        p.text(x + 10, y + 108, 11, "BRACKET MOUNT ASSY")
        p.text(x + 180, y + 90, 8, "CHECKED BY: R. LEE")
        p.text(x + 10, y + 90, 8, "DRAWN BY: J. SMITH")
        p.text(x + 10, y + 72, 8, "DWG NO: 4471-A")
        p.text(x + 180, y + 72, 8, "SIZE: A2")
        p.text(x + 10, y + 54, 8, "SCALE: 1:2")
        p.text(x + 180, y + 54, 8, f"REV: {rev}")
        p.text(x + 10, y + 36, 8, f"DATE: {date}")


def draw_geometry_and_dims(p, dim_value, hole_cx, add_dim=None, remove_dim=None,
                            body_date=None, body_rev=None):
    p.rect(150, 250, 500, 430)
    p.line(560, 680, 610, 630)
    p.text(500, 690, 8, "20 DEG CHAMFER")

    p.circle(hole_cx, 470, 22, fill=True)
    p.text(hole_cx - 15, 500, 8, "R10 TYP")

    p.line(150, 220, 150, 235)
    p.line(650, 220, 650, 235)
    p.line(150, 227, 650, 227)
    p.text(380, 233, 10, dim_value)

    if add_dim:
        p.text(add_dim[0], add_dim[1], 9, add_dim[2])
    if remove_dim:
        p.text(remove_dim[0], remove_dim[1], 9, remove_dim[2])

    if body_date:
        p.text(200, 300, 8, body_date)
    if body_rev:
        p.text(200, 282, 8, body_rev)


def draw_simple_notes(p):
    """Plain, unchanged-across-revisions notes block: header + 4 numbered
    items, all at fixed y (no reflow) — used by fixtures that aren't
    specifically testing note-editing/reflow."""
    p.text(180, 718, 9, "NOTLAR:")
    p.text(180, 700, 9, "1. SHARP EDGES TO BE BROKEN 0.5 MAX")
    p.text(180, 682, 9, "2. ALL DIMENSIONS IN MM UNLESS NOTED")
    p.text(180, 664, 9, "3. SURFACE FINISH 3.2 MICRON MAX")
    p.text(180, 646, 9, "4. MATERIAL PER SPEC XYZ-100")


def save(page, name):
    path = os.path.join(OUT, name)
    page.save(path)
    print("wrote", path, os.path.getsize(path), "bytes")


# ---------------------------------------------------------------------------
# Fixture set A: full grid, letters vertical / numbers horizontal. Exercises
# every diff category in one pair, including a genuine reflow: note 3 grows
# to two lines, pushing note 4 down to a new y position with identical text.
# ---------------------------------------------------------------------------
old = Page(W, H)
draw_frame(old)
draw_grid(old, 'letters_vertical')
draw_title_block(old, rev='B', date='2025-11-03')
draw_geometry_and_dims(
    old, dim_value="125.0", hole_cx=400,
    remove_dim=(900, 500, "OLD-ONLY CALLOUT 8.0"),
    body_date="2025-11-03", body_rev="REV A",  # bare date/rev -> both should be ignored
)
old.text(180, 718, 9, "NOTLAR:")
old.text(180, 700, 9, "1. SHARP EDGES TO BE BROKEN 0.5 MAX")
old.text(180, 682, 9, "2. ALL DIMENSIONS IN MM UNLESS NOTED")
old.text(180, 664, 9, "3. SURFACE FINISH 3.2 MICRON MAX")
old.text(180, 646, 9, "4. MATERIAL PER SPEC XYZ-100")
save(old, 'gridA_old.pdf')

new = Page(W, H)
draw_frame(new)
draw_grid(new, 'letters_vertical')
draw_title_block(new, rev='C', date='2025-12-01')
draw_geometry_and_dims(
    new, dim_value="130.0", hole_cx=460,  # dimension changed + hole moved 60pt
    add_dim=(950, 320, "NEW-ONLY CALLOUT 12.0"),
    body_date="2025-12-01",  # date-like change -> should be ignored
    body_rev="REV B",  # revision-like change -> should be ignored
)
new.text(180, 718, 9, "NOTLAR:")
new.text(180, 700, 9, "1. SHARP EDGES TO BE BROKEN 0.5 MAX")
new.text(180, 682, 9, "2. ALL DIMENSIONS IN MM UNLESS NOTED")
new.text(180, 664, 9, "3. SURFACE FINISH 1.6 MICRON MAX,")  # edited + wraps to 2 lines
new.text(180, 646, 9, "POLISHED PER PROCEDURE QX-9")         # continuation of note 3
new.text(180, 628, 9, "4. MATERIAL PER SPEC XYZ-100")        # note 4 pushed down, same text
save(new, 'gridA_new.pdf')

# ---------------------------------------------------------------------------
# Fixture set B: axis-swapped grid (numbers vertical / letters horizontal) —
# same body content, to check the tool re-derives orientation correctly.
# ---------------------------------------------------------------------------
old_b = Page(W, H)
draw_frame(old_b)
draw_grid(old_b, 'letters_horizontal')
draw_title_block(old_b, rev='B', date='2025-11-03')
draw_geometry_and_dims(old_b, dim_value="125.0", hole_cx=400)
draw_simple_notes(old_b)
save(old_b, 'gridB_old.pdf')

new_b = Page(W, H)
draw_frame(new_b)
draw_grid(new_b, 'letters_horizontal')
draw_title_block(new_b, rev='C', date='2025-12-01')
draw_geometry_and_dims(new_b, dim_value="130.0", hole_cx=400)
draw_simple_notes(new_b)
save(new_b, 'gridB_new.pdf')

# ---------------------------------------------------------------------------
# Fixture set C: no reference grid at all -> fallback path.
# ---------------------------------------------------------------------------
old_c = Page(W, H)
draw_frame(old_c)
draw_title_block(old_c, rev='B', date='2025-11-03')
draw_geometry_and_dims(old_c, dim_value="125.0", hole_cx=400)
draw_simple_notes(old_c)
save(old_c, 'nogrid_old.pdf')

new_c = Page(W, H)
draw_frame(new_c)
draw_title_block(new_c, rev='C', date='2025-12-01')
draw_geometry_and_dims(new_c, dim_value="130.0", hole_cx=400)
draw_simple_notes(new_c)
save(new_c, 'nogrid_new.pdf')

# ---------------------------------------------------------------------------
# Fixture set D: antet internal layout completely reshuffled between
# revisions, everything else byte-identical -> must produce ZERO reported
# lines from the title block (this is the original bug scenario).
# ---------------------------------------------------------------------------
old_d = Page(W, H)
draw_frame(old_d)
draw_grid(old_d, 'letters_vertical')
draw_title_block(old_d, rev='B', date='2025-11-03', shuffle=False)
draw_geometry_and_dims(old_d, dim_value="125.0", hole_cx=400)
draw_simple_notes(old_d)
save(old_d, 'antetshift_old.pdf')

new_d = Page(W, H)
draw_frame(new_d)
draw_grid(new_d, 'letters_vertical')
draw_title_block(new_d, rev='B', date='2025-11-03', shuffle=True)
draw_geometry_and_dims(new_d, dim_value="125.0", hole_cx=400)
draw_simple_notes(new_d)
save(new_d, 'antetshift_new.pdf')

print("done")
