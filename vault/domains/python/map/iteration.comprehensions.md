%% trellis:begin %%
# 推导式与 `else` 块：可读性边界与作用域
*迭代器、生成器与上下文管理器*

掌握推导式有自己的作用域、超过两层控制子表达式应改写为循环、`for/else` 与 `try/else` 的语义，以及何时用 `map/filter`。

**Core** — part of the first pass through this subject.

## Readings
- [[effective-01-pythonic-thinking|Effective Python 3e · 第 1 章 Python 化思维]]
- [[fluent-02-sequences|Fluent Python 2e · 第 2 章 序列构成的数组]]
- [[fluent-18-with-match-else|Fluent Python 2e · 第 18 章 with、match 与 else 语句块]]
- [[peps-pep572-assignment-expressions|PEP 572：赋值表达式（walrus 操作符）]]
- [[pydocs-tutorial-datastructures|Python 教程第 5 章：数据结构]]

## Cards (5)
1. [[comprehension-has-own-scope-vs-for-leaks]]
2. [[for-else-vs-try-else-normal-completion]]
3. [[listcomp-desugars-to-nested-for-if-order]]
4. [[map-filter-vs-comprehension-when-to-prefer]]
5. [[nested-comprehension-beyond-two-levels-antipattern]]
%% trellis:end %%

## Notes
