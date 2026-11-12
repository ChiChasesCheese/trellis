---
slug: construct-string-from-binary-tree
---
## Q
**LC 606 根据二叉树创建字符串**｜Medium

按前序遍历把二叉树转成带括号的字符串：孩子用括号括起，省略空括号，但只有右孩子时必须保留 `()` 表示左孩子缺失。

## A
**一句话。** 递归前序：有右孩子就左右都加括号（左为空写 `()`），只有左孩子只加左括号，叶子只写值。

```python
def tree2str(root):
    if not root:
        return ""
    left, right = tree2str(root.left), tree2str(root.right)
    if root.right:     # 左括号必须保留，左为空时是 "()"
        return f"{root.val}({left})({right})"
    if root.left:
        return f"{root.val}({left})"
    return str(root.val)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 只有右孩子时省略左边的 `()`：`[1,null,2]` 得 `"1(2)"`，应为 `"1()(2)"`。
- 叶子也写 `()`：`"1()()"` 是错的，叶子只有值。

**追问。**
- 链状树 `10^4` 层爆栈？：用显式栈，把 `"("`、`")"` 和孩子按逆序压栈。
- 反过来从字符串还原树？：用栈或递归解析括号（LC 536）。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 536 从字符串生成二叉树、LC 652 寻找重复的子树、LC 572 另一棵树的子树
