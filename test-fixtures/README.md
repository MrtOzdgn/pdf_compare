# Comparator test fixtures (v9/v10)

Synthetic drawing pairs used to validate the `drawing-revision-comparator-tr_vN.html`
ignore-region + reference-grid rework. Generated with `pdfgen.py` (raw PDF
writer, no dependencies) via `make_fixtures.py` (base set), `make_fixtures_v10.py`
(extended set) and `make_fixtures_v10b.py` (table/stress set) — the latter two
import the base script's helpers. Regenerate with:
`python3 make_fixtures.py && python3 make_fixtures_v10.py && python3 make_fixtures_v10b.py`.

All pairs use a 1200x840 synthetic sheet with a title block inset at the
bottom-right (x:820-1140, y:60-275 in PDF points). Before comparing `*_old.pdf`
vs `*_new.pdf` in the tool, calibrate an ignore region roughly covering that
box (fractions ≈ x0:0.675 y0:0.665 x1:0.955 y1:0.935) — the fixtures don't line
up with `DEFAULT_IGNORE_REGIONS`'s bottom-right guess.

## Base set (v9)

- **gridA_old/new** — full reference grid (letters A-F left/right, numbers 1-8
  top/bottom). Exercises everything at once: a dimension change, an added +
  removed dimension in different zones, a note edit that also reflows (note 4
  shifts position with identical text — must NOT be reported), a moved filled
  circle (must trigger MODEL GÖRÜNÜMLERİ), a bare date change and a bare
  revision-letter change in the body (both must be silently dropped), and
  antet fields changing too (must be silent).
- **gridB_old/new** — same content, axis-swapped grid (numbers on left/right,
  letters on top/bottom) — checks the tool re-derives orientation instead of
  assuming letters-are-always-vertical.
- **nogrid_old/new** — no reference grid at all — checks the fallback path
  (whole page treated as the frame, no coordinate tags, "tespit edilemedi"
  warning shown).
- **antetshift_old/new** — identical drawing content; only the title block's
  internal field layout is reshuffled between revisions. With the ignore
  region calibrated over the title block, expected output is
  "İKİ REVİZYON ARASINDA DEĞİŞİKLİK TESPİT EDİLMEMİŞTİR." — regression test
  for the original bug (mismatched antet fields reported as bogus value
  changes).

## Extended set (v10)

- **antetchange_old/new** — body/notes/geometry byte-identical; ONLY antet
  fields change (REV B→C, date, DRAWN BY, CHECKED BY, a new revision-table
  row). Isolates the antet-exclusion path from body-diff noise. Expected:
  zero changes reported.
- **antetcompany_old/new** — same idea, different fields (company name, DWG
  NO). Expected: zero changes reported.
- **multiregion_old/new** — main title block PLUS a separate "approval stamp"
  box (top-left) that also changes content. With only the title block
  calibrated, the stamp box correctly leaks into the report; calibrating
  BOTH regions together makes it disappear — demonstrates the multi-region
  ignore feature is necessary and sufficient.
- **pagecount_old/new** — old has 1 page, new has 2 (page 1 identical) —
  expects a trailing "SAYFA 2 EKLENMİŞTİR." line.
- **multipage_old/new** — both have 2 pages; page 1 has a dimension change,
  page 2 is identical across both files — expects only a "SAYFA 1" section
  (page 2 omitted entirely, per-page independence).
- **movereplace_old/new** — a same-slot dissimilar replacement ("G1/8" →
  "NPT 1/8", low text similarity, must still pair as "modified") plus a pure
  move (identical string "SEE DETAIL A" relocated far away — must be
  silently treated as unchanged, never reported as removed+added).
- **dedup_old/new** — the value "25.0" appears twice on the page; only one
  occurrence changes to "30.0" in the new revision. Expects exactly one
  modified line, no phantom removed/added for the untouched duplicate.
- **aspect_old/new** — different page height between revisions — expects the
  "sayfa boyutu/en-boy oranı farklı" warning banner.
- **notext_old/new** — no embedded text at all (simulates flattened/outlined
  CAD text export) — expects the "gömülü metin bulunamadı" diagnostic on
  both files, and a visual-only "MODEL GÖRÜNÜMLERİ GÜNCELLENMİŞTİR." result
  (a circle moved) since the pixel diff doesn't need text.

## Table / stress set (v10b)

A parts-list (BOM) table lives in the drawing BODY (not an ignored antet
region) with columns ITEM/QTY/DESCRIPTION — this is "engineering content"
that must still be reported, unlike the antet's revision table.

- **bomappend_old/new** — a row is appended at the end, nothing else moves.
  Clean case: expects the new row's cells reported as added.
- **bomqtyedit_old/new** — one cell (a quantity) edited in place, no
  structural change. Expects one clean modified line, same as any dimension.
- **bominsert_old/new** — a row INSERTED in the middle, cascading every row
  below it down one slot and renumbering ITEM #s. This is the genuinely hard
  case: item numbers and quantities are short duplicate digits with no
  per-cell identity, so the position-based differ can (and here, does) latch
  an unrelated old/new pair together as "unchanged" purely because they
  landed the same short distance apart, leaving a DIFFERENT cell's value
  reported as "added" instead of the intuitive one. The result is still safe
  — nothing is ever reported as a false cross-field "X became Y" claim, and
  every real change is surfaced somewhere — but cell-level attribution across
  a shifted table isn't exact. This is a pre-existing property of the
  position/similarity heuristic (see the file's "Known failure modes" #5),
  not something introduced by the ignore-region/grid rework; cross-check the
  visual diff when a table restructures, which is exactly what the tool's
  own docs already recommend for surprising output.
- **dense_old/new** — five dimension values 40pt apart on one line; only the
  middle one changes value and nudges 3pt off its old slot, the other four
  stay byte-identical. Checks tight-but-not-merged spacing doesn't cause
  cross-neighbor mismatches.
- **largegrid_old/new** — a much bigger sheet (2000x1400) with a denser
  reference grid (10 letters x 12 numbers) — checks detectGrid scales past
  the small 6x8 grid used everywhere else. (Note: the very first letter and
  first number in this fixture sit exactly on the marginBand boundary and
  get correctly skipped as corner-ambiguous, so letterCount/numberCount come
  back as 9/11 rather than 10/12 — that's the corner-avoidance guard working
  as intended, not a detection failure; a real template wouldn't print a
  zone label right in the corner anyway.)
