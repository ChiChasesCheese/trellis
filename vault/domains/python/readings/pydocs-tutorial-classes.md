---
nodes:
- classes.pythonic-object
- functions.scope-closure
- classes.inheritance-mro
- classes.attribute-lookup
title: Python 教程第 9 章：类
corpus: python-docs
section: 15-classes
url: https://docs.python.org/3/tutorial/classes.html
tags:
- canonical
---

# Python 教程第 9 章：类

这是官方教程里讲类的入门章节，用最平实的语言建立起类的基本概念：类定义在执行时才创建命名空间，类对象、实例对象、方法对象是三个不同的东西，self 是通过属性查找自动传入的第一个参数而非语法糖。9.6 节私有变量讲清了以双下划线开头的属性名会被 name mangling 成 _ClassName__attr，这是一种防止子类意外覆盖的约定而非真正的访问控制。9.5 节简要介绍了多继承，为理解后面更深入的 MRO 文档打基础。文中反复用作用域和命名空间的例子演示 Python 变量查找规则如何应用到类和函数场景中。这是建立类基础心智模型该读的第一篇，比参考手册更好懂，适合在深入描述符、元类之前先打底。
