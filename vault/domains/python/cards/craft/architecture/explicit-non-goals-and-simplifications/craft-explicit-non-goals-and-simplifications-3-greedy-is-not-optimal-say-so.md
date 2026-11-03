---
id: craft-explicit-non-goals-and-simplifications-3-greedy-is-not-optimal-say-so
node: craft.architecture.explicit-non-goals-and-simplifications
type: qa
step: 3
---
## Q
**明说的简化与非目标 · 分账的债务化简用贪心，怎样诚实地说它不是最少笔数**｜架构

分账（Splitwise）要把「谁欠谁」化简成尽量少的转账。常见做法是贪心：每次让净应收最多的人和净应付最多的人互相结清。面试官问「这是最少的转账笔数吗」，该怎么答？

## A
**要点。** 不要答「是」。贪心有两条保证，但没有第三条：每一步至少让一个人归零，所以 n 个人最多 n−1 笔，这是上界；但它**不保证**笔数最少。真正的最少笔数等价于把所有人分成尽量多个「组内净额和为 0」的子集，一组 k 人需要 k−1 笔，这是子集和（subset sum）类的 NP-hard 问题。题解里写明这一点，并附一个反例。

```python
def simplify(net):                       # 贪心：最大应收 × 最大应付，每步至少结清一人
    tie = count()                        # 同额时用序号打破平局，避免比较 user
    cr = [(-b, next(tie), u) for u, b in net.items() if b > 0]   # 取负数，heapq 当大顶堆
    de = [(b, next(tie), u) for u, b in net.items() if b < 0]    # 本身为负，最小的欠得最多
    heapq.heapify(cr); heapq.heapify(de)
    pays = []
    while cr and de:
        nc, _, c = heapq.heappop(cr)
        d, _, p = heapq.heappop(de)
        amt = min(-nc, -d)
        pays.append((p, c, amt))         # (付款人, 收款人, 金额)
        if -nc - amt > 0: heapq.heappush(cr, (nc + amt, next(tie), c))
        if d + amt < 0:   heapq.heappush(de, (d + amt, next(tie), p))
    return pays

net = {"A": 3, "B": 2, "C": -3, "D": 2, "E": -4}      # 总和为 0
print("贪心:", simplify(net))
print("分组 {A,C} {B,D,E}:", sum(net[u] for u in "AC"), sum(net[u] for u in "BDE"))
print("笔数: 贪心", len(simplify(net)), "最优", (2 - 1) + (3 - 1))
```

实际输出：

```
贪心: [('E', 'A', 3), ('C', 'B', 2), ('E', 'D', 1), ('C', 'D', 1)]
分组 {A,C} {B,D,E}: 0 0
笔数: 贪心 4 最优 3
```

**为什么。** 贪心第一步总是拿最大应付（E 欠 4）去配最大应收（A 是 3），把本来恰好能自成一组的 A 和 C 拆开了；最优解让 A 与 C 直接对冲，剩下 B、D、E 两笔结清，共 3 笔。

**代价。** 实现是 O(n log n)，足够好；追求最优要枚举子集，规模一大就不可行。回答的写法：「贪心给出不超过 n−1 笔的方案，不保证最少；最少是 NP-hard，所以我选择了可预期的贪心，并给出一个它多一笔的例子」。这比声称最优可信得多。
