---
id: problems-google-docs-server-authoritative-ack-flow
node: problems.media.google-docs
type: qa
step: 4
tags: [grown]
---
## Q
In a centralized operational-transformation architecture for collaborative editing, why does the client wait for the server's acknowledgment of its last batch of operations before sending the next batch, instead of sending new local operations as soon as they're produced?

## A
If clients could send continuously without waiting, the server would need to track a separate state space per client (which operations that specific client has and hasn't seen), since any two clients could have divergent unacknowledged histories to transform against — this makes correctness far harder to reason about. By having clients buffer locally-produced operations until the prior batch is acknowledged, the server only ever needs to maintain one state space: its own accumulated operation history. Any incoming batch is transformed against exactly 'what the server has committed since the revision this batch was based on,' which is a single well-defined computation.

## Q zh
在中心化操作转换（OT）的协同编辑架构中，为什么客户端要等服务器对上一批操作确认之后才发送下一批操作，而不是本地一产生新操作就立刻发送？

## A zh
如果客户端可以不等待就持续发送，服务器就需要为每个客户端单独维护一份状态空间（这个客户端具体看到过哪些操作），因为任意两个客户端都可能各自持有不同的、尚未确认的操作历史需要转换裁决——这会让正确性论证变得极其困难。让客户端把本地新产生的操作缓存到上一批被确认为止，服务器就只需要维护一份状态空间：它自己已提交的操作历史。任何到达的一批操作只需要与「自这批操作所基于的版本以来服务器已提交的操作」做转换，这是一个定义明确的单一计算。
