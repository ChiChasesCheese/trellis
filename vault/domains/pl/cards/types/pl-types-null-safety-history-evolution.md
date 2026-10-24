---
id: pl-types-null-safety-history-evolution
node: types.null-safety
type: qa
step: 11
---
## Q
空值的设计是怎样演变的？今天的主流语言为什么都在给类型系统加上「可空」的区分？

## A
1965 年 ALGOL W 引入空引用，之后的 C、C++、Java、C# 都继承了它。2009 年 Hoare 公开反思，这之后新一代语言几乎一致地把缺失放进类型：

- Rust（2015）：`Option<T>`，安全代码里没有 `null`。
- C++（2017）：库类型 `std::optional`（可能没有值的容器类型），语言本身保留空指针；C++ 的第一道防线是「引用不能为空」（1980 年代就有），标准不强制检查，也没有向 `Option` 那样让编译器逼你处理。
- Swift（2014）：`Optional`，语法上写成 `String?`，必须显式解包。
- Kotlin（2016）：类型分为 `String` 和 `String?`，编译器追踪流程中的空检查。
- TypeScript：打开 `strictNullChecks` 后 `null` 和 `undefined` 不能赋给普通类型。
- C# 8（2019）：可空引用类型，用警告的方式向老代码渐进引入。
- Python 3.10：`X | None` 的写法（PEP 604）让可选类型在注解里更简洁，检查由 `mypy` 之类的工具执行。

Java 的路线是渐进补救：Java 8（2014）引入 `Optional`，只作为返回值的约定；社区的 JSpecify 注解尝试统一 `@Nullable` 的语义；语言层面则在研究「空值受限类型」等方向，与值类型的工作一起推进。Go 没有改变 `nil`，它的做法是靠零值和惯例缩小危害。

趋势的原因是经济账：空指针错误的修复成本远高于编译期多写几个 `match`；而当代码库变大、人员流动时，「靠约定记住谁可能为空」不可持续。把约定变成编译器能检查的类型，是少数几乎没有争议的语言演进方向。
