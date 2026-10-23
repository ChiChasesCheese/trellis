---
id: hl-os-debug-publish-flag
node: foundations.os-processes-threads-ipc
type: qa
step: 42
---
## Q
下面的「发布」有什么问题？

```java
class Box { long[] data = new long[8]; boolean ready; }
// 线程 A：box.data[0] = 42; box.ready = true;
// 线程 B：while (!box.ready) { }  System.out.println(box.data[0]);
```

## A
没有同步：`ready` 不是 `volatile`，B 的循环可能被 JIT 提升成死循环（永远读寄存器里的旧值）；即使 B 看到 `ready == true`，也不保证看到 `data[0] == 42`（写重排或缓存未同步）。

修法：`volatile boolean ready`（volatile 写 happens-before 后续对它的读），或 `VarHandle.setRelease` / `getAcquire`。
