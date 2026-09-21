---
id: dict-data-layout-three-parts
node: memory.object-size
type: cloze
source: cpython-internals
---
CPython 的 dict 对象由三部分组成：{{c1::dictobject 结构体本身}}、{{c2::一个 dict-keys 对象（存 key 及其 hash 值）}}、{{c3::一个 values 数组（按位置对应存 value）}}；把 key 表和 value 数组分开存放的设计叫「分裂表」（split table）。
