---
nodes: [problems.components.bounded-blocking-queue]
url: https://docs.python.org/3/library/threading.html
---
# threading — Thread-based parallelism

值得读：`Condition` 的官方文档，尤其是 `wait()`、`wait_for(predicate)`、`notify(n=1)`、
`notify_all()` 的精确语义和"必须持锁调用"的约束。它是本题解决策一（一个条件变量还是
两个）和决策三（`close()` 要不要用 `Event`）的权威依据；没有覆盖的是本题自己设计的
`close()`／超时语义，那部分是这份题解自己的设计。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/threading.html)

## Archived copy
![[src-python-docs-bounded-blocking-queue-clip]]
%% trellis:end %%
