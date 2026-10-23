---
id: hl-javaq-d-q13-say60
node: java-questions.d-memory
type: qa
step: 30
---
## Q
用英文 60 秒回答：How much memory does a Java object take? What's in an object header? How big is `new Integer(5)`, a two-field class, an `int[10]`?

## A
结构：12 字节头（mark word + 类指针）→ 数组加长度、8 字节对齐 → 具体字节数 → 推论（百万装箱整数约 20 MB）→ 压缩指针 32 GB 限制。

> "On 64-bit HotSpot with compressed class pointers, every object has a 12-byte header - 8 bytes of mark word for hash, GC age and lock state, plus a 4-byte class pointer - arrays add a 4-byte length, and everything is padded to 8 bytes. So an empty object is 16 bytes, an `Integer` is 16, a record with two ints is 24, and an `int[10]` is 56. I measured these with the thread-allocated-bytes counter. The practical consequence is that a list of a million boxed Integers is about 20 MB where an `int[]` is 4 MB, and compressed oops, which keep references at 4 bytes, stop working above roughly 32 GB of heap."
