---
id: hl-j16-three-problems
node: java21.j16-concurrency-primitives
type: qa
step: 1
---
## Q
多线程读写同一个变量有哪三类彼此独立的问题（原子性、可见性、有序性）？各举一个例子。

## A
| 问题 | 一句话 | 例子 |
|---|---|---|
| **原子性**（atomicity） | 一个操作会不会被别的线程「看到一半」 | `count++` 其实是读、加 1、写三步，两个线程交错就丢更新 |
| **可见性**（visibility） | A 写的值，B 什么时候、能不能看到 | B 一直读到旧值，永远等不到 `stop = true` |
| **有序性**（ordering） | 代码里先写 x 再写 y，别的线程看到的顺序是不是也这样 | B 看到了 `ready = true`，却看不到 `ready` 之前写的 `data` |

你以为「A 写完 B 就能看到」，其实不是。
