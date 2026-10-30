---
id: tlc-binary-tree-cameras-2-code
node: b.binary-tree-cameras
type: qa
step: 2
---
## Q
**LC 968 监控二叉树**｜写出 Python 实现

二叉树 `root`（节点数 `[1, 1000]`，每个节点的值为 `0`），在节点上装摄像头，每个摄像头监视父节点、自己和直接子节点，返回监控所有节点所需的最少摄像头数。

## A
**思路。** 后序递归，`dfs(node)` 返回该节点的状态，孩子先于父亲。每个节点的状态：`0` 未监控、`1` 已监控、`2` 有摄像头，空节点是 `1`。孩子有 `0` 就必须在当前节点装摄像头；否则孩子有 `2` 则当前已监控；否则当前未监控。根若未监控再补一个。

```python
def min_camera_cover(root: TreeNode | None) -> int:
    UNCOVERED, COVERED, CAMERA = 0, 1, 2
    cameras = 0

    def dfs(node: TreeNode | None) -> int:       # 返回 node 的状态；孩子先于自己处理（后序）
        nonlocal cameras
        if node is None:                         # 空节点当作"已被覆盖"，不需要也不提供摄像头
            return COVERED
        l, r = dfs(node.left), dfs(node.right)
        if l == UNCOVERED or r == UNCOVERED:     # 有孩子没人管：只能在这里装
            cameras += 1
            return CAMERA
        if l == CAMERA or r == CAMERA:           # 被孩子的摄像头覆盖
            return COVERED
        return UNCOVERED                         # 孩子都被覆盖但都没摄像头：把压力留给父亲

    root_state = dfs(root)                       # 先算完再读 cameras，别写成 cameras + (dfs(root) == ...)
    return cameras + (root_state == UNCOVERED)   # 根没人管就在根上补一个
```

运行：`[0,0,null,0,0]` → `1`；`[0,0,null,0,null,0,null,null,0]` → `2`；`[0]` → `1`；`1000` 个节点的左斜链 → `334`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(h)`：递归栈，最坏 `O(n)`。

**写法要点。** `dfs(None)` 直接返回 `COVERED`，不需要对孩子判空；三个常量命名代替魔法数字 `0 / 1 / 2`；`cameras + (state[root] == UNCOVERED)` 用 `bool` 当 `0 / 1` 直接相加；`dfs` 用 `nonlocal cameras` 累计摄像头数，返回值只传状态；`root_state` 先存下再读 `cameras`，避免一行里先读到旧值。
