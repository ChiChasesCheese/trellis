---
id: tlc-step-by-step-directions-from-a-binary-tree-node-to-another-0-whole
node: c.step-by-step-directions-from-a-binary-tree-node-to-another
type: qa
---
## Q
**LC 2096 从二叉树一个节点到另一个节点每一步的方向**｜Medium · LC TikTok 全时段热度 38/100

给定二叉树根节点 `root`，共 `n` 个节点，节点值为 `1..n` 内互不相同的整数，再给起点值 `startValue` 和终点值 `destValue`（二者不同）。返回从起点到终点最短路径的每一步方向：`'L'` 去左孩子，`'R'` 去右孩子，`'U'` 去父节点。`2 <= n <= 10^5`，`1 <= Node.val <= n`，所有值互不相同，`startValue != destValue`。例：`root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6` → `"UURL"`（路径 3 → 1 → 5 → 2 → 6）；`root = [2,1], startValue = 2, destValue = 1` → `"L"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 分别求根到起点、根到终点的 `L/R` 路径，去掉公共前缀（根到最近公共祖先），起点剩下的每一步都换成 `'U'`，再接上终点剩下的路径。

**识别。** 树上两点最短路径必经最近公共祖先（LCA）；节点没有父指针时，用「根到各点的路径」代替父指针，公共前缀就是到 LCA 的路径。

**推导。** 暴力：先建父指针和邻接表，再从起点 BFS 到终点并记录方向，`O(n)` 但要建图。洞察：两条根路径的最长公共前缀对应 LCA，起点从 LCA 向下的路径长度就是要向上走的步数，所以不需要显式找 LCA 节点。

```python
def get_directions(root: TreeNode | None, startValue: int, destValue: int) -> str:
    def find(node: TreeNode | None, target: int, path: list[str]) -> bool:
        if node is None:
            return False
        if node.val == target:
            return True
        path.append("L")                         # 先试左子树，失败再回溯
        if find(node.left, target, path):
            return True
        path[-1] = "R"                           # 复用同一个位置改成 R 试右子树
        if find(node.right, target, path):
            return True
        path.pop()                               # 两边都没有：撤销这一步
        return False

    to_start: list[str] = []
    to_dest: list[str] = []
    find(root, startValue, to_start)             # 根到起点的路径
    find(root, destValue, to_dest)               # 根到终点的路径
    common = 0
    while common < min(len(to_start), len(to_dest)) and to_start[common] == to_dest[common]:
        common += 1                              # 公共前缀对应根到 LCA 的路径，来回都不用走
    return "U" * (len(to_start) - common) + "".join(to_dest[common:])
```

运行：示例一 `UURL`；示例二 `L`；反过来 `root = [2,1], startValue = 1, destValue = 2` → `U`；各 800 棵随机小树上结果与逐点 BFS 的最短路径一致。

**复杂度。** 时间 `O(n)`，空间 `O(h)`（递归栈与路径，`h` 为树高）。

**拓展优化。**
- 链状树深度达 `10^5`，递归版本会 `RecursionError`，改用显式栈，遍历时记录父指针，再沿父指针回溯出两条根路径：

```python
def get_directions_iterative(root: TreeNode | None, startValue: int, destValue: int) -> str:
    parent: dict[int, tuple[int, str]] = {}      # 子节点值 -> (父节点值, 从父到子的方向)
    stack = [root]
    while stack:                                 # 显式栈遍历，记录父指针
        node = stack.pop()
        for child, letter in ((node.left, "L"), (node.right, "R")):
            if child:
                parent[child.val] = (node.val, letter)
                stack.append(child)

    def path_from_root(val: int) -> str:
        letters: list[str] = []
        while val in parent:                     # 沿父指针走到根，再反转
            val, letter = parent[val]
            letters.append(letter)
        return "".join(reversed(letters))

    a, b = path_from_root(startValue), path_from_root(destValue)
    common = 0
    while common < min(len(a), len(b)) and a[common] == b[common]:
        common += 1
    return "U" * (len(a) - common) + b[common:]
```

**易错点。**
- 最坏深度：`n = 10^5` 的链状树递归深度 `10^5`，CPython 默认递归上限约 1000，会抛 `RecursionError`，需要 `sys.setrecursionlimit` 提高或改成迭代。
- 公共前缀处理反了：把终点的剩余路径也换成 `'U'`，或者忘记把起点的剩余路径换成 `'U'`；只有起点一侧向上走。
- 回溯时 `path.pop()` 遗漏：失败的分支会把 `L`、`R` 留在路径里，示例一得到错误的前缀。

**追问。**
- 返回路径节点序列而不是方向：同样的做法，保存节点而不是字符。
- 多次查询同一棵树：预处理父指针和深度，每次查询用倍增 LCA，`O(log n)`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 257 二叉树的所有路径、LC 113 路径总和 II、LC 863 二叉树中所有距离为 K 的结点。
