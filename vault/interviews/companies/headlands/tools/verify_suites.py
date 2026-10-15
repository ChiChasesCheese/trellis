"""Accept a batch of problem sets: reference must be green, empty starter must be red.

usage (from the kit dir): python3 tools/verify_suites.py . "loop/rounds/04_ood/od*"
"""
import pathlib, re, subprocess, sys

KIT = pathlib.Path(sys.argv[1])
PROJECT = str(pathlib.Path(__file__).resolve().parents[5])  # trellis repo root (the uv project)
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def run(path, impl):
    env = dict(__import__("os").environ, IMPL=impl)
    p = subprocess.run(
        ["uv", "run", "--project", PROJECT, "--with", "pytest", "python", "-m", "pytest",
         str(path), "-q", "-p", "no:cacheprovider"],
        cwd=KIT, env=env, capture_output=True, text=True,
    )
    lines = [ANSI.sub("", l) for l in p.stdout.strip().splitlines() if l.strip()]
    return p.returncode, (lines[-1] if lines else p.stderr.strip()[-200:])


ok = True
for d in sorted(KIT.glob(sys.argv[2])):
    if not d.is_dir():
        continue
    rc_s, sol = run(d.relative_to(KIT), "solution")
    rc_t, sta = run(d.relative_to(KIT), "starter")
    good = rc_s == 0 and rc_t != 0
    ok &= good
    print(f"{'OK ' if good else 'BAD'} {d.name:40s} solution: {sol:40s} | starter: {sta}")
print("ALL ACCEPTED" if ok else "SOME REJECTED")
