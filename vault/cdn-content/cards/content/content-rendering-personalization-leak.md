---
id: content-rendering-personalization-leak
node: content.rendering
type: qa
---
## Q
An SSR page reads a session cookie but is accidentally cached at the CDN. What invariant should the rendering layer communicate?

## A
Any representation that depends on per-user request data must be private or uncacheable by a shared cache, unless the cache key safely partitions every personalization dimension. Emit explicit cache policy at the rendering boundary and test it. Prefer moving personalized fragments behind a dynamic hole so the public shell stays shareable. A correct HTML render with the wrong cache metadata is a cross-user data leak.

## Q zh
SSR page 读取 session cookie，却被 CDN 意外缓存。rendering layer 必须传达什么 invariant？

## A zh
任何依赖 per-user request data 的 representation 都必须标为 private 或禁止 shared cache，除非 cache key 能安全区分每个 personalization dimension。rendering boundary 要发出显式 cache policy，并进行测试。最好把 personalized fragment 移到 dynamic hole，使 public shell 仍可共享。HTML 渲染正确但 cache metadata 错误，就是 cross-user data leak。
