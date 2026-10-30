---
id: uth-python-exceptions-context-1-unwind
node: python.exceptions-context
type: qa
step: 1
---
## Q
**出错时程序怎样找到处理者**｜Python · CPython 3.14

函数 `a` 调 `b`，`b` 调 `c`，`c` 里执行了 `1/0`，只有 `a` 写了 `try/except`。这个错误怎样一路传到 `a` 并被接住？

## A
**背景。** 函数调用像叠盘子：每调用一个函数，调用栈（call stack）上就压一个帧（frame）。`c` 出错后没法往下走。最老的办法是每个函数都返回错误码、上层逐层检查，漏检一层，错误就悄悄消失。

**结构。** Python 用异常（exception）：出错处创建一个异常对象，解释器从当前帧开始问「这里有 `try` 管吗」，没有就丢掉这一帧，退回上一层再问，直到有人接住；没人接，就退到最外层，打印回溯（traceback）并结束程序。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 192">
<rect x="20" y="14" width="130" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a   try: b()</text>
<rect x="20" y="70" width="130" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b   c()</text>
<rect x="20" y="126" width="130" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c   1/0</text>
<line x1="45" y1="48" x2="45.0" y2="64.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="45,70 42.0,64.0 48.0,64.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="45" y1="104" x2="45.0" y2="120.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="45,126 42.0,120.0 48.0,120.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="52" y="60" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调用</text>
<line x1="190" y1="150" x2="190.0" y2="34.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,28 193.0,34.0 187.0,34.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="184" y1="148" x2="196" y2="148" stroke-width="1.2" stroke="currentColor"/>
<text x="204" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">c 抛出异常</text>
<line x1="184" y1="94" x2="196" y2="94" stroke-width="1.2" stroke="currentColor"/>
<text x="204" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">b 无 try 退一层</text>
<line x1="184" y1="36" x2="196" y2="36" stroke-width="1.2" stroke="currentColor"/>
<text x="204" y="40" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a 有 except 接住</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没人接就一直退到最外层</text>
</svg>
```

**细节。**

- 每退出一层，异常对象的回溯里就多记一条「文件、行号」，`Traceback (most recent call last)` 打印的就是这串记录。
- 调用栈有深度上限：CPython 3.14 默认 1000 层，超出就抛 `RecursionError`。

**坑。** 递归 DFS 碰到链状的树，深度轻松过 1000：要用 `sys.setrecursionlimit` 调大，或改成显式栈。

**例题：** LC 98 验证二叉搜索树（同类：LC 437 路径总和 III）

判断二叉树是否为有效二叉搜索树：左子树的值都严格小于当前结点，右子树的值都严格大于当前结点，左右子树自身也是。结点数最多 10^4，退化成链时递归深度就是 10^4。

```python
import sys

sys.setrecursionlimit(20000)

class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val, self.left, self.right = val, left, right

def is_valid_bst(root: TreeNode | None) -> bool:
    def valid(node: TreeNode | None, low: float, high: float) -> bool:
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)

    return valid(root, float("-inf"), float("inf"))
```
