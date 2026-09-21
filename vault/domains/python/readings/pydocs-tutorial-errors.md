---
nodes:
- runtime.exceptions
title: Python 教程第 8 章：错误与异常
corpus: python-docs
section: 16-errors
url: https://docs.python.org/3/tutorial/errors.html
tags:
- canonical
---

# Python 教程第 8 章：错误与异常

官方教程对异常处理的入门讲解，用递进的例子讲清 try/except/else/finally 的完整语义：else 子句只有在 try 块没有抛出异常时才执行，适合放确认成功后才做的代码；finally 无论是否发生异常都会执行，常用来做资源清理。异常链一节讲了 raise NewError from original_exc 如何显式关联两个异常（保留原始异常的追踪信息，而不是丢失上下文），这在把底层异常包装成业务异常时很关键。8.10 节介绍了较新的 add_note() 方法，能在不改变异常类型的前提下给异常追加调试信息。这是异常处理体系最好的入口文章，把术语和心智模型讲清楚之后，再去看 Built-in Exceptions 参考文档会更容易理解异常继承体系的设计意图。
