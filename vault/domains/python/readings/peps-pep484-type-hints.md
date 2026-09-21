---
nodes:
- types.basics
- types.gradual-typing
title: PEP 484：类型提示（Type Hints）的奠基文档
corpus: peps
section: 13-pep-0484
url: https://peps.python.org/pep-0484/
tags:
- canonical
---

# PEP 484：类型提示（Type Hints）的奠基文档

这是整个 typing 生态的起点，讲清楚两个常被面试问到的边界：一是类型注解在运行时不做任何检查（no type checking happens at runtime），它们只是存在 __annotations__ 里的元数据，真正的检查由 mypy 这类离线工具完成；二是引入 Any 类型，它与所有类型双向兼容（consistent with all types），这正是“渐进式类型”（gradual typing）思想的核心——允许代码部分标注、部分不标注地混用。文档还说明了类型提示语法为什么用方括号（Sequence[int]）而不引入新语法：靠 __getitem__ 在元类上的实现，对运行时零侵入。读完能回答“类型提示到底能不能防住类型错误”“Any 和不标注有什么区别”这两个高频追问，也是理解后续几乎所有 typing 相关 PEP 的前提。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0484/)

## Archived copy
![[peps-pep484-type-hints-clip]]
%% trellis:end %%
