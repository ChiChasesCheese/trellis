---
id: storage-btree-page-split
node: storage.internals.btree
type: qa
---
## Q
An insert lands on a B-tree leaf page that is already full. Walk through what the engine does, and explain how this mechanism keeps the tree balanced without any rebalancing job.

## A
A **page split**:

1. Allocate a new page; move half the full page's entries into it, so both end ~half full.
2. Insert the new key into the appropriate half.
3. Add a separator key for the new page to the **parent** — which may itself be full, so splits can **cascade upward**; splitting the root is the *only* way the tree gets deeper.

Balance falls out for free: leaves only ever split in half and depth only grows at the root, so **every leaf stays at the same depth** — no background rebalancer needed.

Costs worth naming: a split touches multiple pages, so it must be WAL-protected against a crash mid-split ([[storage-btree-wal-recovery]]); and half-full pages after splits are one source of B-tree **space fragmentation**. Sequential key inserts (auto-increment) split only the rightmost edge — one reason monotonic keys insert faster than random UUIDs.

## Q zh
一次插入落到一个已经满了的 B-tree 叶子页面上。走一遍引擎的处理流程，并解释这个机制如何在没有任何再平衡任务的情况下保持树的平衡。

## A zh
**页面分裂（page split）**：

1. 分配一个新页面；把满页面里一半的条目移过去，两个页面各约半满。
2. 把新 key 插入合适的那一半。
3. 在**父页面**里为新页面添加一个分隔 key — 父页面自己也可能是满的，所以分裂会**向上级联**；分裂根页面是树变深的*唯一*方式。

平衡是免费得到的：叶子只会对半分裂，深度只在根处增长，所以**所有叶子始终处于同一深度** — 不需要后台再平衡器。

值得点名的代价：一次分裂触碰多个页面，所以必须有 WAL 保护以防分裂中途崩溃（[[storage-btree-wal-recovery]]）；分裂后的半满页面是 B-tree **空间碎片化**的来源之一。顺序 key 插入（自增）只分裂最右边缘 — 这是单调 key 比随机 UUID 插入更快的原因之一。
