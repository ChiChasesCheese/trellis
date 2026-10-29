---
id: tlc-sum-root-to-leaf-numbers-2-code
node: b.sum-root-to-leaf-numbers
type: qa
step: 2
---
## Q
**LC 129 求根到叶子节点数字之和**｜写出 Python 实现

二叉树每个节点存 `0` 到 `9` 的数字（节点数 `[1, 1000]`，深度至多 `10`），根到叶子的每条路径表示一个十进制数。返回所有路径所表示的数之和。要求 `O(n)`。

## A
**思路。** 递归函数 `dfs(node, acc)`，`acc` 是从根到父节点形成的数。进入节点时把它接长一位；叶子返回 `acc`，空节点返回 `0`，其余节点返回左右子树之和。

```python
def sum_numbers(root: TreeNode | None) -> int:
    def dfs(node: TreeNode | None, acc: int) -> int:
        if node is None:
            return 0
        acc = acc * 10 + node.val                 # 沿路径把数字“接长”一位
        if node.left is None and node.right is None:
            return acc                            # 叶子：这条路径生成的数
        return dfs(node.left, acc) + dfs(node.right, acc)
    return dfs(root, 0)
```

运行：`[1,2,3]` → `25`，`[4,9,0,5,1]` → `1026`，`[0]` → `0`，`[1,null,2]` → `12`。

**复杂度。** 时间 `O(n)`：每个节点恰好访问一次；空间 `O(h)`：递归栈，题目保证 `h <= 10`。

**写法要点。**
- 把空节点放在递归函数最前面处理，调用方不用再判断孩子是否存在，`dfs(node.left, acc)` 可以直接调。
- 叶子判断写成 `node.left is None and node.right is None`，用 `is None` 比较指针，不用真值判断，免得把「值为 `0`」和「没有节点」混在一起。
- `acc` 是整数参数，按值传递，每层各自一份，回溯时不用撤销；对比用列表记录路径时需要 `append` 后 `pop`。
- 不用 `int("".join(path))`：字符串拼接每层 `O(h)`，位数过多时还会触发 Python 3.11 以后的整数转字符串长度限制。
