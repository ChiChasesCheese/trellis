---
id: hl-j06-two-step-pain
node: java21.j06-instanceof-pattern
type: qa
step: 1
---
## Q
类型转换（cast）为什么转型前习惯先 `instanceof`？Java 8 的两步套路有哪三个痛点？

## A
`(String) o` 把引用"当作"另一类型；真实类型不符则运行时抛 **`ClassCastException`**，所以转型前先 `instanceof`。

Java 8 的固定两步（手写 `equals` 第一步）：
```java
if (!(o instanceof Price)) return false;   // 第一步：检查类型
Price other = (Price) o;                   // 第二步：转型，并再声明一个变量
```
三个痛点：
1. **类型名写两遍**，改一个忘另一个就出错；
2. **噪音**：核心意图被检查、转型、命名分散；
3. **作用域松散**：`other` 在 `if` 外也存在，却只在那一个分支里有意义。
