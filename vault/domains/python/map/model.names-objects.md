%% trellis:begin %%
# 名字绑定、对象身份与 `is` vs `==`
*对象模型：名字、对象与数据模型（data model）*

理解变量是对对象的引用而非容器，`id()`/`is` 比较身份、`==` 调用 `__eq__` 比较值，以及小整数与短字符串驻留（interning）为何只是实现细节。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]], [[domains/python/map/model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]], [[domains/python/map/functions.scope-closure|作用域（LEGB）、闭包与 `nonlocal`]], [[domains/python/map/memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]]

## Readings
- [[cpy-string-interning|字符串驻留与不朽对象：is 比较为什么能又快又准]]
- [[cpyint-05-objects-types|CPython Internals · 对象与类型]]
- [[fluent-06-references-mutability|Fluent Python 2e · 第 6 章 对象引用、可变性与垃圾回收]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]

## Drills
- [[model-predict-identity-and-aliasing|Drill：六段代码，逐段预测输出并解释机制]]

## Cards (6)
1. [[dynamic-string-interning-mechanism]]
2. [[elevator-pitch-is-vs-eq]]
3. [[interning-is-implementation-detail]]
4. [[is-vs-eq-identity-value]]
5. [[runtime-concat-breaks-is-comparison]]
6. [[string-interning-singleton-count]]
%% trellis:end %%

## Notes
