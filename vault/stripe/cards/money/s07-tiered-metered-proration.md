---
id: s07-tiered-metered-proration
node: stripe.money
type: qa
---

## Q
Billing 题里的 "graduated" 阶梯和 "volume" 阶梯有什么区别（个人所得税 vs 批发价）？题面不说清楚时默认用哪种？累进阶梯怎么写、免费额度和按天数比例分摊（proration）各自的坑在哪？

## A
**为什么考**：Billing 团队的题直接对应 Stripe 的定价模型。

**两种阶梯，务必分清**：

| | Graduated（累进） | Volume（整量） |
|---|---|---|
| 含义 | 每一档的量按该档单价计费，逐档累加 | 总量落在哪一档，**全部**按该档单价 |
| 类比 | 个人所得税 | 批发价 |
| 1200 单位，0–1000 @ 10¢，1000+ @ 5¢ | 1000×10 + 200×5 = 11000 | 1200×5 = 6000 |

题面不说清楚时，**"tiered"/"graduated"→ 累进，"volume"→ 整量**，并在注释里写明假设。

**累进的标准写法**（左闭右闭的整数档，`upper=None` 表示无上界）：

```python
def graduated(units, tiers):          # tiers = [(upper, price_per_unit), ...]
    total, prev = 0, 0
    for upper, price in tiers:
        if units <= prev:
            break
        take = (min(units, upper) - prev) if upper is not None else (units - prev)
        total += take * price
        prev = upper if upper is not None else units
    return total
```

**included allowance（免费额度）**：先减额度再进阶梯，`units = max(0, used - included)`。

**proration（按比例分摊）**：中途换套餐时，两段各按**天数占比**计费。
坑在于"天数"的定义：是 `(end - start).days` 还是 `+1`（含首含尾）？
题面通常在样例里透露 —— 用样例反推，别猜。
