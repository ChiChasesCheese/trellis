---
id: fluency-time-float-compare
node: fluency.time-numbers
type: qa
step: 7
---
## Q
汇率换算选路线：要求乘积与最大乘积的差不超过 `1e-5` 才算合格，代码写成 `product == best`；另一处用 `float(s)` 解析汇率，用户传了 `"nan"`、`"1_0"`、`" 5 "`。浮点比较和浮点解析各有什么坑？

## A
**浮点不比相等；解析要拒掉 nan、inf**

- **精确相等不可靠**：`0.1 * 3 == 0.3` 为 `False`，乘积顺序一变末位就变；要写差值：`abs(a - b) <= tol`；
- **容差含边界**：合同说“不超过 1e-5”就是 `<=`，差恰好等于容差仍合格；绝对容差在数值很小时过松，数值很大时退化成精确相等，需要时用 `math.isclose(a, b, rel_tol=…, abs_tol=…)`；
- **`nan` 与比较**：`nan` 和任何数比较（包括它自己）都是 `False`，会悄悄绕过 `lo <= x <= hi` 之类的范围检查，要先 `math.isfinite`；
- **`float()` 比想象的宽**：接受 `"1_0"`、首尾空白、`"nan"`、`"inf"`、`"1e999"`（得 `inf`）和全角数字；边界上先用正则或 `str.isascii()` 卡格式，再转换，再检查有限与范围；
- **整数和浮点混着比**：Python 按精确数值比较，`2**53 + 1 == float(2**53 + 1)` 为 `False`；不要为了比较把大整数转成 `float`，对大整数调 `math.isfinite` 还会 `OverflowError`。

```python
import math

def acceptable(product: float, best: float, tol: float = 1e-5) -> bool:
    return abs(best - product) <= tol          # 含边界：差恰好等于 tol 仍合格

print(0.1 * 3 == 0.3, acceptable(0.1 * 3, 0.3))        # False True
print(float("1_0"), float(" 5 "), float("1e999"))      # 10.0 5.0 inf
x = float("nan")
print(1e-12 <= x <= 1e12, math.isfinite(x))            # False False：必须单独挡
```

**知识点：**时间与数字（Time & Numbers）
