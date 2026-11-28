---
id: hi-c-lld-parking-lot-b03-py-optimistic-claim
node: lld.problem-breakdowns.parking-lot.beyond
type: qa
step: 4
---
## Q
**停车场 · Python：乐观认领与全局解释器锁**｜拓展 · 加分

"无锁搜索、持锁认领并重试"在 Python 里怎么写？它真的比整个方法加锁快吗？

## A
**模式。** 乐观认领（double-checked claim）：先无锁找一个候选，持锁时重新确认再占用。

```python
import threading


class Lot:
    def __init__(self, n: int) -> None:
        self._spots = list(range(n))
        self._occupied: set[int] = set()
        self._lock = threading.Lock()

    def _hint(self) -> int | None:              # 无锁搜索：结果只是线索，随时可能过期
        for s in self._spots:
            if s not in self._occupied:
                return s
        return None

    def enter(self) -> int | None:
        while True:
            s = self._hint()
            if s is None:
                return None                     # 满了
            with self._lock:                    # 权威检查必须在锁内重做
                if s not in self._occupied:
                    self._occupied.add(s)
                    return s
            # 被别人抢先了：回到循环重新找


lot = Lot(10)
res: list[int | None] = []
ts = [threading.Thread(target=lambda: res.append(lot.enter())) for _ in range(50)]
for t in ts:
    t.start()
for t in ts:
    t.join()
got = [r for r in res if r is not None]
assert len(got) == 10 and len(set(got)) == 10   # 50 个线程抢 10 个位：恰好 10 个成功且互不相同
```
- **为什么正确：** 无锁搜索即使读到过期的结果，也只会导致认领失败后重试，不会重复分配，因为唯一的写入口是锁内的再检查。
- **在 Python 里能快多少：** 很少。标准解释器有全局解释器锁（GIL），纯 Python 代码同一时刻只有一个线程在执行字节码，搜索并不能真正并行；这个方案在 Java、Go 等能多核并行的语言里才有意义，或者搜索本身很慢时。
- **隐含的假设：** 无锁地读集合成员依赖解释器对单次集合操作的原子性；这是实现细节，不是语言承诺，所以权威检查一定要在锁内。
- **何时不用：** 面试里默认整个 `enter` 加锁；只有被追问更高并发时才讲这个。
