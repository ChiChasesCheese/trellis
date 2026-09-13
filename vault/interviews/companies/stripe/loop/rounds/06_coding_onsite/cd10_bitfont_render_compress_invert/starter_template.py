"""cd10 Implement Bitmap Font Render/Compress/Invert — YOUR implementation."""

from __future__ import annotations

import json
import sys


def part1(font: dict[str, list[int]], ch: str) -> list[str]:
    """Render glyph `ch` (8 row-ints, MSB-first) as 8 strings of 8 chars, '#'/'.'.
    KeyError if `ch` not in font."""
    # TODO
    return []


def part2(font: dict[str, list[int]], word: str, sep: int = 1) -> list[str]:
    """Render `word` left to right via part1 per character, `sep` '.' columns between glyphs.
    Space is always a blank glyph, never looked up in font. Must call part1, not re-derive
    pixels."""
    # TODO
    return []


def part3_compress(rows: list[int]) -> str:
    """Row-wise RLE: 'count:bit' tokens per row (';'-joined, MSB-first), rows joined by '|'."""
    # TODO
    return ""


def part3_decompress(s: str) -> list[int]:
    """Exact inverse of part3_compress."""
    # TODO
    return []


def part4(font: dict[str, list[int]], ch: str) -> list[str]:
    """Render the bitwise-inverted glyph (row ^ 0xFF for every row) by delegating to part1 on a
    temporary font. Must not mutate the caller's font dict."""
    # TODO
    return []


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
