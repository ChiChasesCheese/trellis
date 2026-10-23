---
id: hl-cq-q22-macros-guarantee-crtp-virtual
node: cpp-questions.e-templates
type: qa
step: 14
---
## Q
三个追问：`constexpr` 相比宏有什么好处？`constexpr` 能保证编译期求值吗？CRTP 和虚函数怎么选？

## A
- **对比宏**：`constexpr` 有类型、有作用域、可调试、能用在模板里，应优先于 `#define`。
- **不保证**：只有在需要常量表达式的地方才一定编译期求值；要强制，用 `consteval`，或把结果赋给一个 `constexpr` 变量。
- **CRTP vs virtual**：类型静态已知的热路径用 CRTP；类型只在运行期才知道，或需要异构容器时用虚函数。
