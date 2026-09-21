---
nodes:
- functions.scope-closure
- functions.arguments
- model.mutability
- model.copy
- functions.first-class
- model.numbers
title: 编程 FAQ：作用域、参数与可变性高频坑
corpus: python-docs
section: 21-programming
url: https://docs.python.org/3/faq/programming.html
tags:
- canonical
---

# 编程 FAQ：作用域、参数与可变性高频坑

这篇超长 FAQ 精选了 Python 里最容易踩坑的具体场景，逐条给出官方解释：为什么明明变量有值却抛 UnboundLocalError（本地赋值让整个函数体内该名字都被当局部变量）；为什么循环里创建的多个 lambda 最后都返回同一个结果（闭包捕获的是变量本身而非某次循环的值，需要用默认参数 lambda x=x 强制立即求值）；为什么修改列表 y 会连带改了 x（两者是同一对象的两个别名，赋值只是绑定引用不是复制）；如何正确复制一个对象（浅拷贝 vs 深拷贝该怎么选）；参数名前的 / 和 * 分别限定只能按位置传和只能按关键字传；以及 -22 // 10 为什么等于 -3 而不是 -2（floor division 向负无穷取整）。每一条都是面试高频追问题，比自己踩坑总结要系统得多。
