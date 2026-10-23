---
id: hl-ld01-memory-order
node: problems.ld01-spsc-channel
type: qa
step: 5
---
## Q
为什么「先写数据再改 tail」还不够？release/acquire 具体保护什么，去掉会怎样，和 `volatile` 比如何？

## A
CPU 和编译器会**重排**无依赖的读写；每个核心有写缓冲（store buffer），写先进缓冲、之后才对别核可见，别核看到的顺序不一定等于程序顺序。生产者两行：`buf[i] = v;`（① 数据）和 `tail = t + 1;`（② 发布）。在弱内存序 CPU（ARM，含 Apple M）上，其他核心可能**先看到 ② 再看到 ①**：消费者看到 `tail` 变了去读 `buf[i]`，读到旧数据（上一圈残留值）。实测把 `TAIL.setRelease` 换成普通写，Apple M 上马上大量出错。x86 内存序更强，同样代码常「碰巧」对——**x86 上测试通过不代表对**。

**release / acquire**：
- `setRelease(x, v)`：之前的读写不会被重排到它之后（向上的单向门）；
- `getAcquire(x)`：之后的读写不会被重排到它之前（向下的单向门）；
- 若消费者 `getAcquire(tail)` 读到了生产者 `setRelease(tail, t+1)` 写下的值，则生产者在该 release 之前写的一切（含 `buf[i]`），消费者在该 acquire 之后都看得到。

```
生产者:  buf[i] = v;                // ① 数据
         TAIL.setRelease(t + 1);    // ② release：① 不能被重排到 ② 之后
消费者:  t = TAIL.getAcquire();     // ③ acquire：④ 不能被重排到 ③ 之前
         v = buf[i];                // ④
```
**反方向同样需要**：消费者读完 `buf[i]` 后才 `HEAD.setRelease(h + 1)`，生产者 `getAcquire` 看到新 `head` 后才敢覆盖该槽位——否则生产者可能在消费者读完前写入（丢一条）。

**为什么不直接 `volatile`**：它是更强的顺序一致，多付「写后读」重排禁止的代价（x86 上要 `lock` 前缀或 `mfence`）；release/acquire 在 x86 上就是普通 `mov`，只约束编译器，无额外 CPU 栅栏。HotSpot 在 AArch64 上两者都编成 `ldar/stlr`，差别应很小（未反汇编验证）。

**可见性**：什么都不加时，消费者 `while (isEmpty())` 里 JIT 可把对普通字段 `tail` 的读提到循环外，永远读不到新值——死循环。

**跨进程呢？** 两进程映射同一批物理页，硬件缓存一致性和内存序同样适用，`setRelease/getAcquire` 编译出同样的屏障指令，所以协议跨进程同样成立；但这是基于硬件与 JIT 实现的推理，**不是 JMM 的形式化保证**（JMM 谈同一程序内的线程），面试别说太绝对。
