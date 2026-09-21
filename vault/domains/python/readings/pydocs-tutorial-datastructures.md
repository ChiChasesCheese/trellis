---
nodes:
- iteration.comprehensions
- model.sequences
- performance.containers
title: Python 教程第 5 章：数据结构
corpus: python-docs
section: 17-datastructures
url: https://docs.python.org/3/tutorial/datastructures.html
tags:
- canonical
---

# Python 教程第 5 章：数据结构

官方教程系统梳理列表、元组、集合、字典的基本用法，其中两点特别值得注意：一是明确指出用 list 当队列（在头部插入/弹出）效率低下，应该用 collections.deque，这是为什么容器选型很重要最直接的官方例证；二是列表推导式和嵌套推导式的写法与可读性边界，文档建议超过两层嵌套就该拆成显式循环。5.6 节循环技巧给出了 zip()、enumerate()、sorted() 组合使用的惯用写法，是写出 Pythonic 循环代码的基础。5.8 节讲了序列之间比较（如元组、列表比较）按字典序逐元素比较的规则。这是数据结构选型和推导式使用边界最好的入门读物，适合在深入 CPython 内部实现细节之前先建立正确的使用直觉。
