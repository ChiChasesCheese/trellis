---
id: hl-cache-padding
node: foundations.cpu-cache-locality
type: qa
step: 25
---
## Q
怎样用填充（padding）避免伪共享？为什么手工填充不是 100% 可靠，更稳妥的做法是什么？

## A
让每个被不同线程高频写的变量独占一个缓存行：
```java
final class PaddedCounter {
    long p1, p2, p3, p4, p5, p6, p7;   // 前填充
    volatile long value;
    long q1, q2, q3, q4, q5, q6, q7;   // 后填充
}
```
前后各 7 个 `long`（56 字节）对 64 字节行够用；Apple 的 128 字节行需要更多。

不可靠的原因：JVM 可能重排字段（按大小分组放置）。稳妥做法是**通过继承层次**强制顺序（Disruptor 就这样）：父类放前填充，子类放字段，孙类放后填充，因为 JVM 不会把子类字段排到父类字段前面。
