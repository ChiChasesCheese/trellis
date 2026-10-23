---
id: hl-cq-q17-script
node: cpp-questions.d-containers
type: qa
step: 6
---
## Q
用英文 60 秒回答：How does `std::vector` grow? What invalidates iterators, pointers and references?

## A
结构：连续缓冲区、翻倍扩容、均摊 O(1) 但偶尔 O(n) → 重新分配使一切失效（ASan 的 `heap-use-after-free`）→ `erase`/`insert` 规则 → `reserve`（11 次变 1 次）、用下标。

- A `std::vector` is **one contiguous buffer** with a size and a capacity. When it fills up it allocates a new buffer - twice as big in libc++ and libstdc++ - moves the elements, and frees the old one. That makes `push_back` **amortized O(1)** but occasionally O(n).
- Consequence: any `push_back` that reallocates **invalidates all iterators, pointers and references**. I've seen it as a `heap-use-after-free` under AddressSanitizer, pointing straight into the reallocation path.
- Rules: `erase` invalidates from the erase point on and returns the next valid iterator; `insert` likewise.
- If I know the size I `reserve` first - in the demo, 11 allocations became one - and I keep indices rather than pointers if the container may grow.
