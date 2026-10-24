---
id: tlc-asteroid-collision-2-code
node: b.asteroid-collision
type: qa
step: 2
---
## Q
**LC 735 小行星碰撞**｜写出 Python 实现

整数数组 `asteroids`（`2 <= 长度 <= 10^4`，`-1000 <= asteroids[i] <= 1000`，不含 `0`），正数向右、负数向左，绝对值是大小；相撞时小的爆炸，等大都爆炸，同向不相撞。返回碰撞结束后的数组。

## A
**思路。** 栈里放还活着的小行星。逐个处理新来者 `a`：只有 `a < 0` 且栈顶向右时才相撞，栈顶小就弹掉并继续撞，等大两个都消失，栈顶大则 `a` 消失。`a` 活到最后才入栈。

```python
def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []                   # 栈里是还活着的小行星，从左到右
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:   # 只有 向右的栈顶 撞 向左的新来者
            top = stack[-1]
            if top <= -a:
                stack.pop()                 # 栈顶爆炸（等大时两个都炸）
            alive = top < -a                # 新来者只有严格更大才活下来
        if alive:
            stack.append(a)
    return stack
```

运行：`[5,10,-5]` → `[5, 10]`，`[8,-8]` → `[]`，`[10,2,-5]` → `[10]`，`[3,5,-6,2,-1,4]` → `[-6, 2, 4]`，`[-2,-1,1,2]` → `[-2, -1, 1, 2]`，`[1,-1,-1]` → `[-1]`；`5000` 个 `1` 后接 `5000` 个 `-1000` 剩 `5000` 颗。

**复杂度。** 时间 `O(n)`：每个元素最多入栈一次、出栈一次，`while` 的总迭代次数不超过 `n`；空间 `O(n)`。

**写法要点。** `alive = top < -a` 一行同时表达三种结果：栈顶更小（继续撞）、等大（双方消失，退出循环）、栈顶更大（新来者消失）；`if top <= -a: stack.pop()` 单独负责弹栈，两件事分开写不易混。`while alive and a < 0 and stack and stack[-1] > 0` 把所有短路条件放在一处，`stack` 判空在 `stack[-1]` 之前。栈直接用 `list`，`append` / `pop` 都是摊还 `O(1)`。
