---
id: hl-hc03-measure-depth
node: problems.hc03-recursive-sum
type: qa
step: 6
---
## Q
Java 里怎么测量递归能到多深？线程栈大小和深度的实测关系是什么？为什么不能依赖固定数字？

## A
`measureDepth(stackBytes)`：新开线程、指定栈大小、递归到爆、数层数。
```java
private static final class Probe { int depth; void dive() { depth++; dive(); } }
var t = new Thread(null, () -> {
    try { probe.dive(); } catch (StackOverflowError _) { }
}, "depth-probe", stackBytes);
t.start(); t.join();
```
- 计数放**对象字段**：栈溢出瞬间没法返回值，字段是唯一带出结果的办法。
- 用新线程：栈大小是**线程**属性，只能在构造 `Thread` 时指定，也避免撑爆调用者的栈。

实测（冷启动第一次 / 预热后）：512 KiB：6 161 / 25 228；1 MiB：17 258（`-Xint`：8 284）/ 57 996；8 MiB：516 748；64 MiB：4 186 764。

结论：①深度大致与栈大小成正比（栈大小 ÷ 帧大小，每 MiB 几万层）；②**同一 JVM 里预热前后差 3–4 倍**，解释器帧大、C1/C2 编译后帧小；③还受 `-Xss`、局部变量个数、是否内联影响。所以测试只能断言「64 MiB 的深度 > 4 × 512 KiB 的深度」这类关系，不断言具体数字。

面试答法：「量级是栈大小 / 栈帧大小，大约每 MiB 栈几万层；我不会依赖它。」
