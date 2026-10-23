---
id: hl-j16-dcl-volatile
node: java21.j16-concurrency-primitives
type: qa
step: 36
---
## Q
双重检查锁（DCL）为什么 `inst` 必须是 `volatile`？

## A
```java
if (inst == null) synchronized (Lock.class) { if (inst == null) inst = new X(); }
```
`inst = new X()` 包含「分配内存、构造对象、赋值引用」，构造与赋值可能被重排。若 `inst` 非 volatile，另一线程可能看到**引用非 null，但对象还没构造完**。

加 `volatile` 后写 `inst` 之前的构造 HB 之后的读，修复了这个问题。
