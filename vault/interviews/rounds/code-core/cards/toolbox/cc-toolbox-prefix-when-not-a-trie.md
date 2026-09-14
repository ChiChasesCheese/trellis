---
id: cc-toolbox-prefix-when-not-a-trie
node: toolbox.prefix-trees
type: qa
---
## Q
The alphabet is `0-9`, keys are 16 digits long, and there are 10^6 of them. Is a trie the right structure?

## A
**Usually not.** A Python dict per node costs a few hundred bytes; 10^6 keys × 16 levels is millions of nodes and hundreds of megabytes — a 256 MB budget dies before the algorithm even runs.

- Fixed-length numeric keys are just integers: sort them and `bisect`, or bucket by the first *k* digits into a dict of lists and scan the bucket.
- If a trie really is needed on a small fixed alphabet, drop the dicts: a `list` of child arrays of size 10 or 26, indexed by node number, is several times smaller and faster.
- Static prefix questions → sorted list plus `bisect` ([[cc-toolbox-prefix-sorted-bisect]]).
- Keep the trie for what only it does well: incremental inserts, per-prefix aggregates ([[cc-toolbox-prefix-node-counts]]), longest-prefix match, and walking several candidate keys in parallel.

## Q zh
字母表是 `0-9`，key 长 16 位，共有 10^6 个。trie 是合适的结构吗？

## A zh
**通常不是。** 每个节点一个 Python dict 要几百字节；10^6 个 key × 16 层就是数百万个节点、几百 MB —— 256 MB 的预算在算法跑起来之前就先挂了。

- 定长数字 key 本质就是整数：排序后 `bisect`，或按前 *k* 位分桶成 dict of list 再在桶内扫描。
- 如果在小的固定字母表上确实需要 trie，就别用 dict：以节点编号索引、每项是长度 10 或 26 的子节点数组的 `list`，体积小几倍也更快。
- 静态前缀问题 → 有序列表加 `bisect`（[[cc-toolbox-prefix-sorted-bisect]]）。
- 把 trie 留给只有它擅长的事：增量插入、每前缀聚合（[[cc-toolbox-prefix-node-counts]]）、最长前缀匹配，以及并行地走多个候选 key。
