---
id: craft-make-unmake-undo-log-1-mutate-then-restore
node: craft.patterns.make-unmake-undo-log
type: qa
step: 1
---
## Q
**做/撤销与撤销日志 · 回溯搜索时，每个分支复制一份状态，还是改了再改回来**｜写法

回溯（backtracking）要在一棵很大的搜索树上试各种选择：N 皇后放一个子、四子棋落一个子、国际象棋走一步。每个分支开始前复制整个状态，和只维护一份状态、进入分支时改（make）、返回时改回来（unmake），代价差在哪里？什么时候这个差别才值得？

## A
**要点。** 复制的代价是**状态大小 × 节点数**，改回来的代价只是**一步改动的大小 × 节点数**。状态小（N 皇后的几个集合）时两者差不多；状态大（带历史、计数表的棋局）时，复制就是主要开销。前提：unmake 必须是 make 的精确逆操作，一次不对称，错误会沿着整棵树累积。

```python
import time

# 同一棵搜索树：深度 d、分支 b；状态是一个大小为 S 的列表（棋盘 + 各种辅助表）
def count_copy(d, b, S):
    def go(depth, state):
        if depth == d: return 1
        total = 0
        for i in range(b):
            nxt = state[:]; nxt[depth] = i + 1       # 每个节点复制整个状态
            total += go(depth + 1, nxt)
        return total
    return go(0, [0] * S)

def count_unmake(d, b, S):
    state = [0] * S
    def go(depth):
        if depth == d: return 1
        total = 0
        for i in range(b):
            old = state[depth]; state[depth] = i + 1  # make：记下被覆盖的旧值
            total += go(depth + 1)
            state[depth] = old                        # unmake：与 make 严格对称
        return total
    return go(0)

for S in (10, 1000, 10000):
    t = time.perf_counter(); a = count_copy(6, 6, S); t1 = time.perf_counter() - t
    t = time.perf_counter(); b = count_unmake(6, 6, S); t2 = time.perf_counter() - t
    print(f"状态大小 S={S:5}  节点数={a}={b}  复制 {t1:.3f}s  撤销 {t2:.3f}s")
```

同一棵树（深度 6、分支 6，共 46656 个叶子），状态是一个 S 个元素的列表；"复制"版每个节点 `state[:]`：

```
状态大小 S=   10  节点数=46656=46656  复制 0.002s  撤销 0.002s
状态大小 S= 1000  节点数=46656=46656  复制 0.035s  撤销 0.002s
状态大小 S=10000  节点数=46656=46656  复制 0.327s  撤销 0.002s
```

**为什么。** 撤销的时间与 S 无关。真实的棋局状态里除了棋盘还有历史、局面计数表、易位权，复制这些每个节点都要付一遍。状态很小的问题（例如 N 皇后只有几个集合）里两者相差不大，这时选复制写法更不容易出错，别为省不下的时间引入对称性负担。

**代价。** 撤销要求你**精确知道一步改了什么**：忘记恢复任何一个字段，错误不会立刻出现，而是搜索到很深处才表现为莫名其妙的结果。保护手段：在测试里对随机着法序列断言「走 n 步再撤销 n 步后，状态与原来完全相等」。

**易错。** 搜索中途抛异常会让状态停在「已 make 未 unmake」；需要在 `try/finally` 里 unmake，或者让搜索函数在副本上运行（见 dry-run-on-a-copy）。
