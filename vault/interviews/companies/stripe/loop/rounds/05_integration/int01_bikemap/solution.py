"""int01 BikeMap — reference solution.

GeoJSON ride -> nearest-landmark analysis -> PNG rendering against the local `maps`
mockserver (`loop/mockserver/maps.py`) -> a small batching/caching CLI.

Public API (same shape as starter.py / starter_template.py):
    load_coordinates(path) -> list[tuple[float, float]]      Part 1
    first_n(coords, n=10) -> list[str]                        Part 1
    render_map(base_url, coords, out_path) -> int              Part 2
    render_route(base_url, coords, landmarks, out_path) -> bytes   Part 3
    nearest_point(coords, landmark) -> tuple[int, float]        Part 4
    nearest_for_all(coords, landmarks) -> dict[str, tuple[int, float]]  Part 4
    cli(argv) -> int                                            Part 5
    main(stdin=sys.stdin, stdout=sys.stdout) -> None            PART n driver for io tests

Only stdlib: `json`, `urllib.request`, `math`, `argparse`, `hashlib`, `pathlib`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import urllib.error
import urllib.request
from pathlib import Path

EARTH_RADIUS_M = 6_371_000.0
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


class MapError(Exception):
    """Raised for any network error or non-200 response from the maps server."""


# --------------------------------------------------------------------------- Part 1


def load_coordinates(path: str) -> list[tuple[float, float]]:
    """Read a GeoJSON FeatureCollection (one LineString feature) and return
    (lat, lng) tuples in ride order.

    GeoJSON coordinates are stored [lng, lat] (the classic trap: it is NOT [lat, lng]
    like most human-facing APIs) — this function does the swap so every other part of
    this module works in (lat, lng) order.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features") if isinstance(data, dict) else None
    if not features:
        raise ValueError(f"{path}: no features in FeatureCollection")

    geometry = features[0].get("geometry", {})
    if geometry.get("type") != "LineString":
        raise ValueError(f"{path}: expected a LineString geometry, got {geometry.get('type')!r}")

    raw_coords = geometry.get("coordinates")
    if not isinstance(raw_coords, list) or len(raw_coords) < 2:
        raise ValueError(f"{path}: LineString needs >= 2 coordinate pairs")

    return [(float(lat), float(lng)) for lng, lat in raw_coords]


def first_n(coords: list[tuple[float, float]], n: int = 10) -> list[str]:
    """Format the first `n` coordinates as 'lat,lng' with 6 decimal places."""
    return [f"{lat:.6f},{lng:.6f}" for lat, lng in coords[:n]]


# --------------------------------------------------------------------------- Part 2


def _post_json(base_url: str, path: str, payload: dict) -> bytes:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise MapError(f"maps server returned HTTP {resp.status}")
            return resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise MapError(f"maps server returned HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise MapError(f"could not reach maps server at {base_url!r}: {e.reason}") from e
    except OSError as e:  # connection refused, timeout, etc. (also a URLError subclass usually)
        raise MapError(f"network error talking to maps server: {e}") from e


def render_map(base_url: str, coords: list[tuple[float, float]], out_path: str) -> int:
    """POST the ride's points to /render and save the PNG response to `out_path`.
    Returns the number of bytes written. Raises MapError on any network error or
    non-200 response."""
    png_bytes = _post_json(base_url, "/render", {"points": [[lat, lng] for lat, lng in coords]})
    with open(out_path, "wb") as f:
        f.write(png_bytes)
    return len(png_bytes)


# --------------------------------------------------------------------------- Part 3


def render_route(
    base_url: str,
    coords: list[tuple[float, float]],
    landmarks: list[dict],
    out_path: str,
) -> bytes:
    """Like render_map, but also sends `landmarks` as markers, and defensively verifies
    the response actually is a PNG (checks the 8-byte magic number) before trusting it
    — a server that returns a JSON error body with a 200 status, or truncated bytes,
    should not silently produce a corrupt file on disk."""
    markers = [[lm["lat"], lm["lng"], lm.get("name", "")] for lm in landmarks]
    png_bytes = _post_json(
        base_url, "/render", {"points": [[lat, lng] for lat, lng in coords], "markers": markers}
    )
    if png_bytes[:8] != PNG_MAGIC:
        raise MapError("response did not look like a PNG (bad magic number)")
    with open(out_path, "wb") as f:
        f.write(png_bytes)
    return png_bytes


# --------------------------------------------------------------------------- Part 4


def _haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def nearest_point(coords: list[tuple[float, float]], landmark: dict) -> tuple[int, float]:
    """Index into `coords` (0-based) of the closest point to `landmark`, and the
    great-circle distance in meters (Haversine, Earth radius 6,371,000 m)."""
    if not coords:
        raise ValueError("coords must be non-empty")
    best_idx, best_dist = 0, math.inf
    lat0, lng0 = landmark["lat"], landmark["lng"]
    for i, (lat, lng) in enumerate(coords):
        d = _haversine_m(lat0, lng0, lat, lng)
        if d < best_dist:
            best_idx, best_dist = i, d
    return best_idx, best_dist


def nearest_for_all(coords: list[tuple[float, float]], landmarks: list[dict]) -> dict[str, tuple[int, float]]:
    """{landmark name -> (nearest index, distance_m)} for every landmark, in the input
    landmarks order (dict preserves insertion order in Python 3.7+, and callers that
    need it explicitly should iterate `landmarks` themselves rather than sort the dict)."""
    return {lm["name"]: nearest_point(coords, lm) for lm in landmarks}


# --------------------------------------------------------------------------- Part 5


def _coords_hash(coords: list[tuple[float, float]]) -> str:
    """Stable content hash of a coordinate set — same coordinates (any two runs that
    load the same ride file) hash identically, so the CLI can skip a re-render."""
    payload = json.dumps([[round(lat, 6), round(lng, 6)] for lat, lng in coords]).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def _load_landmarks(path: str | None) -> list[dict]:
    if not path:
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_cli_args(argv: list[str] | None):
    """argparse setup for `cli`, split out so `cli` itself stays a plain dispatch loop."""
    parser = argparse.ArgumentParser(prog="int01-bikemap")
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--server", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--landmarks", default=None)
    parser.add_argument("--cache-dir", required=True)
    return parser.parse_args(argv)


