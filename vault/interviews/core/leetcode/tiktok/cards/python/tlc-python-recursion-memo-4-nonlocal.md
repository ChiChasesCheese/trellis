---
id: tlc-python-recursion-memo-4-nonlocal
node: python.recursion-memo
type: qa
step: 4
---
## Q
**Python 递归｜闭包里的全局最优：`nonlocal`**

二叉树直径（LC 543）要在 DFS 里更新全局最大值，内层函数里写 `best = max(best, l + r)` 为什么得 `0`？`nonlocal` 解决什么，还有哪些替代写法？

## A
内层函数里**赋值**一个变量，Python 就认为它是内层的局部变量；外层的 `best` 没被改动。

```python
def diameter(root: TreeNode | None) -> int:
    best = 0
    def depth(n: TreeNode | None) -> int:
        nonlocal best                        # 声明：赋值时改的是外层的 best
        if n is None:
            return 0
        l, r = depth(n.left), depth(n.right)
        best = max(best, l + r)              # 经过 n 的最长路径边数 = 左深 + 右深
        return 1 + max(l, r)                 # 返回给父节点的是单边深度
    depth(root)
    return best
t = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
print(diameter(t), diameter(None))   # 3 0
```

三种写法：
1. `nonlocal best`：最直接，用于数字等不可变值。
2. `best = [0]`，更新 `best[0] = max(best[0], ...)`：可变容器，不需要 `nonlocal`（老写法）。
3. 递归函数**返回元组**`(单边深度, 目前最优)`：没有外部状态，函数更纯，但参数和返回更复杂。

- 类里写 `self.best`，在 LeetCode 的 `class Solution` 里很常见；多个测试用例会共用同一个实例的话，要在入口函数里**重置**。
- `nonlocal` 只能指向外层函数的变量；顶层（模块级）变量用 `global`。`nonlocal` 声明必须出现在使用该变量之前。
- 适用：LC 124 最大路径和、LC 543、LC 687、LC 298（树里的全局最优 + 单边返回）。
- **坑**：只读外层变量不需要声明；只要函数里有对它的赋值（包括 `+=`），就必须声明，否则报 `UnboundLocalError`。
