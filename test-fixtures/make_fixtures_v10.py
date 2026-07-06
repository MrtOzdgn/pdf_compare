import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pdfgen import Page, save_pdf
import make_fixtures as mf  # reuses draw_frame/draw_grid/draw_title_block/draw_geometry_and_dims/draw_simple_notes

OUT = mf.OUT
W, H = mf.W, mf.H


def save1(page, name):
    path = os.path.join(OUT, name)
    save_pdf([page], path)
    print("wrote", path, os.path.getsize(path), "bytes")


def savemulti(pages, name):
    path = os.path.join(OUT, name)
    save_pdf(pages, path)
    print("wrote", path, os.path.getsize(path), "bytes")


# ---------------------------------------------------------------------------
# E1: ONLY antet fields change (rev, date, drawn by, checked by, new revision
# row) — body/notes/geometry byte-identical. Isolates the antet-exclusion
# path from any body-diff noise (gridA mixed both together).
# ---------------------------------------------------------------------------
def draw_title_block_people(p, rev, date, drawn_by, checked_by):
    x, y, w, h = mf.TB_BOX['x'], mf.TB_BOX['y'], mf.TB_BOX['w'], mf.TB_BOX['h']
    p.rect(x, y, w, h)
    p.line(x, y + 150, x + w, y + 150)
    p.text(x + 10, y + 255 - 180, 8, "REV")
    p.text(x + 60, y + 255 - 180, 8, "DATE")
    p.text(x + 150, y + 255 - 180, 8, "DESCRIPTION")
    p.text(x + 10, y + 255 - 195, 8, rev)
    p.text(x + 60, y + 255 - 195, 8, date)
    p.text(x + 150, y + 255 - 195, 8, "SEE NOTES")
    if rev != 'B':
        p.text(x + 10, y + 255 - 208, 8, "B")
        p.text(x + 60, y + 255 - 208, 8, "2025-11-03")
        p.text(x + 150, y + 255 - 208, 8, "INITIAL RELEASE")
    fields = [
        (12, "ACME ENGINEERING CO."),
        (11, "BRACKET MOUNT ASSY"),
        (8, "DWG NO: 4471-A"),
        (8, "SCALE: 1:2"),
        (8, f"DATE: {date}"),
        (8, f"DRAWN BY: {drawn_by}"),
        (8, f"CHECKED BY: {checked_by}"),
    ]
    yy = y + 130
    for size, txt in fields:
        p.text(x + 10, yy, size, txt)
        yy -= 18
    p.text(x + 180, y + 130 - 18 * 2, 8, "SIZE: A2")
    p.text(x + 180, y + 130 - 18 * 3, 8, f"REV: {rev}")


old_e1 = Page(W, H)
mf.draw_frame(old_e1)
mf.draw_grid(old_e1, 'letters_vertical')
draw_title_block_people(old_e1, rev='B', date='2025-11-03', drawn_by='J. SMITH', checked_by='R. LEE')
mf.draw_geometry_and_dims(old_e1, dim_value="125.0", hole_cx=400)
mf.draw_simple_notes(old_e1)
save1(old_e1, 'antetchange_old.pdf')

new_e1 = Page(W, H)
mf.draw_frame(new_e1)
mf.draw_grid(new_e1, 'letters_vertical')
draw_title_block_people(new_e1, rev='C', date='2025-12-01', drawn_by='A. JONES', checked_by='M. CHEN')
mf.draw_geometry_and_dims(new_e1, dim_value="125.0", hole_cx=400)  # body untouched
mf.draw_simple_notes(new_e1)
save1(new_e1, 'antetchange_new.pdf')


