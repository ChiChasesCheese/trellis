---
slug: tt-nested-comment-tree
---
## Q
**由扁平记录构建嵌套评论树**｜Medium

扁平评论记录 `{"id", "parent_id", "text", "time"}`，根评论的 `parent_id` 为 `None`。构建嵌套结构（每条多一个 `children`），返回所有根。记录无序；同父的孩子按 `(time, id)` 升序；父亲不存在的孤儿当根；有环抛 `ValueError`；不修改输入。

## A
**一句话。** 先按 `(time, id)` 排序，建 `id -> 节点` 字典后一遍挂接到父亲的 `children`，最后从根遍历计数，数不满就是有环。

```python
def build_comment_tree(records):
    ordered = sorted(records, key=itemgetter("time", "id"))
    nodes = {r["id"]: {**r, "children": []}
             for r in ordered}
    roots = []
    for r in ordered:       # 先排序，append 的孩子天然有序
        node = nodes[r["id"]]
        parent = nodes.get(r["parent_id"])
        if parent is None:  # 无父或孤儿：当根
            roots.append(node)
        else:
            parent["children"].append(node)
    seen, stack = 0, roots[:]   # 环里的节点从根走不到
    while stack:
        seen += 1
        stack.extend(stack.pop()["children"])
    if seen != len(nodes):
        raise ValueError("cycle")
    return roots
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 一遍扫描、假设父亲先出现：`[{id:2, parent:1}, {id:1, parent:None}]` 会得到根 `[2, 1]`。
- 不检测环：`1 <-> 2` 加独立根 `3`，环里的评论悄悄消失，只返回 `[3]`。
- 直接在输入字典上加 `children`：污染调用方数据，要用 `{**r, "children": []}` 复制。

**追问。**
- 评论流式到达？：维护 `id -> 节点`，父亲未到的孩子放进等待表，父亲到达时一次认领。
- 深度很大？：遍历和序列化都用显式栈，递归 1000 层就会 `RecursionError`。

**同模式。** LC 690 员工的重要性、LC 207 课程表、LC 1110 删点成林
