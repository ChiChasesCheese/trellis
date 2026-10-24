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
