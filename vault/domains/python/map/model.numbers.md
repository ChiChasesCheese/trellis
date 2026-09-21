%% trellis:begin %%
# 数值：int 大整数、float 精度与 Decimal
*对象模型：名字、对象与数据模型（data model）*

掌握 int 任意精度、float 是 IEEE 754 双精度导致 `0.1+0.2 != 0.3`、金额为什么用 `Decimal` 或整数分并显式指定舍入，以及 `//` 和 `%` 对负数的定义。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]]

## Readings
- [[py-pydocs-data-model|数据模型（Data Model）参考]]
- [[pydocs-builtin-types|内建类型（Built-in Types）完整参考]]
- [[pydocs-decimal-module|decimal 模块：精确十进制运算]]
- [[pydocs-design-faq|设计与历史 FAQ：CPython 内部实现精选问答]]
- [[pydocs-floating-point-issues|浮点数运算：问题与限制]]
- [[pydocs-programming-faq|编程 FAQ：作用域、参数与可变性高频坑]]

## Cards (6)
1. [[decimal-context-tunable-precision-rounding]]
2. [[decimal-vs-float-for-money]]
3. [[float-53-bit-mantissa-and-repr-shortest]]
4. [[floor-division-negative-numbers]]
5. [[int-arbitrary-precision]]
6. [[why-float-01-plus-02-not-03]]
%% trellis:end %%

## Notes
