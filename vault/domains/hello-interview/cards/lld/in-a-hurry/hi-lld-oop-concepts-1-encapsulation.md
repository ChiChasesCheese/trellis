---
id: hi-lld-oop-concepts-1-encapsulation
node: lld.in-a-hurry.oop-concepts
type: qa
step: 1
---
## Q
**封装（encapsulation）在 LLD 里怎么体现**｜低层设计 · 速览

封装在低层设计面试里是怎样被检查的？为什么返回内部集合要返回副本，字段和 getter 该怎么取舍？

## A
**要点。** 封装是让对象的数据保持私有，由对象自己控制如何使用，外部通过简单方法交互，而不是伸手改内部细节。好处是可预测：`Account` 自己持有余额，只能经 `deposit()` 和 `withdraw()` 修改，就能在方法里强制规则（禁止负余额、记录流水、更新关联状态）。如果余额是公开字段，谁都能直接写，规则无法保证。

**面试检查点。** 你的类是直接暴露字段，还是提供方法？是否返回了可被调用者修改的内部可变集合？

```python
class ParkingLot:
    def __init__(self) -> None:
        self._spots: list[ParkingSpot] = []   # 私有：外部不能直接增删

    @property
    def spots(self) -> list[ParkingSpot]:
        return list(self._spots)              # 返回副本，调用方改它不会影响内部状态
```

**取舍。** 拿不准要不要暴露字段时，写 getter；要返回集合，就返回不可修改的视图或副本。
