---
nodes:
- runtime.exceptions
title: PEP 3134：异常链与内嵌回溯
corpus: peps
section: 20-pep-3134
url: https://peps.python.org/pep-3134/
tags:
- canonical
---

# PEP 3134：异常链与内嵌回溯

解释 raise ... from 和 __context__/__cause__/__traceback__ 三个属性从何而来、各解决什么问题。在这之前，处理异常 A 时如果又抛出异常 B，A 会被直接丢弃，调试时看不到最初的错误——这就是 __context__ 要解决的隐式链（异常处理过程中意外发生了另一个异常）。__cause__ 解决的是另一种场景：故意重新抛出或转译异常类型时，显式记录“这是由谁引起的”。文档还讨论了命名取舍——__cause__ 表示明确因果，__context__ 表示“发生在处理另一个异常的上下文中”，语义比单纯的时间先后更精确。带走的要点：外层看到的异常永远是最近抛出的那个，回溯按从旧到新排列，这与其它语言（Java/Ruby 直接丢弃原异常）的做法形成对比，是回答“except 里再抛异常，原来的信息去哪了”的标准答案。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-3134/)

## Archived copy
![[peps-pep3134-exception-chaining-clip]]
%% trellis:end %%
