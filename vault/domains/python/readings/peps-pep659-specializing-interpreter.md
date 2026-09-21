---
nodes:
- runtime.adaptive-jit
title: PEP 659：特化自适应解释器（Specializing Adaptive Interpreter）
corpus: peps
section: 04-pep-0659
url: https://peps.python.org/pep-0659/
tags:
- canonical
---

# PEP 659：特化自适应解释器（Specializing Adaptive Interpreter）

这是 3.11 性能飞跃背后“为什么不直接上 JIT，而是先做特化字节码”的原始论证。核心思想：把 LOAD_ATTR、CALL、BINARY_ADD 这类通用指令按运行时实际遇到的类型替换成对应的“特化家族”指令（quickening），失败次数过多就用计数器退化回通用版本；由于特化发生在单条字节码内，反优化不需要处理“区域中途退出”的复杂情况，这是它相对学术界更大粒度优化区域方案的关键优势。要带走的面试要点：这不是 JIT（不生成机器码），而是用内联缓存（inline cache）+ 自适应指令实现的解释器级优化，收益主要来自属性查找、全局变量和函数调用这几类高频操作，实测提速 10%-60%。理解这一层是理解后续 PEP 744 JIT 为什么要建立在它之上的前提。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0659/)

## Archived copy
![[peps-pep659-specializing-interpreter-clip]]
%% trellis:end %%
