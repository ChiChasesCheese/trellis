---
id: python-functions-template-method
node: python.first-class-functions
type: qa
step: 5
tags: [grown]
---
## Q
模板方法模式（Template Method）通常用基类固定算法骨架、子类覆盖钩子方法实现，这个骨架能用一个普通函数替代类继承吗？

## A
可以，把“钩子”作为参数传入骨架函数，而不是让子类覆盖方法：
```python
def process_order(order, validate, charge):
    if not validate(order):
        raise ValueError("invalid order")
    charge(order)
    return "done"
```
骨架（先校验再扣费的顺序）固定在函数体里，`validate`/`charge` 这两个“钩子”作为可调用对象注入——不需要一个抽象基类和一堆子类。当骨架本身需要在子步骤之间共享大量状态（不只是参数传递），或者钩子彼此有复杂的组合关系时，继承加覆盖方法依然更自然。
