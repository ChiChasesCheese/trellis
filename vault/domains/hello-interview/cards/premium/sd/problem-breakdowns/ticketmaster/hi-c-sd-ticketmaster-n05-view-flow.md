---
id: hi-c-sd-ticketmaster-n05-view-flow
node: sd.problem-breakdowns.ticketmaster.notes
type: qa
step: 5
---
## Q
**票务系统 · 查看活动的流程**｜摘要 · 必会

用户打开一个活动页时，请求经过哪些组件？

## A
- **活动页内容：** 活动名称和描述、场馆位置、时间、表演者信息，关键是显示座位可用情况的座位图。
- **组件：** 客户端；API 网关（入口，路由请求，也处理认证、限流、日志）；活动服务（Event Service，读取活动、场馆、表演者信息）；活动数据库（Events DB，存活动、表演者、场馆表）。
- **流程：** 客户端发 REST GET 带 eventId；API 网关转给活动服务；活动服务查数据库并返回给客户端。
- **规划方法：** 按功能需求逐个推进，先满足功能，再用非功能需求引导深入。
