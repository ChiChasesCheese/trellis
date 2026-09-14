---
id: runtime-polyglot-contract-first
node: runtimes.polyglot
type: qa
---
## Q
Go emits cache metadata, TypeScript consumes it, and Lua enforces it. How do you prevent each runtime from inventing a slightly different contract?

## A
Define one versioned wire schema with precise field semantics, generated or validated in every language. Specify defaults, unknown-field handling, units, error codes, and compatibility rules; add cross-language golden fixtures and contract tests. Keep the wire contract smaller than any runtime's internal model. JSON interfaces need runtime validation; Protobuf needs disciplined field evolution. Shared documentation alone is not executable evidence.

## Q zh
Go 产生 cache metadata，TypeScript 消费，Lua 执行。如何防止每个 runtime 发明略有不同的 contract？

## A zh
定义一份 versioned wire schema，在每种语言中生成代码或执行 validation。明确 defaults、unknown-field handling、units、error codes 和 compatibility rules；加入 cross-language golden fixtures 与 contract tests。wire contract 应小于任何 runtime 的 internal model。JSON interface 需要 runtime validation；Protobuf 需要严格 field evolution。只有共享文档，不是 executable evidence。
