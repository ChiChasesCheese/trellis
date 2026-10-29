---
id: tlc-tt-nested-comment-tree-0-whole
node: a.tt-nested-comment-tree
type: qa
---
## Q
**由扁平记录构建嵌套评论树**｜Medium · TikTok 高频

给一个扁平的评论记录列表，每条记录是字典 `{"id": int, "parent_id": int | None, "text": str, "time": int}`，根评论的 `parent_id` 为 `None`。构建嵌套结构：每条评论多一个 `children` 列表，返回所有根评论。要求：（1）记录无序，孩子可能出现在父亲之前；（2）同一个父亲下的孩子按 `(time, id)` 升序；（3）父亲不存在的孤儿评论当作根；（4）记录里有环时抛 `ValueError`；（5）不修改传入的记录。记录数不超过 `10^5`，`id` 互不相同。例：`[{id:3,parent:1,time:30}, {id:1,parent:None,time:10}, {id:2,parent:1,time:20}, {id:4,parent:3,time:40}, {id:9,parent:77,time:5}]` → 根为 `9`（孤儿）和 `1`，`1` 的孩子依次是 `2`、`3`，`3` 的孩子是 `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先按 `(time, id)` 排序，再用两遍扫描：第一遍建 `id -> 节点`（复制记录并加空的 `children`），第二遍把每个节点挂到父节点的 `children` 下，找不到父亲就当根；最后从根出发遍历一遍，访问数不等于总数就说明有环。建树 `O(n)`，排序让总体 `O(n log n)`。

**识别。** 「扁平记录 + 父指针」就是一张只记父亲的邻接表，哈希表 `id -> 节点` 把「找父亲」降到 `O(1)`；「记录无序」说明不能边读边挂，要先把所有节点建好；「孤儿、环」是数据质量问题，各自要有明确的处理方式。

**推导。** 暴力：对每个节点扫描整张表找孩子，`O(n^2)`，`10^5` 条记录是 `10^10`；假设父亲一定先出现、一遍线性挂接，输入一乱序就把有父亲的评论当成了根 → 浪费：「找父亲」是重复的线性查找，而顺序依赖又是不必要的假设 → 洞察：先建字典再连边，两遍扫描消除顺序依赖；孩子的顺序由排序一次决定，之后 `append` 的顺序就是展示顺序；环里的节点没有一条路径通到任何根，从根出发的遍历访问不到它们。

```python
from operator import itemgetter


def build_comment_tree(records: list[dict]) -> list[dict]:
    # 每条记录形如 {"id": int, "parent_id": int | None, "text": str, "time": int}
    ordered = sorted(records, key=itemgetter("time", "id"))     # 先排序，之后 append 的孩子天然有序
    nodes = {r["id"]: {**r, "children": []} for r in ordered}   # 第一遍：id -> 节点，与记录顺序无关
    roots: list[dict] = []
    for r in ordered:                                           # 第二遍：挂到父亲下面
        node = nodes[r["id"]]
        parent = nodes.get(r["parent_id"])
        if parent is None:                                      # parent_id 为空，或父亲不存在（孤儿）：当根
            roots.append(node)
        else:
            parent["children"].append(node)
    seen, stack = 0, roots[:]                                   # 环里的节点从根出发走不到
    while stack:
        seen += 1
        stack.extend(stack.pop()["children"])
    if seen != len(nodes):
        raise ValueError("comment records contain a cycle")
    return roots
```

运行：上面的例子 → `[(9, []), (1, [(2, []), (3, [(4, [])])])]`（每项是 `(id, 孩子们)`）；`[]` → `[]`；`1 <-> 2` 互为父亲 → `ValueError`；`10^5` 条记录连成一条链 → `1` 个根，没有递归，不会溢出。

**复杂度。** 排序 `O(n log n)`；建字典、连边、环检测都是 `O(n)`；空间 `O(n)`。

**易错点。**
- 一遍扫描、假设父亲先出现：`[{id:2, parent:1}, {id:1, parent:None}]` 会得到根 `[2, 1]`，正确是只有根 `1`，`2` 是它的孩子。
- 不检测环：`1 <-> 2` 再加一条独立的根 `3`，环里两条评论悄悄消失，只返回 `[3]`，没有任何提示。
- 直接在传入的字典上加 `children`：调用方的数据被污染，再用同一份记录建第二次树时 `children` 会残留旧数据；用 `{**r, "children": []}` 复制一份。

**追问。**
- 评论一条条到达（流式）：维护 `id -> 节点`，父亲还没到的孩子先放进「等待表」，父亲到达时一次认领；新评论 `O(1)` 挂接。
- 深度很大：遍历和序列化都要用显式栈，递归在 `1000` 层就会 `RecursionError`；上面的环检测已经是迭代。
- 限制展示深度、统计子树评论数：BFS 带深度，或后序汇总。

**同模式。** LC 690 员工的重要性、LC 2196 根据描述创建二叉树、LC 207 课程表（环检测）、LC 1110 删点成林。
