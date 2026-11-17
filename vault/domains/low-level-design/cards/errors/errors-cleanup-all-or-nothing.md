---
id: errors-cleanup-all-or-nothing
node: errors.cleanup
type: qa
step: 4
---
## Q
汇率表支持一次登记一批汇率，第三条非法。前两条已经写进去了，要怎么保证“失败的批次不留一点痕迹”？写撤销代码还是别的办法？

## A
**在副本上演算，成功后一次赋值**

- **撤销代码本身会出错**：记下旧值、失败时倒着恢复，这段恢复逻辑很少被测试，一旦漏掉一个字段就出现半截状态；
- **局部副本**：先 `dict(self.table)` 复制，所有解析、校验、合并都在副本上做，出错就丢掉副本，原表从未被碰过；
- **提交只有一条语句**：`self.table = staged`，读者看到的要么是旧表、要么是新表；
- **浅拷贝够用的条件**：值本身不可变（数字、字符串、元组）；值是可变对象就要深拷贝，否则副本和原表共用同一个对象；
- **批次内部的冲突**：同一个币种出现两次，在副本上自然是后一条覆盖前一条，规则写进合同。

```python
class Rates:
    def __init__(self): self.table = {"USD": 1.0}

    def register(self, batch: list[tuple[str, float]]) -> None:
        staged = dict(self.table)             # 局部副本
        for code, rate in batch:
            if not rate > 0: raise ValueError(code)
            staged[code] = rate
        self.table = staged                   # 全部成功才换

r = Rates()
try: r.register([("EUR", 1.1), ("GBP", 1.3), ("JPY", -1)])
except ValueError: print(r.table)             # {'USD': 1.0}：前两条没有漏进去
```

**知识点：**所有路径上的清理（Cleanup on Every Path）
