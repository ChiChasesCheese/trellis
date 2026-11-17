---
id: testing-testable-design-time-in-context
node: testing.testable-design
type: qa
step: 2
---
## Q
支付表单要校验卡的有效期年份不超过「当前年份 + 20」。校验函数里直接调用 `date.today().year`，写出的测试为什么今年通过、几年后全部变红？该怎么改？

## A
**「现在」由调用方传入，规则函数只做计算**

- **隐藏的输入**：函数的结果取决于当前日期，但签名里看不出来；测试里写死的年份过几年就是错的；
- **改法**：把 `today` 或 `current_year` 作为参数；规则函数变成纯函数，同样的输入永远同样的输出；
- **测试要注入「非默认」的年份**：默认值恰好等于真实年份时，把年份写死在代码里的实现也能通过；传入 2040、2031 这样不同的年份，才能证明注入的值真的被用到了；
- **默认值放在最外层**：入口处 `today = date.today()`，往里一路传下去。

```python
from datetime import date

def expiry_ok(month: int, year: int, today: date, window: int = 20) -> bool:
    if not 1 <= month <= 12: return False
    last_valid = (today.year + window, 12)
    return (today.year, today.month) <= (year, month) <= last_valid

print(expiry_ok(3, 2031, date(2030, 6, 1)))     # True
print(expiry_ok(3, 2031, date(2050, 6, 1)))     # False：只改注入的日期，结果就变，证明 today 被用到
print(expiry_ok(5, 2051, date(2030, 6, 1)))     # False：超出窗口
```

**知识点：**可测的设计（Design for Testability）
