%% trellis:begin %%
# 运算符重载：`__add__`/`__radd__`、就地运算符与比较运算
*类、协议与元编程*

理解二元运算符的分派规则（先左操作数、返回 `NotImplemented` 再试反向方法）、`__iadd__` 缺省时退化为 `__add__`，以及比较运算符的反射对应关系。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]]

## Readings
- [[fluent-16-operator-overloading|Fluent Python 2e · 第 16 章 运算符重载]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]

## Drills
- [[classes-design-a-money-value-object|Drill：写一个不可变 `Money` 值对象，再用描述符复用校验]]
- [[model-predict-identity-and-aliasing|Drill：六段代码，逐段预测输出并解释机制]]

## Cards (6)
1. [[binary-op-return-notimplemented-not-raise]]
2. [[comparison-vs-arithmetic-reflection-naming]]
3. [[iadd-fallback-to-add-radd]]
4. [[iadd-tuple-of-list-partial-mutation-trap]]
5. [[index-dunder-for-int-conversion]]
6. [[radd-dispatch-conditions]]
%% trellis:end %%

## Notes
