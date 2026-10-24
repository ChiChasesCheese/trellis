---
id: pl-data-serialization-principle
node: data.serialization
type: qa
step: 1
---
## Q
序列化（serialization）解决什么问题？它的设计空间有哪些维度，四门语言各自站在哪里？

## A
**问题**：内存里的对象有指针、有语言特定的布局，不能直接写到磁盘或发到网络。要存储和传输，必须把对象变成一串字节（序列化），另一端再读回对象（反序列化）。反序列化本质上是**解析来自外部的、不可信的输入**。

**设计空间的三个维度**：
1. **格式绑定谁**：
   - 绑定语言：Java 的 `Serializable`、Python 的 `pickle`，能序列化几乎任何对象，但只有同一语言能读。
   - 与语言无关：JSON、Protocol Buffers、MessagePack，只描述数据，跨语言。
2. **需不需要 schema（模式）**：JSON 是自描述的，每个字段名都在数据里，灵活但体积大；Protocol Buffers 要先有 `.proto` 定义，字段按编号存储，小而快，也更容易演进。
3. **谁来写「对象到数据」的代码**：
   - 运行时反射读字段：Go 的 `encoding/json`、Java 的 Jackson。
   - 编译期生成：Rust 的 serde。
   - 对象自带协议：Python 的 `pickle` 让对象自己说怎么重建。

**取舍轴**：便利和通用对比安全和性能。绑定语言、自动处理一切的方案最省事，但等于允许数据决定要创建哪些对象、执行什么代码，是安全上最危险的；与语言无关、显式 schema 的方案要多写一点定义，换来可演进性和安全。

**四门语言**：Go 靠反射加 struct tag；Java 既有内建二进制序列化，又有以反射和注解为核心的 Jackson；Rust 的 serde 把「数据模型」和「格式」分开，编译期生成代码；Python 有保守的 `json` 和危险但强大的 `pickle`。
