---
id: hl-cq-q29-x86-vs-arm-aba
node: cpp-questions.g-concurrency
type: qa
step: 10
---
## Q
“在 x86 上测过内存序没问题”为什么不能证明正确？`fetch_add` 在 ARM64 上 `seq_cst` 和 `relaxed` 编译成什么、差别多大？什么是 ABA 问题？

## A
- **x86 硬件顺序较强**（几乎只重排 store→load），弱序的 ARM 上不加正确的序更容易暴露问题，所以 x86 上通过证明不了什么。
- **ARM64 的 `fetch_add`**：`seq_cst` 编译成 `ldaddal`（带 acquire+release 语义），`relaxed` 编译成 `ldadd`。两千万次无竞争调用都是 26 ms；差别出现在被竞争的场景和周围内存操作的排序上。
- **ABA 问题**：CAS 看到值仍是 A，但中间被改成 B 又改回 A；用带版本号的指针解决。
