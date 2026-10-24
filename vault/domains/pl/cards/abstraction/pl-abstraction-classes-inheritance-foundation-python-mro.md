---
id: pl-abstraction-classes-inheritance-foundation-python-mro
node: abstraction.classes-inheritance
type: qa
step: 3
---
## Q
Python 的多继承为什么会有「菱形问题」？方法解析顺序（MRO）和 `super()` 是怎样解决它的？

## A
Python 一个类可以同时继承多个类：`class D(B, C)`。当 `B` 和 `C` 又继承同一个 `A` 时，形成菱形：`D` 调用 `hi()`，该找 `B` 的、`C` 的还是 `A` 的？如果 `B` 和 `C` 各自再调用 `A.hi`，`A` 还会被执行两次。

Python 的答案是给每个类预先算好一个**线性顺序**，叫方法解析顺序（method resolution order, MRO），算法是 C3 线性化：子类一定排在父类前面，且保留你写的父类顺序。查找方法就是沿这个顺序找第一个有该名字的类。`super()` 的意思是「顺序里排在我后面的那个类」。

```python
class A:
    def hi(self): print("A")
class B(A):
    def hi(self): print("B"); super().hi()
class C(A):
    def hi(self): print("C"); super().hi()
class D(B, C):
    def hi(self): print("D"); super().hi()
D().hi()                 # 依次打印 D B C A
print([k.__name__ for k in D.__mro__])   # ['D', 'B', 'C', 'A', 'object']
```

`A` 在顺序里只出现一次，所以只执行一次。`B` 里的 `super().hi()` 没有直接去 `A`，而是去了 `C`，因为 `D` 实例的顺序里 `C` 排在 `B` 后面。如果声明的父类顺序彼此矛盾，C3 无法排出顺序，类定义时就抛 `TypeError`。
