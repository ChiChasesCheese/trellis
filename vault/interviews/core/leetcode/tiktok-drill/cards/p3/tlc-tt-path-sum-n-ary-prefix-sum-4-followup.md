---
id: tlc-tt-path-sum-n-ary-prefix-sum-4-followup
node: p3.tt-path-sum-n-ary-prefix-sum
type: qa
step: 4
---
## Q
**N 叉树路径和（前缀和加哈希）**｜追问

N 叉树上统计自上而下、和为 `target` 的路径条数，已用前缀和加哈希做到 `O(n)`。面试官接着问：（1）二叉树版本（LC 437）有什么不同？（2）路径可以向上走（从节点到祖先）呢？（3）要返回路径本身？（4）值全是正数时有更省空间的做法吗？（5）树有 `10^5` 层，递归爆栈怎么办？

## A
1. **二叉树**：算法完全一样，把 `node.children` 换成 `[node.left, node.right]` 里非空的孩子；这是 LC 437，也是最常见的写法。
2. **向上的路径**：对“自底向上、从某个节点走到它的祖先”，把路径反过来看就是“从祖先出发向下”的同一类路径，条数相同；真正不同的是「任意两点之间的路径」（可以先上后下），这时要用后序遍历合并左右子树的计数，复杂度和实现都更复杂，先和面试官确认路径的定义。
3. **返回路径**：哈希表改存 `前缀和 -> 当前链上该前缀和对应的深度列表`，同时维护当前链（一个栈）；命中时用深度切片得到路径节点。输出规模本身可能很大，注意只在需要时构造。
4. **全正数**：前缀和沿链严格递增，可以对当前链用双指针（滑动窗口）或二分，不需要哈希表；遇到负数或零就退回哈希表的方法。
5. **深链爆栈**：`10^5` 层远超默认的递归上限约 1000。可以 `sys.setrecursionlimit` 调高，或改成显式栈：栈里放 `(节点, 父亲的前缀和)`，节点为 `None` 的项是「退出标记」，在所有孩子之后才弹出（后进先出），恰好模拟递归返回时的撤销：

```python
from collections import Counter


def path_sum_stack(root: Node | None, target: int) -> int:
    """统计自上而下的路径条数（起点终点任意，只能往孩子方向走），路径和等于 target。"""
    if root is None:
        return 0
    seen = Counter({0: 1})                        # 前缀和 -> 当前根到当前节点这条链上出现的次数；空前缀 0 出现 1 次
    ans = 0
    stack: list[tuple[Node | None, int]] = [(root, 0)]    # (节点, 父亲的前缀和)；node 为 None 表示「退出」标记
    while stack:
        node, prefix = stack.pop()
        if node is None:
            seen[prefix] -= 1                     # 离开某个节点：撤销它的前缀和（回溯）
            continue
        cur = prefix + node.val                   # 根到 node 的前缀和
        ans += seen[cur - target]                 # 以 node 结尾、和为 target 的路径数
        seen[cur] += 1
        stack.append((None, cur))                 # 先压退出标记，它会在所有孩子处理完之后弹出
        stack.extend((child, cur) for child in node.children)
    return ans
```


**Python 提醒**：`collections.Counter` 读不存在的键返回 `0` 而不插入，`counter[key] -= 1` 可以减到 `0` 甚至负数，键仍然保留；要真的删掉可以 `del`，但这里不需要。`Counter({0: 1})` 用字典初始化最直观，`Counter([0])` 也能得到同样的结果。
