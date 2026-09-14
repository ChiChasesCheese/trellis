---
id: networking-long-polling-costs
node: networking.realtime
type: qa
---
## Q
What does a hanging long-poll request cost the server, and why do thread-per-request servers cap out first?

## A
Every waiting client holds an open connection and a parked request for up to the poll timeout (kept at ~30 s, under proxy idle limits). With thread-per-request servers that is a thread + stack per *idle* client — concurrency caps in the low thousands; event-loop/async servers hold a cheap file descriptor instead and reach 100k+.

Second cost: a broadcast event completes every parked request at once, and all those clients **immediately re-poll** — a synchronized request wave after each event, which SSE/WebSockets avoid by keeping the channel open.

## Q zh
一个挂起的长轮询请求对服务器的成本是什么，为什么 thread-per-request 服务器首先达到上限？

## A zh
每个等待的客户端持有一个打开的连接和一个停泊的请求长达轮询超时（保持在约 30 s，在代理空闲限制下）。使用 thread-per-request 服务器，那是每个*空闲*客户端的线程 + 栈 — 并发上限在低数千；事件循环/异步服务器持有廉价文件描述符并达到 100k+。

第二成本：广播事件一次完成每个停泊的请求，所有这些客户端**立即重新轮询** — 每个事件后的同步请求波，SSE/WebSocket 通过保持通道打开来避免。
