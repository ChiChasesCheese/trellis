---
id: tlc-open-the-lock-0-whole
node: c.open-the-lock
type: qa
---
## Q
**LC 752 打开转盘锁**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2021-08-23（国内 CodeTop）

转盘锁有四个拨轮，每个拨轮有 `0`–`9` 十个数字，可以循环旋转（`9` 变 `0`，`0` 变 `9`），每次只能拨动一个拨轮一位。初始为 `"0000"`。列表 `deadends` 中的数字一旦出现锁就永久锁定。给定 `target`，返回解锁所需的最少旋转次数，无法解锁返回 `-1`。`1 <= deadends.length <= 500`，`deadends[i].length == 4`，`target.length == 4`，`target` 不在 `deadends` 中，二者只含数字。例：`deadends = ["0201","0101","0102","1212","2002"], target = "0202"` → `6`；`deadends = ["8888"], target = "0009"` → `1`；`deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"` → `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每个四位数字是一个状态，每次拨动是一条边（每个状态 8 个邻居），从 `"0000"` 开始广度优先搜索，第一次到达 `target` 的层数就是最少步数。

**识别。** 「最少操作次数」且每步代价相同，状态空间只有 `10^4`：无权图最短路，用 BFS。`deadends` 就是不可进入的节点。

**推导。** 暴力的 DFS 不能保证最短，且要枚举所有路径。洞察：BFS 按层扩展，每个状态第一次被访问时的层数就是最短距离，所以访问过就不再入队；死亡数字在入队前过滤。

```python
from collections import deque


def open_lock(deadends: list[str], target: str) -> int:
    dead = set(deadends)
    if "0000" in dead:                           # 起点就是死亡数字
        return -1
    seen = {"0000"}
    queue = deque([("0000", 0)])                 # (当前数字, 已转动次数)
    while queue:                                 # BFS：第一次到达 target 的步数就是最少步数
        code, steps = queue.popleft()
        if code == target:
            return steps
        for i in range(4):
            for delta in (1, 9):                 # +1 和 -1（9 等价于 -1 mod 10）
                nxt = code[:i] + str((int(code[i]) + delta) % 10) + code[i + 1:]
                if nxt not in seen and nxt not in dead:
                    seen.add(nxt)                # 入队时就标记，避免重复入队
                    queue.append((nxt, steps + 1))
    return -1
```

运行：三个示例依次得到 `6`、`1`、`-1`；`deadends = ["0000"]` → `-1`；`deadends = []`, `target = "0000"` → `0`；`deadends = []`, `target = "5555"` → `20`。

**复杂度。** 时间 `O(10^4 * 4 * 2)`，空间 `O(10^4)`。

**拓展优化。**
- 双向 BFS：从起点和终点同时搜索，每次扩展较小的一侧，相遇即返回，搜索量大幅下降。

```python
def open_lock_bidirectional(deadends: list[str], target: str) -> int:
    dead = set(deadends)
    if "0000" in dead:
        return -1
    if target == "0000":
        return 0
    front, back = {"0000"}, {target}             # 从起点和终点同时向中间搜
    seen = dead | front | back
    steps = 0
    while front and back:
        if len(front) > len(back):               # 永远扩展较小的一侧，搜索量最小
            front, back = back, front
        steps += 1
        nxt_front: set[str] = set()
        for code in front:
            for i in range(4):
                for delta in (1, 9):
                    nxt = code[:i] + str((int(code[i]) + delta) % 10) + code[i + 1:]
                    if nxt in back:              # 两侧相遇
                        return steps
                    if nxt not in seen:
                        seen.add(nxt)
                        nxt_front.add(nxt)
        front = nxt_front
    return -1
```

- 图更大、有启发式信息时可用 A*（环形距离作启发函数）。

**易错点。**
- 起点 `"0000"` 本身在 `deadends` 里：直接返回 `-1`，否则会从死点出发。
- 只写 `+1` 不写 `-1`：`target = "0009"` 会走 9 步而不是 1 步；用 `(d + 9) % 10` 表示 `-1`。
- 出队后才标记 `seen`：同一状态被重复入队，队列膨胀，要在入队时标记。

**追问。**
- 输出具体旋转序列：保存每个状态的前驱 `parent[nxt] = code`，从 `target` 倒推。
- 拨轮数 / 数字数很大：状态数 `10^k`，双向 BFS 或 A* 才吃得消。

**同模式。** LC 127 单词接龙、LC 773 滑动谜题、LC 433 最小基因变化、LC 279 完全平方数、LC 1091 二进制矩阵中的最短路径。
