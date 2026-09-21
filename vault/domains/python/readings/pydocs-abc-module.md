---
nodes:
- classes.abc-protocols
title: abc 模块：抽象基类机制
corpus: python-docs
section: 50-abc
url: https://docs.python.org/3/library/abc.html
tags:
- canonical
---

# abc 模块：抽象基类机制

abc 模块提供了实现抽象基类的底层机制：继承 ABC（或使用 ABCMeta 元类）并用 @abstractmethod 标记的方法，会阻止这个类被直接实例化，必须等到子类把所有抽象方法都实现了才能创建实例，这是 Python 里强制子类必须实现某些方法的官方手段，比只在文档里写请子类实现这个方法的君子协定可靠得多。文档还讲了 register() 方法可以把一个完全不相关继承链的类认证为某个 ABC 的虚拟子类，使 isinstance 检查通过，但注意虚拟子类不会继承 ABC 的具体实现代码。abc 和 collections.abc 是配套关系：前者是造抽象基类的底层机制，后者是用这套机制预先造好的一批容器相关抽象基类，日常写代码大多数时候只需要用后者提供的现成 ABC，少数情况才需要自己用 abc 定义新的抽象基类。
