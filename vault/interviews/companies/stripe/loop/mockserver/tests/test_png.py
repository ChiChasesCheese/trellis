"""Tests for loop.mockserver._png — the hand-rolled PNG encoder (no PIL)."""

import struct
import zlib

from loop.mockserver import _png


def _parse_chunks(data: bytes):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    chunks = []
    i = 8
    while i < len(data):
        length = struct.unpack(">I", data[i : i + 4])[0]
        ctype = data[i + 4 : i + 8]
        cdata = data[i + 8 : i + 8 + length]
        chunks.append((ctype, cdata))
        i += 8 + length + 4  # length + type + data + crc
    return chunks


def test_signature_and_ihdr_dimensions():
    canvas = _png.new_canvas(5, 3, bg=(1, 2, 3))
    data = _png.write_png(5, 3, canvas)
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    chunks = _parse_chunks(data)
    types = [c[0] for c in chunks]
    assert types == [b"IHDR", b"IDAT", b"IEND"]
    width, height, depth, color_type, comp, filt, interlace = struct.unpack(">IIBBBBB", chunks[0][1])
    assert (width, height) == (5, 3)
    assert depth == 8
    assert color_type == 2  # truecolor RGB, no alpha


def test_idat_roundtrips_to_original_pixels():
    canvas = _png.new_canvas(4, 2, bg=(10, 20, 30))
    _png.set_pixel(canvas, 4, 2, 1, 1, (200, 100, 50))
    data = _png.write_png(4, 2, canvas)
    chunks = _parse_chunks(data)
    idat = next(c[1] for c in chunks if c[0] == b"IDAT")
    raw = zlib.decompress(idat)
    # each scanline is 1 filter byte + width*3 pixel bytes
    stride = 1 + 4 * 3
    assert len(raw) == stride * 2
    row0 = raw[0:stride]
    row1 = raw[stride : 2 * stride]
    assert row0[0] == 0 and row1[0] == 0  # filter type None
    assert row0[1:4] == bytes((10, 20, 30))  # untouched pixel
    assert row1[1 + 1 * 3 : 1 + 2 * 3] == bytes((200, 100, 50))  # the pixel we set


def test_write_png_rejects_mismatched_row_count():
    canvas = _png.new_canvas(2, 2)
    try:
        _png.write_png(2, 3, canvas)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for row/height mismatch")


def test_draw_polyline_paints_endpoints_and_midpoint():
    canvas = _png.new_canvas(5, 5, bg=(255, 255, 255))
    _png.draw_polyline(canvas, 5, 5, [(0, 0), (4, 4)], (0, 0, 0))
    assert bytes(canvas[0][0:3]) == bytes((0, 0, 0))
    assert bytes(canvas[4][12:15]) == bytes((0, 0, 0))
    assert bytes(canvas[2][6:9]) == bytes((0, 0, 0))  # diagonal midpoint (2, 2)


def test_draw_polyline_out_of_bounds_points_are_clipped_not_raised():
    canvas = _png.new_canvas(3, 3, bg=(255, 255, 255))
    # should not raise even though (10, 10) is outside the 3x3 canvas
    _png.draw_polyline(canvas, 3, 3, [(0, 0), (10, 10)], (9, 9, 9))
    assert bytes(canvas[0][0:3]) == bytes((9, 9, 9))


def test_draw_marker_fills_a_small_square():
    canvas = _png.new_canvas(9, 9, bg=(255, 255, 255))
    _png.draw_marker(canvas, 9, 9, 4, 4, (0, 128, 0), radius=1)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            assert bytes(canvas[4 + dy][(4 + dx) * 3 : (4 + dx) * 3 + 3]) == bytes((0, 128, 0))
    # outside the marker radius stays background
    assert bytes(canvas[0][0:3]) == bytes((255, 255, 255))
