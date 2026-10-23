---
id: hl-c03-shared-ptr-cost
node: cpp-lessons.c03-smart-pointers
type: qa
step: 10
---
## Q
拷贝 `shared_ptr` 的实测开销是多少？函数参数应该怎么传 `shared_ptr`？

## A
单线程实测每次操作：
- 裸指针 0.88 ns；传 `const shared_ptr&` 0.88 ns（几乎一样快）。
- **按值传** `shared_ptr` 约 3.07 ns，慢好几倍（每次一对原子加减）。
- 4 个线程拷贝**同一个** `shared_ptr`，争抢同一条缓存线上的计数器，每次拷贝约 **100 ns**。

结论：
- 作参数时传 `const shared_ptr&`，或者干脆传 `T&`。
- 热路径不要到处拷贝 `shared_ptr`。
- 别把 `shared_ptr` 当默认选择：它带来不必要的原子操作和不明确的生命周期。
