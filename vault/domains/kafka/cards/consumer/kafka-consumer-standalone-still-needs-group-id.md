---
id: kafka-consumer-standalone-still-needs-group-id
node: consumer.standalone
type: qa
step: 3
source: kafka-2e
---
## Q
使用独立消费者（不调用 `subscribe()`）时，还需不需要配置 `group.id`？为什么？

## A
仍然需要配置 `group.id`。虽然不调用 `subscribe()` 就不会让这个消费者加入任何消费者群组、也不会经历再均衡，但提交偏移量（比如调用 `commitSync()`）时依然要归属到某个群组 ID 下保存进度，所以 `group.id` 这个配置项还是必须设置的，只是它不再用于分区分配和再均衡。
