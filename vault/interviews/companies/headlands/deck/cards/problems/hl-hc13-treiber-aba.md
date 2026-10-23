---
id: hl-hc13-treiber-aba
node: problems.hc13-fixed-memory-pool
type: qa
step: 10
---
## Q
Treiber 栈是什么？ABA 问题怎么发生，带 tag 的 head 怎么解决？

## A
**Treiber 栈**（1986）：用 CAS 实现的并发栈，栈顶是共享变量 `top`：
```
push(x):  loop { t = top;  x.below = t;  if CAS(top, t, x) break; }
pop():    loop { t = top;  if t == null return empty;  n = t.below;  if CAS(top, t, n) return t; }
```
空闲链表本来就是栈（LIFO），直接做成 Treiber 栈：`top` 就是 `head`，节点是槽位编号，`below` 是 `next[]`。

**ABA**：CAS 只看「值是不是 A」，不看期间发生过什么。初始栈 `A→B→C`：
1. 线程 1 `pop()`：读到 `top=A`、`A.below=B`，被操作系统切走；
2. 线程 2 pop 走 A，pop 走 B（B 在线程 2 手里正在使用），再 push A（栈 `A→C`）；
3. 线程 1 恢复：`CAS(top, 期望 A, 新值 B)` 成功（top 确实还是 A）——B 被装回空闲链表，可线程 2 还在用 B，两线程同时拥有 B。这是并发池最经典的 bug（面试标准考点）。

**解法：带 tag 的 head**。`head` 变 `long`：高 32 位 tag（每次成功 push/pop 都 +1），低 32 位栈顶槽位（`-1` = 空）；CAS 比较整个 64 位：
```java
private static long pack(int tag, int index) { return ((long) tag << 32) | (index & 0xFFFFFFFFL); }
private static int tagOf(long h) { return (int) (h >>> 32); }
private static int indexOf(long h) { return (int) h; }
```
线程 2 的 pop、pop、push 让 tag 从 t 变 t+3；线程 1 期望 `(t, A)`，现在是 `(t+3, A)`，不等 → 失败重读。

tag 也会回绕（32 位 = 42 亿次）：重现 ABA 要线程 1 在读和 CAS 之间被挂起整整 2³² 次成功操作，可忽略但要在注释写明；更严格用 hazard pointer / epoch，或 64 位 tag + 128 位 CAS（Java 无直接支持）。`AtomicStampedReference` 是同一思想的对象版（每次更新分配 `Pair`，在池里是反面教材）。

**验证**：去掉 tag（两处 `tagOf(h) + 1` 改成 `tagOf(h)`），多线程压力测试 20 轮有 7 轮丢槽位；加回 tag 全部通过。tag 和 head 分成两个原子变量也不行，必须是**一个** 64 位整体。不允许用 `synchronized` / `Lock` / `AtomicReference` 配对象节点。
