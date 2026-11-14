"""Write the synthetic sweep files in data/ (deterministic).

    uv run --project <repo root> python make_data.py

- data/sweep_ab.csv          models A and B, three traffic profiles, one header style, TTFT in milliseconds.
- data/Model_C_profile_2.csv model C, one profile, no model/profile columns (they come from the file name),
                             other header names, TTFT in seconds.

The numbers follow a simple serving model: per-user speed falls as more users share the hardware, total speed
rises, and the wait for the first token grows with the prompt length and the load. A few defects are planted on
purpose (see PLANTED); the anomaly checker should find exactly those.
"""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
# model -> (per-user tokens/s with one user, how fast that drops with load, prefill ms per 1000 prompt tokens)
MODELS = {"A": (2100.0, 48.0, 30.0), "B": (950.0, 40.0, 70.0), "C": (420.0, 32.0, 160.0)}
PROFILES = {"1": (1000, 300), "2": (8000, 200), "3": (500, 4000)}  # profile -> (input tokens, output tokens)
CONCURRENCY = [1, 4, 16, 64]
PLANTED = {
    ("A", "2", 16): "ttft_drop",         # TTFT lower than at concurrency 4
    ("B", "3", 64): "throughput_drop",   # total tokens/s lower than at 16
    ("C", "2", 4): "total_mismatch",     # total tokens/s does not equal per-user x users
    ("B", "1", 4): "missing_value",      # an empty TTFT cell
}


def point(model: str, profile: str, c: int) -> dict:
    v1, half, prefill = MODELS[model]
    isl, osl = PROFILES[profile]
    tps_user = v1 / (1 + c / half)
    ttft = prefill * isl / 1000 * (1 + c / 12) + 20
    total = tps_user * c
    kind = PLANTED.get((model, profile, c))
    if kind == "ttft_drop":
        ttft *= 0.5
    elif kind == "throughput_drop":
        total *= 0.4
        tps_user *= 0.4
    elif kind == "total_mismatch":
        total *= 1.6
    return {"isl": isl, "osl": osl, "c": c, "ttft_ms": round(ttft, 1), "tpot_ms": round(1000 / tps_user, 2),
            "tps_user": round(tps_user, 1), "total": round(total, 1),
            "missing": kind == "missing_value"}


def main() -> None:
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    with (out / "sweep_ab.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "profile", "input_tokens", "output_tokens", "concurrency", "TTFT (ms)", "TPOT (ms)",
                    "tok/s/user", "total tok/s"])
        for m in ("A", "B"):
            for p in PROFILES:
                for c in CONCURRENCY:
                    r = point(m, p, c)
                    w.writerow([m, p, r["isl"], r["osl"], c, "" if r["missing"] else r["ttft_ms"],
                                r["tpot_ms"], r["tps_user"], r["total"]])
    with (out / "Model_C_profile_2.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ISL", "OSL", "batch_size", "ttft_s", "ITL (ms)", "Tokens/s per user", "Throughput", "notes"])
        for c in CONCURRENCY:
            r = point("C", "2", c)
            w.writerow([r["isl"], r["osl"], c, round(r["ttft_ms"] / 1000, 4), r["tpot_ms"], r["tps_user"],
                        r["total"], "projection"])
    print("wrote data/sweep_ab.csv, data/Model_C_profile_2.csv")


if __name__ == "__main__":
    main()
