---
id: tlc-number-of-good-leaf-nodes-pairs-2-code
node: a.number-of-good-leaf-nodes-pairs
type: qa
step: 2
---
## Q
**LC 1530 好叶子节点对的数量**｜写出 Python 实现

二叉树的根 `root`（节点数 `1..2^10`）和整数 `distance`（`1..10`）。两个叶子之间的最短路径长度 `<= distance` 就算好叶子对，返回好叶子对的数量。注意单链树的深度可达 `1023`。

## A
**思路。** 层序得到节点列表，逆序处理，使孩子先于父亲。每个节点保存 `cnt[d]`：子树里距它恰好 `d` 的叶子数。叶子是 `[1, 0, …]`。内部节点把每个孩子的数组右移一位（距离加一），左右两个数组配对统计，再相加上报。

```python
from itertools import accumulate


def count_pairs(root: TreeNode | None, distance: int) -> int:
    if root is None:
        return 0
    order = [root]                         # 层序：父节点一定排在子节点前面
    for node in order:                     # 遍历列表的同时往里追加，恰好是 BFS
        if node.left:
            order.append(node.left)
        if node.right:
            order.append(node.right)
    cnt: dict[TreeNode, list[int]] = {}    # cnt[x][d]：x 的子树里，距 x 恰好 d 的叶子数（d <= distance）
    ans = 0
    for node in reversed(order):           # 逆层序：孩子先于父亲被处理，免去递归
        if not node.left and not node.right:
            cnt[node] = [1] + [0] * distance          # 叶子自己距自己 0
            continue
        side = []
        for child in (node.left, node.right):
            if child:
                c = cnt.pop(child)
                side.append([0] + c[:distance])        # 孩子子树的叶子，距 node 都多 1
            else:
                side.append([0] * (distance + 1))
        left, right = side
        right_prefix = list(accumulate(right))         # right_prefix[j]：距离 <= j 的右侧叶子数
        ans += sum(left[i] * right_prefix[distance - i] for i in range(distance + 1))
        cnt[node] = [a + b for a, b in zip(left, right)]
    return ans
```

运行：`[1,2,3,null,4]`、`3` → `1`，`[1,2,3,4,5,6,7]`、`3` → `2`，`[7,1,4,6,null,5,3,null,null,null,null,null,2]`、`3` → `1`，`[100]`、`1` → `0`，`[1,1,1]`、`2` → `1`；`1024` 个结点的单链 → `0`；约 `1000` 个结点的满二叉树、`distance = 10` → `7936`，耗时不到 `1 ms`。

**复杂度。** 时间 `O(n · distance)`：每个节点常数个长度 `distance + 1` 的数组操作；空间 `O(n)`。

**写法要点。** 用 `for node in order` 一边遍历一边 `append` 做 BFS，不需要 `deque`；`reversed(order)` 免去显式后序和递归；`cnt.pop(child)` 用完就释放孩子的数组；`[0] + c[:distance]` 一步完成“整体加一并截断到 `distance`”；`accumulate` 给出前缀和，让左右配对变成 `sum(left[i] * right_prefix[distance - i])`；`TreeNode` 对象默认可哈希，直接当字典键。
