"""Accept a batch of problem sets.

  single-file sets (solution.py/starter.py): reference green, empty starter red.
  codebase sets (cbNN_*/acceptance/): acceptance green on solution/, every `core` test red on the untouched
  starter/, and both starter/ and solution/ keep their own test suites green.

usage (from the kit dir): python3 tools/verify_suites.py . "loop/rounds/01_ai_screen/cb*"
"""
import os, pathlib, re, subprocess, sys

KIT = pathlib.Path(sys.argv[1]).resolve()
PROJECT = str(pathlib.Path(__file__).resolve().parents[5])  # trellis repo root (the uv project)
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def run(args, cwd, **env):
    e = dict(os.environ, **env)
    p = subprocess.run(["uv", "run", "--project", PROJECT, "--with", "pytest", "python", "-m", "pytest",
                        *args, "-q", "-p", "no:cacheprovider"], cwd=cwd, env=e, capture_output=True, text=True)
    lines = [ANSI.sub("", l) for l in p.stdout.strip().splitlines() if l.strip()]
    return p.returncode, (lines[-1] if lines else p.stderr.strip()[-200:])


ok = True
for d in sorted(KIT.glob(sys.argv[2])):
    if not d.is_dir():
        continue
    rel = d.relative_to(KIT)
    if (d / "acceptance").is_dir():
        rc_s, sol = run([str(rel / "acceptance")], KIT, IMPL="solution")
        rc_t, sta = run([str(rel / "acceptance"), "-m", "core"], KIT, IMPL="starter")
        starter_all_red = rc_t != 0 and " passed" not in sta
        rc_os, own_s = run([], d / "starter")
        rc_ol, own_l = run([], d / "solution")
        good = rc_s == 0 and starter_all_red and rc_os == 0 and rc_ol == 0
        print(f"{'OK ' if good else 'BAD'} {d.name}\n    acceptance/solution: {sol}\n    acceptance/starter core: {sta}"
              f"\n    own tests starter: {own_s}\n    own tests solution: {own_l}")
    else:
        rc_s, sol = run([str(rel)], KIT, IMPL="solution")
        rc_t, sta = run([str(rel)], KIT, IMPL="starter")
        good = rc_s == 0 and rc_t != 0
        print(f"{'OK ' if good else 'BAD'} {d.name:40s} solution: {sol:40s} | starter: {sta}")
    ok &= good
print("ALL ACCEPTED" if ok else "SOME REJECTED")
