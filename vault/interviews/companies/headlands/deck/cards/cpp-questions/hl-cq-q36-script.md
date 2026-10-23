---
id: hl-cq-q36-script
node: cpp-questions.i-low-latency
type: qa
step: 6
---
## Q
用英文 60 秒回答：How do you keep the hot path allocation-free in C++?

## A
结构：`malloc` 不可预测 → 预分配（`reserve`、对象池、`pmr` 单调竞技场）→ 替换 `operator new` 计数（11 / 1 / 1000 / 0）→ 警惕隐藏分配与预触碰。

- On a hot path `malloc` is **unpredictable**: it can take locks, ask the kernel for memory, and cause page faults. So I **allocate up front**: `reserve` containers, use **object pools** or fixed-capacity containers, and use a **monotonic arena** from `std::pmr` for per-message scratch memory.
- I measure by replacing `operator new` and counting. Pushing 1,000 elements into a vector took 11 allocations without `reserve` and 1 with it; a `std::list` took 1,000; a `pmr` list and strings on a stack buffer took zero, and building 1,000-node lists 2,000 times was about 3x faster than with `malloc`.
- I also watch hidden allocations - `std::string` beyond the small-buffer size, `std::function` with big captures, `shared_ptr` - and I pre-touch pool memory so first use doesn't page-fault.
