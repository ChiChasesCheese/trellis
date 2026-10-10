"""Mutation check: each mutant is a problem's Solution.java with one bug, compiled as class Mutant and graded by the
same tests (-Dimpl=mutant). Every mutant must fail at least one test.

Usage (inside java/): python3 mutation_check.py q01              # mutants of q01/Solution.java
                      python3 mutation_check.py q02 Functional   # mutants of q02/Functional.java (key "q02/Functional")
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
    "q02": {
        "average rounded, not truncated": ("return runtime / jobs;", "return Math.round((double) runtime / jobs);"),
        "ascending by runtime": ("Comparator.comparingLong(Chain::runtime).reversed()", "Comparator.comparingLong(Chain::runtime)"),
        "ties by start descending": (".thenComparingLong(Chain::start)", ".thenComparing(Comparator.comparingLong(Chain::start).reversed())"),
        "header not checked": ("if (end == 0 || !lines.get(0).strip().equals(HEADER)) {", "if (end == 0) {"),
        "split drops trailing empty fields": ('split(",", -1)', 'split(",")'),
        "sign accepted": ('Pattern.compile("\\\\d+")', 'Pattern.compile("[+-]?\\\\d+")'),
        "spaces inside fields trimmed": ("if (!NON_NEGATIVE_INTEGER.matcher(field).matches()) {", "field = field.strip();\n        if (!NON_NEGATIVE_INTEGER.matcher(field).matches()) {"),
        "id 0 allowed": ("if (job.id() == 0) {", "if (false) {"),
        "duplicate id overwrites": ("if (jobs.putIfAbsent(job.id(), job) != null) {", "if (jobs.put(job.id(), job) == job) {"),
        "missing next not checked": ("if (!jobs.containsKey(job.next())) {", "if (false) {"),
        "two predecessors allowed": ("if (!hasPredecessor.add(job.next())) {", "if (!hasPredecessor.add(job.next()) && false) {"),
        "cycle not detected": ("if (jobsOnChains != jobs.size()) {", "if (false) {"),
        "minutes not taken mod 60": ("seconds % 3600 / 60", "seconds / 60"),
        "hours wrapped at 24": ("seconds / 3600, seconds", "seconds / 3600 % 24, seconds"),
        "no opening dash": ('new StringBuilder("-\\n")', "new StringBuilder()"),
        "trailing blank lines rejected": ("while (end > 0 && lines.get(end - 1).isBlank()) {", "while (end < 0) {"),  # while (false) does not compile
        "partial report before the error": ("output = render(chains(parse(lines)));", "var parsed = parse(lines);\n            System.out.print(\"-\\n\");\n            output = render(chains(parsed)).substring(2);"),
    },
    "q02/Functional": {
        "missing next not checked": ("if (!jobs.keySet().containsAll(predecessors.keySet())) {", "if (false) {"),
        "two predecessors allowed": ("anyMatch(count -> count > 1)", "anyMatch(count -> count > 2)"),
        "cycle not detected": ("if (chains.stream().mapToLong(Chain::jobs).sum() != jobs.size()) {", "if (false) {"),
        "ascending by runtime": ("Comparator.comparingLong(Chain::runtime).reversed()", "Comparator.comparingLong(Chain::runtime)"),
        "every job treated as a start": (".filter(job -> !predecessors.containsKey(job.id()))", ".filter(job -> true)"),
        "last job is the first job": ("Collectors.reducing((earlier, later) -> later)", "Collectors.reducing((earlier, later) -> earlier)"),
        "walk stops after the start": ("Stream.iterate(start, Objects::nonNull, job -> jobs.get(job.next()))", "Stream.of(start)"),
    },
}


def grade(problem: str, impl: str) -> tuple[int, str]:
    """Runs the problem's tests against impl; returns (failures + errors, summary). Raises if no test ran."""
    try:
        run = subprocess.run(["mvn", "-B", "-q", "test", f"-Dimpl={impl}", f"-Dtest=headland/{problem}/**",
                              "-Dsurefire.failIfNoSpecifiedTests=true"], capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"impl={impl}: the build itself hung; a test without a time limit?")
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


def main(problem: str, source: str = "Solution") -> int:
    key = problem if source == "Solution" else f"{problem}/{source}"
    pkg = pathlib.Path("src/main/java/headland") / problem
    original = (pkg / f"{source}.java").read_text()
    bad, summary = grade(problem, source[0].lower() + source[1:])
    assert bad == 0, f"{source} itself fails: {summary}"
    print(f"control  {source} -> {summary}")
    mutant_file = pkg / "Mutant.java"
    killed = 0
    try:
        for name, (old, new) in MUTANTS[key].items():
            assert old in original, f"pattern for {name!r} not found"
            code = original.replace(old, new, 1).replace(f"class {source}", "class Mutant").replace(f"{source}()", "Mutant()")
            mutant_file.write_text(code)
            bad, summary = grade(problem, "mutant")
            killed += bad > 0
            print(("KILLED   " if bad else "SURVIVED ") + f"{name} -> {summary}")
    finally:
        mutant_file.unlink(missing_ok=True)
    print(f"{killed}/{len(MUTANTS[key])} killed")
    return 0 if killed == len(MUTANTS[key]) else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
