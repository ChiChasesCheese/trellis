---
id: tlc-all-nodes-distance-k-in-binary-tree-2-code
node: a.all-nodes-distance-k-in-binary-tree
type: qa
step: 2
---
## Q
**LC 863 二叉树中所有距离为 K 的结点**｜写出 Python 实现

二叉树 `root`（结点数 `1..500`，值互不相同）、目标结点 `target`、整数 `k`（`0..1000`）。返回与 `target` 距离恰好为 `k` 的所有结点的值，顺序任意。要求写出能处理「往上走」的解法。

## A
**思路。** 先用一遍迭代 DFS 把每个结点的父结点存进字典，树就有了「向上」的边。然后从 `target` 起做 BFS，邻居是左、右、父三个；用 `seen` 排除已访问结点，一层层扩 `k` 次，最后一层的值就是答案。

```python
def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while stack:                          # 迭代 DFS 给每个结点记父指针（避免递归栈）
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)

    frontier, seen = [target], {target}   # 从 target 出发的 BFS，一层 = 距离 +1
    for _ in range(k):
        nxt: list[TreeNode] = []
        for node in frontier:
            for nb in (node.left, node.right, parent[node]):
                if nb and nb not in seen:  # seen 防止走回刚来的结点
                    seen.add(nb)
                    nxt.append(nb)
        frontier = nxt
    return [node.val for node in frontier]
```

运行：`root=[3,5,1,6,2,0,8,null,null,7,4], target=5, k=2` → `[7, 4, 1]`，`root=[1], target=1, k=3` → `[]`，`同一棵树 target=5, k=0` → `[5]`，`同一棵树 target=7, k=3` → `[6, 3]`。

**复杂度。** 时间 `O(n)`：建父指针遍历每个结点一次，BFS 每个结点至多入队一次；空间 `O(n)`（父指针表、`seen`、栈和队列）。`k` 再大也不增加成本——`frontier` 空了之后每轮是空操作。

**写法要点。** `parent` 是以结点对象为键的字典（`TreeNode` 按对象身份哈希，值互不相同也不依赖它）；`for child in (node.left, node.right)` 把两个孩子一起遍历；`if nb and nb not in seen` 同时过滤 `None`（根的父亲、叶子的孩子）和已访问结点；BFS 用「当前层列表 + 下一层列表」代替 `deque`，因为每轮正好处理一整层，不需要出队计数。深度最多 500，递归本来也够，用显式栈是为了不被递归上限卡住。
