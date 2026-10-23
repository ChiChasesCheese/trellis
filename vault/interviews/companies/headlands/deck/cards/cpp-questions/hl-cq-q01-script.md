---
id: hl-cq-q01-script
node: cpp-questions.a-why-fast
type: qa
step: 6
---
## Q
用英文 60 秒回答：Why is C++ fast?

## A
结构：先答 AOT 原生码且无强制运行时 → 优化器内联（`sort` 对 `qsort` 数字）→ 内存布局连续 → 无隐藏停顿 → 代价是 UB 且速度要自己挣。

- C++ compiles **ahead of time** to native code, and there is **no mandatory runtime** - no garbage collector, no VM, no bounds checks unless I ask for them.
- The optimizer sees the whole translation unit, so abstractions like templates and lambdas get **inlined away** - zero-overhead abstraction. `std::sort` took about 80 ms on five million ints versus 300 ms for `qsort`, because the comparator is inlined instead of called through a function pointer.
- I control **memory layout**: a `std::vector` of structs is one contiguous block, which is **cache friendly**.
- No hidden pauses: allocation is explicit, destruction is **deterministic** (RAII).
- The price is that the compiler may assume **no undefined behavior**, and speed is something you earn - lists of pointers, `shared_ptr` everywhere or exceptions in a hot loop are slow.
