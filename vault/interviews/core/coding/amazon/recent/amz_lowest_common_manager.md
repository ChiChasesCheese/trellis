# 组织架构最低共同上级（Lowest Common Manager）

公司的组织架构是一棵树：根是 CEO，每个人有若干直属下属。给定两名员工，找出他们汇报线上最低的共同上级，也就是两条汇报线第一次合流的那个人。这就是树上的最低公共祖先（LCA）问题。难点在于输入的形式（有没有父指针）、查询的规模（一次还是海量次）、以及边界情形（员工不在树里、一个人是另一个人的上级、不止两个人）。

## 开场先问的澄清问题
1. 树的表示：节点对象带 `reports` 列表，还是 `{经理: [直属下属]}` 字典，还是每人一个 `manager` 指针？
2. 一个人算不算自己的上级？（下面取「算」，即 a 是 b 的上级时返回 a。）
3. 员工不在组织架构里怎么办？（返回 None，不抛异常。）
4. 查询只有一次，还是大量次？多个员工 k 人？
5. 组织可以有多深？（决定能不能递归。）

## 先补一点基础：LCA
- **是什么**：树中两个节点 a、b 的最低公共祖先（Lowest Common Ancestor）：同时是 a 和 b 的祖先的节点里，离根最远（深度最大）的那个。
- **为什么需要**：「汇报线在哪一层合流」就是 LCA。
- **怎么工作**：想象两个人沿着汇报线往上走。深度不同时，先让较深的人上到同一深度；再两人一起向上，第一次相遇的节点就是答案。

## 最笨解
给 a 沿父指针一路到根，把经过的节点放进集合；再让 b 往上走，第一个落在集合里的节点就是答案。时间 O(深度)，内存 O(深度)（见 `_brute`）。

## 逐步改进
1. **问题**：输入给的是「经理 → 下属列表」，没有父指针，没法往上走。
2. **想法**：用一次遍历建 `parent` 与 `depth`（用显式栈，不用递归，因为组织深度可能很深，递归会超过 Python 的栈限制）。
3. **等深度上爬**：先把较深的上爬到同一深度，再同时上爬。相遇点之前两人到根的距离相同，所以不再需要集合，内存 O(1)（除 parent/depth 表）。
4. **多个员工**：LCA 满足结合律，`lca(lca(a,b),c)` 即 k 个人的 LCA；复杂度 O(k·深度)。
5. **大量查询**：每次 O(深度) 在深树上太慢。预处理倍增表 `up[k][v]` = v 的 2^k 级祖先；查询时先按深度差的二进制位提升，再从大到小同时提升到「父节点相同」前一步，答案是它们的父节点。预处理 O(n log n)，每次查询 O(log n)。用预处理换查询速度。

```python
def build(reports):                                       # reports: {manager: [direct reports]}; returns parent, depth, root
    parent, depth = {}, {}
    boss = {r for rs in reports.values() for r in rs}
    root = next(m for m in reports if m not in boss)
    depth[root], parent[root] = 0, None
    stack = [root]                                        # iterative: an org chart can be thousands of levels deep
    while stack:
        u = stack.pop()
        for v in reports.get(u, []):
            parent[v], depth[v] = u, depth[u] + 1
            stack.append(v)
    return parent, depth, root

def lowest_common_manager(parent, depth, a, b):
    if a not in parent or b not in parent:
        return None                                       # an employee who is not in the chart
    while depth[a] > depth[b]:
        a = parent[a]
    while depth[b] > depth[a]:
        b = parent[b]
    while a != b:
        a, b = parent[a], parent[b]
    return a                                              # an employee can be their own lowest common manager

def lcm_of_many(parent, depth, people):
    people = list(people)
    if not people or any(p not in parent for p in people):
        return None
    acc = people[0]
    for p in people[1:]:                                  # LCA is associative: fold it
        acc = lowest_common_manager(parent, depth, acc, p)
    return acc

class Lifting:                                            # O(n log n) build, O(log n) per query
    def __init__(self, parent, depth):
        self.depth = depth
        up = [{v: (p if p is not None else v) for v, p in parent.items()}]   # up[k][v] = 2^k-th ancestor (root points at itself)
        while 2 ** len(up) <= len(parent):
            prev = up[-1]
            up.append({v: prev[prev[v]] for v in parent})
        self.up = up

    def query(self, a, b):
        if a not in self.depth or b not in self.depth:
            return None
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        gap = self.depth[a] - self.depth[b]
        for k, table in enumerate(self.up):
            if gap >> k & 1:
                a = table[a]
        if a == b:
            return a
        for table in reversed(self.up):
            if table[a] != table[b]:
                a, b = table[a], table[b]
        return self.up[0][a]
```

示例：`ceo → [a, b]`，`a → [c, d]`，`b → [e]`，`d → [f]`。`f` 与 `c` 的最低共同上级是 `a`；`f` 与 `e` 是 `ceo`；`a` 与 `f` 是 `a` 自己；`a` 与不存在的人是 None；`f, c, d` 三人是 `a`；`f, e, c` 是 `ceo`。5000 层的链也能运行，因为全程没有递归。

## 复杂度
建表 O(n)；单次查询 O(深度)；倍增 O(n log n) 预处理 + O(log n) 查询；k 个员工 O(k·深度)。

## senior 追问
1. **没有父指针、只能从根遍历**：一次 DFS（后序），节点返回「子树里包含了 a/b 中的几个」，第一次计数到 2 的节点就是答案；深树用显式栈。
2. **员工经常调动（树会变）**：倍增表要重新生成；改用 Link-Cut Tree，或对不常变的部分缓存。若变化频繁而查询少，直接 O(深度) 查。
3. **一个人有两个经理（矩阵组织）**：不再是树而是 DAG，「最低共同上级」可能有多个，需要先问清定义。
4. **极大规模（1e8 员工）**：欧拉序 + 稀疏表（Sparse Table）做 O(1) 查询，或分片按部门存储。
5. **员工不在树里**：先查 `parent` 字典，缺失返回 None，不要 KeyError。
6. **只问「a 是不是 b 的上级」**：DFS 进出时间戳（tin/tout），O(1) 判断区间包含。

## 自测题
1. 为什么先上爬到同一深度？
<details><summary>答案</summary>LCA 一定在两人到根的路径上且深度小于等于较浅者；对齐后同步上爬，首次相同就是 LCA。</details>
2. `a` 本身是 `b` 的上级时返回什么？
<details><summary>答案</summary>`a`：上爬 b 到与 a 同深度时 `a == b`，循环不执行直接返回。</details>
3. 倍增表里根的祖先为什么指向自己？
<details><summary>答案</summary>避免越界，让「提升超过根」的操作停在根上；比较时 `table[a] != table[b]` 对根自然相等。</details>
