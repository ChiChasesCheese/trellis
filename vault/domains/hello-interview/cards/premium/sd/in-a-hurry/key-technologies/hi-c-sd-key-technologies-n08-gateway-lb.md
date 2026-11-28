---
id: hi-c-sd-key-technologies-n08-gateway-lb
node: sd.in-a-hurry.key-technologies.notes
type: qa
step: 8
---
## Q
**关键技术 · API 网关与负载均衡器**｜摘要 · 必会

API 网关和负载均衡器各自负责什么？图里要不要画？L4 和 L7 怎么选？

## A
- **API 网关：** 站在系统最前面，把请求（如 `GET /users/123`）路由到对应的后端服务，并统一处理认证、限流、日志等横切关注点。产品设计题几乎都值得画成客户端的第一站；面试官很少深挖它，更想问和题目相关的细节。常见：AWS API Gateway、Kong、Apigee，也可以是 nginx 或 Apache。
- **负载均衡器：** 只要有多台机器能处理同一类请求就需要它，把流量摊开，避免单机过载或形成热点。面试里当黑盒；不必给每个服务都画一个，只在最前面画一个，或者口头说"服务已水平扩展"。
- **L4 还是 L7：** 有 WebSocket 这类持久连接，倾向 L4（按连接转发，连接长期保持）；其他情况用 L7（看得懂 HTTP，能按路径路由到不同服务，还能收拢下游连接数），更灵活。有时还需要粘性会话（sticky sessions）。
- **常见产品：** AWS ELB、NGINX、HAProxy；极端流量下专用硬件更强，但那是网络工程的范畴。
