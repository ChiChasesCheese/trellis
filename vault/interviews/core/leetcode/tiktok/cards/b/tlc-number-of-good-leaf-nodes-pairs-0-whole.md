---
id: tlc-number-of-good-leaf-nodes-pairs-0-whole
node: b.number-of-good-leaf-nodes-pairs
type: qa
---
## Q
**LC 1530 好叶子节点对的数量**｜Medium · TikTok·字节 高频

给二叉树的根节点 `root` 和整数 `distance`。如果二叉树中两个叶节点之间的最短路径长度小于或等于 `distance`，它们就构成一组好叶子节点对。返回树中好叶子节点对的数量。树的节点数在 `[1, 2^10]` 范围内，每个节点的值在 `[1, 100]` 之间，`1 <= distance <= 10`。例：`root = [1,2,3,null,4]`，`distance = 3` → `1`（叶子 `3` 和 `4` 之间的路径长 `3`）；`root = [1,2,3,4,5,6,7]`，`distance = 3` → `2`；`root = [100]`，`distance = 1` → `0`；`root = [1,1,1]`，`distance = 2` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 树形 DP：每个节点上报一个长度 `distance + 1` 的数组 `cnt`，`cnt[d]` 是它子树里距离它恰好 `d` 的叶子数。在节点处，左右子树的叶子两两配对，路径长是两个叶子各自到该节点的距离之和，用前缀和统计和不超过 `distance` 的对数；再把两侧数组整体加一距离后相加上报。总时间 `O(n · distance)`。

**识别。** 树上两个点的最短路径必经过它们的最近公共祖先（LCA），所以每对叶子恰好在它们的 LCA 处被统计一次。`distance <= 10` 很小，状态可以直接存“各个距离上的叶子数”，距离超过 `distance` 的叶子再也不可能参与配对，数组长度固定为 `11`。

**推导。** 暴力：收集所有叶子，两两用父指针求距离，`O(L^2 · h)`。浪费：每一对叶子独立算路径，没有利用树的结构。洞察：一对叶子的路径长等于各自到 LCA 的距离之和，所以在 LCA 处用“左侧叶子数按距离分布”和“右侧叶子数按距离分布”做一次卷积式的统计即可。右侧用前缀和 `right_prefix[j]`（距离不超过 `j` 的叶子数），左侧每个距离 `i` 贡献 `left[i] * right_prefix[distance - i]`。节点数最多 `1024`，一条链的深度可达 `1023`，超过 Python 默认递归深度，所以不用递归：先层序得到访问顺序，再逆序处理，保证孩子先于父亲。

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

运行：`[1,2,3,null,4]`、`3` → `1`，`[1,2,3,4,5,6,7]`、`3` → `2`，`[7,1,4,6,null,5,3,null,null,null,null,null,2]`、`3` → `1`，`[100]`、`1` → `0`，`[1,1,1]`、`2` → `1`；`1024` 个结点的单链（深度 `1023`）→ `0`；约 `1000` 个结点的满二叉树、`distance = 10` → `7936`，耗时不到 `1 ms`。

**复杂度。** 时间 `O(n · distance)`；空间 `O(n)`（字典里同时存活的数组数量不超过层序的宽度，每个数组长 `distance + 1`）。

**易错点。**
- 把条件写成 `< distance`：`[1,2,3,null,4]`、`distance = 3` 得到 `0`（正确 `1`），`[1,1,1]`、`distance = 2` 得到 `0`（正确 `1`）。题目是“小于或等于”。
- 用递归 DFS：单链结构深度 `1023`，超过默认递归限制 `1000`，抛 `RecursionError`；节点数上限正好是 `2^10`，测试里常有这种链。
- 在节点处同侧配对，或左右各统计一遍：叶子对只在 LCA 处由“左 × 右”统计一次，同一侧内部的叶子对留给更深的祖先。

**追问。**
- 返回具体的叶子对：数组里存叶子本身而不是个数，空间随叶子数增长。
- `distance` 很大（可到 `n`）：每个节点合并数组 `O(n)`，总 `O(n^2)`；改用按深度编号的长链剖分或启发式合并，或点分治。
- 多叉树：对孩子逐个处理，先用已合并的前缀数组与新孩子配对，再合并进去。

**同模式。** LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 687 最长同值路径、LC 834 树中距离之和。
