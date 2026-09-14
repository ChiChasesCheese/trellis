---
id: net-version-connection-scope
node: networking.http-versions
type: qa
---
## Q
Why can one overloaded HTTP/2 connection underperform several well-sized connections despite multiplexing?

## A
Multiplexing removes application-level connection serialization, not all shared limits. Streams still share connection flow control, TCP congestion control, packet loss recovery, server connection state, and sometimes a single processing bottleneck. Observe active streams, flow-control stalls and loss; cap streams per connection or open additional connections only from evidence, not as an HTTP/1 habit.

## Q zh
为什么一个 overloaded HTTP/2 connection 即使支持 multiplexing，也可能不如多个合理大小的连接？

## A zh
multiplexing 消除了 application-level connection serialization，但没有消除所有共享限制。stream 仍共享 connection flow control、TCP congestion control、packet loss recovery、server connection state，有时还共享单个 processing bottleneck。应观察 active stream、flow-control stall 与 loss；只有证据支持时才限制每连接 stream 或增加连接，不要沿用 HTTP/1 习惯。
