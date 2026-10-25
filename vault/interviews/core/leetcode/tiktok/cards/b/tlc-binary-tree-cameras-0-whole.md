---
id: tlc-binary-tree-cameras-0-whole
node: b.binary-tree-cameras
type: qa
---
## Q
**LC 968 监控二叉树**｜Hard · TikTok 高频

给一棵二叉树，在树的节点上安装摄像头。每个摄像头可以监视**它的父节点、它自己和它的直接子节点**。返回监控树上所有节点所需的**最少摄像头数量**。节点数在 `[1, 1000]`，每个节点的值都是 `0`。例：`[0,0,null,0,0]` → `1`（摄像头装在第二层左节点上，覆盖根、它自己和两个孩子）；`[0,0,null,0,null,0,null,null,0]` → `2`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 自底向上的贪心：每个节点返回三种状态之一——`0` 未被监控、`1` 已被监控但没有摄像头、`2` 装了摄像头；只要有孩子是 `0`，当前节点必须装摄像头；否则孩子里有 `2` 则当前被监控；否则当前是 `0`，交给父亲处理；空节点算「已被监控」；最后根若仍是 `0`，再补一个。`O(n)`。

**识别。** 「树上每个节点都要被覆盖，求最少选点数」是树上的覆盖问题（与最小支配集同类），用树形 DP 或自底向上贪心。摄像头装在叶子上总是浪费：装在叶子的父亲上，能多覆盖父亲、祖父那一侧的节点，一定不会更差。节点数最多 `1000`，树可能退化成链，Python 递归会超过默认深度，所以写成迭代。

**推导。** 暴力：枚举所有节点子集，`2^n` → 树形 DP：每个节点有三种情形（自己装 / 被孩子覆盖 / 等父亲覆盖），`O(n)`，但状态多 → 观察叶子：在叶子装摄像头不如在它的父亲装，所以叶子的状态应当是「未被监控」，把压力推给父亲 → 自底向上一律推迟：一个节点只有在不得不（某个孩子未被监控）时才装摄像头，其余情况尽量让上层来覆盖，状态压缩成 `0 / 1 / 2` 三个值 → 先用栈得到先序序列，倒序处理就保证孩子先于父亲。

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

运行：`[0,0,null,0,0]` → `1`；`[0,0,null,0,null,0,null,null,0]` → `2`；`[0]` → `1`；`1000` 个节点的左斜链 → `334`，不抛 `RecursionError`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（`order` 与 `state`）。

**易错点。**
- 忘了处理根：只有一个节点 `[0]` 时，根的状态是「未被监控」，不补就返回 `0`，正确是 `1`。
- 在叶子上装摄像头：`[0,0,null,0,0]` 有两个叶子，得到 `2`，正确是 `1`（装在叶子的父亲上）。
- 把空节点当成「未被监控」：叶子的孩子（空）会迫使每个叶子装摄像头；空节点必须当成「已被监控」，既不需要、也不提供摄像头。

**追问。**
- 每个摄像头有不同成本：贪心失效，要改成三状态树形 DP 并带权，最后一张卡片给出写法。
- 摄像头覆盖半径变成距离不超过 `2`：状态要多记「最近的摄像头在多远」，贪心的「推迟」思路仍可用，但状态更多。
- 要输出摄像头的位置：把 `state[node] == CAMERA` 的节点收集起来。

**同模式。** LC 337 打家劫舍 III、LC 979 在二叉树中分配硬币、LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 1026 节点与其祖先之间的最大差值。
