---
nodes:
- iteration.comprehensions
title: PEP 572：赋值表达式（walrus 操作符）
corpus: peps
section: 22-pep-0572
url: https://peps.python.org/pep-0572/
tags:
- canonical
---

# PEP 572：赋值表达式（walrus 操作符）

讲清楚 := 要解决的真实问题和它的作用域陷阱。Rationale 用真实代码库统计说明：程序员为了省一行代码，宁愿重复调用一次 re.match() 或重新做一次模式匹配，也不愿多写一行赋值——walrus 让 (match := re.match(data)) 这类写法可以直接嵌进表达式里，避免重复计算。这篇要重点带走的是 Scope of the target 一节：赋值表达式不引入新作用域，在推导式里使用时，目标变量会绑定到推导式的外层作用域而不是推导式自己的隐式函数作用域——这与推导式变量本身的作用域规则（PEP 289）形成鲜明对比，是“列表推导式有没有自己的作用域”这个问题最容易被问倒的例外情况，面试里常被用来考察是否真的理解推导式的作用域边界。
