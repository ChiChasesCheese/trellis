---
nodes:
- classes.properties-descriptors
- classes.pythonic-object
- classes.attribute-lookup
title: 描述符指南（Descriptor Guide）
corpus: python-docs
section: 05-descriptor
url: https://docs.python.org/3/howto/descriptor.html
tags:
- canonical
---

# 描述符指南（Descriptor Guide）

描述符是 Python 里最容易被低估的机制：property、classmethod、staticmethod、方法本身，甚至 __slots__，底层全部靠描述符协议（__get__/__set__/__set_name__）实现。这篇官方指南从最简单的"返回常量的描述符"讲到完整的校验器（validator）案例，再到用纯 Python 重新实现 property、classmethod、staticmethod，让你看清这些内建装饰器其实是什么而不是该怎么用。文中还讲清了数据描述符（同时定义 __get__ 和 __set__）优先级高于实例 __dict__，而非数据描述符（只有 __get__，如普通方法）优先级低于实例属性，这正是"为什么实例属性能覆盖方法"的根本原因。读完能用描述符统一实现多个属性共享的校验逻辑，而不是给每个属性写一遍重复的 @property。
