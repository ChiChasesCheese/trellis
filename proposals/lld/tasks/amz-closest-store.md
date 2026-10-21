# Task: amazon.amz-closest-store

- **Leaf id**: `amazon.amz-closest-store`   **slug**: `amz-closest-store`   **kind**: problem
- **题目**: 增删查最近值（Add / Remove / Closest）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- 1p3a 1189934 (2026-09-17, 🍌厂(=Amazon)电面; body hidden behind 积分>200): a reader asked 2026-10-04 「这道 add/remove/search 的题～这里的 search 是单纯判断一个元素是否存在吗？题目后来给的 range constrai…」 and the OP answered 「原来题目是ood，排序一次然后search和target最近的数」 https://www.1point3acres.com/bbs/thread-1189934-1-1.html [low–medium: fragments only]

## (reconstructed) — not in any visible report

- the exact API, tie-breaking, the value range ('range constraint' was given later), duplicates. Build stages: 1 sort once + bisect closest; 2 add/remove; 3 the range constraint → bucketed / Fenwick structure; 4 thread safety or k-closest

## Reuse / link (our own repo first)

- concept leaves python.data-model, oop.interfaces
- `bisect` docs https://docs.python.org/3/library/bisect.html
- LeetCode 658 Find K Closest Elements as a neighbour (link only)

## Card ladder notes

- ladder per AMAZON_AGENT.md; the data-structure card compares sorted list + bisect (O(n) insert) vs value-range buckets vs a balanced tree you would have to write
