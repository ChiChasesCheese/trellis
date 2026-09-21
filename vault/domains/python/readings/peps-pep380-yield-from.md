---
nodes:
- iteration.yield-from
title: PEP 380：yield from 委托子生成器语法
corpus: peps
section: 07-pep-0380
url: https://peps.python.org/pep-0380/
tags:
- canonical
---

# PEP 380：yield from 委托子生成器语法

解决的是“把带 yield 的代码块拆成子函数很难”这个具体痛点：用 for v in g: yield v 只能转发值，一旦子生成器需要正确响应 send()、throw()、close()，手写转发代码极其繁琐且容易漏掉边界情况。yield from 把这套协议转发完整封装：子生成器 yield 的值直接传给调用者，调用者 send() 的值直接转发给子生成器，异常通过 throw() 转发，子生成器用 return value 结束时该值成为 yield from 表达式本身的值（依赖 StopIteration 新增的 value 属性实现）。面试要点是理解形式化语义那段给出的展开代码——本质是一个状态机，处理了正常迭代、send、异常、GeneratorExit 四种路径。这是 async/await 出现之前，Python 协程能够“委托调用”的唯一机制，也是 PEP 492 的直接铺垫。
