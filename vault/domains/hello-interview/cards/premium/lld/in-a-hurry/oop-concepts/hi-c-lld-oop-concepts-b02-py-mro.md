---
id: hi-c-lld-oop-concepts-b02-py-mro
node: lld.in-a-hurry.oop-concepts.beyond
type: qa
step: 2
---
## Q
**面向对象概念 · Python：多重继承与 MRO**｜拓展 · 加分

Python 的 `super()` 在多重继承里调用的是谁？这对"组合优于继承"有什么启示？

## A
**模式。** 协作式多重继承（cooperative inheritance）与混入（mixin）。

```python
class A:
    def hello(self) -> str:
        return "A"


class Loud(A):
    def hello(self) -> str:
        return super().hello().upper() + "!"


class Polite(A):
    def hello(self) -> str:
        return "please " + super().hello()


class Both(Loud, Polite):
    pass


assert [c.__name__ for c in Both.__mro__] == ["Both", "Loud", "Polite", "A", "object"]
assert Both().hello() == "PLEASE A!"   # Loud 里的 super() 指向 Polite，而不是 A
```
- **底层：** `super()` 按方法解析顺序（MRO，C3 线性化）找"下一个"类，不是"父类"；菱形里 `A` 只被调用一次
- **含义：** 一个类的 `super()` 调用谁，取决于最终子类怎么组合，读代码很难预测
- **何时用混入：** 小而无状态的能力（日志、序列化），每个混入都协作调用 `super()`
- **何时不用：** 有状态或重写同一方法的混入，改用组合
