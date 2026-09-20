---
id: patterns-factory-method-vs-abstract-factory
node: patterns.creational
type: qa
step: 3
---
## Q
Factory Method 在 Python 里常见的实现形式是什么？它和 Abstract Factory 的区别是什么？

## A
Factory Method 经常就是一个 `classmethod`（比如 `Shape.from_config(cfg)`），或者上一张卡片里那种"字典查表"——只负责创建**一种**产品，通常和调用它的类定义在一起。Abstract Factory 是一组必须配套出现的 Factory Method（`create_button()`、`create_checkbox()` 都属于同一个"主题工厂"，保证造出来的东西风格一致）。

判断标准：只是想让子类或配置决定"造哪一个"，用 Factory Method；需要保证一整套相关对象来自同一个变体（暗色主题的按钮必须配暗色主题的输入框），才需要 Abstract Factory。
