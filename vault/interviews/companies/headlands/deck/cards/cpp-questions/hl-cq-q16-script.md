---
id: hl-cq-q16-script
node: cpp-questions.c-memory-ownership
type: qa
step: 33
---
## Q
用英文 60 秒回答：What do `sizeof`, `alignof` and padding mean? How would you lay out a hot struct?

## A
结构：对齐与填充、大小补齐 → 成员顺序实例（24 对 16 字节，大的在前）→ `alignas(64)` 防伪共享 → 热结构体紧凑、定宽类型、不对线路 `memcpy`。

- Every type has an **alignment**; the compiler inserts **padding** so each member sits at an aligned offset, and the struct's size is rounded to its largest alignment.
- So member order matters: the same four fields were **24 bytes** with a char first and a double second, and **16 bytes** with the double first. Rule: **largest first**.
- `alignas(64)` puts an object on its own cache line, which I use to avoid **false sharing**.
- For hot data I keep structs compact, hot fields together, ideally within one **64-byte cache line**, and I use fixed-width types from `<cstdint>`. I don't `memcpy` a struct onto the wire because padding and endianness vary.
