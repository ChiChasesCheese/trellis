---
id: tlc-binary-tree-cameras-2-code
node: b.binary-tree-cameras
type: qa
step: 2
---
## Q
**LC 968 监控二叉树**｜写出 Python 实现

二叉树 `root`（节点数 `[1, 1000]`，每个节点的值为 `0`），在节点上装摄像头，每个摄像头监视父节点、自己和直接子节点，返回监控所有节点所需的最少摄像头数。要求不因树退化成链而递归爆栈。

## A
**思路。** 用栈得到先序序列，倒序处理使孩子先于父亲。每个节点的状态：`0` 未监控、`1` 已监控、`2` 有摄像头，空节点是 `1`。孩子有 `0` 就必须在当前节点装摄像头；否则孩子有 `2` 则当前已监控；否则当前未监控。根若未监控再补一个。

```python
def min_camera_cover(root: TreeNode | None) -> int:
    UNCOVERED, COVERED, CAMERA = 0, 1, 2
    order: list[TreeNode] = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    state: dict[TreeNode | None, int] = {None: COVERED}   # 空节点当作"已被覆盖"，不需要也不提供摄像头
    cameras = 0
    for node in reversed(order):                         # 孩子先于父亲
        l, r = state[node.left], state[node.right]
        if l == UNCOVERED or r == UNCOVERED:             # 有孩子没人管：只能在这里装
            state[node] = CAMERA
            cameras += 1
        elif l == CAMERA or r == CAMERA:                 # 被孩子的摄像头覆盖
            state[node] = COVERED
        else:                                            # 孩子都被覆盖但都没摄像头：把压力留给父亲
            state[node] = UNCOVERED
    return cameras + (state[root] == UNCOVERED)          # 根没人管就在根上补一个
```

运行：`[0,0,null,0,0]` → `1`；`[0,0,null,0,null,0,null,null,0]` → `2`；`[0]` → `1`；`1000` 个节点的左斜链 → `334`。

**复杂度。** 时间 `O(n)`：先序一遍、倒序一遍；空间 `O(n)`。

**写法要点。** 把 `{None: COVERED}` 预先放进字典，查孩子的状态时不需要判空；三个常量命名代替魔法数字 `0 / 1 / 2`；`cameras + (state[root] == UNCOVERED)` 用 `bool` 当 `0 / 1` 直接相加；先序倒序代替递归后序，深度再大也安全。
