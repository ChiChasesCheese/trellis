---
slug: minimum-genetic-mutation
---
## Q
**LC 433 最小基因变化**｜Medium

基因是 8 位 `ACGT` 字符串，每次变一个字符，且变化后必须在基因库 `bank` 中（`start` 可以不在）。求 `start` 变成 `end` 的最少次数，不能则返回 `-1`。

## A
**一句话。** 序列是节点、改一个字符且在库中是边，从 `start` 做 BFS，第一次碰到 `end` 的层数就是答案。

```python
def min_mutation(start, end, bank):
    valid = set(bank)
    q = deque([(start, 0)])
    seen = {start}
    while q:
        gene, steps = q.popleft()
        if gene == end:
            return steps
        for i in range(8):
            for c in "ACGT":
                nxt = gene[:i] + c + gene[i + 1:]
                if nxt in valid and nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, steps + 1))
    return -1
```

**复杂度。** 时间 `O(|bank|·8·4·8)`，空间 `O(|bank|)`。

**易错点。**
- 不要求变化结果在库里：`("AAAAAAAA","AAAAAACC",["AAAAAACC"])` 得 `2`，应为 `-1`。
- 要求 `start` 也在库里：示例一的 `start` 不在 `bank`，却是合法起点。
- 没有 `seen`：序列能变回去，队列无限增长。

**追问。**
- 怎么再加速？：双向 BFS，从 `start` 和 `end` 同时扩，相遇即停。
- 库很大时枚举 32 个候选还划算吗？：改成两两比较汉明距离为 `1` 建图，或按通配符模式分桶（类似单词接龙）。

**同模式。** LC 127 单词接龙、LC 752 打开转盘锁、LC 126 单词接龙 II、LC 773 滑动谜题
