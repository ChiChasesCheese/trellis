"""int01 BikeMap — tests. Uses the `impl` fixture from the repo-root conftest.py
(loads solution.py, or starter.py under IMPL=starter) and the `maps_server` fixture
from this directory's conftest.py (a real loop.mockserver.maps instance on a random
port). `run_script` (repo-root conftest.py) drives the module as a subprocess for io
tests. Data files: data/ride-simple.json (500-point GeoJSON LineString, generated with
random.Random(0) around a fixed Berlin-ish center) and data/landmarks.json (9 points
near the route)."""

from __future__ import annotations

import json
import http.server
import threading
import time
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"
RIDE_PATH = str(DATA_DIR / "ride-simple.json")
LANDMARKS_PATH = str(DATA_DIR / "landmarks.json")

EXPECTED_FIRST_10 = [
    "52.514000,13.390000",
    "52.514043,13.390256",
    "52.514075,13.390517",
    "52.514111,13.390776",
    "52.514156,13.391031",
    "52.514200,13.391287",
    "52.514247,13.391541",
    "52.514284,13.391799",
    "52.514328,13.392055",
    "52.514372,13.392311",
]


def _landmarks():
    return json.loads(Path(LANDMARKS_PATH).read_text())


class _NonPngHandler(http.server.BaseHTTPRequestHandler):
    """A fake /render that returns 200 with a JSON body instead of a PNG -- exercises the
    "don't trust a 200 status alone" defensive-parsing path in render_route."""

    def log_message(self, *a):
        pass

    def do_POST(self):
        body = b'{"not": "a png"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


@pytest.fixture()
def bad_png_server():
    """Base URL of a real local HTTP server whose /render always returns a non-PNG 200."""
    server = http.server.HTTPServer(("127.0.0.1", 0), _NonPngHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)


# --------------------------------------------------------------------------- Part 1


@pytest.mark.part1
def test_worked_example_first_10(impl):
    coords = impl.load_coordinates(RIDE_PATH)
    assert len(coords) == 500
    assert impl.first_n(coords, 10) == EXPECTED_FIRST_10


@pytest.mark.part1
@pytest.mark.edge
def test_lng_lat_order_is_swapped_not_identity(impl, tmp_path):
    """The classic GeoJSON trap: coordinates are [lng, lat]. A solution that forgets to
    swap will return (lng, lat) instead of (lat, lng) -- assert against a point where
    lat and lng are clearly distinguishable (lat near 52, lng near 13)."""
    geo = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[13.4, 52.5], [13.41, 52.51]]},
            }
        ],
    }
    p = tmp_path / "tiny.json"
    p.write_text(json.dumps(geo))
    coords = impl.load_coordinates(str(p))
    assert coords[0] == (52.5, 13.4)
    assert coords[1] == (52.51, 13.41)


@pytest.mark.part1
@pytest.mark.edge
def test_fewer_than_two_points_raises(impl, tmp_path):
    geo = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[13.4, 52.5]]}}],
    }
    p = tmp_path / "one_point.json"
    p.write_text(json.dumps(geo))
    with pytest.raises(Exception):
        impl.load_coordinates(str(p))


@pytest.mark.part1
@pytest.mark.fmt
def test_first_n_six_decimal_format(impl):
    coords = [(1.0, 2.0), (3.14159265, -4.987654321)]
    out = impl.first_n(coords, 2)
    assert out == ["1.000000,2.000000", "3.141593,-4.987654"]


@pytest.mark.part1
@pytest.mark.edge
def test_first_n_fewer_than_n_available(impl):
    coords = [(1.0, 2.0), (3.0, 4.0)]
    assert impl.first_n(coords, 10) == ["1.000000,2.000000", "3.000000,4.000000"]


# --------------------------------------------------------------------------- Part 2


@pytest.mark.part2
def test_render_map_happy_path(impl, maps_server, tmp_path):
    coords = impl.load_coordinates(RIDE_PATH)
    out_path = tmp_path / "ride.png"
    n_bytes = impl.render_map(maps_server, coords, str(out_path))
    assert out_path.exists()
    assert n_bytes == out_path.stat().st_size
    assert out_path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


