---
id: net-stream-cancellation
node: networking.streaming
type: qa
---
## Q
The client disconnects halfway through a large response, but origin CPU and storage reads continue. What contract is missing?

## A
**Cancellation propagation.** The edge must detect the closed downstream, cancel proxy work and the upstream request, and make transforms/storage reads observe that signal and release buffers. Also distinguish expected client cancellation from server faults in metrics; otherwise abandoned downloads waste capacity and create noisy false alerts.

## Q zh
client 在大响应传到一半时断开，但 origin CPU 与 storage read 仍继续。缺少什么 contract？

## A zh
缺少 **cancellation propagation**。edge 必须检测 downstream close，取消 proxy work 与 upstream request，并让 transformation/storage read 感知该信号、释放 buffer。metrics 还要区分预期 client cancellation 与 server fault；否则 abandoned download 会浪费 capacity，并制造噪声告警。
