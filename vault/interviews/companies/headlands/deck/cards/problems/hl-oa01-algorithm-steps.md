---
id: hl-oa01-algorithm-steps
node: problems.oa01-job-chain
type: qa
step: 6
---
## Q
任务链报表的完整算法分哪几步？时间和空间复杂度是多少？

## A
1. **建表**：`LinkedHashMap<id, Job>`，用 `putIfAbsent` 返回非 null 判重复 id（遍历顺序等于插入顺序，输出确定）。
2. **找头并查悬空 / 分叉**：把每个非 0 的 `next` 记进 `hasPredecessor` 集合；`next` 不在表里 → 悬空；`Set.add` 返回 false（已存在）→ 入度 2。没进集合的就是头。
3. **走链**：对每个头计数、累加时长（`long` + `Math.addExact`）、记尾，走过的编号放进 `visited`。
4. **查环**：`visited.size() != byId.size()` → 有环。
5. **排序输出**：总时长降序，相同时头编号升序。

复杂度：O(n + k log k)（k = 链数 ≤ n），内存 O(n)。被问「百万行多快」答：线性，每行只进哈希表一次、只被走一次，100 万行（平均链长 100、行序打乱）整题不到 1 秒；压常数第一刀是解析，第二刀是去掉 `Integer` 装箱。
