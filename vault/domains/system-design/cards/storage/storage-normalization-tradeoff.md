---
id: storage-normalization-tradeoff
node: storage.relational.operations
type: qa
---
## Q
Normalized vs denormalized schema: what exactly does each optimize, and what breaks when you denormalize?

## A
- **Normalized**: every fact stored **once** (many-to-one refs by ID). Optimizes writes and integrity — an update touches one row, no risk of divergent copies. Reads pay with joins.
- **Denormalized**: copies of data placed where they're read (author name embedded in each post). Optimizes **read locality** — one fetch, no joins. Writes now must find and update **every copy**, usually without a transaction spanning them; miss one and copies silently disagree.

Modern resolution: keep the system of record normalized; generate denormalized **derived views** (caches, search docs, read models) from its change stream, accepting eventual consistency there — see [[analytics-derived-data-framing]].

## Q zh
规范化 vs 非规范化 schema：各优化什么，非规范化什么会破裂？

## A zh
- **规范化**：每个事实存储**一次**（多对一 ID 引用）。优化写和完整性——更新接触一行，无发散副本的风险。读用 join 付出代价。
- **非规范化**：数据副本放在它们被读的地方（作者名称嵌入在每个帖子）。优化**读局部性**——一次获取，无 join。写现在必须找到和更新**每个副本**，通常没有跨越它们的事务；漏掉一个副本无声地不同意。

现代解决：保持记录系统规范化；从其变更流生成非规范化**衍生视图**（缓存、搜索文档、读模型），接受最终一致性——见 [[analytics-derived-data-framing]]。
