---
id: distributed-sequence-crdt-positions
node: distributed.crdt
type: qa
---
## Q
Two collaborative-text replicas both apply "insert at index 5" — and the document diverges, because their index 5s were different characters. How do sequence CRDTs (text/list CRDTs) identify positions so that concurrent edits merge correctly?

## A
Indexes are **relative to a state that other replicas don't share**, so sequence CRDTs abandon them: every element gets a **permanent, globally unique position identifier** at creation, and an insert says "between identifier P and identifier Q", which stays meaningful no matter what else happened concurrently.

- Identifiers are drawn from a **dense order** — between any two you can always mint another (fractional numbering, or paths in a tree), with the author's **replica id as tiebreaker** so two replicas can't mint the same one and all replicas sort ties identically.
- **Deletion can't reuse or renumber**: a removed element leaves a **tombstone** (or is kept invisibly) because a concurrent edit may still reference it as an anchor.

The costs this design carries: per-character metadata and tombstone growth (needs compaction), and the classic **interleaving problem** — two concurrently typed runs at the same spot may merge as "HeWorldllo" character-interleaved; newer designs (e.g. RGA-family, Fugue) order identifiers to keep each author's run contiguous.

## Q zh
两个协作文本副本都应用了"在下标 5 处插入"——文档却分叉了，因为两边的下标 5 是不同的字符。序列 CRDT（文本/列表 CRDT）如何标识位置，才能让并发编辑正确合并？

## A zh
下标是**相对于一个其他副本并不共享的状态**而言的，所以序列 CRDT 干脆抛弃它：每个元素在创建时获得一个**永久的、全局唯一的位置标识符**，插入操作说的是"在标识符 P 和标识符 Q 之间"，无论并发期间发生了什么，这句话都保持有意义。

- 标识符取自一个**稠密序**——任意两个之间总能再造出一个（分数编号，或树中的路径），并以作者的**replica id 作平局裁决**，保证两个副本造不出同一个标识符、且所有副本对平局排序一致。
- **删除不能复用或重排编号**：被删元素留下 **tombstone（墓碑）**（或不可见地保留），因为并发的编辑可能仍以它为锚点。

这个设计背负的代价：每字符的元数据和不断增长的 tombstone（需要压缩），以及经典的**交错问题（interleaving）**——两段在同一位置并发输入的文字可能合并成"HeWorldllo"式的逐字符交错；较新的设计（如 RGA 家族、Fugue）通过标识符排序让每个作者的连续输入保持成块。
