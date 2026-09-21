%% trellis:begin %%
# 可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）
*对象模型：名字、对象与数据模型（data model）*

掌握可变性如何决定函数参数的副作用、`def f(x, acc=[])` 为什么共享状态、tuple 为什么能做字典键，以及 `+=` 在两类对象上的不同行为。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.names-objects|名字绑定、对象身份与 `is` vs `==`]]

**Unlocks:** [[domains/python/map/model.copy|浅拷贝、深拷贝与切片复制]], [[domains/python/map/model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]], [[domains/python/map/functions.arguments|参数传递：`*args`/`**kwargs`、仅关键字与仅位置参数、默认值求值时机]]

## Readings
- [[fluent-06-references-mutability|Fluent Python 2e · 第 6 章 对象引用、可变性与垃圾回收]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]
- [[pydocs-programming-faq|编程 FAQ：作用域、参数与可变性高频坑]]

## Drills
- [[model-predict-identity-and-aliasing|Drill：六段代码，逐段预测输出并解释机制]]

## Cards (6)
1. [[aliasing-shared-list-mutation]]
2. [[augmented-assign-list-vs-tuple-int]]
3. [[immutable-tuple-with-mutable-element]]
4. [[inplace-mutation-returns-none-convention]]
5. [[mutable-default-argument-trap]]
6. [[pass-by-object-reference-not-by-reference]]
%% trellis:end %%

## Notes
