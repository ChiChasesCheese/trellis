# BUILD — under-the-hood（工具里的数据结构与算法）

Purpose: a light companion to the LeetCode decks. Each card ties one real implementation (language runtime, standard
library, Redis, Kafka, database, OS, developer tool) to the data structure or algorithm inside it and to the LeetCode
problems that use the same idea. Ordered by how often a backend engineer touches the tool.

## Sources

Primary sources only, checked per claim: source code at a named tag (CPython, OpenJDK, libstdc++, libc++, Go, Rust,
hashbrown, Redis, Kafka, Linux, git, RE2, Lucene, RocksDB, InnoDB / PostgreSQL) and official documentation. The
per-claim ledger is `research/domains/under-the-hood/claims-U*.md`.

## Ledger

| step | date | result |
|---|---|---|
| skeleton | 2026-10-28 | 9 branches, 63 leaves (`skeleton/under-the-hood.yaml`) |
| cards | 2026-10-28 | four card agents (U1 Python + Java, U2 C++ + Go/Rust + Redis, U3 Kafka + storage, U4 OS/network + devtools) |

Readings are deliberately absent: cards first, each with a short mechanism and the matching LeetCode problems.
