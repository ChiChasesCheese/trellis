---
id: principles-hierarchy-explosion
node: principles.composition
type: qa
---
## Q
Coffee add-ons modeled as subclasses: `CoffeeWithMilk`, `CoffeeWithMilkAndSugar`, `CoffeeWithSoyMilkAndSugar`... Why does this hierarchy rot, and what's the composition fix?

## A
- **Combinatorial explosion**: n independent add-ons ⇒ up to 2^n subclasses, because inheritance forces all variation axes into one tree.
- Every base change ripples through the tree (fragile base class).

Fix: make the varying dimension a composed object — decorators wrapping a `Beverage`, or a list of `AddOn` components. Composition lets independent axes vary independently.

## Q zh
把咖啡的配料建模成子类：`CoffeeWithMilk`、`CoffeeWithMilkAndSugar`、`CoffeeWithSoyMilkAndSugar`……这个层次为什么会腐烂，用组合怎么修？

## A zh
- **组合爆炸**：n 个相互独立的配料 ⇒ 最多 2^n 个子类，因为继承把所有变化轴都硬塞进了同一棵树。
- 基类的每次改动都会沿树扩散（fragile base class）。

修法：把那个变化的维度变成被组合进来的对象 —— 用 decorator 包住一个 `Beverage`，或者持有一组 `AddOn` 组件。组合让相互独立的轴能够独立变化。
