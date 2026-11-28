---
id: hi-c-sd-dynamodb-x10-choose-db
node: sd.deep-dives.dynamodb.exam
type: qa
step: 10
---
## Q
**DynamoDB · DynamoDB 还是 PostgreSQL**｜考点 · 追问

(1) 电商后台需要按任意字段组合筛选订单、做销售报表；(2) 一个会话存储，按会话 ID 读写，峰值每秒 50 万次；(3) 一个中小团队的用户和订单系统，数据量 200 GB，查询模式多变。分别选 DynamoDB 还是 PostgreSQL？

## A
- **(1) PostgreSQL：** 即席筛选、聚合和 JOIN 是关系库强项，DynamoDB 只能走预先设计好的键，大量使用 GSI 说明选错了。
- **(2) DynamoDB：** 单键读写、规模大、延迟低，按会话 ID 分区正好；每秒 50 万次要算清成本，因为按请求收费，必要时用 DAX 吸收读取。
- **(3) PostgreSQL：** 200 GB 单机轻松承载，查询模式多变时灵活性比无限扩展更重要；避免为用不上的扩展性付出建模复杂度。
- **判断顺序：** 先看查询是否固定、规模是否真的超出单机，再谈成本与是否绑定 AWS。
