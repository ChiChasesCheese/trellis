"""cd09 Bitfont Repository: Implement Decoders and Compose Them — YOUR implementation."""

from __future__ import annotations

import sys

FLAG_RLE = 0b01
FLAG_COMPACT = 0b10


def part1(payload: bytes, flags: int) -> list[list[int]]:
    """Glyph decoder. payload/flags -> 8x8 grid of 0/1 ints. Does not know about frames.
    Raise ValueError for: wrong-length raw/COMPACT payload, malformed RLE, or RLE+COMPACT both
    set. See problem.md for the raw/RLE/COMPACT encodings."""
    # TODO
    return []


def part2(data: bytes) -> list[tuple[int, bytes]]:
    """Stream decoder: parse `data` into [(flags, payload), ...] in order. Never decode payload
    contents. Raise EOFError if the stream ends mid-frame (partial header or short payload)."""
    # TODO
    return []


def part3(data: bytes) -> list[list[list[int]]]:
    """Compose: [part1(payload, flags) for flags, payload in part2(data)]. Do not change
    part1/part2 to make this work."""
    # TODO
    return []


def _grid_to_lines(grid: list[list[int]]) -> list[str]:
    return ["".join(str(bit) for bit in row) for row in grid]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text = stdin.read()
    header, _, rest = text.partition("\n")
    part = int(header.strip().split()[-1])
    line2 = rest.strip("\n").split("\n", 1)[0].strip()
    if part == 1:
        flags_str, payload_hex = line2.split()
        grid = part1(bytes.fromhex(payload_hex), int(flags_str))
        stdout.write("\n".join(_grid_to_lines(grid)) + "\n")
    elif part == 2:
        data = bytes.fromhex(line2) if line2 else b""
        frames = part2(data)
        out_lines = [f"{flags} {payload.hex()}" for flags, payload in frames]
        stdout.write("\n".join(out_lines) + ("\n" if out_lines else ""))
    else:
        data = bytes.fromhex(line2) if line2 else b""
        glyphs = part3(data)
        blocks = ["\n".join(_grid_to_lines(g)) for g in glyphs]
        stdout.write("\n\n".join(blocks) + ("\n" if blocks else ""))


if __name__ == "__main__":
    main()
