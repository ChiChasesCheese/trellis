#!/usr/bin/env python3
"""Transcribe an interview recording locally (nothing leaves the machine).

  uv run --extra debrief python vault/interviews/core/debrief/transcribe.py <audio> -o <outdir>
      [--model mlx-community/whisper-large-v3-turbo] [--language en] [--force]

Writes into <outdir>:
  transcript.json   raw Whisper result: segments with word-level timestamps (input to analyze.py)
  transcript.md     human-readable, one line per segment: [mm:ss–mm:ss] text

Backends (picked automatically): mlx-whisper on Apple Silicon (fast, Metal), else faster-whisper
(CTranslate2, CPU/CUDA). Both are open source; see README.md for the survey.
Any format ffmpeg can read works — mp3, m4a, wav, webm — Whisper decodes through ffmpeg.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

DEFAULT_MLX_MODEL = "mlx-community/whisper-large-v3-turbo"
DEFAULT_CT2_MODEL = "large-v3-turbo"


def _fmt(sec: float) -> str:
    sec = max(0, int(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def _is_apple_silicon() -> bool:
    return sys.platform == "darwin" and platform.machine() == "arm64"


def transcribe_mlx(audio: Path, model: str, language: str | None) -> dict:
    import mlx_whisper  # noqa: WPS433 (optional dependency)

    return mlx_whisper.transcribe(
        str(audio),
        path_or_hf_repo=model,
        language=language,
        word_timestamps=True,
        # Each window is decoded on its own: a hallucinated "Thank you." in a quiet stretch must not
        # seed the next window (Whisper's classic repeat-loop failure on long recordings).
        condition_on_previous_text=False,
    )


def transcribe_ct2(audio: Path, model: str, language: str | None) -> dict:
    from faster_whisper import WhisperModel  # noqa: WPS433 (optional dependency)

    wm = WhisperModel(model, compute_type="int8")
    segments, info = wm.transcribe(
        str(audio), language=language, word_timestamps=True, condition_on_previous_text=False, vad_filter=True
    )
    out = []
    for i, s in enumerate(segments):
        out.append(
            {
                "id": i,
                "start": s.start,
                "end": s.end,
                "text": s.text,
                "no_speech_prob": s.no_speech_prob,
                "words": [{"word": w.word, "start": w.start, "end": w.end, "probability": w.probability} for w in (s.words or [])],
            }
        )
    return {"text": " ".join(s["text"] for s in out), "segments": out, "language": info.language}


def _plain(obj):
    """numpy floats → Python floats so json.dumps works on either backend's output."""
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_plain(v) for v in obj]
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path)
    ap.add_argument("-o", "--outdir", type=Path, required=True)
    ap.add_argument("--model", default=None, help="HF repo (mlx) or CTranslate2 model name (faster-whisper)")
    ap.add_argument("--language", default="en", help="ISO code, or 'auto' to let Whisper detect")
    ap.add_argument("--force", action="store_true", help="re-transcribe even if transcript.json exists")
    a = ap.parse_args()

    if not a.audio.exists():
        sys.exit(f"no such audio: {a.audio}")
    a.outdir.mkdir(parents=True, exist_ok=True)
    out_json = a.outdir / "transcript.json"
    if out_json.exists() and not a.force:
        print(f"{out_json} exists — use --force to redo")
        return

    language = None if a.language == "auto" else a.language
    t0 = time.time()
    if _is_apple_silicon():
        backend, model = "mlx-whisper", a.model or DEFAULT_MLX_MODEL
        result = transcribe_mlx(a.audio, model, language)
    else:
        backend, model = "faster-whisper", a.model or DEFAULT_CT2_MODEL
        result = transcribe_ct2(a.audio, model, language)
    result = _plain(result)
    result["_meta"] = {
        "audio": str(a.audio),
        "backend": backend,
        "model": model,
        "language": language or "auto",
        "seconds": round(time.time() - t0, 1),
    }
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = [f"# transcript · {a.audio.name}", "", f"> {backend} · {model} · {len(result['segments'])} segments · {result['_meta']['seconds']} s", ""]
    for s in result["segments"]:
        text = s["text"].strip()
        if text:
            lines.append(f"[{_fmt(s['start'])}–{_fmt(s['end'])}] {text}")
    (a.outdir / "transcript.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{backend} · {model} · {len(result['segments'])} segments · {result['_meta']['seconds']} s → {a.outdir}")


if __name__ == "__main__":
    main()
