---
id: tlc-super-washing-machines-4-followup
node: b.super-washing-machines
type: qa
step: 4
---
## Q
**LC 517 超级洗衣机**｜追问

面试官接着问：（1）如果每一步全局只能移动一件衣服，最少步数是多少？（2）洗衣机排成一个环、求最少的总搬运件数？（3）换成一棵二叉树，每个结点有若干硬币，每步把一枚硬币沿一条边移动（LC 979）？

## A
1. **每步只移动一件**：每件衣服每过一条边算一步，答案是总搬运量 `Σ|flow_i|`（对每条边的前缀余量取绝对值求和）。`[1,0,5]` 的前缀余量是 `-1, -3`，答案 `4`。
2. **环形**：环上多一条边（最后一台到第一台），它的流量 `x` 是未知数，其余各边流量是 `x - c_i`（`c_i` 由前缀余量决定）。总搬运量 `Σ|x - c_i|`，`x` 取 `c_i` 的中位数时最小（中位数到各点的绝对距离之和最小）。
3. **树（LC 979）**：一条边的流量是它下方子树的余量（硬币数 − 结点数），每枚硬币过一条边算一步，答案是所有边 `|余量|` 之和。后序遍历返回子树余量，边处累加绝对值。

```python
def distribute_coins(root: TreeNode | None) -> int:
    moves = 0

    def excess(node: TreeNode | None) -> int:   # 返回子树的余量：硬币数 - 结点数
        nonlocal moves
        if node is None:
            return 0
        left, right = excess(node.left), excess(node.right)
        moves += abs(left) + abs(right)        # 两条子边各自的流量
        return node.val + left + right - 1

    excess(root)
    return moves
```

**Python 提醒**：嵌套函数要修改外层变量必须声明 `nonlocal moves`，否则 `moves += …` 会把它当成局部变量，抛 `UnboundLocalError`。
