---
id: craft-dry-run-on-a-copy-1-predict-with-the-real-function
node: craft.patterns.dry-run-on-a-copy
type: qa
step: 1
---
## Q
**在副本上试运行 · 预测为什么要调用真实逻辑本身**｜模式

餐厅等位系统有两个功能：真实入座（谁坐哪张桌），和「现在来一桌 2 人大概等多久」的预测。直接的写法是为预测另写一段推演代码。后来入座规则加了一条「小桌优先给小团」，只改了真实入座。会发生什么？有什么写法让这件事不可能发生？

## A
**要点。** 预测不要重写规则：把「入座规则」写成一个只吃参数的函数 `drain`（就地修改传进来的队列和空桌集合），真实路径传真状态，预测路径传复制品、再把时间往前拨。规则只存在一份，预测和实际就不会各说各话。

```python
from dataclasses import dataclass

@dataclass
class W:
    id: str
    size: int
    skipped: int = 0

def drain(queue, free, sizes):
    """规则的唯一实现，就地改传入的 queue / free。"""
    seated = []
    while True:
        for i, w in enumerate(queue):
            fits = [(sizes[t], t) for t in free if sizes[t] >= w.size]
            if fits:
                table = min(fits)[1]                    # 能坐下的最小桌
                for earlier in queue[:i]:
                    earlier.skipped += 1
                del queue[i]; free.remove(table); seated.append((w.id, table))
                break
        else:
            return seated

def estimate(queue, free, busy, target, sizes):
    q = [W(w.id, w.size, w.skipped) for w in queue] + [W(*target)]    # 复制品
    f, b, t = set(free), dict(busy), 0
    while True:
        for wid, table in drain(q, f, sizes):           # 同一个 drain
            if wid == target[0]: return t
            b[table] = t + 60                           # 入座后占桌 60 分钟
        t = min(b.values())                             # 时间跳到下一张桌子空出的时刻
        for k in [k for k, v in b.items() if v <= t]:
            del b[k]; f.add(k)

sizes, free = [2, 4], {1}                               # 桌 0 坐 2 人（被占），桌 1 坐 4 人（空）
queue = [W("A", 4), W("B", 2)]
drain(queue, free, sizes)                               # 真实：传真状态，A 坐进桌 1
busy = {0: 60, 1: 90}                                   # 桌 -> 空出的时刻（分钟）
print("真实：", [w.id for w in queue], "free =", free)
print("预测 C(2人) 要等：", estimate(queue, free, busy, ("C", 2), sizes), "分钟")
print("预测后真实状态没变：", [w.id for w in queue], free, busy)
```

运行（A 要 4 人桌、B 要 2 人桌，两张桌子分别在 60、90 分钟后空出）：

```
真实： ['B'] free = set()
预测 C(2人) 要等： 90 分钟
预测后真实状态没变： ['B'] set() {0: 60, 1: 90}
```

**为什么。** 两份规则迟早分叉，而且分叉时没有任何报错，只是预测悄悄变得不准。共用一个函数后，改规则的人只有一个地方可改。

**代价。** 要求规则不读实例属性（`self._free` 之类），所以要把状态当参数传进来，函数才能分别喂给真身和复制品。
