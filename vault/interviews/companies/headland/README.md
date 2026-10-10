# Headland kit

Started 2026-10-10 for a Headland mock coding test that Chi takes in **Java 21**. This is not yet a full kit: the
GitHub-first survey, `catalog/CATALOG.md` ranking and loop guide from `building-company-interview-kits` have not been
done. See `CHECKPOINT.md`.

| Path | What |
|---|---|
| `catalog/raw/` | sources, verbatim, URL or photo + date |
| `java/` | one Maven project (Java 21, JUnit 5) for every problem in this kit; one package per problem |
| `study/` | 中文：逐题带写、Java 21 语法与最佳实践回顾 |
| `java/mutation_check.py` | one-bug variants of a problem's `Solution.java`; every one must fail a test (`python3 mutation_check.py q01`) |

| Problem | Package | Tests | Study |
|---|---|---|---|
| q01 FizzBuzz | `headland.q01` | `FizzBuzzTest` (12), 7/7 mutants killed | `study/q01_fizzbuzz.md` |
| q02 Job Runner | `headland.q02` (`Solution` imperative, `Functional` streams throughout) | `JobRunnerTest` (42); mutants 17/17 and 15/15 | `study/q02_job_runner.md` |

```bash
cd vault/interviews/companies/headland/java
mvn -q test                                   # reference solutions (default -Dimpl=solution)
mvn -q test -Dimpl=starter                    # your code
mvn -q test -Dimpl=starter -Dtest='headland/q01/**'  # one problem
```

Layout per problem `qNN_name` (package `headland.qNN`): the interface in `src/main/java/headland/qNN/`,
`Starter.java` (yours) and `Solution.java` (reference) next to it, tests in `src/test/java/headland/qNN/`, one class per
level. Tests pick the implementation from the `impl` system property, so the same suite grades both.
`.java` files are invisible to Obsidian and ignored by `trellis` (it reads `*.md` only); `java/target/` is git-ignored.
