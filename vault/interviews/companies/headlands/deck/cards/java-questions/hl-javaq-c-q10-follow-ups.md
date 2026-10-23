---
id: hl-javaq-c-q10-follow-ups
node: java-questions.c-languages
type: qa
step: 15
---
## Q
追问：Java 为什么选择类型擦除？能不能写一个对 `int` 不装箱的泛型方法？热路径还有什么常见追问？
Why was erasure chosen? Can you write a generic method that works on int without boxing?

## A
- **为什么擦除**：兼容旧代码和字节码，保证迁移兼容性。
- **能不能对 `int` 不装箱**：不能；只能写重载，或用 `IntBinaryOperator` 这类**原始类型特化的函数接口**。
- 常见追问：自己写 `class LongIntMap`，用**开放寻址表**存原始类型键值（避免 `HashMap<Long,Integer>` 的装箱和节点对象）。
- 口述时的数字：百万元素 `ArrayList<Integer>` 约为 `int[]` 的 5 倍内存，遍历还要追指针。
