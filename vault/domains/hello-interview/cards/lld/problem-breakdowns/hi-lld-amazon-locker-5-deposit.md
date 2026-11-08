---
id: hi-lld-amazon-locker-5-deposit
node: lld.problem-breakdowns.amazon-locker.exam
type: qa
step: 5
---
## Q
**存件方法的逻辑**｜低层设计 · 题目拆解

请写出快递柜 deposit_package 的核心逻辑，说明步骤顺序，以及这个实现做了哪些简化假设。

## A
```python
def deposit_package(self, size: Size) -> str:
    comp = self._get_available_compartment(size)
    if comp is None:
        raise Exception(f"No compartment of size {size}")
    comp.open()           # 门解锁，快递员放入包裹
    comp.mark_occupied()
    token = self._generate_access_token(comp)
    self.access_token_mapping[token.get_code()] = token
    return token.get_code()  # 只返回码
```

**步骤。** 找空格口，没有就报错；开门；标记占用；生成取件码（随机码，过期时间为现在加 7 天）；存入查找表；返回码。

**简化假设。** 假设快递员开门后确实放了包裹，门约 30 秒后由硬件自动锁上；尺寸非法时在查找格口那一步自然找不到而失败。这段先开门再登记；开门无法撤销，更稳妥的顺序是先登记内存状态、最后开门，开门失败再回滚。生产里可以改成两阶段确认，或用传感器确认包裹在位，再生成码，这会增加状态管理，面试里一般不展开。
