---
id: hl-javaq-c-q10-costs
node: java-questions.c-languages
type: qa
step: 14
---
## Q
Java 泛型类型擦除带来哪几项后果（成本与好处）？100 万个整数用 `int[]` 和 `ArrayList<Integer>` 各占多少字节？

## A
1. **装箱成本**：100 万元素，`int[1M]` = **4,000,016 字节**；`ArrayList<Integer>`（含 100 万个 `Integer` 对象）= **20,000,208 字节**，约 5 倍。
2. **没有运行时类型信息**：不能 `new T()`、`T[]`、`instanceof List<String>`；用 `Class<T>` token 或 `Supplier<T>` 绕。
3. **不能用原始类型做类型参数**：所以有 `IntStream`、fastutil 的 `Int2IntMap` 等专门版本。
4. **好处**：二进制兼容、没有代码膨胀、字节码大小稳定。
5. Valhalla（值类对象 + 泛型特化）正是为此而做，21 里还没有。
