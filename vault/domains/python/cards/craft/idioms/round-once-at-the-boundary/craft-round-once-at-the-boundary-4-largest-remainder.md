---
id: craft-round-once-at-the-boundary-4-largest-remainder
node: craft.idioms.round-once-at-the-boundary
type: qa
step: 4
---
## Q
**在边界处取整一次 · 各份取整后的和不等于总额，余数怎么分**｜写法

100 分三个人均摊，每人 33.33 分，各自取整是 33、33、33，加起来 99，丢了 1 分；10 分六等分，每份 1.67，取整后每人 2，加起来 12，凭空多出 2 分。分账怎么保证加总一定等于总额？

## A
**要点。** 最大余数法（largest remainder method）：先把每份**向下取整**，算出被取整丢掉的最小单位个数 `leftover`，再按「小数部分」从大到小，每人补一个最小单位，补满为止。小数部分相同的，按固定顺序（参与人在列表里的先后）补，不随机。这样总和必为总额，规则确定，同样输入永远同样输出，可以对着账单解释。

```python
def naive_round(amount: int, weights: list[int]) -> list[int]:
    total = sum(weights)
    return [round(amount * w / total) for w in weights]      # 每份各自取整

def largest_remainder(amount: int, weights: list[int]) -> list[int]:
    total = sum(weights)
    exact = [Fraction(amount * w, total) for w in weights]
    floors = [e.numerator // e.denominator for e in exact]    # 先全部向下取整
    leftover = amount - sum(floors)                           # 损失的最小单位个数
    # 小数部分大的优先补一分；相同时按位置靠前，可复现
    order = sorted(range(len(weights)), key=lambda i: (-(exact[i] - floors[i]), i))
    for i in order[:leftover]:
        floors[i] += 1
    return floors

print("100 分三等分 朴素取整:", naive_round(100, [1, 1, 1]), "和 =", sum(naive_round(100, [1, 1, 1])))
print("100 分三等分 最大余数:", largest_remainder(100, [1, 1, 1]))
print("10 分六等分   朴素取整:", naive_round(10, [1] * 6), "和 =", sum(naive_round(10, [1] * 6)), "(多出来的钱)")
print("10 分六等分   最大余数:", largest_remainder(10, [1] * 6), "和 =", sum(largest_remainder(10, [1] * 6)))
print("输入顺序决定谁多一分，但同样输入永远同样结果:", largest_remainder(100, [1, 1, 1]) == largest_remainder(100, [1, 1, 1]))
```

实际输出：

```
100 分三等分 朴素取整: [33, 33, 33] 和 = 99
100 分三等分 最大余数: [34, 33, 33]
10 分六等分   朴素取整: [2, 2, 2, 2, 2, 2] 和 = 12 (多出来的钱)
10 分六等分   最大余数: [2, 2, 2, 2, 1, 1] 和 = 10
输入顺序决定谁多一分，但同样输入永远同样结果: True
```

**变化。** 放大到分账、分润、对账系统，这条规则就是「守恒」：钱只能在账户之间搬运，不能凭空多少。余数分配规则必须**确定并可复现**，因为对账会重放同一笔分账，两次结果不同就对不上；也要写进文档，因为分给谁多一分是用户能看到的。

**代价。** 个别人比「理论公平」多 1 分或少 1 分，不可避免；这是守恒的代价。取整位置要在分账函数内一次完成，不要先取整、再回头修补差额。

**信号。** 一笔钱按比例分成多份、且每份要是整数；账单行加总必须等于总额。
