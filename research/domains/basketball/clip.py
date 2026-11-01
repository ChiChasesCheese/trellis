"""Download one clip for the basketball deck, or extract frames to check a clip.

    uv run --with yt-dlp --with imageio-ffmpeg python research/domains/basketball/clip.py <url> <leaf-slug> [--start S] [--end S]
    uv run --with imageio-ffmpeg python research/domains/basketball/clip.py --frames <clip.mp4> <out-prefix>

Clips are personal study copies: they live in vault/domains/basketball/media/ (gitignored, never in the public repo) and
reach Anki inside the .apkg. research/domains/basketball/clips.json records only the source link and the cut.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[3]
MEDIA = ROOT / "vault/domains/basketball/media"
LOG = ROOT / "research/domains/basketball/clips.json"
FF = imageio_ffmpeg.get_ffmpeg_exe()
MAX_SECONDS = 120


def frames(clip: str, prefix: str) -> None:
    Path(prefix).parent.mkdir(parents=True, exist_ok=True)
    probe = subprocess.run([FF, "-i", clip], capture_output=True, text=True).stderr
    import re
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", probe)
    total = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 20
    for i in range(4):
        t = total * (i + 0.5) / 4
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", clip, "-frames:v", "1", "-vf", "scale=480:-1",
                        f"{prefix}-{i}.png"], check=True)
    print(f"{total:.1f}s; frames at {prefix}-0..3.png")


def sheet(url: str, prefix: str) -> None:
    """Download a source once and print a contact sheet (one frame every 5 s, numbered) to pick the densest segment."""
    Path(prefix).parent.mkdir(parents=True, exist_ok=True)
    raw = Path(prefix + ".src.mp4")
    if not raw.exists():
        subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-playlist", "--js-runtimes", "node", "--ffmpeg-location", FF, "-f",
                        "b[height<=480][ext=mp4]/bv*[height<=480][ext=mp4]+ba[ext=m4a]/b", "--merge-output-format", "mp4",
                        "-o", str(raw), url], check=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(raw), "-vf",
                    "fps=1/5,scale=240:-1,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=18:fontcolor=white:box=1:boxcolor=black,tile=6x10",
                    f"{prefix}-sheet-%d.png"], check=True)
    print(f"{prefix}-sheet-*.png (each tile = 5 s)")


def main(argv: list[str]) -> None:
    if argv[0] == "--frames":
        frames(argv[1], argv[2])
        return
    if argv[0] == "--sheet":
        sheet(argv[1], argv[2])
        return
    url, slug = argv[0], argv[1]
    start = float(argv[argv.index("--start") + 1]) if "--start" in argv else 0.0
    end = float(argv[argv.index("--end") + 1]) if "--end" in argv else None
    MEDIA.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw.mp4"
        subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-playlist", "--js-runtimes", "node", "--ffmpeg-location", FF, "-f",
                        "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/b", "--merge-output-format", "mp4",
                        "-o", str(raw), url], check=True)
        dur = (end - start) if end is not None else MAX_SECONDS
        out = MEDIA / f"bb-{slug}.mp4"
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(start), "-i", str(raw), "-t", str(min(dur, MAX_SECONDS)),
                        "-vf", "scale=640:-2", "-c:v", "libx264", "-profile:v", "baseline", "-pix_fmt", "yuv420p", "-crf", "30",
                        "-preset", "veryfast", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(out)], check=True)
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {}
    log[slug] = {"url": url, "start": start, "end": end}
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    print(out, f"{out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main(sys.argv[1:])
