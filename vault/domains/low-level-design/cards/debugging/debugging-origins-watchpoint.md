---
id: debugging-origins-watchpoint
node: debugging.failure-origins
type: qa
step: 2
---
## Q
购物车合计在结算时出现负数，但代码里有十几处会改 `total`。逐处读代码太慢，怎么让程序自己告诉你是谁写了第一个错值？

## A
**在“写入点”设观察点：值一变坏就当场停下，栈里就是真凶**

- **把属性包成 `@property` 加 setter**：每次赋值都经过它，在里面检查不变量（合计不能为负），违反就抛异常；
- **异常的栈指向写入者**：不是后面读到负数的那一行，而是最先把它写成负数的那一行；
- **失败位置 ≠ 出错位置**：读到负数、打印负数、把负数写进数据库，都是下游；观察点要放在值产生的地方；
- **用完就撤**：它是诊断手段，查明后可以留成永久的断言（见防止复发那一张），也可以删掉；
- **调试器里的等价做法**：`pdb` 的条件断点 `b 文件:行号, total < 0`，或在 setter 里 `breakpoint()`。

```python
import traceback

class Cart:
    def __init__(self): self._total = 100
    @property
    def total(self): return self._total
    @total.setter
    def total(self, v):
        if v < 0: raise ValueError(f"total={v}")     # 观察点
        self._total = v

def apply_coupon(cart): cart.total -= 150            # 真凶：扣得比合计多
try: apply_coupon(Cart())
except ValueError as e:
    print(e, [f.name for f in traceback.extract_tb(e.__traceback__)])
```

栈里倒数第二层 `apply_coupon` 就是写入者。

**知识点：**追踪失败源头（Tracking Failure Origins）
