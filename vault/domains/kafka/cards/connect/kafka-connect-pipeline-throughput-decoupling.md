---
id: kafka-connect-pipeline-throughput-decoupling
node: connect.pipeline-design
type: qa
source: kafka-2e
---
## Q
如果生产者写入 Kafka 的速度突然远超消费者处理数据的速度，为什么不需要在管道里实现复杂的回压（backpressure）机制来协调两端？

## A
因为 Kafka 把生产者和消费者的吞吐量也解耦了：生产者写入的数据会先积压保存在 Kafka 里，而不是直接冲击消费者，等消费者的处理能力追上来之后再慢慢消化这些积压数据即可。生产者端和消费者端还可以各自独立地动态扩缩容（比如单独增加消费者实例）来应对吞吐量的变化，不需要精细协调两端的处理节奏。这也是为什么用 Kafka 做数据管道时通常不用太担心突发流量的伸缩性问题——一般规模的集群本身就能支撑很高的吞吐量。
