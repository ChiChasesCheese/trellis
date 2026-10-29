---
id: tlc-merge-two-binary-trees-0-whole
node: a.merge-two-binary-trees
type: qa
---
## Q
**LC 617 合并二叉树**｜Easy · CodeTop 国内累计 7 次 · 最近 2025-10-29（CodeTop）

给两棵二叉树 `root1` 和 `root2`。把其中一棵盖到另一棵上，重叠的节点值相加，只在一棵树里存在的节点原样保留；合并必须从两棵树的根节点开始，返回合并后的二叉树。两棵树的节点数都在 `[0, 2000]`，`-10^4 <= Node.val <= 10^4`。例：`root1 = [1,3,2,5]`，`root2 = [2,1,3,null,4,null,7]` → `[3,4,5,5,4,null,7]`；`root1 = [1]`，`root2 = [1,2]` → `[2,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 同步遍历两棵树：两个对应节点都存在，就把值加到 `root1` 的节点上并继续比较它们的左右孩子；只有一边存在，就把那一侧的整棵子树直接挂过来。用显式栈做遍历，避免链状树把递归栈撑爆。`O(min(n1, n2))`。

**识别。** 「两棵树按位置对应」是**同步遍历**（parallel traversal）的信号，同类有 LC 100 相同的树、LC 101 对称二叉树。「一边为空就整棵搬过去」让工作量只取决于重叠部分。节点数最多 2000，链状树深度可达 2000，超过 Python 默认递归深度 1000，所以主解法用显式栈。

**推导。** 朴素想法：把两棵树各自展开成数组再按下标相加——树形不规则，下标对不上。递归最直观：`merge(a, b)` 中任一为空就返回另一个；否则 `a.val += b.val`，`a.left = merge(a.left, b.left)`，`a.right = merge(a.right, b.right)`。每个重叠节点访问一次，`O(min(n1, n2))`。但递归深度等于树高，2000 层的链会触发 `RecursionError`。把递归的调用栈换成显式栈：栈里放「一对对应节点」；两边孩子都在才入栈，一边为空就直接把另一边挂上去，不必再走进去。

```python
def merge_trees(root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
    if root1 is None:
        return root2
    if root2 is None:
        return root1
    stack = [(root1, root2)]                 # 每项是一对位置相同、都存在的节点
    while stack:
        a, b = stack.pop()
        a.val += b.val                       # 合并结果直接写在 root1 的节点上
        if a.left is None:
            a.left = b.left                  # root1 缺左孩子：整棵挂过来（可能为 None）
        elif b.left is not None:
            stack.append((a.left, b.left))   # 两边都有：继续往下合并
        if a.right is None:
            a.right = b.right
        elif b.right is not None:
            stack.append((a.right, b.right))
    return root1
```

运行：`[1,3,2,5], [2,1,3,null,4,null,7]` → `[3,4,5,5,4,null,7]`，`[1], [1,2]` → `[2,2]`，`[], []` → `[]`，`[1], []` → `[1]`，`两条 2000 个节点的链` → `2000`。

**复杂度。** 时间 `O(min(n1, n2))`：只访问两棵树的重叠部分，其余子树整棵挂接；空间 `O(h)`：栈中至多保存重叠部分一条路径加上待处理的兄弟节点，`h` 为重叠部分的高度。

**易错点。**
- 一边为空时要把另一侧子树**挂上去**（`a.left = b.left`）。写成「两边都存在才处理」会丢掉 `root2` 独有的子树：`[1]` 与 `[1,2]` 得到 `[2]`（正确 `[2,2]`）。
- 根节点也要先判空，否则 `root1` 为 `None` 时 `a.val` 直接报 `AttributeError`。
- 递归写法在 2000 层的链状树上抛 `RecursionError`；用显式栈不受深度影响。结果会复用 `root2` 的子树（节点共享）并改动 `root1`，需要保留输入时见追问。

**追问。**
- 不允许修改输入：递归新建节点 `TreeNode(a.val + b.val, …)`，缺失一侧当作值 0、空孩子处理。
- 递归版本最短，但受递归深度限制；调高 `sys.setrecursionlimit` 只是补丁，面试里优先说明深度问题并给显式栈。
- 合并 k 棵树：逐棵两两合并，总代价 `O(Σ n_i)`（每次只走重叠部分）。

**同模式。** LC 100 相同的树、LC 101 对称二叉树、LC 226 翻转二叉树、LC 572 另一棵树的子树。
