---
id: hl-j16-who-reorders
node: java21.j16-concurrency-primitives
type: qa
step: 29
---
## Q
重排序到底发生在哪一层？javac、JIT、CPU 各做什么？`volatile` 在字节码里是什么样？

## A
- **javac 几乎不重排**；重排主要在 **JIT（C2）** 和 **CPU**。
- `volatile` 字段读写在字节码里只是带 `ACC_VOLATILE` 的 `getfield/putfield`，真正约束由 JIT 生成机器码时落实。
- **JIT 实现 HB**：在 volatile 读写前后**插入内存屏障**，并禁止编译器跨屏障重排和缓存。普通字段没有屏障阻止，所以 JIT 能把 `stop` 提出循环。
