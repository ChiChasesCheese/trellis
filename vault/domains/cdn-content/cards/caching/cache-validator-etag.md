---
id: cache-validator-etag
node: caching.validators
type: qa
---
## Q
When should an origin use a strong ETag rather than a weak ETag for content delivery?

## A
A **strong ETag** means byte-for-byte equivalence and is required when exact representation identity matters, such as validating range requests. A weak ETag (`W/`) means semantic equivalence despite byte differences and is suitable for revalidation when harmless re-serialization occurs. Never generate unstable validators that change on every request; that defeats `304` reuse.

## Q zh
content delivery 中，origin 什么时候应使用 strong ETag，而不是 weak ETag？

## A zh
**strong ETag** 表示 byte-for-byte equivalent，适用于 range request validation 等需要精确 representation identity 的场景。weak ETag（`W/`）表示虽然字节不同但语义等价，适合会发生无害重新序列化的 revalidation。不要生成每次请求都变化的 unstable validator，否则 `304` 复用失效。
