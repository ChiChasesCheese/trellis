---
id: content-isr-stale-revalidate
node: content.isr
type: qa
---
## Q
An ISR page reaches its revalidation time while receiving 5,000 requests/s. What should users see, and how many renders should start?

## A
Continue serving the last successful stale page immediately and allow one collapsed background regeneration for that cache key; the other requests must not stampede the renderer. Publish the new artifact atomically only after success. Revalidation age is permission to refresh, not permission to discard a usable representation. Track stale age and regeneration duration so a permanently failing refresh is visible.

## Q zh
ISR page 到达 revalidation 时间时正承受 5,000 requests/s。用户应该看到什么，应启动多少次 render？

## A zh
立即继续服务上一次成功的 stale page，并只允许该 cache key 启动一个 collapsed background regeneration；其他请求不能 stampede renderer。只有成功后才原子 publish 新 artifact。revalidation age 是允许 refresh，不是允许丢弃可用 representation。要跟踪 stale age 和 regeneration duration，使永久失败的 refresh 可见。
