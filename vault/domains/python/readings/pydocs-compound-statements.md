---
nodes:
- iteration.context-managers
- runtime.exceptions
- types.protocols-generics
- types.basics
title: 复合语句语法参考：with / try / 泛型参数
corpus: python-docs
section: 04-compound-stmts
url: https://docs.python.org/3/reference/compound_stmts.html
tags:
- canonical
---

# 复合语句语法参考：with / try / 泛型参数

这是 if/while/for/try/with/match/函数与类定义等所有复合语句的权威语法定义，最值得精读的是三处：with 语句给出了逐字节码级别的执行步骤，明确了 __exit__() 返回真值会把异常吞掉、返回假值或 None 时异常会重新抛出；try 语句区分了 except、except*（异常组）、else（无异常时才执行）、finally（无论如何都执行）四个子句各自的时机；3.12 引入的类型参数列表语法（def f[T](x: T) -> T、class Box[T]）展示了泛型的现代写法。读这一章的目的不是背语法，而是把"with 到底保证了什么""try/else 和直接写在 try 里有什么区别"这类问题的答案钉死在权威定义上。
