---
nodes:
- classes.abc-protocols
title: PEP 3119：引入抽象基类（ABC）
corpus: peps
section: 19-pep-3119
url: https://peps.python.org/pep-3119/
tags:
- canonical
---

# PEP 3119：引入抽象基类（ABC）

从面向对象理论的“调用 vs 检视”（invocation vs inspection）二分讲起，说明为什么 Python 需要给“检视对象类型”这件事一个标准做法。在 ABC 之前，判断“这是不是一个可变序列容器”要么查 list 基类、要么查有没有 __getitem__ 方法，两种做法都不准确（一个漏检、一个误检）。ABC 的方案是把这些检视规则标准化并组织进一个类层级，通过重载 isinstance()/issubclass() 让检查同时具备鸭子类型的灵活性和名义继承的可靠性；abc 模块提供元类和 @abstractmethod 装饰器阻止不完整实现被实例化。这是 collections.abc（Iterable、Sized 等）能够 register 虚拟子类的根基，也是理解 PEP 544 Protocol 为什么要在此基础上再补一层结构化检查的前提。
