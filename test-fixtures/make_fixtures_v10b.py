import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pdfgen import Page, save_pdf
import make_fixtures as mf

OUT = mf.OUT
W, H = mf.W, mf.H


def save1(page, name):
    path = os.path.join(OUT, name)
    save_pdf([page], path)
    print("wrote", path, os.path.getsize(path), "bytes")


def bom_header(p, x0=700, y=760):
    p.text(x0, y, 8, "ITEM")
    p.text(x0 + 60, y, 8, "QTY")
    p.text(x0 + 110, y, 8, "DESCRIPTION")


def bom_row(p, y, item, qty, desc, x0=700):
    p.text(x0, y, 8, item)
    p.text(x0 + 60, y, 8, qty)
    p.text(x0 + 110, y, 8, desc)


# ---------------------------------------------------------------------------
# M: BOM table — a new row simply APPENDED at the end (no shift of existing
# rows). Clean case: expect the new row's cells reported as added, nothing
# else touched.
# ---------------------------------------------------------------------------
old_m = Page(W, H)
mf.draw_frame(old_m)
mf.draw_grid(old_m, 'letters_vertical')
mf.draw_title_block(old_m, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(old_m, dim_value="125.0", hole_cx=400)
bom_header(old_m)
bom_row(old_m, 740, "1", "2", "BOLT M6X20")
bom_row(old_m, 720, "2", "4", "WASHER M6")
save1(old_m, 'bomappend_old.pdf')

new_m = Page(W, H)
mf.draw_frame(new_m)
mf.draw_grid(new_m, 'letters_vertical')
mf.draw_title_block(new_m, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(new_m, dim_value="125.0", hole_cx=400)
bom_header(new_m)
bom_row(new_m, 740, "1", "2", "BOLT M6X20")
bom_row(new_m, 720, "2", "4", "WASHER M6")
bom_row(new_m, 700, "3", "1", "BRACKET PLATE")
save1(new_m, 'bomappend_new.pdf')


# ---------------------------------------------------------------------------
# N: BOM table — a single cell value edited in place (qty 4 -> 6), no
# structural change. Should behave like any other dimension edit.
# ---------------------------------------------------------------------------
old_n = Page(W, H)
mf.draw_frame(old_n)
mf.draw_grid(old_n, 'letters_vertical')
mf.draw_title_block(old_n, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(old_n, dim_value="125.0", hole_cx=400)
bom_header(old_n)
bom_row(old_n, 740, "1", "2", "BOLT M6X20")
bom_row(old_n, 720, "2", "4", "WASHER M6")
save1(old_n, 'bomqtyedit_old.pdf')

new_n = Page(W, H)
mf.draw_frame(new_n)
mf.draw_grid(new_n, 'letters_vertical')
mf.draw_title_block(new_n, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(new_n, dim_value="125.0", hole_cx=400)
bom_header(new_n)
bom_row(new_n, 740, "1", "2", "BOLT M6X20")
bom_row(new_n, 720, "2", "6", "WASHER M6")  # 4 -> 6
save1(new_n, 'bomqtyedit_new.pdf')


# ---------------------------------------------------------------------------
# O: BOM table — a row INSERTED in the middle, cascading every row below it
# down by one slot and renumbering ITEM #s. This is the genuinely hard case:
# short duplicate digits (item numbers, quantities) scattered across a table
# have no per-cell identity for a position-based differ to track — expect a
# plausible but not necessarily "perfect" result (documented limitation, not
# a bug to fix). Recorded here so the actual behavior is known and stable.
# ---------------------------------------------------------------------------
old_o = Page(W, H)
mf.draw_frame(old_o)
mf.draw_grid(old_o, 'letters_vertical')
mf.draw_title_block(old_o, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(old_o, dim_value="125.0", hole_cx=400)
bom_header(old_o)
bom_row(old_o, 740, "1", "2", "BOLT M6X20")
bom_row(old_o, 720, "2", "4", "WASHER M6")
bom_row(old_o, 700, "3", "1", "BRACKET PLATE")
save1(old_o, 'bominsert_old.pdf')

new_o = Page(W, H)
mf.draw_frame(new_o)
mf.draw_grid(new_o, 'letters_vertical')
mf.draw_title_block(new_o, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(new_o, dim_value="125.0", hole_cx=400)
bom_header(new_o)
bom_row(new_o, 740, "1", "2", "BOLT M6X20")
bom_row(new_o, 720, "2", "1", "NUT M6")          # inserted
bom_row(new_o, 700, "3", "4", "WASHER M6")       # shifted down one slot
bom_row(new_o, 678, "4", "1", "BRACKET PLATE")   # shifted down one slot
save1(new_o, 'bominsert_new.pdf')


# ---------------------------------------------------------------------------
# P: dense dimension stress — five closely-spaced (40pt apart) dimension
# values on one line; only the middle one changes value AND shifts slightly
# (a realistic small correction), all neighbors stay byte-identical.
# ---------------------------------------------------------------------------
def draw_dense_row(p, values, base_x=180, y=600, dx=40, offsets=None):
    offsets = offsets or {}
    for i, v in enumerate(values):
        p.text(base_x + i * dx + offsets.get(i, 0), y, 8, v)


old_p = Page(W, H)
mf.draw_frame(old_p)
mf.draw_grid(old_p, 'letters_vertical')
mf.draw_title_block(old_p, rev='B', date='2025-11-03')
draw_dense_row(old_p, ["5.0", "6.0", "7.0", "8.0", "9.0"], y=600)
save1(old_p, 'dense_old.pdf')

new_p = Page(W, H)
mf.draw_frame(new_p)
mf.draw_grid(new_p, 'letters_vertical')
mf.draw_title_block(new_p, rev='B', date='2025-11-03')
# middle value changes AND nudges 3pt right (small real-world correction);
# all four neighbors stay byte-identical at their exact original slots.
draw_dense_row(new_p, ["5.0", "6.0", "7.2", "8.0", "9.0"], y=600, offsets={2: 3})
save1(new_p, 'dense_new.pdf')


# ---------------------------------------------------------------------------
# Q: larger sheet with a denser reference grid (10 letters x 12 numbers) —
# checks detectGrid scales past the small 6x8 grid used everywhere else.
# ---------------------------------------------------------------------------
BIG_W, BIG_H = 2000, 1400
BIG_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']  # 10, skip I
BIG_LETTER_YFRACS = [0.06 + i * 0.09 for i in range(10)]
BIG_NUMBERS = [str(i) for i in range(1, 13)]  # 1..12
BIG_NUMBER_XFRACS = [0.05 + j * 0.078 for j in range(12)]


def draw_big_grid(p):
    left_x, right_x = 25, BIG_W - 25
    top_y, bottom_y = p.yfrac_to_pdf(0.018), p.yfrac_to_pdf(0.982)
    for ch, yf in zip(BIG_LETTERS, BIG_LETTER_YFRACS):
        y = p.yfrac_to_pdf(yf)
        p.text(left_x, y, 11, ch)
        p.text(right_x, y, 11, ch)
    for ch, xf in zip(BIG_NUMBERS, BIG_NUMBER_XFRACS):
        x = p.xfrac_to_pdf(xf)
        p.text(x, top_y, 11, ch)
        p.text(x, bottom_y, 11, ch)


old_q = Page(BIG_W, BIG_H)
old_q.rect(60, 60, BIG_W - 120, BIG_H - 120)
draw_big_grid(old_q)
old_q.text(1000, 700, 12, "88.0")
save1(old_q, 'largegrid_old.pdf')

new_q = Page(BIG_W, BIG_H)
new_q.rect(60, 60, BIG_W - 120, BIG_H - 120)
draw_big_grid(new_q)
new_q.text(1000, 700, 12, "92.0")
save1(new_q, 'largegrid_new.pdf')

print("done v10b fixtures")
