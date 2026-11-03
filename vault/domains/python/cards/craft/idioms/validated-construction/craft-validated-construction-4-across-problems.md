---
id: craft-validated-construction-4-across-problems
node: craft.idioms.validated-construction
type: qa
step: 4
---
## Q
**构造即校验 · 通配符、阶梯费率、购物车行里同一个 `__post_init__`**｜写法

消息订阅的主题通配符、计费的阶梯费率、折扣引擎的购物车行、外卖配送的高峰时段，这四处都在 `__post_init__` 里校验。它们各校验了什么，哪些部分一样？

## A
**要点。** 一样的是结构：数据类字段声明 → `__post_init__` 里检查 → 违反时抛领域异常。不同的是检查的**形状**，从单字段一路到跨元素的关系。

```python
# amz-discount-engine.LineItem：单个字段的范围
if self.qty <= 0 or self.unit_cents < 0:
    raise InvalidCartError(f"{self.sku}: 数量必须为正、单价不能为负")

# pub-sub.TopicPattern：字符串拆开后的结构（# 只能在末尾）
segments = self.pattern.split(".")
if not self.pattern or any(s == "" for s in segments):
    raise InvalidPatternError(f"empty segment in pattern {self.pattern!r}")
if any(s == "#" for s in segments[:-1]):
    raise InvalidPatternError(f"'#' must be the last segment: {self.pattern!r}")

# billing-tax-engine.Tiered：序列的整体性质（严格递增，末档不封顶）
ok = (bool(uppers) and uppers[-1] is None
      and all(a < b for a, b in zip(uppers[:-2], uppers[1:-1])))
if not ok:
    raise InvalidRuleSet(f"{self.rule_id}: 阶梯上限必须严格递增，且最后一档为 None")
```

外卖的 `PayPlan` 再往前一步：校验费率集合恰好覆盖每个状态、高峰窗口两两不重叠，同时把字典拷成只读视图（见第 2 张卡）。

**代价。** 图像流水线里 `Crop` 与 `Resize` 各写了一份几乎相同的「必须是正整数」，没有共享。两份时重复比抽象更清楚；三份以上、或者要保证报错措辞统一，再抽成一个小函数在 `__post_init__` 里调用。描述符（descriptor）对冻结数据类并不顺手，一般不值得。

**见于。** image-transform-pipeline、dasher-payout、billing-tax-engine、amz-discount-engine、pub-sub。

**信号。** 一个值对象带着「必须满足某条件才有意义」的字段，且会被多处创建。