@pytest.mark.part2
@pytest.mark.edge
def test_render_map_connection_refused_raises_maperror(impl, tmp_path):
    coords = [(0.0, 0.0), (1.0, 1.0)]
    with pytest.raises(impl.MapError):
        impl.render_map("http://127.0.0.1:1", coords, str(tmp_path / "x.png"))


@pytest.mark.part2
@pytest.mark.edge
def test_render_map_non_200_raises_maperror(impl, maps_server, tmp_path):
    # > 10000 points -> maps server responds 413
    coords = [(0.0001 * i, 0.0001 * i) for i in range(10001)]
    with pytest.raises(impl.MapError):
        impl.render_map(maps_server, coords, str(tmp_path / "x.png"))


# --------------------------------------------------------------------------- Part 3


@pytest.mark.part3
def test_render_route_with_markers_is_valid_png(impl, maps_server, tmp_path):
    coords = impl.load_coordinates(RIDE_PATH)
    out_path = tmp_path / "route.png"
    png_bytes = impl.render_route(maps_server, coords, _landmarks(), str(out_path))
    assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"
    assert out_path.read_bytes() == png_bytes


@pytest.mark.part3
@pytest.mark.edge
def test_render_route_rejects_non_png_response(impl, bad_png_server, tmp_path):
    """A defensive client should not trust a 200 status alone -- if the server (bug, or
    a misconfigured endpoint) returns a 200 with a non-PNG body, render_route must
    raise MapError rather than silently writing garbage to out_path."""
    coords = [(0.0, 0.0), (1.0, 1.0)]
    with pytest.raises(impl.MapError):
        impl.render_route(bad_png_server, coords, [], str(tmp_path / "bad.png"))
    assert not (tmp_path / "bad.png").exists()


# --------------------------------------------------------------------------- Part 4


@pytest.mark.part4
def test_nearest_point_haversine_known_value(impl):
    # 1 degree of latitude at the equator is ~111,195 m (great-circle, R=6,371,000)
    coords = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    landmark = {"name": "L", "lat": 0.0, "lng": 0.0}
    idx, dist = impl.nearest_point(coords, landmark)
    assert idx == 0
    assert dist == pytest.approx(0.0, abs=1e-6)

    landmark2 = {"name": "L2", "lat": 1.0, "lng": 0.0}
    idx2, dist2 = impl.nearest_point(coords, landmark2)
    assert idx2 == 1
    assert dist2 == pytest.approx(0.0, abs=1e-6)


@pytest.mark.part4
def test_nearest_point_ties_pick_first_index(impl):
    coords = [(0.0, 0.0), (0.0, 0.0), (10.0, 10.0)]
    landmark = {"name": "L", "lat": 0.0, "lng": 0.0}
    idx, dist = impl.nearest_point(coords, landmark)
    assert idx == 0
    assert dist == pytest.approx(0.0, abs=1e-6)


@pytest.mark.part4
def test_worked_example_nearest_for_all(impl):
    coords = impl.load_coordinates(RIDE_PATH)
    result = impl.nearest_for_all(coords, _landmarks())
    assert set(result) == {lm["name"] for lm in _landmarks()}
    idx, dist = result["Museumsufer"]
    assert idx == 189
    assert dist == pytest.approx(2.6, abs=0.5)


# --------------------------------------------------------------------------- Part 5


@pytest.mark.part5
def test_cli_renders_and_prints_summary(impl, maps_server, tmp_path, capsys):
    out_dir = tmp_path / "out"
    cache_dir = tmp_path / "cache"
    rc = impl.cli(
        [
            "--input",
            RIDE_PATH,
            "--server",
            maps_server,
            "--out",
            str(out_dir),
            "--cache-dir",
            str(cache_dir),
            "--landmarks",
            LANDMARKS_PATH,
        ]
    )
    assert rc == 0
    png_files = list(out_dir.glob("*.png"))
    assert len(png_files) == 1
    assert png_files[0].read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    captured = capsys.readouterr()
    assert "rendered" in captured.out
    assert "Museumsufer" in captured.out


