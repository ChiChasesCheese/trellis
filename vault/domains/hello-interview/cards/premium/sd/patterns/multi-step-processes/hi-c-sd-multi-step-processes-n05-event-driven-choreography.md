---
id: hi-c-sd-multi-step-processes-n05-event-driven-choreography
node: sd.patterns.multi-step-processes.notes
type: qa
step: 5
---
## Q
**多步流程 · 事件驱动的编舞怎么运转**｜摘要 · 必会

用事件日志（如 Kafka）驱动订单流程，具体怎么流转，补偿怎么走？

## A
- **思路：** 不再保存"当前状态"，而是保存导致当前状态的事件流，工作者对事件作出反应来推进流程。常用持久日志，Kafka 是常见选择，Redis Streams 有些场景也行。
- **与事件溯源（event sourcing）的关系：** 事件溯源把日志当唯一事实来源并由它推出状态；这里主要用日志协调工作，两者常一起出现但不是必须。
- **流转：** API 服务只是薄薄的入口，收到订单发出 `OrderPlaced`。支付工作者看到后调用支付服务，回调到来后发 `PaymentCharged` 或 `PaymentFailed`；库存工作者看到 `PaymentCharged` 后发 `InventoryReserved` 或 `InventoryFailed`。
- **补偿同样靠事件，只是倒着走：** 支付工作者也订阅 `InventoryFailed`，收到后退款并发出 `PaymentRefunded`。
- **存储的双重角色：** 既是系统的完整历史，也是推动下一步的触发器。
