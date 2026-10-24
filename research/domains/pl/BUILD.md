# Programming languages (`pl`) — BUILD

> Build record for skill `building-study-domains`, started 2026-10-23. Skeleton `skeleton/pl.yaml`, cards
> `vault/domains/pl/cards/`. Chi asked for a cards-first deck that compares Go, Java, Rust and Python from general
> language features, with examples, to understand languages from first principles, their modern evolution and what is
> unique to each; a wide, structured map.

## Step 1 — field outlines the skeleton is the union of

| Outline | Covers |
|---|---|
| Pierce, *Types and Programming Languages* (TOC) | static/dynamic, inference, subtyping, polymorphism, ADTs |
| Scott, *Programming Language Pragmatics* (TOC) | names and scopes, control flow, types, subroutines, data abstraction, concurrency, runtime, compilation |
| Krishnamurthi, *PLAI*; Nystrom, *Crafting Interpreters* | execution models, closures, GC, interpreters |
| Official references: Go spec + memory model, JLS + JVMS, The Rust Reference + Nomicon, Python Language Reference + CPython internals | each language's semantics |
| Common interview / comparison topics (GC vs ownership, goroutines vs threads vs async, generics implementations, error models) | probes |

Out of scope: formal semantics, logic and dependent types, parsing theory beyond the pipeline overview, language-specific
library tours.

## Step 2 — skeleton

13 branches, 94 leaves, `lang: zh`; core = foundations, types, memory, errors, concurrency. `validate` 0 errors.

## Step 4 — cards

Five agent groups (`research/domains/pl/prompt_*.md`), 6–8 cards per leaf, every code example compiled and run on the
local toolchains (Go 1.27, Rust 1.99, Java 25, Python 3.14).

## Ledger

| Date | Step | Result |
|---|---|---|
| 2026-10-23 | 2 skeleton | 107 nodes / 94 leaves, 0 errors |
| 2026-10-23 | 4 cards | Chi redirected twice mid-run: senior framing (reasoning, trade-offs, best practice; no syntax tours), then foundation cards introducing every feature from zero; groups revised accordingly |
| 2026-10-23 | 5 review | agents' least-sure claims checked; fixed: Go Green Tea collector (verified in Go 1.27 source), CPython 3.14 tail-call interpreter gain worded as single-digit percent; Go 1.27 generic methods found by compiling |
| 2026-10-23 | 8 ship | 944 cards, 94/94 leaves ordered, validate 0 errors; anki-push published (944 in Anki) |

## Next action

Chi's gap review (2026-10-23), proposed and awaiting a go: new branches "names, binding and evaluation" (scope,
binding time, parameter passing, evaluation strategy and order) and "engineering: measure and verify" (profilers,
benchmarks, fuzzing, property tests, sanitizers, Miri, race detector); extend runtime (syntax and parsing, linking and
ABI, optimisations), concurrency (I/O models: readiness vs completion, netpoller, NIO, mio, asyncio), types (soundness,
HKT, type classes vs traits, associated types, affine/linear types, effects); one drill per branch.
