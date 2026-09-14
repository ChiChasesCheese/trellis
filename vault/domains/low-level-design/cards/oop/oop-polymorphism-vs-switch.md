---
id: oop-polymorphism-vs-switch
node: oop.pillars
type: qa
---
## Q
When do you replace a switch-on-type with polymorphism — and when is keeping the switch the better design?

## A
- **Replace** when the same type-switch recurs in several places and new variants keep arriving: one class per variant localizes each addition to one file (this is OCP in action).
- **Keep** a single exhaustive switch over a closed enum in one place: the compiler flags missing cases, and class-per-variant there is speculative generality.

Count the switch sites and the expected variants before reaching for the hierarchy.

## Q zh
什么时候该把 switch-on-type 换成多态——什么时候保留 switch 反而是更好的设计？

## A zh
- **该换**：同一个类型 switch 在多处重复出现，而且新变体还在不断加进来 —— 每个变体一个类，能把每次新增都收敛到一个文件里（这就是 OCP 的实际形态）。
- **该留**：只有一处、针对封闭 enum 的穷尽 switch —— 编译器会替你标出漏掉的分支，这种情况下每个变体建一个类属于 speculative generality。

伸手去建层次结构之前，先数两个数：switch 出现了几处，预期会有多少变体。
