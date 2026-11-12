---
slug: asteroid-collision
---
## Q
**LC 735 小行星碰撞**｜Medium

数组中正数向右、负数向左，绝对值是大小；相撞时小的爆炸，等大同归于尽，返回碰撞结束后剩下的。

## A
**一句话。** 用栈存活着的行星，向左的新来者只会撞栈顶向右的，更小就弹出继续撞。

```python
def asteroid_collision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            top = stack[-1]
            if top <= -a:
                stack.pop()      # 栈顶爆炸（等大两个都炸）
            alive = top < -a     # 新来者严格更大才活
        if alive:
            stack.append(a)
    return stack
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 等大时新来者没消失：`[8,-8]` 得 `[-8]`，应为 `[]`。
- 用 `if` 代替 `while`：`[3,5,-6,2,-1,4]` 得 `[3,-6,2,4]`，应为 `[-6,2,4]`。
- 漏掉 `stack[-1] > 0`：`[-2,-1,1,2]` 里同向的 `-2` 被误弹。

**追问。**
- 要返回幸存者的原下标？：栈里存下标，比较时读 `asteroids[stack[-1]]`。
- 流式输入？：栈就是全部状态，每颗均摊 `O(1)`。

**同模式。** LC 1047 删除字符串中的所有相邻重复项、LC 20 有效的括号、LC 739 每日温度、LC 84 柱状图中最大的矩形
