---
id: hi-c-sd-api-gateway-n09-managed
node: sd.deep-dives.api-gateway.notes
type: qa
step: 9
---
## Q
**API 网关 · 托管网关产品：各自擅长什么**｜摘要 · 必会

云厂商的托管网关有哪些？它们各自的特点和总体取舍是什么？

## A
- **总体取舍：** 全托管、与自家云集成好、几乎不用运维，是最省事的选择，也是最贵的。
- **AWS API Gateway：** 支持 REST 与 WebSocket；内置请求限流、API key 与用量计划，能直接触发 Lambda，用 CloudWatch 监控。
- **Azure API Management：** OAuth 与 OpenID Connect 支持强，用策略配置行为，带开发者门户和 API 文档。
- **Google Cloud Endpoints：** 与 GCP 深度集成，gRPC 支持好，自动生成 OpenAPI 文档。
- **面试说法：** 说"用云厂商的托管网关"即可，不必逐个比较。
