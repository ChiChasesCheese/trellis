---
id: kafka-consumer-fetch-max-wait-ms-with-fetch-min-bytes
node: consumer.poll-config
type: qa
step: 2
source: kafka-2e
---
## Q
如果同时设置了 `fetch.min.bytes=1MB` 和 `fetch.max.wait.ms=100`，broker 在什么情况下会提前返回数据，而不是一直等到凑够1MB？

## A
这两个参数是「哪个条件先满足就按哪个来」的关系：只要累计数据达到 `fetch.min.bytes` 指定的量（这里是1MB），broker 就会立刻返回；如果一直没攒够，最多等到 `fetch.max.wait.ms` 指定的时间（这里是100毫秒）后，也会把当前已有的数据（哪怕不到1MB）返回给消费者。这样 `fetch.max.wait.ms` 就为「用 fetch.min.bytes 换吞吐量」设了一个延迟上限，避免消费者被无限期地晾着。
