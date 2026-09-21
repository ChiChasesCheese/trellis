---
id: money-decimal-str-vs-float-ctor
node: engineering.money-time
type: qa
source: python-docs
---
## Q
`Decimal(str(1.1))` 和 `Decimal(1.1)` 为什么结果不一样？

## A
`Decimal(1.1)` 是对 `float` 值做无损转换，而 `1.1` 在二进制浮点里本身就不精确，所以转换出的是那个二进制近似值的完整展开（一长串 `1.100000000000000088817841970012523233890533447265625`）。`Decimal(str(1.1))` 先把 `float` 格式化成人类看到的 `'1.1'` 字符串，再按该字符串构造，得到的就是精确的 `Decimal('1.1')`。要保留用户输入的原始精度，应从字符串构造，不要直接传 `float`。
