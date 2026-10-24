---
id: pl-testing-found-junit-rust
node: engineering.testing
type: qa
step: 4
---
## Q
Java 的 JUnit 5 和 Rust 内置的测试框架在组织方式上有什么不同？Rust 的单元测试、集成测试、文档测试怎样分工？

## A
**Java**：JUnit 5 是外部库，由 Maven 或 Gradle 引入。测试类放在单独的源集 `src/test/java`，目录与生产代码镜像，不会进入发布产物。用注解驱动：`@Test` 标记用例，`@ParameterizedTest` 做参数化，`@BeforeEach` 做准备，`@ExtendWith` 挂扩展（Spring、Mockito 等都用这个机制）。测试由构建工具触发。

**Rust**：测试是语言加 Cargo 的内置能力，不需要任何依赖，分三类：
1. **单元测试**：写在被测文件里的 `#[cfg(test)] mod tests`，用 `#[test]` 标记。因为在同一模块内，能测试私有函数；`cfg(test)` 保证它不进入发布构建。
2. **集成测试**：`tests/` 目录下每个文件被编译成一个独立 crate，只能用公开 API，相当于外部用户的视角。
3. **文档测试**：文档注释里的代码块也会被编译并运行，保证示例不会过期。

`cargo test` 一次跑完三类，真实输出（节选）：

```text
Running unittests src/lib.rs    test tests::doubles ... ok
Running tests/api.rs            test public_api ... ok
Doc-tests t2                    test src/lib.rs - double (line 3) ... ok
```

**背后的取舍**：Rust 把测试当作工具链的一等公民，标准化、零依赖；单元测试与实现同文件，鼓励二者一起演进。Java 的做法反映企业软件的文化：生产代码与测试代码分离，框架可替换、可扩展，换来的是更丰富的生态（参数化、扩展、IDE 支持），也带来更多配置。
