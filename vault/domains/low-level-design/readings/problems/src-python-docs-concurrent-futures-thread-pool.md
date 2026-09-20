---
nodes: [problems.components.thread-pool]
url: https://docs.python.org/3/library/concurrent.futures.html
---
# concurrent.futures — Launching parallel tasks

值得读：标准库现成的线程池和 `Future`，`ThreadPoolExecutor.submit`／`shutdown(wait=,
cancel_futures=)` 的官方语义，本题解决策一、二直接对照的原型。和本题解不同的是标准库
`ThreadPoolExecutor` 的内部任务队列没有容量上限，`submit()` 永远立刻成功、从不阻塞也
不拒绝，这正是本题要在它之上补一层信号量背压的原因；`cancel_futures` 也只能取消还没
开始执行的任务，正在运行的那个依然会跑完，这一点两者一致。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/concurrent.futures.html)

## Archived copy
![[src-python-docs-concurrent-futures-thread-pool-clip]]
%% trellis:end %%
