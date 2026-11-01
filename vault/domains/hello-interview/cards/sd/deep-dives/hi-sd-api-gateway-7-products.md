---
id: hi-sd-api-gateway-7-products
node: qb.sd.distributed-rate-limiter.pre-sd-deep-dives-api-gateway
type: qa
step: 7
---
## Q
**网关选型：托管还是开源**｜系统设计 · 深入技术

常见的 API 网关产品有哪些？托管服务与开源方案各自的取舍是什么？

## A
**托管服务。** 云厂商全托管，集成好但最贵。
- AWS API Gateway：支持 REST 与 WebSocket，内置限流、API key 与用量计划、Lambda 集成、CloudWatch 监控
- Azure API Management：OAuth 与 OpenID Connect 支持强，策略式配置，带开发者门户
- Google Cloud Endpoints：深度集成 GCP，gRPC 支持强，自动生成 OpenAPI 文档

**开源。** 想要更多控制或本地部署时用。
- Kong：基于 NGINX，插件生态丰富
- Tyk：原生支持 GraphQL，自带分析，多数据中心
- Express Gateway：Node.js 实现，轻量

**说法。** 面试里一般说「用托管网关或 Kong」即可，不必比较细节。
