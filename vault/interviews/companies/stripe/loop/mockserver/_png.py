"""Minimal PNG encoder — no PIL, stdlib `zlib` only.

Produces uncompressed-filter-type-0, 8-bit truecolor (RGB, colour type 2) PNGs. That is
the simplest valid PNG a decoder (Pillow, browsers, `file(1)`) will accept: one 8-byte
signature, an IHDR chunk, a single IDAT chunk holding zlib-compressed scanlines (each
scanline prefixed with filter byte 0 = "None"), and an empty IEND chunk.

Canvas representation: a "canvas" is `list[bytearray]`, one bytearray per row, each of
length `width * 3` holding packed RGB bytes (no filter byte — that's added by
`write_png`). Use `new_canvas` to create one and `set_pixel`/`draw_polyline`/
`draw_marker` to paint into it, then `write_png` to encode.
"""

from __future__ import annotations

import struct
import zlib

RGB = tuple  # (r, g, b) ints 0-255, documentation alias only


def _chunk(chunk_type: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    )


def write_png(width: int, height: int, rows: list) -> bytes:
    """Encode `rows` (see module docstring) as a PNG file, return the bytes."""
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if len(rows) != height:
        raise ValueError(f"expected {height} rows, got {len(rows)}")
    raw = bytearray()
    for row in rows:
        if len(row) != width * 3:
            raise ValueError(f"row length {len(row)} != width*3 ({width * 3})")
        raw.append(0)  # filter type 0 = None, one byte per scanline
        raw.extend(row)
    compressed = zlib.compress(bytes(raw), 9)
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(
        ">IIBBBBB",
        width,
        height,
        8,  # bit depth
        2,  # colour type 2 = truecolor (RGB, no alpha)
        0,  # compression method (only valid value)
        0,  # filter method (only valid value)
        0,  # interlace method (0 = no interlace)
    )
    return signature + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", compressed) + _chunk(b"IEND", b"")


def new_canvas(width: int, height: int, bg=(255, 255, 255)) -> list:
    """A `height`-row canvas, each row `width` pixels of `bg`, ready for drawing."""
    row_template = bytes(bg) * width
    return [bytearray(row_template) for _ in range(height)]


def set_pixel(rows: list, width: int, height: int, x: int, y: int, color) -> None:
    """Set one pixel, silently clipping out-of-bounds coordinates (drawing helpers
    routinely compute points slightly outside the canvas at the edges)."""
    if 0 <= x < width and 0 <= y < height:
        i = x * 3
        rows[y][i : i + 3] = bytes(color)


def draw_polyline(rows: list, width: int, height: int, points, color, thickness: int = 1) -> None:
    """Draw straight segments through consecutive `points` (list of (x, y) pixel
    coordinates, already projected) using Bresenham's line algorithm. `thickness` > 1
    also paints the immediate neighbor pixels for a slightly bolder line."""
    if len(points) < 2:
        for x, y in points:
            _paint_thick(rows, width, height, int(round(x)), int(round(y)), color, thickness)
        return
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        _draw_segment(
            rows,
            width,
            height,
            int(round(x0)),
            int(round(y0)),
            int(round(x1)),
            int(round(y1)),
            color,
            thickness,
        )


def _draw_segment(rows, width, height, x0, y0, x1, y1, color, thickness):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        _paint_thick(rows, width, height, x, y, color, thickness)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def _paint_thick(rows, width, height, x, y, color, thickness):
    set_pixel(rows, width, height, x, y, color)
    if thickness > 1:
        r = thickness // 2
        for ddx in range(-r, r + 1):
            for ddy in range(-r, r + 1):
                set_pixel(rows, width, height, x + ddx, y + ddy, color)


def draw_marker(rows: list, width: int, height: int, x: int, y: int, color, radius: int = 3) -> None:
    """Fill a small square marker of `radius` centered on (x, y)."""
    x, y = int(round(x)), int(round(y))
    for ddx in range(-radius, radius + 1):
        for ddy in range(-radius, radius + 1):
            set_pixel(rows, width, height, x + ddx, y + ddy, color)
