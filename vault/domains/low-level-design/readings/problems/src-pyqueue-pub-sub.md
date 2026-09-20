---
nodes: [problems.components.pub-sub]
url: https://docs.python.org/3/library/queue.html
---
# queue — A synchronized queue class（标准库文档）

值得读：本题"有界"与"满了怎么办"这两件事的权威出处。重点三处：`Queue(maxsize=...)` 的满/空
阻塞语义、`put_nowait` 在满时抛 `Full` 而不是悄悄丢、`task_done()` 与 `join()` 的配对关系
（"队列里已有的活全干完了"这个判断只能这样做）。本题解**没有**直接用 `queue.Queue`：它是队列
不是日志——取出即消失，给不了重放，也给不了多个订阅者各自的位点。但三种溢出策略的语义刻意与
它保持一致（阻塞对应 `put(block=True)`，拒绝对应 `put_nowait` 抛 `Full`），这样面试时可以用
一句"和标准库的 Queue 同义"把语义说清。
