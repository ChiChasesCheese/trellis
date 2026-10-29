---
id: tlc-asteroid-collision-4-followup
node: a.asteroid-collision
type: qa
step: 4
---
## Q
**LC 735 小行星碰撞**｜追问

面试官接着问：（1）要返回幸存者在原数组里的下标？（2）输入是流式的，一颗一颗地到来，怎么维护答案？（3）规则改成“大小相同时只有新来者爆炸”或者“速度与大小成正比”？

## A
1. **幸存者下标**：栈里存下标，比较时读 `asteroids[stack[-1]]`。

```python
def survivors(asteroids: list[int]) -> list[int]:
    stack: list[int] = []
    for i, a in enumerate(asteroids):
        alive = True
        while alive and a < 0 and stack and asteroids[stack[-1]] > 0:
            top = asteroids[stack[-1]]
            if top <= -a:
                stack.pop()
            alive = top < -a
        if alive:
            stack.append(i)
    return stack
```

   `[3,5,-6,2,-1,4]` → `[2, 3, 5]`，即 `-6`、`2`、`4` 的下标。
2. **流式输入**：栈本身就是全部状态。每来一颗按同样的循环处理，均摊 `O(1)`；任何时刻栈的内容就是“到目前为止”的答案。
3. **改规则**：等大时只让新来者消失，只需把弹栈条件 `top <= -a` 改成 `top < -a`，`alive = top < -a` 那一行不变；仍是一个栈。速度与大小成正比时，谁先相遇不再由位置顺序决定，要按相遇时间排序的事件堆（`heapq`）模拟，复杂度变为 `O(n log n)`。

**Python 提醒**：栈用 `list.append` / `list.pop()`，都是摊还 `O(1)`；不要对列表用 `pop(0)`，那是 `O(n)`（需要队列时用 `collections.deque`）。`stack[-1]` 在空列表上抛 `IndexError`，所以 `stack and ...` 必须放在前面利用短路。
