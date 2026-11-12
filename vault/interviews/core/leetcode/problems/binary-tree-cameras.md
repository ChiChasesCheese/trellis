---
slug: binary-tree-cameras
---
## Q
**LC 968 监控二叉树**｜Hard

在树的节点上装摄像头，每个摄像头覆盖父节点、自己和直接子节点。求覆盖整棵树所需的最少摄像头数。

## A
**一句话。** 后序贪心：节点返回 `0` 未覆盖、`1` 已覆盖、`2` 有摄像头，孩子有未覆盖的就在当前装。

```python
def min_camera_cover(root):
    cams = 0
    def dfs(node):
        nonlocal cams
        if not node:
            return 1                   # 空节点视为已覆盖
        l, r = dfs(node.left), dfs(node.right)
        if l == 0 or r == 0:           # 孩子没人管：只能在这里装
            cams += 1
            return 2
        if l == 2 or r == 2:           # 被孩子的摄像头覆盖
            return 1
        return 0                       # 把压力留给父亲
    state = dfs(root)
    return cams + (state == 0)         # 根没人管就补一个
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 忘了处理根：`[0]` 只有根，状态是未覆盖，不补返回 `0`，应为 `1`。
- 在叶子上装摄像头：`[0,0,null,0,0]` 得 `2`，应为 `1`（装在叶子的父亲上）。
- 写成 `cams + (dfs(root) == 0)`：Python 先读 `cams` 再调 `dfs`，读到的还是 `0`。

**追问。**
- 为什么空节点算已覆盖？：算未覆盖会逼每个叶子都装摄像头。
- 摄像头成本不同？：贪心失效，改三状态树形 DP 带权。

**同模式。** LC 337 打家劫舍 III、LC 979 在二叉树中分配硬币、LC 124 二叉树中的最大路径和
