%% trellis:begin %%
# 浅拷贝、深拷贝与切片复制
*对象模型：名字、对象与数据模型（data model）*

理解 `copy.copy`、切片、`list()` 只复制一层，`copy.deepcopy` 递归复制并处理环，以及什么时候别名反而是想要的。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]]

## Readings
- [[fluent-06-references-mutability|Fluent Python 2e · 第 6 章 对象引用、可变性与垃圾回收]]
- [[pydocs-copy-module|copy 模块：浅拷贝与深拷贝]]
- [[pydocs-programming-faq|编程 FAQ：作用域、参数与可变性高频坑]]

## Drills
- [[model-predict-identity-and-aliasing|Drill：六段代码，逐段预测输出并解释机制]]

## Cards (6)
1. [[copy-method-vs-copy-copy-subclass]]
2. [[copy-module-skips-runtime-singletons]]
3. [[custom-copy-dunder-methods]]
4. [[deepcopy-memo-breaks-recursive-reference]]
5. [[shallow-copy-nested-list-pitfall]]
6. [[shallow-vs-deep-copy-definition]]
%% trellis:end %%

## Notes
