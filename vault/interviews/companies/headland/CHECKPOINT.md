# CHECKPOINT — Headland kit

**State (2026-10-10):** environment only. `java/` is a Maven project on Java 21 + JUnit 5.11; `mvn -q test` passes the
toolchain smoke test (sealed interface, records, pattern `switch`).

**q01 FizzBuzz (2026-10-10):** statement from a photo of the HackerRank screen; `Solution.java` 12/12, empty
`Starter.java` 12/12 red, `mutation_check.py q01` 7/7 killed; `study/q01_fizzbuzz.md`.

**q02 Job Runner (2026-10-10):** statement from photos; malformed rules the statement leaves open are decided and
labelled *inferred* in `study/q02_job_runner.md` §1. `Solution.java` 42/42, empty `Starter.java` all red,
`mutation_check.py q02` 17/17 killed (two survivors found and fixed by new tests).

**q02 functional variant (2026-10-10):** `Functional.java` written with streams throughout (`List.reversed` +
`dropWhile`, whole-line regex + `Optional`, `groupingBy`/`counting`, `Stream.iterate`, `teeing`, `joining` prefix,
`Duration` parts) passes the same 42 tests; `mutation_check.py q02 Functional` 15/15.

**Next action:** Chi read the reference block by block, then rewrites `headland/q02/Starter.java` from scratch and
pastes it for a line-by-line review. q01 Starter still open.
