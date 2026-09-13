---
id: fnd-request-latency-budget
node: foundations.request-path
type: qa
---
## Q
You have a 200 ms p99 TTFB target for an edge miss. How should you allocate it so one downstream does not silently consume the entire deadline?

## A
Create a **deadline budget**, not independent 200 ms timeouts: reserve time for DNS/connection and response overhead, then give edge, shield, origin, and storage bounded sub-deadlines whose worst-case sum fits the user deadline. Propagate the remaining deadline downstream and stop work on cancellation; otherwise nested retries can turn a 200 ms objective into seconds.

## Q zh
edge miss 的 p99 TTFB 目标是 200 ms。怎样分配时间，才能避免某个 downstream 悄悄吃掉整个 deadline？

## A zh
建立 **deadline budget**，不要给每一层独立设置 200 ms timeout：先为 DNS/connection 和响应开销预留时间，再给 edge、shield、origin、storage 设置有界的 sub-deadline，保证最坏情况总和仍落在用户 deadline 内。向下游传播剩余 deadline，并在 cancellation 时停止工作，否则嵌套 retry 会把 200 ms 目标拖成几秒。
