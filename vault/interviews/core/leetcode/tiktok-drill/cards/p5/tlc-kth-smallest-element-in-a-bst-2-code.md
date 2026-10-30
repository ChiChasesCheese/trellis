---
id: tlc-kth-smallest-element-in-a-bst-2-code
node: p5.kth-smallest-element-in-a-bst
type: qa
step: 2
---
## Q
**LC 230 二叉搜索树中第 K 小的元素**｜写出 Python 实现

BST 有 `n` 个节点，`1 <= k <= n <= 10^4`，节点值在 `[0, 10^4]`。返回第 `k` 小的值，树可能退化成链，不要依赖递归。

## A
**思路。** 迭代中序：一路向左把节点压栈；弹出栈顶就是当前最小的未访问节点，给 `k` 减一，减到 `0` 就返回；否则转向它的右子树继续。

```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    stack: list[TreeNode] = []
    node = root
    while stack or node:
        while node:                    # 一路向左，沿途入栈
            stack.append(node)
            node = node.left
        node = stack.pop()             # 弹出的顺序就是升序
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    raise ValueError("k 超过节点数")
```

运行：`[3,1,4,null,2]`、`k=1` → `1`；`[5,3,6,2,4,null,null,1]`、`k=3` → `3`；`10^4` 个节点的右链，`k=10000` → `9999`，`k=1` → `0`。

**复杂度。** 时间 `O(h + k)`；空间 `O(h)`，`h` 为树高，栈中最多一条根到叶的路径。

**写法要点。** `while stack or node` 同时覆盖「还有未处理的左链」和「还有待回溯的祖先」；`k` 直接当计数器递减，省一个变量；`stack: list[TreeNode]` 声明元素类型；循环结束仍没返回说明 `k > n`，用 `raise` 比返回魔法值 `-1` 更明确（题目保证不会发生）。生成器版 `yield from` 的递归中序写法很短，但同样受递归深度限制。
