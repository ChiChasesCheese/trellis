---
id: kafka-consumer-serializer-deserializer-must-match
node: consumer.deserialization
type: qa
step: 1
source: kafka-2e
---
## Q
生产者用 `IntSerializer` 把消息值序列化成字节数组，如果消费者用 `StringDeserializer` 去反序列化，会发生什么？为什么反序列化器必须和当初的序列化器相对应？

## A
会出错甚至得到无意义的结果，因为字节数组本身没有自描述能力，反序列化器只是按照约定好的编码方式去解析这些字节；如果解析方式和写入时用的编码方式不一致（比如整型的字节布局被当成字符串来解析），得到的 Java 对象要么解析失败抛异常，要么是一堆没有意义的乱码。所以开发者必须清楚知道某个主题里的消息是用哪种序列化器写入的，并保证消费这个主题的反序列化器与之匹配。
