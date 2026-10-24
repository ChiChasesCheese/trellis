---
id: pl-cpp-safety-best-practice
node: cpp.safety
type: qa
step: 8
---
## Q
如果一个团队要用现代 C++ 写长期维护的服务，应当怎样分层地提高内存安全？有哪些具体的清单？

## A
**分层防御**（每层挡一类问题，叠加使用）：

**1. 写法层（预防）**
- 业务代码不出现裸 `new`/`delete`；资源用 RAII；所有权用 `unique_ptr`；
- 连续数据传 `std::span`，不传指针加长度；字符串参数用 `std::string_view`（注意寿命）；
- 容器访问在边界不确定处用 `.at()` 或确保有前置检查；
- 变量就地初始化，开启 `-ftrivial-auto-var-init=zero`（Clang/GCC，默认零初始化栈变量作为兜底）；
- lambda 逃出作用域时**按值捕获**（`[=]` 或显式 `[x = std::move(x)]`），不要按引用；
- 避免 C 风格强制转换和 `reinterpret_cast`，用 `static_cast`、`std::bit_cast`、`std::variant`。

**2. 编译层（编译器帮忙）**
- `-Wall -Wextra -Wconversion -Wshadow` 并把警告当错误；
- 开启 `-Wdangling-gsl`、`-Wreturn-stack-address`（Clang 默认或随 `-Wall`）；
- 使用 `[[clang::lifetimebound]]` 标注返回借用参数的函数；
- 栈保护、`_FORTIFY_SOURCE`、PIE/ASLR、控制流完整性（CFI）。

**3. 库层（运行时加固）**
- **生产构建开启标准库加固**：libc++ 用 `FAST` 或 `EXTENSIVE` 档；libstdc++ 用 `-D_GLIBCXX_ASSERTIONS`；
- 先在测试环境测量开销，再推广。

**4. 工具层（测试时发现）**
- CI 里固定任务：ASan+UBSan 一轮，TSan 一轮；
- 对任何解析不可信输入的代码用**模糊测试**（libFuzzer、AFL++），并在 ASan 下跑；
- `clang-tidy`（`cppcoreguidelines-*`、`bugprone-*`、`cert-*`）、`cppcheck`；
- 静态分析器（Clang Static Analyzer、CodeQL）定期扫。

**5. 架构层（缩小攻击面）**
- 把解析不可信输入的部分隔离成最小模块，必要时放进沙盒进程；
- 输入在边界处完整校验，内部再依赖前置条件；
- 新写的、攻击面大的组件优先考虑内存安全语言，边界用 C ABI 或 IDL。

**6. 流程层**
- 代码评审的检查清单里列出生命周期审查："引用或视图是否比它所指向的数据活得久"；
- 把 sanitizer/fuzz 发现的缺陷当作最高优先级，不挂 backlog。

**什么时候打破**：热路径上单点的检查开销有影响时，先量，再对该处使用 `[[assume]]` 或不检查的版本，并写测试和注释说明前置条件。

**为什么**：任何单一措施都不完整。加固不抓生命周期，sanitizer 只抓执行过的路径，静态分析有误报漏报，所以靠叠加，并让每一层自动化。
