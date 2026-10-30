---
id: tlc-number-of-good-leaf-nodes-pairs-4-followup
node: b.number-of-good-leaf-nodes-pairs
type: qa
step: 4
---
## Q
**LC 1530 好叶子节点对的数量**｜追问

面试官接着问：（1）要返回具体的叶子对？（2）`distance` 不再限制在 `10` 以内，可以到 `n`？（3）树不是二叉树，每个节点有任意多个孩子？（4）单链树让递归爆栈？

## A
1. **返回叶子对**：数组里不再存个数，改存叶子本身，`bucket[d]` 是距离当前节点 `d` 的叶子列表。配对时对满足 `i + j <= distance` 的 `(i, j)`，把 `bucket_left[i]` 与 `bucket_right[j]` 做笛卡尔积收集。输出规模可达 `O(L^2)`，所以耗时和空间都由输出大小决定。
2. **`distance` 很大**：每个节点的数组长度是 `distance + 1`，合并代价 `O(n)`，总 `O(n^2)`。改进：数组长度只需要等于子树高度，合并时把较短的数组并入较长的（启发式合并，或长链剖分），配对时只扫较短数组的下标，总复杂度降到 `O(n log n)` 级别；也可以用点分治。
3. **多叉树**：对孩子逐个处理，维护已合并孩子的距离数组 `merged` 及其前缀和。每来一个新孩子的数组 `child`，先统计 `child` 与 `merged` 的配对数，再把 `child` 并入 `merged`，其余逻辑不变。

```python
from itertools import accumulate


def pair_count(left: list[int], right: list[int], distance: int) -> int:
    """left[i]、right[j]：两侧距离为 i、j 的叶子数；统计 i + j <= distance 的对数。"""
    right_prefix = list(accumulate(right))
    return sum(left[i] * right_prefix[distance - i] for i in range(distance + 1))
```

   `pair_count([0, 1, 0, 0], [0, 1, 1, 0], 3)` → `2`（距离分别是 `1+1=2` 与 `1+2=3`，两对都不超过 `3`）。两个数组长度都必须是 `distance + 1`。
4. **递归爆栈**：`1024` 个结点的单链，深度 `1023`，超过默认递归上限约 `1000`。调大 `sys.setrecursionlimit`，或层序得到访问顺序、逆序处理（孩子先于父亲）：

```python
from itertools import accumulate


def count_pairs_iter(root: TreeNode | None, distance: int) -> int:
    if root is None:
        return 0
    order = [root]                         # 层序：父节点一定排在子节点前面
    for node in order:                     # 遍历列表的同时往里追加，恰好是 BFS
        if node.left:
            order.append(node.left)
        if node.right:
            order.append(node.right)
    cnt: dict[TreeNode, list[int]] = {}    # cnt[x][d]：x 的子树里，距 x 恰好 d 的叶子数
    ans = 0
    for node in reversed(order):           # 逆层序：孩子先于父亲被处理
        if not node.left and not node.right:
            cnt[node] = [1] + [0] * distance
            continue
        side = []
        for child in (node.left, node.right):
            if child:
                c = cnt.pop(child)
                side.append([0] + c[:distance])
            else:
                side.append([0] * (distance + 1))
        left, right = side
        right_prefix = list(accumulate(right))
        ans += sum(left[i] * right_prefix[distance - i] for i in range(distance + 1))
        cnt[node] = [a + b for a, b in zip(left, right)]
    return ans
```

**Python 提醒**：`for node in order` 边遍历边向 `order` 追加，只对列表安全（迭代器按下标取值，会看到新增元素），对集合和字典会抛 `RuntimeError`；`TreeNode` 做字典键依赖默认的对象哈希，若自定义了 `__eq__` 但没定义 `__hash__`，实例会变得不可哈希。
