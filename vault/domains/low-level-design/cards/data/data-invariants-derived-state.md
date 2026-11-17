---
id: data-invariants-derived-state
node: data.invariants
type: qa
step: 4
---
## Q
预约服务既存了 `active_count`，又存了 `available_slots`，每次预约两处都要更新。这为什么容易出错？什么时候可以不现算？

## A
**能算出来的就不存**

- **两份真相**：同一事实存两处，不变量多出一条“两者一致”，漏改一处就悄悄偏离；
- **现算**：`available = capacity - len(active)`，`flagged`、`total_quantity`、`is_expired` 同理，永远一致，不用同步；
- **例外**：现算要扫大表时才存缓存；此时把“缓存等于重新计算的结果”写成不变量，只在一个方法里更新；
- **过期**：存 `expires_at`，用当前时间现算是否过期，不存 `expired` 标志，因为没有谁来把它翻成真。

```python
class Session:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._active: set[str] = set()
    @property
    def available_slots(self) -> int:
        return self.capacity - len(self._active)         # 恒等，不用同步
    def book(self, user: str):
        if user in self._active or self.available_slots == 0:
            raise ValueError("cannot book")
        self._active.add(user)

s = Session(1)
s.book("ann")
print(s.available_slots)     # 0，没有第二处要同步的计数
```

**知识点：**不变量与封装（Invariants）
