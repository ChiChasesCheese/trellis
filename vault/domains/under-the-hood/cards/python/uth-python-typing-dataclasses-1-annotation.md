---
id: uth-python-typing-dataclasses-1-annotation
node: python.typing-dataclasses
type: qa
step: 1
---
## Q
**类型注解只是便签**｜Python · CPython 3.14

`x: int = "hello"` 会报错吗？`def f(a: int)` 里的 `int` 到底被拿去做了什么？

## A
**背景。** 动态语言不用声明类型，写短脚本很快；项目一大，就没人知道 `f` 该传什么了。想补上提示，又不想让运行变慢、变严格。

**结构。** 注解（annotation）就是贴在变量、参数上的便签：解释器把它存下来（放进 `__annotations__`），之后再不看。真正检查类型的是外部工具（mypy、pyright、IDE），它们在运行之前读这些便签。`f("abc")`、`x: int = "hello"` 都照常运行。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="8" y="58" width="74" height="40" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="45" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">源码</text>
<text x="45" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x: int</text>
<line x1="82" y1="70" x2="115.4" y2="41.9" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120,38 117.3,44.2 113.5,39.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="82" y1="86" x2="115.8" y2="119.8" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120,124 113.6,121.9 117.9,117.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="12" width="212" height="46" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="226" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Python 解释器</text>
<text x="226" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存下便签 不检查 照常运行</text>
<rect x="120" y="102" width="212" height="46" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="226" y="121" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">mypy / pyright / IDE</text>
<text x="226" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">运行之前读便签 报类型错</text>
</svg>
```

**细节。**

- 3.14 起（PEP 649、749）注解不再在定义时立刻求值，而是存成一个函数，有人读 `__annotations__` 时才计算。类里写 `m: Undefined` 不报错，读取时才 `NameError`。
- 函数体里的局部变量注解，既不求值也不保存。

**坑。** 3.13 及更早，类体里还没有类自己的名字，`left: Node` 要写成 `"Node"`（加引号）；3.14 起不用。

**例题：** LC 98 验证二叉搜索树

判断二叉树是否为有效二叉搜索树：左子树的值都严格小于当前结点，右子树的值都严格大于当前结点，左右子树自身也是。代码里 `TreeNode` 的注解 `"TreeNode | None"` 就是上面说的加引号的前向引用。

```python
class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val, self.left, self.right = val, left, right

def is_valid_bst(root: TreeNode | None) -> bool:
    stack: list[TreeNode] = []
    node = root
    prev_val: int | None = None
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev_val is not None and node.val <= prev_val:
            return False
        prev_val = node.val
        node = node.right
    return True
```
