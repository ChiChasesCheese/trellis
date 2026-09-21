---
id: datetime-naive-vs-aware
node: runtime.stdlib-map
type: qa
source: python-docs
---
## Q
`datetime` 对象的 naive（无时区）和 aware（带时区）两种状态有什么区别？为什么两者不能直接混着比较？

## A
aware 对象带着 `tzinfo`，能明确定位到时间轴上的某个绝对时刻，可以和其它 aware 对象无歧义地比较；naive 对象不带时区信息，它到底代表 UTC、本地时区还是别的时区完全由程序自己认定，`datetime` 模块本身并不知道。混合比较 naive 和 aware 对象会直接抛异常，因为没法确定它们是不是同一参考系下的时刻——这也是「时间戳该带时区」这条建议的来源。
