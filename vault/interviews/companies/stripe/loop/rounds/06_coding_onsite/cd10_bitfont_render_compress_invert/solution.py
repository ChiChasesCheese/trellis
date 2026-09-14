"""cd10 Implement Bitmap Font Render/Compress/Invert — reference solution.

See problem.md for the full (low-confidence, largely reconstructed) contract. Font: dict mapping
a single character to a list of 8 ints (one per row, MSB-first = leftmost pixel). Part 1 renders
one glyph, Part 2 composes Part 1 across a word, Part 3 does row-wise RLE compress/decompress,
Part 4 renders the bitwise-inverted glyph by delegating back to Part 1 (never re-implementing
rendering).
"""

from __future__ import annotations

import json
import sys


def _render_row(byte: int) -> str:
    return "".join("#" if (byte >> (7 - col)) & 1 else "." for col in range(8))


def part1(font: dict[str, list[int]], ch: str) -> list[str]:
    """Render glyph `ch` as 8 strings of 8 chars ('#'/'.'), MSB-first. KeyError if missing."""
    rows = font[ch]
    return [_render_row(byte) for byte in rows]


def part2(font: dict[str, list[int]], word: str, sep: int = 1) -> list[str]:
    """Render `word` left to right via part1 per character, `sep` '.' columns between glyphs.
    Space is always a blank glyph (never looked up in font)."""
    blank_rows = [_render_row(0) for _ in range(8)]
    glyph_renders = [blank_rows if ch == " " else part1(font, ch) for ch in word]
    sep_str = "." * sep
    return [sep_str.join(glyph[row] for glyph in glyph_renders) for row in range(8)]


def part3_compress(rows: list[int]) -> str:
    """Row-wise RLE: each row -> ';'-joined 'count:bit' tokens (MSB-first), rows joined by '|'."""
    row_tokens = []
    for byte in rows:
        bits = [(byte >> (7 - col)) & 1 for col in range(8)]
        tokens = []
        i = 0
        while i < 8:
            j = i
            while j < 8 and bits[j] == bits[i]:
                j += 1
            tokens.append(f"{j - i}:{bits[i]}")
            i = j
        row_tokens.append(";".join(tokens))
    return "|".join(row_tokens)


def part3_decompress(s: str) -> list[int]:
    """Exact inverse of part3_compress."""
    rows = []
    for row_str in s.split("|"):
        byte = 0
        for token in row_str.split(";"):
            count_str, bit_str = token.split(":")
            count, bit = int(count_str), int(bit_str)
            for _ in range(count):
                byte = (byte << 1) | bit
        rows.append(byte)
    return rows


def part4(font: dict[str, list[int]], ch: str) -> list[str]:
    """Render the bitwise-inverted glyph by delegating to part1 on a temporary font -- must not
    duplicate part1's rendering logic, and must not mutate the caller's font dict."""
    inverted_rows = [byte ^ 0xFF for byte in font[ch]]
    return part1({ch: inverted_rows}, ch)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text = stdin.read()
    header, _, rest = text.partition("\n")
    part = int(header.strip().split()[-1])
    payload = json.loads(rest)
    if part == 1:
        out = part1(payload["font"], payload["ch"])
        stdout.write("\n".join(out) + "\n")
    elif part == 2:
        out = part2(payload["font"], payload["word"], payload.get("sep", 1))
        stdout.write("\n".join(out) + "\n")
    elif part == 3:
        if payload["op"] == "compress":
            stdout.write(part3_compress(payload["rows"]) + "\n")
        else:
            stdout.write(",".join(str(v) for v in part3_decompress(payload["s"])) + "\n")
    else:
        out = part4(payload["font"], payload["ch"])
        stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
