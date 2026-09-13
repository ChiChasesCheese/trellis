---
id: content-versioning-deployment-id
node: content.versioning
type: qa
---
## Q
A page from release B references an asset from release A because cache and routing update at different times. What identity should bind a response to one release?

## A
Resolve an immutable deployment ID at request start and use it for the route manifest, server code, and every non-content-addressed artifact lookup. Content-hashed assets may be shared safely, but mutable names must stay within the snapshot. Atomically change only the production pointer. This prevents a request from observing a mixture while caches, regions, and instances converge.

## Q zh
由于 cache 和 routing 更新时间不同，release B 的 page 引用了 release A 的 asset。什么 identity 能把一次响应绑定到同一个 release？

## A zh
请求开始时解析 immutable deployment ID，并把它用于 route manifest、server code 和所有非 content-addressed artifact lookup。content-hashed asset 可安全共享，但 mutable name 必须留在该 snapshot 内。只原子切换 production pointer。这样在 cache、region 和 instance 收敛期间，一次请求也不会观察到版本混合。
