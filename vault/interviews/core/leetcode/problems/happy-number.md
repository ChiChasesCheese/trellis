---
slug: happy-number
---
## Q
**LC 202 快乐数**｜Easy

反复把 `n` 替换成各位数字的平方和，若最终变成 `1` 就是快乐数，否则会进入死循环。判断 `n` 是否快乐数。

## A
**一句话。** 数字平方和序列要么到 `1` 要么成环，用快慢指针判环。

```python
def is_happy(n):
    def step(x):
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    slow, fast = n, step(n)    # 错开一步，循环才进得去
    while fast != 1 and slow != fast:
        slow = step(slow)
        fast = step(step(fast))
    return fast == 1
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- `slow = fast = n` 又写 `while slow != fast`：一次都不进循环，`19` 返回 `false`，应为 `true`。
- 不判环：`n = 2` 会无限循环。

**追问。**
- 不用快慢指针怎么判环？：用集合记录见过的值，空间 `O(log n)`。
- 为什么序列不会无限增大？：`n` 过一步后很快压到三位数以内（不超过 `810`），必然重复或到 `1`。

**同模式。** LC 141 环形链表、LC 142 环形链表 II、LC 287 寻找重复数
