---
id: problems-chat-messaging-sync-vs-async-fanout-threshold
node: problems.social.chat-messaging
type: qa
step: 6
tags: [grown]
---
## Q
In a chat system, why does group message fan-out need to switch from synchronous push to an asynchronous queue past some group-size threshold, and what determines where roughly that threshold sits?

## A
If a gateway synchronously pushes a message to every online recipient's gateway before acknowledging the sender, the sender's tail latency grows with the number of recipients — one slow cross-gateway RPC delays the whole send. The threshold is roughly the sender's acceptable latency budget divided by the typical cost of one cross-gateway delivery hop: e.g. a 200ms budget over a 5ms typical hop gives a theoretical ceiling around 40 synchronous fan-out targets, so in practice teams set the cutover well below that (on the order of 100 recipients) and hand larger groups to an async fan-out queue that acknowledges the sender immediately and delivers in the background.

## Q zh
在一个聊天系统中，为什么群消息扇出必须在群规模超过某个阈值后，从同步推送切换到异步队列？这个阈值大致由什么决定？

## A zh
如果网关在给发送方回确认之前，同步地把消息推给每个在线收件人的网关，发送方的尾延迟就会随收件人数量增长——一次慢的跨网关 RPC 就会拖慢整次发送。阈值大致等于发送方可接受的延迟预算除以单次跨网关投递的典型开销：例如 200ms 预算除以 5ms 的典型单跳开销，理论上限约为 40 个同步扇出目标，实践中团队会把切换点设在明显更低的位置（数量级在 100 个收件人左右），并把更大的群交给一个异步扇出队列，让它立刻确认发送方、在后台完成投递。
