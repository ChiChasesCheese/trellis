---
id: tlc-tt-nested-comment-tree-2-code
node: a.tt-nested-comment-tree
type: qa
step: 2
---
## Q
**由扁平记录构建嵌套评论树**｜写出 Python 实现

输入是评论记录列表（`n <= 10^5`），每条 `{"id": int, "parent_id": int | None, "text": str, "time": int}`，`id` 互不相同，根评论的 `parent_id` 为 `None`。返回根评论列表，每条评论带 `children`，孩子按 `(time, id)` 升序；父亲不存在的评论当根；有环抛 `ValueError`；不修改输入。

## A
**思路。** 排序一次，然后两遍：第一遍复制每条记录并加空 `children`，放进字典；第二遍把每个节点挂到父节点的 `children`，找不到父亲就加入根列表。最后用栈从根遍历，计数不足总数说明有环。

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

运行：`[{id:3,parent:1,time:30}, {id:1,parent:None,time:10}, {id:2,parent:1,time:20}, {id:4,parent:3,time:40}, {id:9,parent:77,time:5}]` → `[(9, []), (1, [(2, []), (3, [(4, [])])])]`（每项是 `(id, 孩子们)`）；`[]` → `[]`；两条记录互为父亲 → `ValueError`；`10^5` 条记录连成一条链 → `1` 个根。

**复杂度。** 时间 `O(n log n)`（排序），其余 `O(n)`；空间 `O(n)`。

**写法要点。** `itemgetter("time", "id")` 一次取出元组做复合排序键；字典推导式 `{**r, "children": []}` 复制记录，原记录不被改动；`nodes.get(r["parent_id"])` 对 `None` 键和不存在的键都返回 `None`，孤儿和根走同一个分支；环检测用显式栈而不是递归，链深 `10^5` 也不会 `RecursionError`；`stack.extend(stack.pop()["children"])` 一行完成弹出和展开。
