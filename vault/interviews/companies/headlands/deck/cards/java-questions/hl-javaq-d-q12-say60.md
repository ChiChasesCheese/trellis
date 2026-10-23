---
id: hl-javaq-d-q12-say60
node: java-questions.d-memory
type: qa
step: 29
---
## Q
用英文 60 秒回答：`System.arraycopy` vs a hand-written loop vs `Arrays.copyOf` vs `clone` - what's the difference? How does that compare to `std::copy` vs `memcpy`?

## A
结构：memcpy 不能重叠、std::copy 类型感知 → arraycopy 是 memmove 语义加检查 → intrinsic → copyOf 多了分配 → 稳态循环一样快但仍用 arraycopy。

> "`memcpy` is a raw byte copy that's undefined on overlapping regions and wrong for non-trivially-copyable types; `std::copy` is type-aware and for trivial types typically ends up as `memmove`. The Java counterpart is `System.arraycopy`, which behaves like `memmove` - overlapping copies are correct, I checked by shifting an array onto itself - but adds bounds and type checks, throwing `ArrayIndexOutOfBounds` or `ArrayStore`. HotSpot treats it as an intrinsic, so it's inlined or uses an optimised stub. `Arrays.copyOf` is arraycopy plus allocation and zeroing, so it's slower for big arrays. In steady state a simple loop gets recognised by C2 and is as fast, but I'd still use arraycopy for clarity and because it's fast during warm-up too."
