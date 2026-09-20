---
id: patterns-simple-factory-enough
node: patterns.creational
type: qa
---
## Q
为什么 Simple Factory（不是 Factory Method）对许多 LLD 场景来说已经足够？

## A
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
