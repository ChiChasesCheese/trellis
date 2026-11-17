---
id: api-specs-intervals
node: api.specs
type: qa
step: 8
---
## Q
规格写“验证码 30 秒内有效”。为什么要改写成 `[0, 30)` 并列出边界例子？代码里该用 `<` 还是 `<=`？

## A
**边界写成区间，并给边界上的例子**

- **自然语言有歧义**：“30 秒内”“不超过”“超过”，端点算不算在内，每个人读法不同；
- **区间记号**：`[0, 30)` 左闭右开，0 秒和 29.9 秒有效，恰好 30 秒已过期；
- **例子**：规格里列出 0、29.9、30、30.1 四个点的结果，实现与测试都对着它；
- **代码**：有效是 `0 <= age < 30`，过期是 `age >= 30`；负年龄（时钟倒退）不在区间里，也无效；
- **日期区间**同理：`[start, end)` 里 end 当天不算，相邻区间首尾相接，不重不漏。

```python
TTL = 30.0

def is_valid(created: float, now: float) -> bool:
    age = now - created
    return 0 <= age < TTL

for age in (0, 29.9, 30, 30.1, -1):
    print(age, is_valid(100.0, 100.0 + age))
```

**知识点：**规格与契约（Specifications）
