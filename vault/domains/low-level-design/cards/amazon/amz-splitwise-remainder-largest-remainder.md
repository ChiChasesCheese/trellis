---
id: amz-splitwise-remainder-largest-remainder
node: amazon.amz-splitwise
type: qa
step: 3
tags: [grown]
---
## Q
在分账设计里，100 分钱按 1:1:1 分给三个人，除不尽的余数怎么分？怎么保证加起来恰好等于总额？

## A
先给每人取整数部分，再把剩下的几分钱按「小数余数最大者优先」逐个补上（最大余数法，Largest Remainder）。100 分三等份：基础 33、33、33，余数相同，补 1 分给第一个人，得 34、33、33，总和恰好 100。绝不能每人四舍五入（33+33+33=99，丢一分）也不能用浮点。
```python
def largest_remainder(amount, weights):
    total = sum(weights)
    base = [amount * w // total for w in weights]
    order = sorted(range(len(weights)),
                   key=lambda i: -(amount * weights[i] % total))
    for i in order[:amount - sum(base)]:
        base[i] += 1
    return base
```
