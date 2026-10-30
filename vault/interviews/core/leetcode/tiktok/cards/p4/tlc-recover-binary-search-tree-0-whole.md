---
id: tlc-recover-binary-search-tree-0-whole
node: p4.recover-binary-search-tree
type: qa
---
## Q
**LC 99 恢复二叉搜索树**｜Medium · CodeTop 国内累计 6 次 · 最近 2026-06-02（国内 CodeTop）

给二叉搜索树的根结点 `root`，其中**恰好两个**结点的值被错误地交换了。请在**不改变树结构**的情况下恢复这棵树（原地交换两个结点的值即可）。结点数在 `[2, 1000]`，`-2^31 <= Node.val <= 2^31 - 1`。例：`root = [1,3,null,null,2]` → `[3,1,null,null,2]`；`root = [3,1,4,null,null,2]` → `[2,1,4,null,null,3]`。进阶：用 `O(n)` 空间很容易，能否只用 `O(1)` 空间？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** BST 的中序遍历（in-order）应当严格升序；两个值互换后，序列里会出现 1 处（相邻互换）或 2 处（不相邻互换）逆序对。中序遍历时记住前驱 `prev`：**第一处逆序取较大者，最后一处逆序取较小者**，遍历完交换这两个结点的值。LC 99 是 LC 98 的追问：LC 98 判断「有没有逆序」，LC 99 找「逆序在哪」。

**识别。**
- 「BST」+「值被破坏」→ 想到中序升序这条性质；它是 LC 98（验证 BST）的追问，与 LC 230（第 K 小）同出一源：都把 BST 摊平成有序序列再处理。
- 「不改变结构」「恰好两个」→ 只需要定位两个结点再换值，不用重建。
- 进阶要求 `O(1)` 空间 → 中序遍历要摆脱栈 / 递归：Morris 遍历（见追问）。

**推导。** 暴力：中序收集所有结点到数组 `O(n)`，排序后与原值逐一比较，不同的两处就是答案，`O(n log n)`。浪费在排序：数组本来只有一对结点放错，不必排序。观察：升序数组交换两个元素，不相邻时产生两个「下降」`a[i] > a[i+1]`，相邻时只产生一个。第一个下降的左元素 `a[i]` 一定是被换到前面的大值，最后一个下降的右元素 `a[j+1]` 一定是被换到后面的小值；相邻时两者就在同一个下降里。于是一遍中序遍历、只留 `prev`、`first`、`second` 三个引用，`O(n)`。

```python
def recover_tree(root: TreeNode | None) -> None:
    prev: TreeNode | None = None       # 中序遍历中刚访问过的前一个结点
    first = second = None              # 两个被交换的结点

    def inorder(node: TreeNode | None) -> None:
        nonlocal prev, first, second
        if node is None:
            return
        inorder(node.left)
        if prev and prev.val > node.val:        # 一处逆序对
            if first is None:
                first = prev           # 第一处逆序：较大的那个是被换错的结点
            second = node              # 最后一处逆序：较小的那个是另一个
        prev = node
        inorder(node.right)

    inorder(root)
    if first and second:
        first.val, second.val = second.val, first.val
```

运行：`[1,3,null,null,2]` → `[3,1,null,null,2]`，`[3,1,4,null,null,2]` → `[2,1,4,null,null,3]`，`[1,2]` → `[2,1]`；1000 个结点的单链右斜树，首尾值互换后可恢复（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`，每个结点访问一次；空间 `O(h)`（递归栈），`h` 为树高，最坏 `O(n)`。

**易错点。**
- 把 `second` 只在第一处逆序时赋值：不相邻互换会漏掉第二处。中序 `3,2,1`（示例 1）里，第一处逆序是 `(3,2)`，第二处是 `(2,1)`，只处理第一处会交换 `3` 和 `2`，得到 `2,3,1`，仍不是升序；正确是交换 `3` 和 `1`。
- 每处逆序都更新 `first`：中序 `1,5,3,4,2,6` 有两处逆序 `(5,3)`、`(4,2)`，应交换 `5` 和 `2`；`first` 被刷新成 `4` 会交换 `4` 和 `2`，得到 `1,5,3,2,4,6`，错误。
- 交换的是**值**，不是结点指针；用 `first.val, second.val = second.val, first.val` 即可。
- 递归深度：结点数 `1000` 的单链树，递归深度 `1000` 层以上，超过 CPython 默认递归上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）。

**追问。**
- 迭代中序：把递归换成显式栈，逆序检测逻辑不变，不受递归上限限制：
```python
def recover_tree(root: TreeNode | None) -> None:
    stack: list[TreeNode] = []
    prev: TreeNode | None = None
    first = second = None
    node = root
    while stack or node:
        while node:                    # 一路向左压栈
            stack.append(node)
            node = node.left
        node = stack.pop()             # 弹出的顺序就是中序（升序）顺序
        if prev and prev.val > node.val:
            if first is None:
                first = prev
            second = node
        prev = node
        node = node.right
    if first and second:
        first.val, second.val = second.val, first.val
```
- `O(1)` 空间：Morris 遍历（用空闲的右指针临时做线索回到祖先），逆序检测逻辑完全相同，遍历结束时树结构已还原。
- 不允许改动结点值、只能改指针：要找到两个结点的父指针并交换位置，相邻、父子关系要分情况，面试里通常不要求。
- 如果被换错的是任意 `k` 个结点：要么排序比较（`O(n log n)`），要么求中序序列里不在最长非降子序列上的结点；已不是单遍扫描的问题。

**同模式。** LC 98 验证二叉搜索树（前置题：判断有无逆序）、LC 230 BST 中第 K 小的元素（同样靠中序升序）、LC 530 BST 的最小绝对差、LC 501 BST 中的众数。
