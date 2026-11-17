---
id: debugging-prevent-expected-by-hand
node: debugging.prevent
type: qa
step: 3
---
## Q
贷款申请同时违反了两条规则：金额是负数，并且超过了余额。规格规定先报哪一个？写回归测试时，期望值能从程序当前的输出里抄吗？

## A
**期望值由规格决定、自己手写；测试要用“同时违反两条”的输入**

- **只违反一条的输入测不出顺序**：两条规则谁先检查，得用同时违反两条的输入才看得到；
- **期望值从规格来**：抄当前输出，等于让缺陷给自己出答案，测试会永远是绿的；
- **让测试变绿不等于修了**：为了变绿去改期望值（尤其是让智能体自己改测试）要拒绝，除非规格确实变了；
- **验证测试有效**：故意把检查顺序换一下，测试必须变红；不会红的测试不防任何事；
- **一条测试盯一个行为**：用例名写成规格的话（`test_invalid_amount_reported_before_balance`）。

```python
def check_a(amount, balance):                    # 规格：先查金额格式，再查余额
    if amount <= 0: return "bad_amount"
    if amount > balance: return "insufficient"
    return "ok"

def check_b(amount, balance):                    # 顺序被人改反
    if amount > balance: return "insufficient"
    if amount <= 0: return "bad_amount"
    return "ok"

for f in (check_a, check_b):
    print(f.__name__, f(-5, -10) == "bad_amount")   # 手写的期望：先报金额
# check_a True / check_b False：只有同时违反两条，才分得出这两个版本
```

**知识点：**防止复发（Prevent Recurrence）
