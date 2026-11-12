---
slug: alien-dictionary
---
## Q
**LC 269 火星词典**｜Hard

`words` 已按某种未知字母顺序排好，还原出一种合法的字母顺序；矛盾则返回 `""`。

## A
**一句话。** 相邻两词第一个不同的字母给出一条有向边，对字母图做拓扑排序，排不完就是有环。

```python
def alien_order(words):
    # 所有出现过的字母都是结点
    graph = {ch: set() for w in words for ch in w}
    indeg = dict.fromkeys(graph, 0)
    for a, b in pairwise(words):
        for x, y in zip(a, b):
            if x != y:                # x 排在 y 前
                if y not in graph[x]:
                    graph[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):       # 长词在其真前缀前：非法
                return ""
    q = deque(ch for ch, d in indeg.items() if d == 0)
    order = []
    while q:
        ch = q.popleft()
        order.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    if len(order) < len(graph):
        return ""              # 没排完：有环
    return "".join(order)
```

**复杂度。** 时间 `O(C)`（`C` 为字符总数），空间 `O(1)`（字母表大小）。

**易错点。**
- 漏掉前缀情形：`["abc","ab"]` 没有边，会返回 `"abc"`，应为 `""`。
- 只从边里收集字母：`["z"]` 会丢掉 `z`，所有出现过的字母都要先登记。
- 重复的边重复计入度：`["ab","ac","xb","xc"]` 里 `b→c` 出现两次，`indeg` 永远减不到 `0`，边要先判重。

**追问。**
- 要字典序最小的合法顺序？：队列换成最小堆。
- 怎么判断合法顺序是否唯一？：Kahn 过程中队列始终只有一个元素。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 953 验证外星语词典、LC 444 序列重建
