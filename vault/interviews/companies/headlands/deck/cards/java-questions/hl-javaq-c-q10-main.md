---
id: hl-javaq-c-q10-main
node: java-questions.c-languages
type: qa
step: 13
---
## Q
Java 泛型和 C++ 模板有什么区别？什么是类型擦除（type erasure），代价是什么？
How do Java generics differ from C++ templates? What is type erasure and what does it cost?

## A
一句话：C++ 模板**为每个类型实例化一份代码**；Java 泛型在编译期检查，运行时**擦除**成 `Object`，所以泛型容器不能装原始类型（要装箱），运行时也没有 `T`——这就是 `List<Integer>` 比 `int[]` 慢且占内存的原因。

- C++ `vector<int>`：编译后专为 `int` 生成代码，元素是 4 字节连续排列。
- Java `List<Integer>`：擦除成 `List`（元素类型 `Object`），内存是 `[ref][ref][ref]...`，每个 ref 指向堆上一个 `Integer` 对象（16 字节）。
- 热路径上优先用 `int[]` / `long[]` 或第三方原始类型集合；根本解法是 Valhalla 的值类，21 里还没有。