@pytest.mark.part5
@pytest.mark.edge
def test_cli_cache_hit_avoids_second_render(impl, maps_server, tmp_path, capsys):
    out_dir = tmp_path / "out"
    cache_dir = tmp_path / "cache"
    common = ["--server", maps_server, "--out", str(out_dir), "--cache-dir", str(cache_dir)]

    rc1 = impl.cli(["--input", RIDE_PATH, *common])
    assert rc1 == 0
    first_out = capsys.readouterr().out
    assert "rendered" in first_out

    # A different filename, identical coordinate content -> same hash -> cache hit.
    dup_path = tmp_path / "ride-copy.json"
    dup_path.write_text(Path(RIDE_PATH).read_text())
    rc2 = impl.cli(["--input", str(dup_path), *common])
    assert rc2 == 0
    second_out = capsys.readouterr().out
    assert "cached" in second_out
    assert "rendered" not in second_out


@pytest.mark.part5
def test_cli_batch_multiple_inputs(impl, maps_server, tmp_path):
    out_dir = tmp_path / "out"
    cache_dir = tmp_path / "cache"
    small_a = tmp_path / "a.json"
    small_b = tmp_path / "b.json"
    small_a.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[13.0, 52.0], [13.01, 52.01], [13.02, 52.02]],
                        },
                    }
                ],
            }
        )
    )
    small_b.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[14.0, 53.0], [14.01, 53.01], [14.02, 53.02]],
                        },
                    }
                ],
            }
        )
    )
    rc = impl.cli(
        [
            "--input",
            str(small_a),
            str(small_b),
            "--server",
            maps_server,
            "--out",
            str(out_dir),
            "--cache-dir",
            str(cache_dir),
        ]
    )
    assert rc == 0
    assert sorted(p.name for p in out_dir.glob("*.png")) == ["a.png", "b.png"]


# --------------------------------------------------------------------------- io


@pytest.mark.part1
@pytest.mark.io
def test_io_part1(run_script):
    r = run_script(f"PART 1\n{RIDE_PATH}\n10\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EXPECTED_FIRST_10) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_io_part3_happy(run_script, maps_server, tmp_path):
    out_path = tmp_path / "route.png"
    r = run_script(f"PART 3\n{maps_server}\n{RIDE_PATH}\n{LANDMARKS_PATH}\n{out_path}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == f"{out_path.stat().st_size} bytes\n"
    assert out_path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.edge
def test_io_part3_not_png(run_script, bad_png_server, tmp_path):
    """The PART n driver must catch render_route's MapError and print 'NOT_PNG' per
    problem.md, not let the exception crash the process with a nonzero exit code."""
    out_path = tmp_path / "bad.png"
    r = run_script(f"PART 3\n{bad_png_server}\n{RIDE_PATH}\n{LANDMARKS_PATH}\n{out_path}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "NOT_PNG\n"
    assert not out_path.exists()


@pytest.mark.part4
@pytest.mark.io
def test_io_part4(run_script):
    r = run_script(f"PART 4\n{RIDE_PATH}\n{LANDMARKS_PATH}\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.strip().splitlines()
    assert len(lines) == len(_landmarks())
    assert lines[3].startswith("Museumsufer: index=189")


@pytest.mark.part1
@pytest.mark.io
def test_io_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0
    assert r.stdout == ""


# --------------------------------------------------------------------------- perf


@pytest.mark.part4
@pytest.mark.perf
def test_perf_nearest_for_all_100k_points(impl):
    import random

    rng = random.Random(0)
    coords = [(52.0 + rng.random() * 0.5, 13.0 + rng.random() * 0.5) for _ in range(100_000)]
    landmarks = [
        {"name": f"lm{i}", "lat": 52.0 + rng.random() * 0.5, "lng": 13.0 + rng.random() * 0.5}
        for i in range(10)
    ]
    t0 = time.perf_counter()
    result = impl.nearest_for_all(coords, landmarks)
    elapsed = time.perf_counter() - t0
    assert len(result) == 10
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"
