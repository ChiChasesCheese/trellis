---
id: pl-testing-table
node: engineering.testing
type: qa
step: 7
---
## Q
Go、Java、Rust、Python、C++ 的测试文化有什么差异？各自换来什么，代价是什么？

## A
| 语言 | 工具与风格 | 换来 | 代价 |
|---|---|---|---|
| Go | 标准库 `testing` 加 `go test`；表驱动；没有断言库；竞争检测、覆盖率、基准、fuzz 全部内置 | 零依赖，工具统一，读任何 Go 项目的测试都很相似 | 样板多，复杂断言冗长；测试替身靠手写 |
| Java | JUnit 5 加 Mockito 加构建工具；Testcontainers 起真实依赖 | 生态最成熟：参数化、扩展、IDE 支持、框架级测试支持（如 Spring） | 偏重；Mockito 容易让测试与实现细节耦合；容器化的上下文启动慢 |
| Rust | 内置 `#[test]`；单元测试同文件，`tests/` 放集成测试，文档测试 | 工具链内置，私有函数可测，编译器已经排除了一大类错误 | 无内置 mock 与参数化（靠 `mockall`、`rstest` 等 crate）；编译时间长 |
| C++ | 没有内置框架；Google Test（加 gMock）、Catch2 或 doctest，CTest 驱动；测试是链接被测库的独立可执行文件 | 灵活；可在测试构建里加 ASan/UBSan，把未定义行为变成失败 | 构建配置重；mock 要求被测代码有虚接口或模板接缝；UB 让“测试通过”不等于正确 |
| Python | pytest 加 fixture；`unittest.mock` 与 `monkeypatch`；Hypothesis | 测试写法最短；动态性使得几乎什么都能替换 | 什么都能 patch，测试容易绑定实现；类型错误要到运行时才暴露，需要更多测试兜底 |

**规律**：语言在编译期能排除的错误越多，测试越集中在**行为**上，而不是「会不会崩」。Rust 的类型和借用检查替代了很多检查空值、越界、竞争的测试；Python 恰好相反，动态性让测试承担了类型检查的一部分责任。三种文化也是三种价值观：Go 的极简（测试只是代码）、Java 的框架化（可扩展、可替换）、Python 的魔法化（最短的写法）。C++ 的位置在 Java 一侧但更碎：语言不带测试设施，多家框架并存；它的特殊之处在于测试要承担“发现未定义行为”的责任，所以好的 C++ 测试必须在 sanitizer 下运行，否则通过的测试可能只是碰巧。
