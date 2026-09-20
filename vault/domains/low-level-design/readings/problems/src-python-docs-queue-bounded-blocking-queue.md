---
nodes: [problems.components.bounded-blocking-queue]
url: https://docs.python.org/3/library/queue.html
---
# queue — A synchronized queue class

值得读：标准库现成的有界阻塞队列，`Queue(maxsize=)`、`put`/`get` 的 `block`/`timeout`
参数、超时抛出的 `Full`/`Empty` 异常。本题解决策二（超时该抛异常还是返回哨兵值）直接
沿用了这里的先例；和本题解不同的是标准库版本不提供 `close()` 这种优雅关闭语义，也不区分
"停止接收新工作"和"排空已有工作"两个阶段，这是本题在它之上自己设计的部分。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/queue.html)

## Archived copy
![[src-python-docs-queue-thread-pool-clip]]
%% trellis:end %%
