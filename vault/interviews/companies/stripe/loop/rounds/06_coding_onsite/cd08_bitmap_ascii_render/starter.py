"""cd08 Convert Bitmap into ASCII Characters — YOUR implementation."""

from __future__ import annotations

import json
import sys


def part1(bitstring: str, width: int, height: int) -> list[str]:
    """Decode one row-major glyph bitstring ('1'->'#', '0'->'.') into `height` strings of
    length `width` each. Raise ValueError if len(bitstring) != width * height."""
    # TODO
    return []


def part2(font: dict[str, str], width: int, height: int, text: str) -> list[str]:
    """Render `text` by placing glyphs side by side, one '.' separator column between them.
    Space is always a blank glyph (never looked up in font). Happy path: assume every non-space
    character in text is present in font with a valid-length bitstring."""
    # TODO
    return []


def part3(font: dict[str, str], width: int, height: int, text: str) -> list[str]:
    """Same as part2, but raise ValueError if a non-space character in text is missing from
    font or has an invalid-length bitstring. Do not change part1/part2 to make this work."""
    # TODO
    return []


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
