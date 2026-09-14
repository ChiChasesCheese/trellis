---
id: patterns-factory-method-vs-abstract-factory
node: patterns.creational
type: qa
---
## Q
Factory method vs abstract factory — what does each vary, and what's the tell for which one you need?

## A
- **Factory method** varies **one product** via an overridable creation step: subclasses (or a lambda/registry) decide which concrete class to instantiate. Tell: "callers shouldn't `new` the concrete type."
- **Abstract factory** varies a **family of related products** that must be used together (e.g. `Button` + `Checkbox` per UI theme, or connection + statement + transaction per DB vendor). Tell: "products must stay mutually consistent — never mix a Mac button with a Windows checkbox."
- An abstract factory is typically **implemented as** a set of factory methods; the pattern distinction is the *consistency-of-family* requirement, not the mechanics.

## Q zh
Factory Method vs Abstract Factory——两者都隐藏创建。什么时候你选择哪一个？

## A zh
- **Factory Method**：一个类中的**一个** `create()` 方法或接口方法。用于创建**一个产品系列**（如 `PDFGenerator.create()`）。简单、单一职责。
- **Abstract Factory**：跨多个产品**系列**的**许多**工厂方法。用于**互相关联的产品组**（如 UIComponentFactory 有 `createButton()`、`createTextBox()` 等）。

简单的启发式：
- 需要选择**一个产品类型**？→ Factory Method。
- 需要创建**多个相关产品**并确保它们来自**同一系列**（主题、平台、风格）？→ Abstract Factory。
