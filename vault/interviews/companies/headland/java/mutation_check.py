"""Mutation check: each mutant is a problem's Solution.java with one bug, compiled as class Mutant and graded by the
same tests (-Dimpl=mutant). Every mutant must fail at least one test.

Usage (inside java/): python3 mutation_check.py q01
"""
import pathlib
import re
import subprocess
import sys

MUTANTS = {
    "q01": {
        "15 checked after 3": ("if (i % 15 == 0) {\n                line = \"FizzBuzz\";\n            } else if (i % 3 == 0) {\n                line = \"Fizz\";",
                               "if (i % 3 == 0) {\n                line = \"Fizz\";\n            } else if (i % 15 == 0) {\n                line = \"FizzBuzz\";"),
        "stops at n - 1": ("i <= n", "i < n"),
        "starts at 0": ("int i = 1", "int i = 0"),
        "wrong case": ('"FizzBuzz"', '"Fizzbuzz"'),
        "space instead of newline": (".append('\\n')", ".append(' ')"),
        "trailing space": (".append('\\n')", ".append(\" \\n\")"),
        "own PrintWriter, never flushed": ("System.out.print(out);\n        System.out.flush();",
                                           "new java.io.PrintWriter(System.out).print(out);"),
    },
}


def grade(problem: str, impl: str) -> tuple[int, str]:
    """Runs the problem's tests against impl; returns (failures + errors, summary). Raises if no test ran."""
    run = subprocess.run(["mvn", "-B", "-q", "test", f"-Dimpl={impl}", f"-Dtest=headland/{problem}/**",
                          "-Dsurefire.failIfNoSpecifiedTests=true"], capture_output=True, text=True)
    out = run.stdout + run.stderr
    found = re.findall(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+)", out)
    if not found:
        if run.returncode == 0:   # -q prints nothing when everything passes; count from the reports
            reports = pathlib.Path("target/surefire-reports").glob(f"headland.{problem}.*.txt")
            found = [m for r in reports for m in re.findall(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+)", r.read_text())]
        if not found:
            raise RuntimeError(f"no test summary for impl={impl}: compile error or no tests matched\n{out[-2000:]}")
    ran, failures, errors = map(int, found[-1])
    if ran == 0:
        raise RuntimeError(f"impl={impl}: zero tests ran")
    return failures + errors, f"Tests run: {ran}, Failures: {failures}, Errors: {errors}"


def main(problem: str) -> int:
    pkg = pathlib.Path("src/main/java/headland") / problem
    solution = (pkg / "Solution.java").read_text()
    bad, summary = grade(problem, "solution")
    assert bad == 0, f"the reference itself fails: {summary}"
    print(f"control  solution -> {summary}")
    mutant_file = pkg / "Mutant.java"
    killed = 0
    try:
        for name, (old, new) in MUTANTS[problem].items():
            assert old in solution, f"pattern for {name!r} not found"
            code = solution.replace(old, new, 1).replace("class Solution", "class Mutant").replace("Solution()", "Mutant()")
            mutant_file.write_text(code)
            bad, summary = grade(problem, "mutant")
            killed += bad > 0
            print(("KILLED   " if bad else "SURVIVED ") + f"{name} -> {summary}")
    finally:
        mutant_file.unlink(missing_ok=True)
    print(f"{killed}/{len(MUTANTS[problem])} killed")
    return 0 if killed == len(MUTANTS[problem]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
