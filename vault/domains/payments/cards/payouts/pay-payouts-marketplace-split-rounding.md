---
id: pay-payouts-marketplace-split-rounding
node: payouts.marketplace-split
type: qa
step: 2
---
## Q
订单金额按比例拆给多方（卖家、平台、推广者）时，最小货币单位的整数无法整除，怎么保证各方份额之和恰好等于总额？

## A
**问题**：订单 USD 100.01，即 10001 个美分，平台佣金 12.5%。精确值是卖家 8750.875 分、平台 1250.125 分，分不能有小数。如果每方各自四舍五入，三方平分 100 分时就会各得 33，合计 99，凭空少了 1 分；这一分不属于任何人，对账时就成了差异。

**做法：最大余数法（largest remainder）**
1. 每方先取整数部分（向下取整）。
2. 算出还差几分：总额减各方整数部分之和。
3. 把差的几分，按"小数部分最大"的顺序依次补给各方。

保证份额之和**严格等于**总额，每方与精确值相差不到一分。

```python
def split(total: int, weights: list[int]) -> list[int]:
    s = sum(weights)
    base = [total * w // s for w in weights]
    rest = total - sum(base)
    order = sorted(range(len(weights)), key=lambda i: -(total * weights[i] % s))
    for i in order[:rest]:
        base[i] += 1
    return base

print(split(10001, [875, 125]))
print(split(100, [1, 1, 1]))
```
实际输出：
```
[8751, 1250]
[34, 33, 33]
```
10001 拆成卖家 8751、平台 1250，合计 10001；100 分三等分得 34、33、33，合计 100。

**要点**：全程整数运算，没有浮点；"多出来的一分给谁"必须有确定的规则（余数最大者，平局按固定顺序），否则不同服务算出不同结果，会产生对账差异。
