---
id: cc-performance-memory-object-cost
node: performance.memory
type: cloze
---
On 64-bit CPython an empty `dict` costs about {{c1::64}} bytes (a few hundred once it holds fields), a `tuple` about {{c2::40}} bytes plus 8 per slot, an `int` {{c3::28}} bytes and a one-character `str` about {{c4::50}}. At 10^6 records the *container* choice, not the data, decides whether you fit inside a 256 MB budget.

## zh
在 64 位 CPython 上，空 `dict` 约 {{c1::64}} 字节（装上字段后是几百字节），`tuple` 约 {{c2::40}} 字节加每槽 8 字节，`int` 是 {{c3::28}} 字节，单字符 `str` 约 {{c4::50}} 字节。在 10^6 条记录的规模上，决定你能否塞进 256 MB 预算的是**容器**的选择，不是数据本身。
