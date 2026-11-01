---
id: hi-lld-amazon-locker-8-expired
node: lld.problem-breakdowns.amazon-locker
type: qa
step: 8
---
## Q
**过期格口的处理**｜低层设计 · 题目拆解

快递柜里员工要打开所有过期取件码对应的格口来取包裹退件。open_expired_compartments 怎么写？为什么这里不调用 clear_deposit？

## A
```python
def open_expired_compartments(self) -> None:
    for token in self.access_token_mapping.values():
        if token.is_expired():
            token.get_compartment().open()
```

**逻辑。** 遍历所有取件码，对已过期的打开它的格口。员工看到哪些门开了，就取出包裹并处理退回。

**为什么不清理。** 门打开不等于包裹已被取走，格口在员工真正取走前仍是占用状态。取走后，应由另一个方法（不在范围内）调用清理，释放格口并删除过期码。

**取舍。** 过期的码采取惰性清理：只在被访问或批量处理时才处理。简单，但过期码和占用的格口会在表里留到员工处理为止，可接受。

**要点。** 过期后的码是否惰性清理，是资深面试里常被追问的取舍。
