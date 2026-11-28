---
id: hi-c-sd-dynamodb-n13-security
node: sd.deep-dives.dynamodb.notes
type: qa
step: 18
---
## Q
**DynamoDB · 安全：只需说这三点**｜摘要 · 追问

面试里需要提 DynamoDB 的哪些安全能力？该讲多深？

## A
- **加密：** 静态数据默认加密；所有 API 调用强制 TLS，传输加密，无需额外配置。
- **访问控制：** 与 IAM 集成，通过策略精细控制谁可以对哪些数据做什么操作。
- **网络：** 可通过 VPC 终端节点（endpoint）从 VPC 内访问，流量不经过公网。
- **讲多深：** 涉及敏感用户数据时点一下"默认静态加密、传输走 TLS"就够，再往下讲基本是多余。
