%% trellis:begin %%
# 金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`
*工程实践：健壮性、测试与交付*

能解释为什么金额绝不 float 累加、`Decimal(str(x))` 与 `Decimal(x)` 的区别、`ROUND_HALF_UP` 显式指定，以及 naive 与 aware datetime 混用会抛错。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.numbers|数值：int 大整数、float 精度与 Decimal]]

## Readings
- [[effective-12-data-structures-algorithms|Effective Python 3e · 第 12 章 数据结构与算法]]
- [[pydocs-datetime-module|datetime 模块：日期时间完整参考]]
- [[pydocs-decimal-module|decimal 模块：精确十进制运算]]

## Cards (6)
1. [[money-decimal-exact-vs-float]]
2. [[money-decimal-str-vs-float-ctor]]
3. [[money-naive-aware-datetime-mix-typeerror]]
4. [[money-quantize-rounding-explicit]]
5. [[money-utcnow-deprecated]]
6. [[money-zoneinfo-vs-fixed-timezone]]
%% trellis:end %%

## Notes
