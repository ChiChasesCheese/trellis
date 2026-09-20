---
id: patterns-factory-method-vs-abstract-factory
node: patterns.creational
type: qa
---
## Q
Factory Method vs Abstract Factory——两者都隐藏创建。什么时候你选择哪一个？

## A
- **Factory Method**：一个类中的**一个** `create()` 方法或接口方法。用于创建**一个产品系列**（如 `PDFGenerator.create()`）。简单、单一职责。
- **Abstract Factory**：跨多个产品**系列**的**许多**工厂方法。用于**互相关联的产品组**（如 UIComponentFactory 有 `createButton()`、`createTextBox()` 等）。

简单的启发式：
- 需要选择**一个产品类型**？→ Factory Method。
- 需要创建**多个相关产品**并确保它们来自**同一系列**（主题、平台、风格）？→ Abstract Factory。