# ---------------------------------------------------------------------------
# E2: company name + DWG NO change (different fields than E1), body untouched.
# ---------------------------------------------------------------------------
def draw_title_block_company(p, company, dwgno):
    x, y, w, h = mf.TB_BOX['x'], mf.TB_BOX['y'], mf.TB_BOX['w'], mf.TB_BOX['h']
    p.rect(x, y, w, h)
    p.line(x, y + 150, x + w, y + 150)
    p.text(x + 10, y + 255 - 180, 8, "REV")
    p.text(x + 60, y + 255 - 180, 8, "DATE")
    p.text(x + 150, y + 255 - 180, 8, "DESCRIPTION")
    p.text(x + 10, y + 255 - 195, 8, "B")
    p.text(x + 60, y + 255 - 195, 8, "2025-11-03")
    p.text(x + 150, y + 255 - 195, 8, "SEE NOTES")
    fields = [
        (12, company),
        (11, "BRACKET MOUNT ASSY"),
        (8, f"DWG NO: {dwgno}"),
        (8, "SCALE: 1:2"),
        (8, "DATE: 2025-11-03"),
        (8, "DRAWN BY: J. SMITH"),
        (8, "CHECKED BY: R. LEE"),
    ]
    yy = y + 130
    for size, txt in fields:
        p.text(x + 10, yy, size, txt)
        yy -= 18
    p.text(x + 180, y + 130 - 18 * 2, 8, "SIZE: A2")
    p.text(x + 180, y + 130 - 18 * 3, 8, "REV: B")


old_e2 = Page(W, H)
mf.draw_frame(old_e2)
mf.draw_grid(old_e2, 'letters_vertical')
draw_title_block_company(old_e2, company="ACME ENGINEERING CO.", dwgno="4471-A")
mf.draw_geometry_and_dims(old_e2, dim_value="125.0", hole_cx=400)
mf.draw_simple_notes(old_e2)
save1(old_e2, 'antetcompany_old.pdf')

new_e2 = Page(W, H)
mf.draw_frame(new_e2)
mf.draw_grid(new_e2, 'letters_vertical')
draw_title_block_company(new_e2, company="ACME ENGINEERING CORP.", dwgno="4471-B")
mf.draw_geometry_and_dims(new_e2, dim_value="125.0", hole_cx=400)
mf.draw_simple_notes(new_e2)
save1(new_e2, 'antetcompany_new.pdf')


# ---------------------------------------------------------------------------
# F: main title block PLUS a second "approval stamp" box (top-left, inside
# the frame) — both change content between revisions. Tests multiple
# independently-marked ignore regions used together.
# ---------------------------------------------------------------------------
STAMP_BOX = dict(x=90, y=680, w=220, h=70)


def draw_stamp(p, approver, stamp_date):
    x, y, w, h = STAMP_BOX['x'], STAMP_BOX['y'], STAMP_BOX['w'], STAMP_BOX['h']
    p.rect(x, y, w, h)
    p.text(x + 8, y + 48, 8, "APPROVAL STAMP")
    p.text(x + 8, y + 30, 8, f"APPROVED: {approver}")
    p.text(x + 8, y + 12, 8, f"STAMP DATE: {stamp_date}")


old_f = Page(W, H)
mf.draw_frame(old_f)
mf.draw_grid(old_f, 'letters_vertical')
mf.draw_title_block(old_f, rev='B', date='2025-11-03')
draw_stamp(old_f, approver="T. WALKER", stamp_date="2025-11-04")
mf.draw_geometry_and_dims(old_f, dim_value="125.0", hole_cx=400)
save1(old_f, 'multiregion_old.pdf')

new_f = Page(W, H)
mf.draw_frame(new_f)
mf.draw_grid(new_f, 'letters_vertical')
mf.draw_title_block(new_f, rev='C', date='2025-12-01')
draw_stamp(new_f, approver="S. PATEL", stamp_date="2025-12-02")
mf.draw_geometry_and_dims(new_f, dim_value="125.0", hole_cx=400)  # body untouched
save1(new_f, 'multiregion_new.pdf')


# ---------------------------------------------------------------------------
# G: page-count mismatch — old has 1 page, new has 2.
# ---------------------------------------------------------------------------
def simple_page(dim_value):
    p = Page(W, H)
    mf.draw_frame(p)
    mf.draw_grid(p, 'letters_vertical')
    mf.draw_title_block(p, rev='B', date='2025-11-03')
    mf.draw_geometry_and_dims(p, dim_value=dim_value, hole_cx=400)
    return p


savemulti([simple_page("125.0")], 'pagecount_old.pdf')
savemulti([simple_page("125.0"), simple_page("200.0")], 'pagecount_new.pdf')


