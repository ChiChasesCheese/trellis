---
id: hi-c-sd-discord-messages-scylladb-b03-singleflight
node: sd.in-the-wild.discord-messages-scylladb.beyond
type: qa
step: 3
---
## Q
**Discord 消息存储 · 请求合并（singleflight）的通用性与陷阱**｜拓展 · 加分

请求合并还在哪些地方出现？实现时有哪些坑？

## A
- **同一个想法有很多名字：** Go 标准扩展库里的 `singleflight`，CDN 与反向代理里的请求折叠（request collapsing，如 Varnish、Nginx 的缓存锁），缓存防击穿的"互斥重建"。共同点是：同一个键的重复工作只做一次。
- **坑一，错误共享：** 第一个请求失败了，所有等待者一起失败；要考虑是否对等待者重试一次。
- **坑二，取消与超时：** 发起查询的那个调用方取消了，不应让后面的等待者也被取消；查询要独立于第一个调用方的生命周期，带自己的超时。
- **坑三，键要选对：** 键必须包含所有影响结果的参数（用户权限、分页游标），否则会把一个人能看的结果给了另一个人。
- **坑四，内存：** 进行中映射必须在完成或失败后清理，防止泄漏。
