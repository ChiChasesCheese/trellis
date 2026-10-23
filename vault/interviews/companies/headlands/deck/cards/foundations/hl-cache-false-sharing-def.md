---
id: hl-cache-false-sharing-def
node: foundations.cpu-cache-locality
type: qa
step: 22
---
## Q
什么是伪共享（false sharing）？为什么两个线程各改各的变量也会互相拖慢？

## A
同一个缓存行（64 或 128 字节）里放着两个互不相关的变量：`counterA` 由线程 1 写，`counterB` 由线程 2 写。
- 线程 1 在核 A 写 `counterA` → 整行在核 B 上失效；
- 线程 2 在核 B 写 `counterB` → 整行在核 A 上失效；
- 这一行在两个核之间来回「乒乓」，每次写都是跨核通信，约 **50–100 ns**。

两个线程逻辑上完全独立，却因物理上挨在同一缓存行而互相拖慢，所以叫「伪」共享。
