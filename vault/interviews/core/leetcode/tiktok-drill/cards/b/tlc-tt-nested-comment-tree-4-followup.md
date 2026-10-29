---
id: tlc-tt-nested-comment-tree-4-followup
node: b.tt-nested-comment-tree
type: qa
step: 4
---
## Q
**由扁平记录构建嵌套评论树**｜追问

面试官接着问：（1）评论是一条条实时到达的，怎么增量维护这棵树；（2）树的深度可能很大，序列化为 JSON 时怎么办；（3）每条评论要显示子树里的评论总数。

## A
1. **增量维护**：保存 `id -> 节点`；父亲还没到的孩子放进「等待表」`waiting[父亲 id]`；一条评论到达时，先认领等待表里已经在等它的孩子，再把自己挂到父亲下面（父亲已到），或登记进等待表（父亲未到）。每条评论 `O(1)`。

```python
from collections import defaultdict


class CommentForest:
    def __init__(self) -> None:
        self.nodes: dict[int, dict] = {}
        self.waiting: defaultdict[int, list[dict]] = defaultdict(list)   # 父亲 id -> 已到达但父亲还没到的孩子

    def add(self, record: dict) -> None:
        node = {**record, "children": self.waiting.pop(record["id"], [])}   # 先认领已经到达的孩子
        self.nodes[record["id"]] = node
        pid = record["parent_id"]
        if pid is None:
            return
        parent = self.nodes.get(pid)
        if parent is not None:
            parent["children"].append(node)
        else:
            self.waiting[pid].append(node)

    def roots(self) -> list[dict]:
        top = [n for n in self.nodes.values() if n["parent_id"] is None]
        orphans = [n for kids in self.waiting.values() for n in kids]
        return top + orphans
```

孩子按到达顺序排列；要按 `(time, id)` 展示，读出时再对每个 `children` 排序。
2. **深度大**：递归遍历和 `json.dumps` 都会在约 `1000` 层深时碰到递归上限。做法：用显式栈自己遍历，或按层 BFS 分页地输出；展示层通常本来就限制最大嵌套深度，超过的折叠成「查看更多」。
3. **子树评论数**：后序汇总。迭代做法是先得到节点的访问顺序，再逆序遍历，让每个节点把自己的计数加到父节点上，`O(n)`。

**Python 提醒**：`dict.pop(key, default)` 一步完成「取出并删除」，`waiting.pop(record["id"], [])` 在没有人等它时直接给一个新的空列表；`defaultdict` 读取不存在的键会插入它，所以判断「有没有人等我」要用 `pop(key, default)` 或 `in`，不要直接下标读。
