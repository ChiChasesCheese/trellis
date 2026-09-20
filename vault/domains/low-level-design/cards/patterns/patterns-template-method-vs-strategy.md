---
id: patterns-template-method-vs-strategy
node: patterns.behavioral
type: qa
step: 5
---
## Q
Template Method 和直接传一个函数相比，继承换来的"骨架复用"什么时候真正值得？

## A
Template Method 把固定顺序的步骤写在基类方法里，只留一两个钩子（hook）给子类覆盖，比如 `PaymentFlow.run()` 固定调用 `validate()` → `charge()` → `confirm()`，子类只重写其中某一步。当只有**一个**钩子要变时，Python 里通常直接给这个固定流程的函数传一个回调参数，比专门声明子类更直接：

```python
def run_payment(charge, amount: int) -> None:
    print("validate")
    charge(amount)
    print("confirm")
```

继承版本值得的场景是：钩子不止一个，而且几个钩子之间要共享状态（写在 `self` 上），传参数会让函数签名爆炸；只有一个钩子、也不需要共享状态时，传函数更简单，不必为每种变体建一个子类。
