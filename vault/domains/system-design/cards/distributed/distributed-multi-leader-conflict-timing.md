---
id: distributed-multi-leader-conflict-timing
node: distributed.replication.multi-leader
type: cloze
---
The reason multi-leader conflicts are painful is *when* they are detected: in single-leader (or serializable) systems the second writer is {{c1::blocked or given an error while it is still on the request path, so the user can be asked to retry}}, whereas in multi-leader replication both writes are {{c2::accepted and acknowledged locally, and the conflict only surfaces asynchronously when the two leaders exchange logs — nobody is on the line to ask}}. The practical consequence is that resolution must be {{c3::automatic and deterministic (every replica must reach the same answer independently), or deferred by storing siblings for a later on-read merge}}. It also means synchronous conflict detection ("make one write wait for the other leader") is possible but {{c4::throws away the entire point of multi-leader — independent local writes — so you should use single-leader instead}}.

## zh
多主复制中冲突之所以棘手是因为*何时*检测到：在单主（或可序列化）系统中，第二个写者是 {{c1::被阻止或给出错误，且仍在请求路径上，所以可以要求用户重试}}，而在多主复制中，两个写入都是 {{c2::被本地接受和确认，冲突只在两个主交换日志时异步浮现 — 没人在线询问}}。实际后果是解决必须是 {{c3::自动且确定性的（每个副本必须独立得出相同答案），或通过存储兄弟版本推迟到读时合并}}。这也意味着同步冲突检测（让一个写入等待另一个主）是可能的，但 {{c4::会失去多主的全部好处 — 独立本地写入 — 所以应该改用单主}}
