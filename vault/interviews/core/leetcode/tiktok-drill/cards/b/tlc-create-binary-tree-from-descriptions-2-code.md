---
id: tlc-create-binary-tree-from-descriptions-2-code
node: b.create-binary-tree-from-descriptions
type: qa
step: 2
---
## Q
**LC 2196 根据描述创建二叉树**｜写出 Python 实现

`descriptions[i] = [parent_i, child_i, isLeft_i]`（`1 <= descriptions.length <= 10^4`，值在 `1` 到 `10^5` 之间互不相同，`isLeft_i` 为 `0` 或 `1`），描述一棵有效的二叉树；`isLeft_i == 1` 表示左孩子，`0` 表示右孩子。构造这棵树并返回根节点。

## A
**思路。** 字典 `nodes` 保存每个值对应的唯一 `TreeNode`；读到一条描述就确保父、子两个节点存在，再按 `is_left` 连边，同时把父记进 `parents`、子记进 `children`。扫描结束后根就是 `parents - children` 里唯一的元素。

```python
def create_binary_tree(descriptions: list[list[int]]) -> TreeNode | None:
    nodes: dict[int, TreeNode] = {}
    parents: set[int] = set()
    children: set[int] = set()
    for parent, child, is_left in descriptions:
        for v in (parent, child):
            if v not in nodes:                          # 第一次见到才创建节点
                nodes[v] = TreeNode(v)
        if is_left:
            nodes[parent].left = nodes[child]
        else:
            nodes[parent].right = nodes[child]
        parents.add(parent)
        children.add(child)
    (root,) = parents - children                        # 只出现过当父、从没当过孩子的就是根
    return nodes[root]
```

运行：`[[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]` → 根 `50`，层序 `[50, 20, 80, 15, 17, 19]`；`[[1,2,1],[2,3,0],[3,4,1]]` → `[1, 2, None, None, 3, 4]`；`[[5,1,0]]` → `[5, None, 1]`；`10^4` 条描述连成的左链深度为 `10001`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`，字典与两个集合各最多 `n + 1` 项。

**写法要点。** `for parent, child, is_left in descriptions` 直接解包，比下标可读；`for v in (parent, child)` 把「创建节点」写一遍；`if v not in nodes` 而不是 `nodes.setdefault(v, TreeNode(v))`，后者每次都会先构造一个 `TreeNode` 再丢掉；`(root,) = parents - children` 用单元素解包同时完成取值和「恰有一个」的断言；整个过程没有递归，链很深也不会溢出。
