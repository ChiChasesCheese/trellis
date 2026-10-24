---
id: pl-cpp-safety-found-guidelines-profiles
node: cpp.safety
type: qa
step: 4
---
## Q
C++ Core Guidelines、GSL 和 profiles 提案各是什么？它们和 Rust 的"安全子集"思路有什么共同点和差别？

## A
**C++ Core Guidelines**：由 Bjarne Stroustrup 和 Herb Sutter 主持、开源社区维护的编码规则集合，每条规则有编号（如 R.11 "避免显式 `new` 和 `delete`"）和理由。它的目标是定义一个"**现代 C++ 的安全子集**"：只要遵守规则，类型安全和资源安全可以得到保证。规则分类：接口（I）、函数（F）、类（C）、资源管理（R）、表达式（ES）、并发（CP）、错误处理（E）等。

**GSL（Guidelines Support Library）**：配套的小库，提供规则里要用的类型：
- `gsl::not_null<T*>`：保证非空的指针；
- `gsl::owner<T*>`：标记"这个裸指针拥有对象"（给分析工具看）；
- `gsl::span`：后来进入标准成为 `std::span`；
- `gsl::finally`：作用域退出时执行代码。

**怎样执行规则**：靠工具。`clang-tidy` 的 `cppcoreguidelines-*` 检查组，MSVC 的 Core Check，编译器的警告（如 clang 的 `-Wdangling-gsl`，在本机能捕获 `string_view` 指向即将销毁的临时 `string`）。违反规则不是编译错误，是静态分析警告。

**profiles 提案**：把"安全子集"做成语言机制。思路：定义若干 profile（类型安全、边界安全、生命周期安全等），源码声明启用某个 profile 后，编译器**强制**其规则，对违规写法报错；不能静态检查的地方插入运行时检查。目标是**渐进采用**：不改变现有语法，一个文件、一个模块一个模块地启用。截至 C++26，profiles 仍是提案/研究方向，**没有成为已发布标准的一部分**。

**和 Rust 的对比**：
- **共同点**：都是"限定一个安全子集，再用工具/编译器强制"；Rust 的 safe Rust 就是安全子集，`unsafe` 是出口。
- **差别 1：强制力**。Rust 的规则由编译器**强制**，无法绕开（除了 `unsafe`）；C++ Core Guidelines 是**可选**的，靠 CI 里的静态分析；
- **差别 2：证明力**。Rust 的借用检查器有完整的生命周期信息（函数签名里的标注），能做局部证明；C++ 没有这些标注，分析器只能启发式地猜，漏报和误报都有；
- **差别 3：兼容**。profiles 想让旧代码也能逐步启用，Rust 的规则要求代码从一开始就按所有权设计。

**社区还讨论过更激进的方案**：给 C++ 增加类似 Rust 的借用检查（"Safe C++" 一类提案），能给出更强的保证，但意味着新的语言子集和大量标准库重做；委员会没有选择这个方向。

**要记住的一点**：Core Guidelines 是规则，GSL 是工具类型，profiles 是想让编译器强制规则的未来方案；今天能用的是前两者加静态分析。
