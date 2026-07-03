# Drawing Revision Comparator

A single-file, client-side tool for comparing two PDF exports of the same technical drawing (old vs. new revision) and producing a written change summary plus a visual diff. No build step, no backend — everything runs in the browser via [pdf.js](https://mozilla.github.io/pdf.js/); drawing content is never uploaded anywhere.

**[Live demo](https://mrtozdgn.github.io/pdf_compare/)**

## What it does

- Extracts embedded text/dimension objects from the PDF (not just pixels) to detect precise changes like `"120.5" → "125.0"`.
- Lets you calibrate a title block region once (saved in your browser) so revision/date/drawn-by changes are reported separately from the rest of the drawing.
- Renders a visual overlay diff (red = removed, blue = added, gray = unchanged), a before/after slider, and old-only/new-only views.
- Generates a written summary of title block changes, added/removed/modified dimensions and notes, and an overall visual-difference percentage.

See the comments at the top of `index.html` for the underlying approach, assumptions, and known limitations (in particular: it needs the source PDF to contain real embedded text, not text flattened to vector outlines — the tool will warn you per-file if that's the case).

## Sample files

`sample_old_revB.pdf` and `sample_new_revC.pdf` are synthetic test drawings (not real technical drawings) used to exercise every diff category the tool detects — a revision/date change, a corrected dimension, a reworded note, an added note, a removed note, and a hole that physically moved.

## Usage

Open `index.html` directly in a browser (no server required), or use the [live demo](https://mrtozdgn.github.io/pdf_compare/).
