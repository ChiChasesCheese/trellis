---
id: net-stream-backpressure
node: networking.streaming
type: qa
---
## Q
A fast origin streams a 2 GiB object through a proxy to a slow mobile client. What happens without backpressure?

## A
The proxy buffers the producer-consumer gap in memory until it is exhausted or latency becomes unbounded. Backpressure must propagate from the downstream socket through the proxy to the upstream reader: pause reads when buffers cross a high-water mark, resume below a low-water mark, and bound total per-connection and fleet buffering.

## Q zh
fast origin 通过 proxy 向 slow mobile client 流式发送 2 GiB object。没有 backpressure 会怎样？

## A zh
proxy 会把 producer-consumer 速度差积累在 memory 中，直到 memory 耗尽或 latency 无界增长。backpressure 必须从 downstream socket 经 proxy 传播到 upstream reader：buffer 超过 high-water mark 时暂停读取，降到 low-water mark 后恢复，并限制 per-connection 与全 fleet buffering。
