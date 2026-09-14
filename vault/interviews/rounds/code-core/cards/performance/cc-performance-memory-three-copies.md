---
id: cc-performance-memory-three-copies
node: performance.memory
type: qa
---
## Q
A solution reads 10^5 users plus 10^5 events, keeps the parsed row objects, builds every output string up front, and sorts with `key=`. Peak RSS is 282 MB against a 256 MB budget. Name the changes.

## A
**Stop holding three copies of the same data.**

- Keep the raw line or one compact tuple per record — not parsed objects *and* rendered strings.
- Format lazily: sort tuples of `(sort keys…, payload)` and render only while writing.
- Drop `key=` where the tuple already sorts correctly ([[cc-performance-memory-sort-key-cost]]).
- Give any record class `__slots__`, and stream output with `write` instead of accumulating one giant list.

Measured on a real problem: 282 MB → 197 MB with exactly these four changes and no algorithmic change at all.

## Q zh
一个方案读入 10^5 个用户加 10^5 个事件，保留解析后的行对象，提前构造好全部输出字符串，并用 `key=` 排序。峰值 RSS 是 282 MB，而预算是 256 MB。说出要改什么。

## A zh
**别再同时持有同一份数据的三个副本。**

- 每条记录只留原始行或一个紧凑 tuple —— 不要既留解析后的对象**又**留渲染好的字符串。
- 延迟格式化：排序 `(排序键…, 载荷)` 的 tuple，只在写出时渲染。
- 元组本身就能正确排序时就去掉 `key=`（[[cc-performance-memory-sort-key-cost]]）。
- 给记录类加 `__slots__`，输出用 `write` 流式写出，而不是攒成一个巨大的 list。

真实题目上的实测：仅这四处改动、算法一字未动，282 MB → 197 MB。
