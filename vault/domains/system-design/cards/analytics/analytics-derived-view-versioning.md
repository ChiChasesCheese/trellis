---
id: analytics-derived-view-versioning
node: analytics.derived
type: qa
---
## Q
A bug shipped in the transformation logic behind a derived table that consumers query in production. What's the safe repair pattern?

## A
**Build v2 side-by-side, then swap** — never patch in place:

1. Fix the logic, run it as a new derived view from the retained log / raw source, writing to a separate table or index.
2. Let it catch up to the live position; validate against v1 (row counts, spot diffs).
3. Atomically repoint consumers (alias swap, view redefinition, config flip) and keep v1 briefly for rollback.

This works only because inputs are immutable and the view is recomputable — the same property behind [[analytics-idempotent-reruns]] and search's reindex-then-alias-swap. In-place patching risks serving a half-fixed view and leaves no rollback.

## Q zh
派生表背后的转换逻辑中的 bug 被运送，consumer 在生产中查询。安全修复模式是什么？

## A zh
**并排构建 v2，然后交换** — 永远不要就地修补：

1. 修复逻辑，从保留日志 / 原始源作为新派生视图运行它，写入单独的表或索引。
2. 让它追上实时位置；对 v1 验证（行计数、spot diff）。
3. 原子性地重新指向 consumer（别名交换、视图重定义、config flip）并保持 v1 简短用于回滚。

这只在输入不可变且视图可重计算时有效 — 与幂等重运背后的相同属性和搜索的重索引后别名交换。就地修补风险服务一个半修复视图并不留回滚。
