---
nodes: [problems.foundations.unique-id-generator]
url: https://www.rfc-editor.org/rfc/rfc9562.html
---
# RFC 9562 — Universally Unique IDentifiers (UUIDs)

值得读：IETF 标准文档一手定义了 UUIDv7 的精确位布局——48 位毫秒级时间戳、4 位
版本位、12 位 `rand_a`、2 位变体位、62 位 `rand_b`，并给出了用这些随机位实现同
毫秒内单调性的几种方法，明确指出相比 UUIDv4 的改进在于自然的时间排序和更好的
数据库索引局部性。本题解用这份规范里的位布局，独立算出了本设计场景下纯随机模式
的生日悖论碰撞概率，量化论证"即使不用计数器模式，UUIDv7 在这个规模下也不会因为
随机性本身撞车"，这个数字规范原文没有给出。
