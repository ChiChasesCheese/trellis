---
id: patterns-simple-factory-enough
node: patterns.creational
type: qa
---
## Q
In a machine-coding round you need to create the right `Vehicle` subtype from an input string. Do you reach for factory method, or something simpler?

## A
A **simple (static) factory** — one function with the type switch — is the right first move:

```java
static Vehicle of(String type) {
    return switch (type) {
        case "car"  -> new Car();
        case "bike" -> new Bike();
        default -> throw new IllegalArgumentException(type);
    };
}
```

- It centralizes the only `switch` on type in one place; callers stay decoupled from concretes.
- Upgrade to a **registry map** (`Map<String, Supplier<Vehicle>>`) when new types must be added without editing the switch, and to **factory method** only when *creation itself* must vary per subclass of the creator.
- Saying "simple factory now, registry if types grow" scores better than pattern-dropping GoF names.

## Q zh
为什么 Simple Factory（不是 Factory Method）对许多 LLD 场景来说已经足够？

## A zh
Simple Factory 是一个**单一类或方法**，根据输入参数创建对象：

```java
class ShapeFactory {
    static Shape create(String type) {
        if (type.equals("circle")) return new Circle();
        // ...
    }
}
```

**优点**：
- 集中、可读。
- 无需 Factory Method 接口或子类。
- 对于**预定数量的固定类型**足够。

**何时足够**：
- 选择的集合**不改变**（shape types、数据库驱动程序）。
- 不需要**各种创建策略**（例如，不是「XML 工厂」和「JSON 工厂」）。

**何时不足**：
- 想让**客户端定义创建**（框架插件）。
- 多个**独立产品系列**需要协调。

面试偏好：从 Simple Factory 开始；如果问题扩展，升级到 Factory Method 或 Abstract Factory。
