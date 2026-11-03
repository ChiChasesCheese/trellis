---
id: craft-dry-run-on-a-copy-2-copy-depth
node: craft.patterns.dry-run-on-a-copy
type: qa
step: 2
---
## Q
**在副本上试运行 · 复制到多深才算「副本」**｜模式

`estimate_wait` 里复制队列时写的是 `[_Waiting(w.id, w.size, w.skipped) for w in queue]`，而不是看起来更简洁的 `list(queue)`。为什么？写成后者，预测一次会发生什么？

## A
**要点。** 副本必须复制「会被函数改写的每一层」。`list(queue)` 只复制了外层列表，里面的 `_Waiting` 对象仍是同一批。`drain` 会给被越过的人 `skipped += 1`，改在了真实对象上，调一次预测，真实排队的「被插队次数」就被偷偷推高了。

```python
from dataclasses import dataclass

@dataclass
class W:
    id: str; size: int; skipped: int = 0

def drain(queue, free):
    """就地改：队首坐不下，就让后面坐得下的人越过，并给被越过的人记一笔。"""
    for i, w in enumerate(queue):
        if w.size <= free:
            for earlier in queue[:i]:
                earlier.skipped += 1
            del queue[i]; return w.id

real = [W("big", 6), W("small", 2)]
drain(list(real), free=2)           # list() 只复制了列表，没复制里面的对象
print("浅复制后真实的 big.skipped =", real[0].skipped)

real = [W("big", 6), W("small", 2)]
drain([W(w.id, w.size, w.skipped) for w in real], free=2)  # 逐个复制元素
print("逐个复制后真实的 big.skipped =", real[0].skipped)
```

实际输出：

```
浅复制后真实的 big.skipped = 1
逐个复制后真实的 big.skipped = 0
```

**为什么。** 这个错最难发现：预测返回的数字完全正确，污染出现在之后的某次真实入座（有人莫名其妙被提前「挡路」）。

**怎么选。** 对象很小、字段都是数字：像上面这样手写复制，最清楚。嵌套很深、结构复杂：`copy.deepcopy`，更慢但不会漏层。对象本身不可变（frozen dataclass、tuple）：浅复制就够，这也是把状态写成不可变值的又一个理由。

**易错。** 只复制「被改写的那一层」是诱人的省事，但下一次有人在 `drain` 里多改一个字段，你的复制就悄悄过时了。
