---
id: review-ai-missed-boundary
node: review.ai-code
type: qa
step: 2
---
## Q
AI 写的 `top(xs, k)` 用 `sorted(xs)[-k:]` 取最大的 k 个，示例都对。评审时你会拿什么输入去试它？

## A
**AI 的代码擅长“快乐路径”，评审要专门去试边界：空、零、一个、重复、越界**

- **`k = 0`**：`xs[-0:]` 等于 `xs[0:]`，返回整个列表，而不是空列表；
- **`k` 大于长度**：切片不会报错，悄悄返回全部，可能是想要的也可能不是，要对照规格；
- **空输入**：`max([])` 抛 `ValueError`，除法抛 `ZeroDivisionError`；
- **重复值与并列**：最大的两个相等时，谁排前面？
- **评审时的做法**：为每个边界各写一条测试，期望值按规格自己手写，而不是看着 AI 的输出抄。

```python
def top(xs, k):
    return sorted(xs)[-k:]                  # AI 版本：示例里 k >= 1 都对

print(top([3, 1, 2], 2))                    # [2, 3]
print(top([3, 1, 2], 0))                    # [1, 2, 3]：k=0 应该是 []
print(top([3, 1, 2], 10), top([], 3))       # [1, 2, 3] []

def top_fixed(xs, k):
    return sorted(xs)[len(xs) - k:] if k > 0 else []   # 显式处理 k = 0

assert top_fixed([3, 1, 2], 0) == []
```

**知识点：**评审 AI 生成的代码（Reviewing AI Code）
