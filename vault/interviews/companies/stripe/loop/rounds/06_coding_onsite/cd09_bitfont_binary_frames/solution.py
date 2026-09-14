"""cd09 Bitfont Repository: Implement Decoders and Compose Them — reference solution.

See problem.md for the full (low-medium confidence, reconstructed) contract: a custom binary
FRAME format (LEN_HI, LEN_LO, FLAGS, PAYLOAD), 8x8 monochrome glyphs encoded raw / RLE / COMPACT.
Part 1 (glyph decoder) and Part 2 (stream/frame decoder) are deliberately independent -- Part 2
never inspects payload bytes beyond counting them, and Part 1 never sees frame headers. Part 3 is
their obvious composition and must not need to change either.
"""

from __future__ import annotations

import sys

FLAG_RLE = 0b01
FLAG_COMPACT = 0b10


def _decode_raw(payload: bytes) -> list[list[int]]:
    if len(payload) != 8:
        raise ValueError(f"raw payload must be 8 bytes, got {len(payload)}")
    return [[(byte >> (7 - col)) & 1 for col in range(8)] for byte in payload]


def _decode_rle(payload: bytes) -> list[list[int]]:
    if len(payload) % 2 != 0:
        raise ValueError("RLE payload must have even length")
    pixels: list[int] = []
    for i in range(0, len(payload), 2):
        count, value = payload[i], payload[i + 1]
        if value not in (0, 1):
            raise ValueError(f"RLE value must be 0 or 1, got {value}")
        if count == 0:
            raise ValueError("RLE count must be >= 1")
        pixels.extend([value] * count)
    if len(pixels) != 64:
        raise ValueError(f"RLE pixel total must be 64, got {len(pixels)}")
    return [pixels[r * 8 : (r + 1) * 8] for r in range(8)]


def _decode_compact(payload: bytes) -> list[list[int]]:
    if len(payload) != 4:
        raise ValueError(f"COMPACT payload must be 4 bytes, got {len(payload)}")
    rows: list[list[int]] = []
    for byte in payload:
        for nibble in (byte >> 4, byte & 0xF):
            row = [(nibble >> (3 - col)) & 1 for col in range(4)] + [0, 0, 0, 0]
            rows.append(row)
    return rows


def part1(payload: bytes, flags: int) -> list[list[int]]:
    """Glyph decoder ('Decoder A'). Does not know about frames or lengths."""
    rle = bool(flags & FLAG_RLE)
    compact = bool(flags & FLAG_COMPACT)
    if rle and compact:
        raise ValueError("RLE and COMPACT flags are mutually exclusive")
    if rle:
        return _decode_rle(payload)
    if compact:
        return _decode_compact(payload)
    return _decode_raw(payload)


def part2(data: bytes) -> list[tuple[int, bytes]]:
    """Stream decoder ('Decoder B'). Parses framing only -- never decodes PAYLOAD contents."""
    frames: list[tuple[int, bytes]] = []
    pos = 0
    n = len(data)
    while pos < n:
        if n - pos < 3:
            raise EOFError("stream ended in frame header")
        length = (data[pos] << 8) | data[pos + 1]
        flags = data[pos + 2]
        pos += 3
        if n - pos < length:
            raise EOFError("stream ended mid-payload")
        payload = data[pos : pos + length]
        pos += length
        frames.append((flags, payload))
    return frames


def part3(data: bytes) -> list[list[list[int]]]:
    """Compose: the obvious composition of part2 (framing) then part1 (glyph decode) per frame.
    Must not need to change part1 or part2's logic."""
    return [part1(payload, flags) for flags, payload in part2(data)]


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
