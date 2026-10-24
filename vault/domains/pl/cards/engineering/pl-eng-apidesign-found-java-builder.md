---
id: pl-eng-apidesign-found-java-builder
node: engineering.api-design
type: qa
step: 3
---
## Q
Java 为什么需要构建器（builder）模式？构建器和 `record` 怎样配合，校验应该放在哪里？

## A
Java 有方法重载，却没有默认参数和命名参数。想让一个有 3 个必填、5 个可选字段的对象易用，只有两条老路：

1. **重叠构造器**（telescoping constructors）：`Server(addr)`、`Server(addr, timeout)`、`Server(addr, timeout, retries)`……组合爆炸，调用处 `new Server(":8080", null, 0, true)` 完全看不懂每个值是什么；
2. **JavaBean 风格**：无参构造器加一串 setter。对象在构造完成前处于**半初始化**状态，可变，也无法保证不变式。

**构建器**把两者的缺点都避开：必填项放构造器，可选项用链式命名方法，最后 `build()` 一次产出一个**完整且不可变**的对象。校验集中在一处：
```java
record Server(String addr, Duration timeout, int retries) {
    Server { if (retries < 0) throw new IllegalArgumentException("retries < 0"); }
    static Builder builder(String addr) { return new Builder(addr); }
    static class Builder { /* fields with defaults, chained setters, build() */ }
}
// builder(":8080").build()                      -> Server[addr=:8080, timeout=PT30S, retries=3]
// builder(":8080").timeout(Duration.ofSeconds(2)).retries(0).build() -> ... PT2S, retries=0
// builder(":8080").retries(-1).build()          -> IllegalArgumentException: retries < 0
```
`record`（Java 16 起）自动生成构造器、访问器、`equals`、`hashCode`、`toString`，并默认不可变；**紧凑构造器**（compact constructor）是放校验逻辑的地方，无论对象怎么构造（构建器、反序列化、直接 `new`）都会经过它。

**为什么这是 Java 的地道写法**：Java 的价值观是显式和可预测：对象一旦构造就应当合法且不变。构建器用一点样板换来可读的调用处（`.timeout(...)`、`.retries(...)` 自带名字）和无半初始化对象。IDE 和 Lombok 的 `@Builder` 减轻了样板。

**不要滥用**：字段只有两三个且都必填时，直接用构造器或静态工厂方法（`Duration.ofSeconds(2)`）更清楚；构建器适合“可选项多、会增长”的类型。
