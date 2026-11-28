---
id: hi-sdx-arch-registry-compat-order
node: more.architecture
type: qa
step: 6
---
## Q
**兼容模式决定上线顺序**｜补充 · 服务架构：微服务、服务发现、Serverless · 追问

面试官：「事件的 schema 放在 schema registry 里，兼容模式选 BACKWARD、FORWARD 还是 FULL？它们各规定了谁先升级？Kafka 上为什么默认用 BACKWARD？」

## A
**结论。** BACKWARD（新 schema 能读旧数据）要先升级消费者，再升级生产者；FORWARD（旧 schema 能读新数据）先升级生产者；FULL 两边都满足，顺序随意。Kafka 默认 BACKWARD，因为消费者要能重读日志里的旧事件；registry 在发布或 CI 阶段就拒绝不兼容的新版本。

**要点。**
- **BACKWARD：** 新消费者读旧数据，所以消费者先升。
- **FORWARD：** 旧消费者读新数据，所以生产者先升；旧消费者必须忽略不认识的字段。
- **FULL：** 新旧版本同时在线最安全，滚动发布时不用管顺序。
- **默认不是传递的：** BACKWARD 只和上一个版本比。要保证能重放日志里所有历史版本写下的数据，用 BACKWARD_TRANSITIVE，和全部历史版本比。
- **安全的改动：** 新增带默认值的可选字段；不删除、不改名、不改类型、不复用字段编号。

**为什么。** 兼容模式回答的是「哪一端先见到新格式」。让 registry 机械地检查，比靠代码评审可靠得多。

**面试里这样说。** 「我用 BACKWARD：先升消费者再升生产者，新版本只加带默认值的可选字段。如果需要从头重放整条日志，就用 BACKWARD_TRANSITIVE，让新版本和所有历史版本都兼容，检查放在 CI 里。」

**易错。**
- **以为 BACKWARD 能读所有历史：** 它只保证相邻版本；跳过几个版本的旧数据可能读不了。
- **FORWARD 下先升消费者：** 旧生产者写出的数据新消费者未必能读。
