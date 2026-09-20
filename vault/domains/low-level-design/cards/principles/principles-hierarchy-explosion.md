---
id: principles-hierarchy-explosion
node: principles.composition
type: qa
step: 2
---
## Q
把咖啡的配料建模成子类：`CoffeeWithMilk`、`CoffeeWithMilkAndSugar`、`CoffeeWithSoyMilkAndSugar`……这个层次为什么会腐烂，用组合怎么修？

## A
- **组合爆炸**：n 个相互独立的配料 ⇒ 最多 2^n 个子类，因为继承把所有变化轴都硬塞进了同一棵树。
- 基类的每次改动都会沿树扩散（fragile base class，脆弱基类）。

修法：把那个变化的维度变成被组合进来的对象——用 decorator 包住一个 `Beverage`，或者让它持有一组 `AddOn` 组件的列表。组合让相互独立的轴能够独立变化，而不必为每种组合都开一个类。
