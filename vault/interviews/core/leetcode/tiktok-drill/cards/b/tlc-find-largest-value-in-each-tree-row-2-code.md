---
id: tlc-find-largest-value-in-each-tree-row-2-code
node: b.find-largest-value-in-each-tree-row
type: qa
step: 2
---
## Q
**LC 515 在每个树行中找最大值**｜写出 Python 实现

二叉树（节点数 `0` 到 `10^4`，值覆盖整个 32 位有符号整数）：返回每层的最大值，从上到下。空树返回 `[]`。

## A
**思路。** 用列表 `level` 保存当前整层；对它取 `max` 追加到答案，再用列表推导收集所有非空孩子作为下一层，直到某层为空。

```python
def largest_values(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    level = [root] if root else []
    while level:
        ans.append(max(node.val for node in level))                              # 这一层的最大值
        level = [c for node in level for c in (node.left, node.right) if c]       # 下一层：所有非空孩子
    return ans
```

运行：`[1,3,2,5,3,null,9]` → `[1, 3, 9]`，`[1,2,3]` → `[1, 3]`，`[]` → `[]`，`[-3,-5]` → `[-3, -5]`，`10^4` 个节点的链 → 长度 `10000` 的列表。

**复杂度。** 时间 `O(n)`；空间 `O(w)`，`w` 是最大层宽。

**写法要点。** 「整层换整层」的写法不需要 `deque`，也不需要 `for _ in range(len(queue))` 来数这一层有几个；双层列表推导 `for node in level for c in (...)` 的顺序与嵌套 `for` 循环相同，`if c` 过滤掉空孩子；`max` 接生成器表达式，不建中间列表。
