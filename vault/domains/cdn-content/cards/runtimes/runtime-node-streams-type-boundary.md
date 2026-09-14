---
id: runtime-node-streams-type-boundary
node: runtimes.node-streams
type: qa
---
## Q
An upstream JSON field is typed with `as CacheMetadata`, then a missing `vary` field poisons cache keys. What should TypeScript do at this boundary?

## A
Static types disappear at runtime; `as` asserts trust and performs no validation. Parse unknown input with a runtime schema, reject or default invalid fields explicitly, then narrow to `CacheMetadata`. Keep wire types separate from validated domain types and version the schema. The hot path may use trusted types after validation, but crossing process or storage boundaries must convert untrusted bytes into proven invariants.

## Q zh
upstream JSON 字段通过 `as CacheMetadata` 强制标注，随后缺失的 `vary` 字段污染了 cache key。TypeScript 在这个 boundary 应怎么做？

## A zh
static type 在 runtime 会消失；`as` 只是声明信任，不执行 validation。应把外部输入视为 `unknown`，用 runtime schema 解析，显式 reject 或 default 无效字段，再 narrow 为 `CacheMetadata`。wire type 与 validated domain type 分离，并对 schema versioning。hot path 可在验证后使用可信类型，但跨 process 或 storage boundary 时必须把不可信 bytes 转换为已证明的 invariant。
