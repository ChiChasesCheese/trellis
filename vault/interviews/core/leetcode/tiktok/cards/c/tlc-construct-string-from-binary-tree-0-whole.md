---
id: tlc-construct-string-from-binary-tree-0-whole
node: c.construct-string-from-binary-tree
type: qa
---
## Q
**LC 606 根据二叉树创建字符串**｜Medium · LC TikTok 全时段热度 25/100 · CodeTop 国内累计 1 次 · 最近 2025-04-07（国内 CodeTop）

给定二叉树的根节点 `root`，按前序遍历创建字符串表示：每个节点用它的整数值表示；如果节点至少有一个孩子，孩子的表示用括号括起来紧跟在节点值之后，先左后右；省略所有空括号对 `()`，但有一种例外：当节点只有右孩子没有左孩子时，必须保留一对空括号表示左孩子缺失。节点数 `[1, 10^4]`，`-1000 <= Node.val <= 1000`。例：`root = [1,2,3,4]` → `"1(2(4))(3)"`；`root = [1,2,3,null,4]` → `"1(2()(4))(3)"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归前序：节点值之后，有右孩子就左右都加括号（左为空写 `()`），只有左孩子就只加左括号，叶子什么都不加。

**识别。** 「树的前序序列化」：每个节点的字符串由自己的值和孩子的字符串拼成，典型的后序式递归（先得到孩子的串，再决定如何拼）。唯一的规则是什么时候保留空括号。

**推导。** 先写出完整形式（每个缺失的孩子都写 `()`），再去掉多余的空括号，容易出错。直接按情况拼：有右孩子时，左边必须有括号（左为空时是 `()`）；没有右孩子但有左孩子，只需要左括号；两个都没有就是叶子。

```python
def tree2str(root: TreeNode | None) -> str:
    if root is None:
        return ""                                # 空孩子的表示是空串，外层决定是否写括号
    left = tree2str(root.left)
    right = tree2str(root.right)
    if root.right:                               # 有右孩子：左括号必须保留，左为空时是 "()"
        return f"{root.val}({left})({right})"
    if root.left:                                # 只有左孩子：右边的 "()" 省略
        return f"{root.val}({left})"
    return str(root.val)                         # 叶子
```

运行：`[1,2,3,4]` → `"1(2(4))(3)"`，`[1,2,3,null,4]` → `"1(2()(4))(3)"`；`[1]` → `"1"`；`[-1,null,2]` → `"-1()(2)"`。

**复杂度。** 时间 `O(n)`（字符串拼接在每层产生拷贝，最坏链状树约 `O(n²)` 字符复制，`n = 10^4` 可忽略），空间 `O(h)`。

**拓展优化。**
- 避免反复拼接：用一个列表 `parts`，递归时 `append`，最后 `"".join(parts)`，保证 `O(n)` 复制。
- 递归深度超限时改用显式栈（见追问）。

**易错点。**
- 只有右孩子时省略了左边的 `()`：`[1,null,2]` 变成 `"1(2)"`，无法区分它是左孩子还是右孩子，正确是 `"1()(2)"`。
- 左孩子为空右孩子也为空时写了 `()`：叶子应该只有值，`"1()()"` 是错的。
- 最坏深度：10^4 个节点的链状树，CPython 默认递归上限约 1000，会抛 `RecursionError`，要 `sys.setrecursionlimit` 调高或改用显式栈。

**追问。**
- 显式栈：栈里放节点和字符串片段，片段 `"("`、`")"` 按后进先出的顺序倒着压入。

```python
def tree2str_iter(root: TreeNode | None) -> str:
    out: list[str] = []
    stack: list[TreeNode | str] = [root]         # 元素是节点，或要原样输出的 "(" / ")"
    while stack:
        cur = stack.pop()
        if isinstance(cur, str):
            out.append(cur)
            continue
        out.append(str(cur.val))
        if cur.right:                            # 先压右（后处理）：弹出顺序是 "(" 右子树 ")"
            stack += [")", cur.right, "("]
        if cur.left:
            stack += [")", cur.left, "("]
        elif cur.right:                          # 左为空但右非空：写 "()"
            stack += [")", "("]
    return "".join(out)
```

- 反向：从这个字符串还原二叉树（LC 536），用栈或递归解析括号。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 536 从字符串生成二叉树、LC 652 寻找重复的子树、LC 572 另一棵树的子树、LC 144 二叉树的前序遍历。