# ---------------------------------------------------------------------------
# H: both files have 2 pages; each page has its OWN independent change, to
# check per-page reporting (separate SAYFA headers, separate grid lookups).
# ---------------------------------------------------------------------------
savemulti([simple_page("125.0"), simple_page("300.0")], 'multipage_old.pdf')
savemulti([simple_page("150.0"), simple_page("300.0")], 'multipage_new.pdf')
# page 1: 125.0 -> 150.0 changes; page 2: 300.0 unchanged on both -> no page-2 lines expected.


# ---------------------------------------------------------------------------
# I: dissimilar same-slot replacement ("G1/8" -> "NPT 1/8", low text
# similarity but same position -> still "modified") + a pure move (identical
# string deleted from one spot, re-added far away -> must be silently
# unchanged, never reported as removed+added).
# ---------------------------------------------------------------------------
def draw_move_and_replace(p, thread_value, detail_pos):
    p.rect(150, 250, 500, 430)
    p.text(300, 550, 9, thread_value)  # same slot across old/new, value replaced
    p.text(detail_pos[0], detail_pos[1], 9, "SEE DETAIL A")  # position varies old vs new


old_i = Page(W, H)
mf.draw_frame(old_i)
mf.draw_grid(old_i, 'letters_vertical')
mf.draw_title_block(old_i, rev='B', date='2025-11-03')
draw_move_and_replace(old_i, thread_value="G1/8", detail_pos=(200, 680))
save1(old_i, 'movereplace_old.pdf')

new_i = Page(W, H)
mf.draw_frame(new_i)
mf.draw_grid(new_i, 'letters_vertical')
mf.draw_title_block(new_i, rev='B', date='2025-11-03')
draw_move_and_replace(new_i, thread_value="NPT 1/8", detail_pos=(900, 300))  # far away, same text
save1(new_i, 'movereplace_new.pdf')


# ---------------------------------------------------------------------------
# J: a value ("25.0") appears twice on the page; in the new revision only ONE
# occurrence changes to "30.0", the other stays "25.0" -> the redundancy
# dedup guard should leave exactly one modified line, no phantom
# removed/added for the untouched duplicate.
# ---------------------------------------------------------------------------
def draw_duplicate_value(p, val_a, val_b):
    p.rect(150, 250, 500, 430)
    p.text(250, 600, 9, val_a)
    p.text(550, 350, 9, val_b)


old_j = Page(W, H)
mf.draw_frame(old_j)
mf.draw_grid(old_j, 'letters_vertical')
mf.draw_title_block(old_j, rev='B', date='2025-11-03')
draw_duplicate_value(old_j, "25.0", "25.0")
save1(old_j, 'dedup_old.pdf')

new_j = Page(W, H)
mf.draw_frame(new_j)
mf.draw_grid(new_j, 'letters_vertical')
mf.draw_title_block(new_j, rev='B', date='2025-11-03')
draw_duplicate_value(new_j, "30.0", "25.0")
save1(new_j, 'dedup_new.pdf')


# ---------------------------------------------------------------------------
# K: aspect-ratio mismatch between old/new page sizes.
# ---------------------------------------------------------------------------
old_k = Page(1200, 840)
mf.draw_frame(old_k)
mf.draw_grid(old_k, 'letters_vertical')
mf.draw_title_block(old_k, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(old_k, dim_value="125.0", hole_cx=400)
save1(old_k, 'aspect_old.pdf')

new_k = Page(1200, 1000)  # different height -> different aspect ratio
mf.draw_frame(new_k)
mf.draw_grid(new_k, 'letters_vertical')
mf.draw_title_block(new_k, rev='B', date='2025-11-03')
mf.draw_geometry_and_dims(new_k, dim_value="130.0", hole_cx=400)
save1(new_k, 'aspect_new.pdf')


# ---------------------------------------------------------------------------
# L: no embedded text at all (simulates flattened/outlined-text CAD export)
# -> updateTextDiagnostic should warn, text-based diff categories go silent.
# ---------------------------------------------------------------------------
old_l = Page(W, H)
old_l.rect(150, 250, 500, 430)
old_l.circle(400, 470, 22, fill=True)
old_l.line(150, 227, 650, 227)
save1(old_l, 'notext_old.pdf')

new_l = Page(W, H)
new_l.rect(150, 250, 500, 430)
new_l.circle(460, 470, 22, fill=True)  # moved -> only the visual diff can see this
new_l.line(150, 227, 650, 227)
save1(new_l, 'notext_new.pdf')

print("done v10 fixtures")
