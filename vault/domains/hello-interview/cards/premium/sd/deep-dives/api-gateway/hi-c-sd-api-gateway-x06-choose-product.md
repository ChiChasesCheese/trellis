---
id: hi-c-sd-api-gateway-x06-choose-product
node: sd.deep-dives.api-gateway.exam
type: qa
step: 6
---
## Q
**API 网关 · 托管还是开源**｜考点 · 追问

一个 5 人创业团队，全部系统跑在 AWS 上，流量不大；另一家公司有合规要求，必须在自有机房部署，并需要自定义鉴权插件。分别该选哪类网关？为什么？

## A
- **创业团队选 AWS API Gateway：** 全托管，不用运维，与 Lambda、CloudWatch 直接集成，流量小时按量计费也便宜；缺点是按请求计费，流量很大时会变贵，且被云厂商绑定。
- **合规公司选开源（如 Kong）：** 能在自有机房运行，用插件机制写自定义鉴权，没有云依赖；代价是自己运维、升级和扩容。
- **判断依据：** 团队运维能力、合规与部署位置、流量规模决定的成本曲线，以及对定制化的需求。
- **2026 亮点：** 网关跑在 Kubernetes 上时，入口层的标准接口是 Gateway API（v1 GA）而不是 Ingress：基础设施方管 GatewayClass，集群运维管 Gateway（监听、TLS、允许挂路由的 namespace），业务团队在自己的 namespace 写 HTTPRoute/GRPCRoute，用权重字段做灰度分流；Ingress NGINX 已在 2026 年 3 月退役，不再有安全补丁，不要再当默认方案。代价是迁移不是一对一替换，各实现对扩展特性的支持程度不同。
