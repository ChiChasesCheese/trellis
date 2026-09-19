---
id: kafka-streams-async-microservice-requirements
node: streams.choosing-framework
type: qa
step: 3
source: kafka-2e
---
## Q
要用流式处理框架给异步微服务（负责执行大型业务流程里某个简单操作，比如更新库存信息）搭建本地状态缓存，这个框架至少需要具备哪两项能力，分别解决什么问题？

## A
第一，需要能与消息总线（最好就是 Kafka 本身）集成，并具备变更捕获（CDC，change data capture）能力，这样上游数据源的变更才能被实时同步进来，用来持续更新微服务自己维护的本地缓存，避免缓存数据过时。第二，需要支持本地存储，把它当作这个微服务数据的缓存和物化视图使用，这样微服务在处理请求时可以直接读本地缓存获得低延迟响应，而不用每次都远程查询上游系统。
