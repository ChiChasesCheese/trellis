---
id: hl-cq-q15-script
node: cpp-questions.c-memory-ownership
type: qa
step: 29
---
## Q
用英文 60 秒回答：What's the difference between `std::copy`, `memcpy` and `memmove`?

## A
结构：`memcpy` 字节/不可重叠，`memmove` 可重叠，都限 trivially copyable → `std::copy` 类型感知 → 不慢（汇编是一次 `memmove`）→ 原始拷贝为何破坏非平凡类型 → `bit_cast`。

- `memcpy` copies **raw bytes** and the ranges **must not overlap** - that's undefined; `memmove` handles overlap. Both are only valid for **trivially copyable** types.
- `std::copy` is **type-aware**: it assigns element by element, so it's correct for strings and anything with a copy operator, and it works with any iterator.
- It's not slower: for trivially copyable types the library dispatches to `memmove` - I looked at the assembly for an `int` array and it was a single call to `memmove`.
- Why raw copying breaks non-trivial types: an object holding a pointer into itself, or a `std::string` with its heap buffer, would end up shared or pointing at the original.
- For type punning I use `std::bit_cast`, not pointer casts.
