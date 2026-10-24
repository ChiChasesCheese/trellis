---
id: pl-binding-evaluation-order-pitfall-tuple-assign
node: binding.evaluation-order
type: qa
step: 9
---
## Q
Python 里反转链表时 `prev, cur, cur.next = cur, cur.next, prev` 为什么会崩，而 `cur.next, prev, cur = prev, cur, cur.next` 却是对的？

## A
Python 的多目标赋值分两步：**先把右边所有表达式算完**得到一个元组，再**从左到右**依次赋给目标。每个目标里的子表达式（比如 `cur.next` 里的 `cur`）在轮到它赋值的那一刻才求值。

链表节点：

```python
class N:
    def __init__(s, v, nxt=None): s.v, s.next = v, nxt

def reverse_bad(head):
    prev, cur = None, head
    while cur:
        prev, cur, cur.next = cur, cur.next, prev
    return prev
```

右边先算完：`(cur, cur.next, prev)`，没有问题。接着赋值：

1. `prev = cur`；
2. `cur = cur.next`，此时 `cur` 已经指向**下一个节点**；
3. `cur.next = prev`，这里的 `cur` 是新的 `cur`，于是改写了**下一个节点**的指针，而不是当前节点的。

当 `cur` 走到链表末尾变成 `None`，第三步就变成给 `None` 设属性：

```text
AttributeError: 'NoneType' object has no attribute 'next'
  and no __dict__ for setting new attributes
```

调换目标的顺序，让依赖旧 `cur` 的目标排在前面：

```python
cur.next, prev, cur = prev, cur, cur.next
```

`cur.next` 先赋，此时 `cur` 还是当前节点；之后才改 `prev` 与 `cur`。`reverse_ok` 对 `1→2→3` 得到 `[3, 2, 1]`。

这是真实会出现在面试和算法代码里的 bug：它能通过「看起来对」的评审，只在特定输入下崩溃，或者在更隐蔽的情形下静默地改错节点。

对策：
- 目标之间有依赖时，**把依赖旧值的目标放在最前面**，或者拆成多条语句，用临时变量保存 `nxt = cur.next`。
- 同样结构的 Go 代码 `prev, cur, cur.next = cur, cur.next, prev` 却是**正确的**，输出 `3 2 1`。Go 把多重赋值分成两个阶段：第一阶段把左边的下标和指针间接寻址（这里是 `cur.next` 里的 `cur`）连同右边所有表达式一起求值；第二阶段才从左到右赋值。所以 `cur.next` 指向的仍是旧节点。不要在语言之间直接搬运多重赋值的写法。
