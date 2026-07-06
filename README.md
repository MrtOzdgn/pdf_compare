# Çizim Revizyon Karşılaştırıcı (Drawing Revision Comparator)

A single-file, client-side tool for comparing two PDF exports of the same technical drawing (old vs. new revision) and producing a written Turkish revision-note summary plus a visual diff. No build step, no backend — everything runs in the browser via [pdf.js](https://mozilla.github.io/pdf.js/); drawing content is never uploaded anywhere. The current version is `drawing-revision-comparator-tr_v10.html`; `index.html` just redirects to it (this is what GitHub Pages serves).

**[Live demo](https://mrtozdgn.github.io/pdf_compare/)**

## What it does

- Extracts embedded text/dimension objects from the PDF (not just pixels) to detect precise changes like `"120.5" → "125.0"`.
- Lets you mark one or more "ignore regions" (antet, revision table, signatures, …) once per template; nothing inside them is ever diffed or reported, text or visual.
- Auto-detects a drawing's reference/zone grid (letters + numbers printed in the sheet margin, à la ISO 5457) directly from the new revision and tags every reported change with its zone, e.g. `[C-4]`. Falls back gracefully (no tag) when no grid is found.
- Silently drops trivial changes (bare dates, bare revision letters) instead of reporting them.
- Renders a visual overlay diff (red = removed, blue = added, gray = unchanged), a before/after slider, and old-only/new-only views.
- Generates a written Turkish summary of added/removed/modified dimensions and notes, plus an overall "MODEL GÖRÜNÜMLERİ" flag for visual-only geometry changes.

See the comments at the top of `drawing-revision-comparator-tr_v10.html` for the underlying approach, assumptions, and known limitations (in particular: it needs the source PDF to contain real embedded text, not text flattened to vector outlines — the tool will warn you per-file if that's the case).

## Sample files

`sample_old_revB.pdf` / `sample_new_revC.pdf` are the original English-tool samples. `test-fixtures/` holds a much larger synthetic regression suite (grid detection, ignore regions, multi-page, table restructuring, and other edge cases) generated with the scripts in that folder — see `test-fixtures/README.md`.

## Usage

Open `drawing-revision-comparator-tr_v10.html` directly in a browser (no server required), or use the [live demo](https://mrtozdgn.github.io/pdf_compare/).
