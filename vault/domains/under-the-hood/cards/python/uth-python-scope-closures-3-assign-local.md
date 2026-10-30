---
id: uth-python-scope-closures-3-assign-local
node: python.scope-closures
type: qa
step: 3
---
## Q
**为什么 += 会报 UnboundLocalError，nonlocal 又改了什么**｜Python · CPython 3.14

嵌套函数里写 `best = max(best, x)`，运行时说 `best` 还没有值；加一行 `nonlocal best` 就好了。编译器到底看到了什么？

## A
**背景。** Python 没有 `int best` 这样的声明，编译器怎么知道 `best` 是新的局部变量，还是外层那个？

**结构。** 规则：函数体里任何位置对一个名字赋值，这个名字在整个函数里都是局部变量；编译时扫一遍函数体就定了，与执行顺序无关。`nonlocal best` 声明「这个名字就是外层函数的那个 cell」，赋值写进 cell；`global` 同理，指向模块级。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<rect x="10" y="20" width="320" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22" y="46" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">print(x)</text>
<text x="110" y="46" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读的是局部 x 此刻还没有值</text>
<text x="22" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">x += 1</text>
<text x="110" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有赋值 x 整个函数都是局部</text>
<line x1="170" y1="84" x2="170" y2="110" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,110.0 167.0,104.0 173.0,104.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">UnboundLocalError</text>
<rect x="10" y="148" width="320" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">nonlocal x</text>
<text x="110" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x 指向外层那个 cell</text>
<text x="22" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">x += 1</text>
<text x="110" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读写的都是 cell</text>
</svg>
```

**细节。**

- 只读外层变量不用声明，只有赋值才会让名字变成局部。
- `best += 1` 先读后写，而局部的 `best` 还没有值，3.14 报 `cannot access local variable 'best' where it is not associated with a value`。
- `nonlocal` 的名字在外层函数里找不到，编译时就报 `SyntaxError`。
- `best.append(1)` 不是赋值，不用声明。

**为什么。** 读宽写严：默认写就是局部，免得一不小心改掉外层的状态。

**例题：** LC 543 二叉树的直径

给一棵二叉树的根节点，返回树的直径：任意两个节点之间最长路径的边数，路径不一定经过根。节点数在 `[1, 10^4]`。例：`root = [1,2,3,4,5]` 得 `3`。

```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
    best = 0

    def height(node: TreeNode | None) -> int:    # 子树高度（按结点数），空树为 0
        nonlocal best
        if node is None:
            return 0
        lh, rh = height(node.left), height(node.right)
        best = max(best, lh + rh)                # 经过 node 的最长路径的边数 = 左高 + 右高
        return 1 + max(lh, rh)

    height(root)
    return best
```
