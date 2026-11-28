---
id: hi-c-lld-coordination-n07-shutdown
node: lld.concurrency.coordination.notes
type: qa
step: 7
---
## Q
**并发协调 · 优雅停机**｜摘要 · 必会

工人都阻塞在 `take()`，应用要停机时怎么让它们退出？Java 里的 `InterruptedException` 该怎么处理？

## A
- **中断线程：** 被阻塞的线程抛出中断异常，捕获后跳出循环；最简单
- **带超时的 poll：** 到时没任务返回空，借机检查停机标志；一个超时周期内退出
- **毒丸（poison pill）：** 提交特殊哨兵任务，每个工人一颗，取到就退出；适合不能中断或不想用超时的场景
- **`InterruptedException`：** 不能吞掉，要么向上抛，要么捕获后重新设置中断状态，让上层知道线程被中断了
