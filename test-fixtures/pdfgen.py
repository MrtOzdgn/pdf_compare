"""Minimal raw-PDF writer (no dependencies) for synthetic test drawings.
Produces PDFs with real embedded Type1/Helvetica text (WinAnsiEncoding) at
exact coordinates, plus simple vector graphics (lines/rects/circles) — this
is what the comparator tool's pdf.js text extraction needs to be exercised
meaningfully (flattened/rasterized text would defeat the whole point).
"""

def esc(s):
    return s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')

class Page:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.ops = ["1 w"]

    def text(self, x, y, size, s):
        self.ops.append(f"BT /F1 {size} Tf {x:.2f} {y:.2f} Td ({esc(s)}) Tj ET")

    def line(self, x1, y1, x2, y2):
        self.ops.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def rect(self, x, y, w, h):
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re S")

    def circle(self, cx, cy, r, fill=False):
        k = 0.5522847498 * r
        op = "f" if fill else "S"
        self.ops.append(
            f"{cx-r:.2f} {cy:.2f} m "
            f"{cx-r:.2f} {cy+k:.2f} {cx-k:.2f} {cy+r:.2f} {cx:.2f} {cy+r:.2f} c "
            f"{cx+k:.2f} {cy+r:.2f} {cx+r:.2f} {cy+k:.2f} {cx+r:.2f} {cy:.2f} c "
            f"{cx+r:.2f} {cy-k:.2f} {cx+k:.2f} {cy-r:.2f} {cx:.2f} {cy-r:.2f} c "
            f"{cx-k:.2f} {cy-r:.2f} {cx-r:.2f} {cy-k:.2f} {cx-r:.2f} {cy:.2f} c {op}"
        )

    def yfrac_to_pdf(self, yfrac):
        """Top-origin fraction (matches the tool's yFrac) -> PDF y (bottom-origin)."""
        return (1 - yfrac) * self.h

    def xfrac_to_pdf(self, xfrac):
        return xfrac * self.w

    def build(self):
        content = ("\n".join(self.ops) + "\n").encode('latin-1', errors='replace')
        objs = []
        objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        objs.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.w} {self.h}] "
            f"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>".encode()
        )
        objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        objs.append(f"<< /Length {len(content)} >>\nstream\n".encode() + content + b"\nendstream")

        out = bytearray(b"%PDF-1.4\n")
        offsets = []
        for i, body in enumerate(objs, start=1):
            offsets.append(len(out))
            out += f"{i} 0 obj\n".encode()
            out += body
            out += b"\nendobj\n"
        xref_offset = len(out)
        out += f"xref\n0 {len(objs)+1}\n".encode()
        out += b"0000000000 65535 f \n"
        for off in offsets:
            out += f"{off:010d} 00000 n \n".encode()
        out += f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode()
        return bytes(out)

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.build())
