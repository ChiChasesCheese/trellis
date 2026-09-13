"""cd08 Convert Bitmap into ASCII Characters — reference solution.

See problem.md for the full contract. Part 1 decodes one glyph's row-major bitstring into a
`height`-row ASCII grid ('#' for '1', '.' for '0'). Part 2 lays out full text by calling Part 1
per character (happy path: every non-space character is assumed present in `font` with a
valid-length bitstring). Part 3 is the source's full `render_bitmap_text` contract: same layout,
plus a ValueError for a missing/invalid-length glyph.
"""

from __future__ import annotations

import json
import sys


def _decode_glyph_rows(bitstring: str, width: int, height: int) -> list[str]:
    """Row-major decode: rows of length `width`, top to bottom. '1' -> '#', '0' -> '.'."""
    if len(bitstring) != width * height:
        raise ValueError(f"invalid bitstring length: expected {width * height}, got {len(bitstring)}")
    rows = []
    for r in range(height):
        row_bits = bitstring[r * width : (r + 1) * width]
        rows.append("".join("#" if bit == "1" else "." for bit in row_bits))
    return rows


def part1(bitstring: str, width: int, height: int) -> list[str]:
    """Decode a single already-valid glyph bitstring into its ASCII grid."""
    return _decode_glyph_rows(bitstring, width, height)


def _blank_glyph(width: int, height: int) -> list[str]:
    return ["." * width] * height


def part2(font: dict[str, str], width: int, height: int, text: str) -> list[str]:
    """Happy-path layout: place glyphs side by side with one '.' separator column. Space is
    always a blank glyph, never looked up in `font`. Assumes every non-space char is valid."""
    glyphs = [
        _blank_glyph(width, height) if ch == " " else _decode_glyph_rows(font[ch], width, height)
        for ch in text
    ]
    return [".".join(glyph[row] for glyph in glyphs) for row in range(height)]


def part3(font: dict[str, str], width: int, height: int, text: str) -> list[str]:
    """Full contract (== source's render_bitmap_text): Part 2's layout, plus validation.

    Raises ValueError if a non-space character in `text` is missing from `font` or has an
    invalid bitstring length. Never mutates or bypasses Part 1/Part 2's decoding logic.
    """
    glyphs = []
    for ch in text:
        if ch == " ":
            glyphs.append(_blank_glyph(width, height))
            continue
        if ch not in font:
            raise ValueError(f"character {ch!r} is missing from font")
        glyphs.append(_decode_glyph_rows(font[ch], width, height))
    return [".".join(glyph[row] for glyph in glyphs) for row in range(height)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text_in = stdin.read()
    header, _, rest = text_in.partition("\n")
    part = int(header.strip().split()[-1])
    payload = json.loads(rest)
    if part == 1:
        out = part1(payload["bitstring"], payload["width"], payload["height"])
    elif part == 2:
        out = part2(payload["font"], payload["width"], payload["height"], payload["text"])
    else:
        out = part3(payload["font"], payload["width"], payload["height"], payload["text"])
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
