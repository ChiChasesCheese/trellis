---
nodes:
- iteration.iterator-protocol
- iteration.generators
- iteration.itertools
- functions.functools
- functions.first-class
title: 函数式编程 HOWTO
corpus: python-docs
section: 10-functional
url: https://docs.python.org/3/howto/functional.html
tags:
- canonical
---

# 函数式编程 HOWTO

这篇 HOWTO 把 Python 里函数式的那一面串了起来：可迭代对象（iterable）和迭代器（iterator）的区别、生成器表达式与列表推导式的内存差异（前者惰性、后者一次性物化）、yield 如何让函数变成可暂停的生成器工厂、send() 如何往生成器里塞值。中段系统介绍了 itertools 模块的工具分类（创建新迭代器、对元素调用函数、筛选元素、组合数学函数、分组），以及 functools 模块里 reduce、partial、lru_cache 等高阶函数工具。文章反复强调函数式风格的好处：更容易做形式化证明、更容易做单元测试（无副作用的小函数易于隔离验证）、组合性更强。这是把迭代器/生成器/高阶函数这几块知识串成一条线的最佳读物，读完再去看具体模块的参考文档会容易得多。
