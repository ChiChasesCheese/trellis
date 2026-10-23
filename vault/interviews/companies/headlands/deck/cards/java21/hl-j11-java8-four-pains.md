---
id: hl-j11-java8-four-pains
node: java21.j11-structured-concurrency
type: qa
step: 2
---
## Q
用 Java 8 的 `ExecutorService` 并行做两件事（一件 1500 ms 后成功，一件 100 ms 后失败），会同时暴露哪四个痛点？

## A
用 `pool.submit` 得到 `a`、`b` 两个 `Future`，先 `a.get()` 再 `b.get()`，结果 `b` 100 ms 就失败，`main` 却在 `a.get()` 上傻等了 1.5 秒：
1. **失败不传播**：失败的任务不会通知其他代码。
2. **取消不传播**：`b` 失败后 `a` 已没意义，却被允许做完（可能是昂贵的下游调用），得自己写 `a.cancel(true)`。
3. **泄漏**：任何异常路径漏掉 `shutdown()`/`cancel()`，线程和下游请求就成孤儿。
4. **看不清谁是谁的父**：线程 dump 里这两个线程与发起它们的方法毫无关系，排查生产问题很难把线程对回某个请求。
