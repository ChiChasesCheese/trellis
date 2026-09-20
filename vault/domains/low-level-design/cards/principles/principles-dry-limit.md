---
id: principles-dry-limit
node: principles.simplicity
type: qa
step: 4
---
## Q
什么时候应该容忍代码重复，而不是硬套 DRY（Don't Repeat Yourself）原则？

## A
当两段代码看起来相似，但：
- 它们改变的原因不同（各自有不同的"为什么会变"）；
- 它们会随着不同的业务方向各自演化，早晚会分岔；
- 把它们提取到同一个位置，会造出一个虚假的抽象，反而限制了各自本该有的演化空间。

一个常见的例子：两条验证规则一开始看起来一样，但分别属于不同的业务场景，后续会因为不同的需求各自变化。这种情况下"WET"（Write Everything Twice，宁可重复）比强行提取公共代码更好。
