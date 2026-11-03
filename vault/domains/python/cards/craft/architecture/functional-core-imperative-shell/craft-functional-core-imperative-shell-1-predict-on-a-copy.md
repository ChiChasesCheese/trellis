---
id: craft-functional-core-imperative-shell-1-predict-on-a-copy
node: craft.architecture.functional-core-imperative-shell
type: qa
step: 1
---
## Q
**函数式核心 + 命令式外壳 · 为什么要把「谁坐哪桌」抽成不碰 self 的函数**｜架构

餐厅等位系统（候位队列 + 若干张桌）有两个需求：桌子空出来时真的安排入座；顾客问「我大概等多久」时要预测。如果入座规则写在 `finish()` 方法里，直接读写 `self._queue`、`self._free`，预测只能把整个对象拷一份，或者把规则再抄一遍。怎么只写一份规则，同时服务这两条路径？

## A
**要点。** 把决策写成纯核心（functional core）：只从参数读输入，只通过参数和返回值输出，不读 `self`、时钟、锁。有状态的外壳（imperative shell）负责持有真实状态：真实路径喂真状态，预测路径喂副本，规则只存在一处。

```python
def best_fit(size: int, free: dict[int, int]) -> int | None:
    fits = [(cap, t) for t, cap in free.items() if cap >= size]
    return min(fits)[1] if fits else None          # 最小够坐的桌，容量相同取编号小

def drain(queue: list[tuple[str, int]], free: dict[int, int]) -> list[tuple[str, int]]:
    """决策只读参数：没有 self，没有时钟，没有锁。就地改参数，返回 (人, 桌号)。"""
    seated = []
    for who, size in list(queue):
        if (t := best_fit(size, free)) is not None:
            queue.remove((who, size))
            del free[t]
            seated.append((who, t))
    return seated

class Restaurant:                                   # 外壳：持有真实状态
    def __init__(self) -> None:
        self.free: dict[int, int] = {}
        self.queue = [("甲", 4), ("乙", 2)]

    def finish(self, table: int, cap: int) -> list[tuple[str, int]]:
        self.free[table] = cap
        return drain(self.queue, self.free)         # 真实路径：喂真状态

    def preview(self, table: int, cap: int) -> list[tuple[str, int]]:
        return drain(list(self.queue), {**self.free, table: cap})   # 预测：喂副本

r = Restaurant()
print("预测:", r.preview(1, 4), "队列仍是", r.queue)
print("实际:", r.finish(1, 4), "队列剩", r.queue)
```

队列 `[甲4人, 乙2人]`，4 人桌空出，实际输出：

```
预测: [('甲', 1)] 队列仍是 [('甲', 4), ('乙', 2)]
实际: [('甲', 1)] 队列剩 [('乙', 2)]
```

**为什么。** 规则只有一份，预测与真实不会各改各的；核心用几个 list 和 dict 就能单独测，不需要线程、时钟。

**代价。** 核心要的所有输入都得显式传进来，参数会变长；规则很小、也没有预测需求时，这层拆分是多余的。
