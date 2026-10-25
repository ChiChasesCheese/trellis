---
id: pay-correctness-money-representation-allocation
node: correctness.money-representation
type: qa
step: 4
---
## Q
把 100.00 美元平均分给 3 方，每份 33.33，总和变成 99.99，少了一分钱。怎么做到分摊后总和守恒？

## A
**问题**：按比例分摊（分账、税分摊到商品行、优惠券摊到各商品）时，每份单独舍入后，总和与原金额可能差几分。

**最大余数法**（largest remainder）
1. 每份先向下取整到最小单位：10000 分 ÷ 3 = 3333 余 1。
2. 算出剩余的分数：总额 − 各份之和 = 10000 − 9999 = 1 分。
3. 按"小数部分最大"的顺序，每份多分 1 分，直到分完。

```python
def split(total: int, weights: list[int]) -> list[int]:
    s = sum(weights); base = [total * w // s for w in weights]
    rem = total - sum(base)
    order = sorted(range(len(weights)), key=lambda i: -(total * weights[i] % s))
    for i in order[:rem]: base[i] += 1
    return base
print(split(10000, [1, 1, 1]), sum(split(10000, [1, 1, 1])))
print(split(1000, [50, 30, 20]))
```

实际输出：

```
[3334, 3333, 3333] 10000
[500, 300, 200]
```

**要点**
1. 守恒：各份之和一定等于总额，一分不多不少。
2. 平局要有确定的规则（如先分给排序靠前的一方），保证重算结果一致。
3. 另一种做法：前 n−1 份舍入，最后一份 = 总额 − 其余之和，把误差全放在最后一份。简单，但对最后一方不公平，多次累计会偏向一方。
4. 同样的规则要用于退款的反向分摊，否则退款后各方对不上。
