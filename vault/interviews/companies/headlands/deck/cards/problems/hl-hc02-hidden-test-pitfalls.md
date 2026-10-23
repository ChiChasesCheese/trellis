---
id: hl-hc02-hidden-test-pitfalls
node: problems.hc02-merge-k-streams
type: qa
step: 16
---
## Q
合并 K 路流题的测试会打哪些坑？边界清单是什么？

## A
**坑**：
- 用 `a - b` 比较（`Long.MIN_VALUE` / `MAX_VALUE` 溢出）；
- 稳定性：比较键没带序列号，相等元素顺序依赖堆内部细节；
- `k = 0` / 全空 / 空序列夹在中间：堆为空时 `poll()` 返回 `null`；
- 构造时就预读所有 source（惰性测试会数 `next()` 调用次数）；
- 刚输出 x 就阻塞去取 x 后面的元素（延迟补位测试）；
- 「先到先出」：有流没数据时输出别的流的元素（`tryNext` 应一直 `Pending`）；
- 无界队列（`backpressureBoundsReadAhead` 精确断言 `capacity + 1`）；
- 生产者出错没留标记 → 消费者永远 `take()`；`close()` 没中断生产者 → 线程泄漏；
- 吞掉 `InterruptedException`；
- `mergeAll` 用普通线程池 + `Future.get()`：永远阻塞的 source 让方法挂住。

**边界清单**：`k=0`、全空、单个序列、空序列在中间；大量相等元素；`Long.MIN/MAX`；乱序出现在序列中间；一个 source 永远不给数据；一个 source 抛异常；消费者不消费时生产者被背压挡住；`close()` 时生产者阻塞在 source 里。

测试并发代码：多次重复 + 随机让出打乱交错，与顺序实现对拍，看门狗把死锁变成失败。
