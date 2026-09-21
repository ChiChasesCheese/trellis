# Python — BUILD

> Durable record for skill `building-study-domains` (`.claude/skills/building-study-domains/SKILL.md`), started 2026-09-21.
> Why now: Millennium LEaD R1 (45 min live coding + Python-internals questions) exposed that `vault/interviews/companies/millennium/loop/rounds/02_python_internals/` is a 40-question checklist, not understanding. Plan: 7 days full-time; the interview cut (`core: true`) first, the rest after.

## 1. Field survey (step 1)

GitHub first (`search/repositories`): `python interview questions` → yakimka/python_interview_questions (2.6k★, Russian, Q&A), Devinterview-io/python-interview-questions (100 Q, 15 public); `python internals cpython guide` → nothing curated beyond one 19★ handbook; `fluent python example code` → fluentpython/example-code-2e (4.1k★, chapter directories = the book's TOC). No maintained "awesome-python-internals"; the canonical outlines are books + official docs.

| Source | Kind / licence | Covers | How used |
|---|---|---|---|
| **Fluent Python, 2e** (Ramalho, O'Reilly 2022) — TOC from `fluentpython/example-code-2e` README | commercial book; example code MIT | 24 chapters: data model, sequences, dict/set, text vs bytes, data class builders, references & GC, first-class functions, type hints, decorators & closures, Pythonic object, protocols/ABCs, inheritance, operator overloading, iterators/generators/coroutines, with/match/else, concurrency models, executors, async, dynamic attributes, descriptors, class metaprogramming | primary outline for `model`, `functions`, `iteration`, `classes`, `asyncio`; readings tagged `no-archive` per chapter |
| **Effective Python, 3e** (Slatkin, 2024) — TOC from effectivepython.com | commercial | 125 items in 14 chapters: pythonic thinking, strings, loops/iterators, dicts, functions, comprehensions/generators, classes, metaclasses/attributes, concurrency & parallelism, robustness, performance, data structures, testing, collaboration | second outline; `engineering`, `performance`, `concurrency` items; card "contrast" prompts |
| **High Performance Python, 2e** (Gorelick & Ozsvald) — TOC from `mynameisfiber/high_performance_python_2e` | commercial | profiling, lists/tuples, dict/set, iterators, matrix/vector (NumPy), compiling to C, concurrency, multiprocessing, clusters, using less RAM | outline for `performance`, `memory.object-size`, `performance.less-ram` |
| **CPython Internals** (Shaw, Real Python) — chapter list from memory of the book (site 403) | commercial | source layout, compiler, lexer/parser, evaluation loop, memory management, parallelism & concurrency, objects & types, stdlib, testing, debugging, benchmarking | outline for `runtime`, `memory`; the free substitute is CPython InternalDocs (below) |
| **Python Concurrency with asyncio** (Fowler, Manning 2022) — ch. 1 sections from liveBook | commercial | I/O vs CPU bound, concurrency vs parallelism, processes/threads, GIL release, single-threaded concurrency, event loop; later chapters: aiohttp, DB, map-reduce, threads mixing | outline for `concurrency.choosing`, `asyncio.*`, `asyncio.blocking-and-threads` |
| **Python Language Reference** (docs.python.org/3/reference) | PSF, free-online | data model (objects/values/types, type hierarchy, special methods, coroutines), execution model, import system, compound statements | corpus `python-docs`; `model`, `runtime` |
| **Python HOWTOs** | PSF, free-online | descriptor guide, conceptual overview of asyncio (new, ~3.5k words), free-threading, MRO, sorting, functional, unicode, annotations, logging, enum | corpus `python-docs`; `classes.properties-descriptors`, `asyncio.event-loop`, `concurrency.free-threading` |
| **Library reference** (concurrent execution, asyncio sub-pages, runtime services, data types) | PSF, free-online | threading, multiprocessing, concurrent.futures, queue, contextvars, asyncio-task/eventloop/future/sync/queue/dev/runner/exceptions/streams/protocol/threading, gc, weakref, copy, sys, tracemalloc, functools, itertools, contextlib, dataclasses, collections(.abc), abc, typing, exceptions, decimal, datetime, pickle, json, heapq, bisect, array, stdtypes, dis, timeit, profile, unittest.mock, logging, warnings, venv | corpus `python-docs` |
| **CPython InternalDocs** (`python/cpython/InternalDocs`) | PSF, free-online | structure, parser, compiler, code objects, generators, frames, interpreter, JIT, garbage collector, exception handling, QSBR, string interning, asyncio; plus `Objects/listsort.txt`, `Objects/dictnotes.txt` | corpus `cpython-internals`; `runtime.*`, `memory.cyclic-gc`, `memory.interning-immortal`, `performance.containers` |
| **PEPs** 703 · 734 · 683 · 659 · 744 · 492 · 380 · 342 · 343 · 318 · 3148 · 557 · 484 · 544 · 526 · 612 · 695 · 649 · 3119 · 3134 · 654 · 572 · 636 · 412 · 567 · 20 | open, free-online | design + rejected alternatives per feature | corpus `peps`; "why" cards and follow-ups |
| yakimka/python_interview_questions · Devinterview-io | GitHub, Q&A | memory/GC, mutable vs immutable, list vs tuple, `is` vs `==`, decorators, generators, GIL, args/kwargs, modules | interview-probe cross-check: every question maps to a leaf (§3) |
| `vault/interviews/companies/millennium/loop/rounds/02_python_internals/questions.md` | own kit | 40 first-hand/aggregator questions (asyncio, GIL, decorators, memory, pandas, Java HashMap) | every question maps to a leaf (§3); Java rows stay in the kit, out of scope here |

Out of scope (deliberate): C-API and extension writing, curses/tkinter/GUI, packaging for distribution (`zipapp`), Windows/Unix-specific services, networking protocol modules beyond what asyncio needs, Django/Flask frameworks, Java/C++ comparisons (kit-only).

## 2. Skeleton (step 2)

`skeleton/python.yaml`: 11 top-level nodes, 74 leaves, 32 `core: true` (the interview cut). `study: core-first`, 30 new/day so the cut lands in a week.

Outline → node mapping (every surveyed heading lands on a leaf or an out-of-scope line):

| Surveyed heading | Leaf |
|---|---|
| FP ch1 data model · LR 3.3 special methods | `model.dunder-protocols`, `classes.operator-overloading` |
| FP ch2 sequences · EP ch2–3 | `model.sequences`, `iteration.comprehensions`, `performance.containers` |
| FP ch3 dict/set · EP ch4 · dictnotes · PEP 412 | `model.dict-set-internals`, `model.hash-eq` |
| FP ch4 text vs bytes · Unicode HOWTO | `model.text-bytes` |
| FP ch5 data class builders · PEP 557 · EP 51/56 | `classes.dataclasses` |
| FP ch6 references, mutability, GC · EP 30/36 | `model.names-objects`, `model.mutability`, `model.copy`, `memory.refcounting`, `memory.weakref` |
| FP ch7/10 first-class functions · EP ch5 | `functions.first-class`, `functions.arguments`, `functions.functools` |
| FP ch9 decorators & closures · PEP 318 · EP 33/38 | `functions.scope-closure`, `functions.decorators`, `functions.decorator-patterns` |
| FP ch8/15 type hints · PEP 484/544/526/612/695/649 · annotations HOWTO | `types.*` |
| FP ch11–14 Pythonic object, protocols/ABC, inheritance · MRO HOWTO · PEP 3119 · EP ch7 | `classes.pythonic-object`, `classes.abc-protocols`, `classes.inheritance-mro` |
| FP ch17 iterators/generators/coroutines · PEP 342/380 · EP ch6 | `iteration.*` |
| FP ch18 with/match/else · PEP 343/636 · EP 82 | `iteration.context-managers`, `iteration.comprehensions` (match: out of scope beyond one card) |
| FP ch19–20 concurrency models, executors · EP ch9 · HPP ch8–9 · Fowler ch1 · PEP 703/734/3148 · free-threading HOWTO | `concurrency.*` |
| FP ch21 async · asyncio HOWTO · library asyncio-* · PEP 492 · InternalDocs asyncio | `asyncio.*` |
| FP ch22–24 dynamic attributes, descriptors, class metaprogramming · descriptor HOWTO · EP ch8 | `classes.attribute-lookup`, `classes.properties-descriptors`, `classes.metaprogramming` |
| CPython Internals: compiler, eval loop, memory, objects · InternalDocs compiler/interpreter/frames/code objects/generators/GC/interning/JIT · PEP 659/744/683 | `runtime.compile-bytecode`, `runtime.frames-eval`, `runtime.adaptive-jit`, `memory.*` |
| LR import system · tutorial modules · EP 119/122 | `runtime.import-system` |
| LR execution model · EP 91 | `runtime.namespaces-execution` |
| tutorial errors · library exceptions · PEP 3134/654 · EP ch10 | `runtime.exceptions`, `engineering.robustness` |
| HPP profiling, using less RAM, compiling to C · EP ch11 · tracemalloc | `performance.profiling`, `performance.less-ram`, `performance.compiling`, `memory.leaks-tracemalloc` |
| HPP matrix/vector · pandas practice (Millennium R3 first-hand) | `performance.numpy-vectorization`, `performance.pandas-at-scale` |
| EP ch12 data structures (sort key, bisect, deque, heapq, datetime, decimal, pickle) | `runtime.stdlib-map`, `engineering.money-time`, `engineering.serialization` |
| EP ch13 testing · unittest.mock | `engineering.testing` |
| EP ch14 collaboration (venv, packages, warnings, typing) · logging HOWTO | `engineering.packaging-env`, `engineering.logging-config`, `types.gradual-typing` |
| EP ch1 pythonic thinking (PEP 8, walrus, match) | out of scope except one card each under `iteration.comprehensions` |

## 3. Interview probes → leaves (cross-check)

| Question (source) | Leaf |
|---|---|
| Explain asyncio / write working coroutine code (LC Discuss R2) | `asyncio.coroutines-tasks`, `asyncio.event-loop` |
| Missing output in async HTTP flow (PracHub 2025-10) | `asyncio.debugging` |
| Multithreading vs multiprocessing; pandas aggregation on millions of rows (LC Discuss R3) | `concurrency.choosing`, `performance.pandas-at-scale` |
| GIL (all aggregators) | `concurrency.gil` |
| Decorators, generators, context managers (LC Discuss author) | `functions.decorators`, `iteration.generators`, `iteration.context-managers` |
| list vs tuple; memory management for long-running processes (InterviewQuery) | `model.mutability`, `memory.leaks-tracemalloc`, `memory.allocator` |
| Thread-safe singleton (InterviewQuery) | `concurrency.locks-races` |
| `is` vs `==`, mutable vs immutable, memory allocation & GC (Devinterview) | `model.names-objects`, `model.mutability`, `memory.refcounting`, `memory.cyclic-gc` |
| `*args/**kwargs`, lambda, modules (Devinterview) | `functions.arguments`, `functions.first-class`, `runtime.import-system` |
| Favorite data structure and trade-offs (devclub-iitd) | `performance.containers`, `model.dict-set-internals` |
| Money with floats (kit CONVENTIONS) | `model.numbers`, `engineering.money-time` |

## 4. Corpora (step 3)

| id | licence | chapters | status |
|---|---|---|---|
| `python-docs` | free-online | 70 URLs (reference, HOWTO, tutorial, FAQ, library) | declared |
| `cpython-internals` | free-online | 15 (InternalDocs + listsort/dictnotes) | declared |
| `peps` | free-online | 26 | declared |
| Fluent Python 2e / Effective Python 3e / HPP 2e / CPython Internals / Fowler | commercial | — | readings only (`no-archive`); if Chi supplies epubs, declare `license: commercial` + `file:` and ingest into `sources/local/` |

## Ledger

| Date | Step | Result | Evidence |
|---|---|---|---|
| 2026-09-21 | 1 survey | 5 book outlines + official docs + InternalDocs + 26 PEPs + 3 question sets; GitHub has no curated internals outline | §1 |
| 2026-09-21 | 2 skeleton | `skeleton/python.yaml` — 11 nodes / 74 leaves / 32 core; mapping table §2 | `validate` (see below) |

## Next action

3. Ingest the three corpora (`uv run --extra clip trellis ingest python-docs` etc.), triage each onto leaves, accept; record gap verdicts and leaves with no reading.
4. Cards, core leaves first, by top-level node in groups of ≤ 3 sonnet agents (prompt file `vault/domains/python/proposals/AGENT_CARDS.md`).
