---
nodes:
- functions.scope-closure
- runtime.namespaces-execution
title: 执行模型：命名空间与作用域
corpus: python-docs
section: 02-executionmodel
url: https://docs.python.org/3/reference/executionmodel.html
tags:
- canonical
---

# 执行模型：命名空间与作用域

这一章用权威语言讲清了 Python 变量到底活在哪里：模块、函数体、类体各自是独立的代码块（block），有自己的命名空间；一个名字如果在块内任何位置被赋值，整个块内对它的引用都会被当作局部变量处理，这正是很多人踩过的坑——先用后赋值会抛 UnboundLocalError 而不是退回外层作用域。文中给出了名字解析顺序（LEGB 的官方表述）、global/nonlocal 语句如何改变绑定目标，以及类作用域的特殊之处（方法体访问不到类体里定义的名字，但注解作用域可以）。读完能准确回答"为什么这段代码会报 UnboundLocalError"这类面试常见追问，而不是停留在"闭包能记住外部变量"的表面理解。
