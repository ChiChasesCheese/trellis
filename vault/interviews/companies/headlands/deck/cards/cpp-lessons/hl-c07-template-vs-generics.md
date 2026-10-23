---
id: hl-c07-template-vs-generics
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 1
---
## Q
面试问：C++ 模板和 Java 泛型有什么区别？
Interview question: How do C++ templates differ from Java generics?

## A
- **Java**：泛型编译后**擦除**为 `Object`。`List<Integer>` 里是装箱对象的引用，运行时没有 `T`，不能 `new T()`，不能用基本类型；单份代码。
- **C++**：对每个实际用到的类型**生成一份专门的代码**（实例化，monomorphisation）。`vector<int>` 是真正连续的 `int`；`T` 在编译期完全已知，可内联，可用基本类型，可用**非类型参数**（如数组大小），支持特化。
- 代价：**代码膨胀**、**编译慢**、**报错信息长**。
- 零开销抽象：全部在编译期解析，没有虚表、没有装箱，与手写特化版本等价。
