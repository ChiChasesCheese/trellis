---
id: hi-c-sd-key-technologies-b04-cdn-private
node: sd.in-a-hurry.key-technologies.beyond
type: qa
step: 4
---
## Q
**关键技术 · CDN 缓存私有内容与更新内容**｜拓展 · 加分

付费视频要经 CDN 分发，只有买了的人能看；同时文件更新后用户要马上看到新版本。CDN 怎么处理这两件事？

## A
- **私有内容：** 用带签名和过期时间的 URL（或签名 Cookie）。CDN 边缘校验签名，通过才返回缓存内容；链接过期后即失效。比每次回源鉴权省源站压力。
- **更新内容的两种办法：** ① 主动失效（purge / invalidation），通知 CDN 删掉某路径；有传播延迟，且通常按次数或路径收费，量大时贵。② 版本化文件名（内容哈希放进路径，如 `app.3f9a.js`），新版本是新 URL，旧缓存自然不再被访问，不需要失效。
- **选择：** 静态资源首选版本化文件名，TTL 可以设得很长；HTML 入口之类不能改名的，用短 TTL 或失效。
