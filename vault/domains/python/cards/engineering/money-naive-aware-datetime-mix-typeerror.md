---
id: money-naive-aware-datetime-mix-typeerror
node: engineering.money-time
type: qa
source: python-docs
---
## Q
把一个不带时区信息的 `datetime`（naive）和一个带时区信息的 `datetime`（aware）相减或比较，会发生什么？

## A
naive 对象不携带时区信息，无法定位自己相对世界时间的位置；aware 对象携带 `tzinfo`（且其 `utcoffset()` 不返回 `None`），能精确定位到某一时刻。两者相减或比较时，只要一个 naive 一个 aware，就会抛出 `TypeError`；只有两者都是 naive，或都是 aware，运算才被允许。这是 Python 用类型系统强迫你先统一时区语义再做时间运算。
