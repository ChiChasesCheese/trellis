---
slug: open-the-lock
---
## Q
**LC 752 打开转盘锁**｜Medium

四位转盘锁从 `"0000"` 起，每次拨一个拨轮 ±1（循环），碰到 `deadends` 就锁死。求到 `target` 的最少步数，不可达返回 `-1`。

## A
**一句话。** 每个四位数是一个状态，每次拨动是一条边，从 `"0000"` 做 BFS，层数即步数。

```python
def open_lock(deadends, target):
    dead = set(deadends)
    if "0000" in dead:
        return -1
    seen = {"0000"}
    q = deque([("0000", 0)])
    while q:
        code, steps = q.popleft()
        if code == target:
            return steps
        for i in range(4):
            for d in (1, 9):          # +1 和 -1
                x = (int(code[i]) + d) % 10
                nxt = code[:i] + str(x) + code[i+1:]
                if nxt not in seen and nxt not in dead:
                    seen.add(nxt)     # 入队即标记
                    q.append((nxt, steps + 1))
    return -1
```

**复杂度。** 时间 `O(10^4)`，空间 `O(10^4)`。

**易错点。**
- 起点 `"0000"` 就在 `deadends`：必须直接返回 `-1`。
- 只写 `+1`：`target="0009"` 走 9 步而不是 1 步，`-1` 用 `+9 % 10`。
- 出队后才标记 `seen`：同一状态重复入队，队列膨胀。

**追问。**
- 要输出具体旋转序列？：记前驱 `parent[nxt] = code`，从 `target` 倒推。
- 拨轮数很大？：状态数 `10^k`，改用双向 BFS 或 A*。

**同模式。** LC 127 单词接龙、LC 773 滑动谜题、LC 433 最小基因变化、LC 279 完全平方数