def _render_or_reuse(
    input_path: str,
    coords: list[tuple[float, float]],
    server: str,
    out_dir: Path,
    cache_dir: Path,
    index: dict[str, str],
) -> tuple[str, int]:
    """Render one ride's PNG to `out_dir`, or copy it from `cache_dir` if the coordinate
    content hash is already cached. Returns (status, bytes_written); mutates `index` in
    place on a fresh render (caller persists it once after the whole batch)."""
    h = _coords_hash(coords)
    out_path = out_dir / (Path(input_path).stem + ".png")
    cache_path = cache_dir / f"{h}.png"

    if h in index and cache_path.exists():
        out_path.write_bytes(cache_path.read_bytes())
        return "cached", out_path.stat().st_size

    n_bytes = render_map(server, coords, str(out_path))
    cache_path.write_bytes(out_path.read_bytes())
    index[h] = input_path
    return "rendered", n_bytes


def cli(argv: list[str] | None = None) -> int:
    """Batch-render one or more ride files, reusing the maps server response when two
    input files produce the identical coordinate set (content-hash cache under
    --cache-dir), and print each ride's nearest-landmark summary to stdout.

    --input       one or more GeoJSON ride files
    --server      base URL of the maps mockserver
    --out         output directory for rendered PNGs (one per --input, named
                  '<stem>.png')
    --landmarks   landmarks JSON (optional — nearest-landmark lines are skipped if
                  omitted)
    --cache-dir   directory holding '<hash>.png' cache entries + 'index.json'
                  (hash -> source input path), created if missing
    """
    args = _parse_cli_args(argv)
    out_dir, cache_dir = Path(args.out), Path(args.cache_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    index_path = cache_dir / "index.json"
    index: dict[str, str] = json.loads(index_path.read_text()) if index_path.exists() else {}
    landmarks = _load_landmarks(args.landmarks)

    for input_path in args.input:
        coords = load_coordinates(input_path)
        status, n_bytes = _render_or_reuse(input_path, coords, args.server, out_dir, cache_dir, index)
        print(f"{input_path}: {status} ({n_bytes} bytes)")
        for lm in landmarks:
            idx, dist = nearest_point(coords, lm)
            print(f"  {lm['name']}: index={idx} distance_m={dist:.1f}")

    index_path.write_text(json.dumps(index, indent=2))
    return 0


# --------------------------------------------------------------------------- PART n stdin driver


def _read_nonblank(stdin) -> list[str]:
    return [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """Dispatches on a leading 'PART n' line, remaining non-blank lines are that part's
    positional arguments. Used by io tests; not the primary way this module is used
    (Parts 1-5's functions and `cli` are)."""
    lines = _read_nonblank(stdin)
    if not lines or not lines[0].upper().startswith("PART"):
        return
    part = int(lines[0].split()[1])
    args = lines[1:]
    out: list[str] = []

    if part == 1:
        input_path = args[0]
        n = int(args[1]) if len(args) > 1 else 10
        out = first_n(load_coordinates(input_path), n)

    elif part == 2:
        server, input_path, out_path = args
        coords = load_coordinates(input_path)
        n_bytes = render_map(server, coords, out_path)
        out = [f"{n_bytes} bytes"]

    elif part == 3:
        server, input_path, landmarks_path, out_path = args
        coords = load_coordinates(input_path)
        landmarks = _load_landmarks(landmarks_path)
        try:
            png_bytes = render_route(server, coords, landmarks, out_path)
        except MapError:
            out = ["NOT_PNG"]
        else:
            out = [f"{len(png_bytes)} bytes"]

    elif part == 4:
        input_path, landmarks_path = args
        coords = load_coordinates(input_path)
        landmarks = _load_landmarks(landmarks_path)
        for lm in landmarks:
            idx, dist = nearest_point(coords, lm)
            out.append(f"{lm['name']}: index={idx} distance_m={dist:.1f}")

    elif part == 5:
        cli(args)
        stdout.flush()
        return

    else:
        raise ValueError(f"unknown PART {part!r}")

    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
