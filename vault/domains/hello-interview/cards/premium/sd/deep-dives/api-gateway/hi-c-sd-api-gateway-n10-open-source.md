---
id: hi-c-sd-api-gateway-n10-open-source
node: sd.deep-dives.api-gateway.notes
type: qa
step: 11
---
## Q
**API 网关 · 开源网关：什么时候选**｜摘要 · 追问

想自己掌控或必须本地部署时，有哪些开源网关？各有什么特点？

## A
- **何时选开源：** 要更多控制权、本地部署、避免云厂商锁定，代价是自己运维。
- **Kong：** 基于 NGINX，插件生态丰富，既能当传统网关也能配合服务网格（service mesh）部署。
- **Tyk：** 原生支持 GraphQL，自带 API 分析，能跨多数据中心。
- **Express Gateway：** 用 Node.js 写成，轻量、对开发者友好，适合 Node.js 微服务。
- **面试说法：** 点名 Kong 就够，其余了解特点即可。
