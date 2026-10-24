---
id: pl-data-serialization-intro-java
node: data.serialization
type: qa
step: 4
---
## Q
Java 有哪两条序列化路线：内建的 `Serializable` 和以 Jackson 为代表的 JSON 库？它们的工作方式和风险有何不同？

## A
**Jackson（和 Gson 等）**：Java 生态里 JSON 的事实标准。`ObjectMapper` 通过反射读 getter/字段，用注解（如 `@JsonProperty("user_id")`、`@JsonIgnore`）定制键名和是否输出，反序列化时用反射创建对象并填充字段。与 Go 的 `encoding/json` 同类，但功能更丰富：多态类型、自定义序列化器、流式 API。Spring Boot 默认用它。

**`java.io.Serializable`（内建二进制序列化）**：一个类只要声明 `implements Serializable`，就可以用 `ObjectOutputStream` 写出整个对象图（含类名、字段、引用关系），用 `ObjectInputStream.readObject()` 读回。这是 Java 1.1 的老机制，RMI、早期会话复制都依赖它。

**它的两个特性使它成为安全问题的根源**：
1. **读取时由数据决定创建哪个类**。流里写着类名，`readObject()` 就去加载并实例化它，然后调用它的 `readObject` 回调。只要类路径上有某个类的回调里存在危险操作，攻击者就能构造一个字节流触发它（反序列化小工具链，gadget chain）。
2. **绕过构造函数**。对象是由运行时直接填字段创建的，构造函数里的校验不会执行。

结论：Java 从 JDK 9 起提供 `ObjectInputFilter`（反序列化类白名单），但业界的共识仍然是**不要把 `Serializable` 用作数据交换格式**。

**要记住的一点**：Java 同时拥有最灵活（Jackson 的反射加注解）和最危险（内建序列化）的两个极端，选哪个基本决定了你有没有序列化漏洞。
