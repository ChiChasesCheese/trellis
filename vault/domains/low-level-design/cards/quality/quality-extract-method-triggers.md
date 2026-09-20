---
id: quality-extract-method-triggers
node: quality.refactoring
type: qa
step: 1
---
## Q
提炼方法（extract method）最常见的两个触发信号是什么？提炼之后一个"组合良好的方法"应该长什么样？

## A
第一个信号：一句给代码块起标题的注释——`# 校验输入并计算折扣` 上面跟着六行代码，说明这几行想成为一个叫 `validate_and_discount` 的方法，用名字取代那句注释。第二个信号：一段你需要停下来仔细读才能看懂在干嘛的代码，或者一段你想复用、想单独写测试的代码——这两种情况都值得单独拎出来命名。

```python
def checkout(cart: Cart) -> None:
    validate(cart)
    total = price_with_discounts(cart)
    charge(cart.customer, total)
```
目标形态是"组合方法"（composed method）：方法体读起来是一串处在同一抽象高度、以意图命名的步骤，读者不需要下钻到实现细节就能看懂整体流程在做什么。
