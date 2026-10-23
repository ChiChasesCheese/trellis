---
id: hft-java-at-hft-interop-schema
node: java-at-hft.interop
type: qa
step: 1
---
## Q
C++ 和 Java 组成的交易系统，怎样共享消息格式而不用在两边各写一遍解析代码？

## A
用共享的 **schema**。例如 SBE（Simple Binary Encoding）用一份 XML 文件描述消息的字段、类型和顺序，代码生成器同时输出 C++ 和 Java 的编解码器。

因为二进制布局是固定的（定长字段在固定偏移、字节序一致），两边读到的是同一个偏移上的同一个值：订单消息的价格字段在偏移 8，不管是 C++ 还是 Java，都是 `getLong(offset + 8)`。两边都是 flyweight 风格，没有解析阶段、没有分配。

好处：schema 是唯一的真相来源，改了之后两边重新生成，不兼容会在编译期暴露；比文本的 FIX 或需要解码成对象的格式快得多。
