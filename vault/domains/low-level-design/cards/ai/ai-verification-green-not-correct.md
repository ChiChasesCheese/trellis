---
id: ai-verification-green-not-correct
node: ai.verification
type: qa
step: 1
---
## Q
智能体改完代码，公开测试全绿，类型检查也过了。为什么这还不能说明实现满足合同？

## A
**绿灯只说明测过的点没坏**

- **测试**：只覆盖写测试的人想到的输入。公开测试多是合同里的示例加几条冒烟，缺陷常在边界和失败路径上，那里它们不去；
- **类型检查**：看类型对不对得上，不看逻辑。`<` 写成 `<=`，类型一模一样；
- **“看起来对”**：顺着智能体的思路读代码，会和它一起漏掉同一处；
- **做法**：合同每条规则至少一个断言，边界取前一格、恰好、后一格三点；失败路径和并发自己补；说“全修好了”的话不算证据，测试输出才算。

```python
def allowed(used: int, limit: int) -> bool:
    return used <= limit            # 合同：已用满 limit 次就拒绝，应为 used < limit

def public_tests():                 # 合同里的两个示例
    assert allowed(0, 10)
    assert not allowed(11, 10)

def boundary_tests():
    assert not allowed(10, 10)      # 恰好满额

public_tests(); print("public: green")
try: boundary_tests()
except AssertionError: print("boundary: red")
```

<details class="pt"><summary>延伸</summary>

换成 `used < limit` 之后，两组测试都绿。边界测试不是给这一次改动写的，它是留给下一次改动的：以后任何人（包括智能体）再动这个函数，它会在第一时间变红。

</details>

**知识点：**验证输出（Verification）
