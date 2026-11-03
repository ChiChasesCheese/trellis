%% trellis:begin %%
# 金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`
*工程实践：健壮性、测试与交付*

能解释为什么金额绝不 float 累加、`Decimal(str(x))` 与 `Decimal(x)` 的区别、`ROUND_HALF_UP` 显式指定，以及 naive 与 aware datetime 混用会抛错。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.numbers|数值：int 大整数、float 精度与 Decimal]]

**Unlocks:** [[domains/python/map/craft.patterns.injected-clock-three-forms|注入时钟的三种形态：Clock 参数 / 时间戳参数 / tick 步进]], [[domains/python/map/craft.patterns.effective-dated-versions|生效时间版本表：按事件发生时刻取规则（effective-dated lookup）]], [[domains/python/map/craft.patterns.half-open-intervals|区间一律左闭右开：[start, end)]], [[domains/python/map/craft.idioms.money-types|金额类型选型：整数分 / 基点 / Decimal / Fraction]], [[domains/python/map/craft.idioms.round-once-at-the-boundary|取整点：Decimal.quantize、ROUND_HALF_EVEN 与整数四舍五入]], [[domains/python/map/craft.idioms.time-types|时间类型选型：monotonic / aware datetime / 整数时间戳]], [[domains/python/map/craft.architecture.event-time-vs-processing-time|事件时间 vs 处理时间：乱序、重复、迟到的事实]]

## Readings
- [[effective-12-data-structures-algorithms|Effective Python 3e · 第 12 章 数据结构与算法]]
- [[pydocs-datetime-module|datetime 模块：日期时间完整参考]]
- [[pydocs-decimal-module|decimal 模块：精确十进制运算]]

## Drills
- [[engineering-harden-a-payment-script|Drill：把一段收款脚本改成生产可用的版本]]

## Cards (6)
1. [[money-decimal-exact-vs-float]]
2. [[money-decimal-str-vs-float-ctor]]
3. [[money-naive-aware-datetime-mix-typeerror]]
4. [[money-quantize-rounding-explicit]]
5. [[money-utcnow-deprecated]]
6. [[money-zoneinfo-vs-fixed-timezone]]
%% trellis:end %%

## Notes
