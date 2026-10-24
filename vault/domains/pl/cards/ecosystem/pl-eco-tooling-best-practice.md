---
id: pl-eco-tooling-best-practice
node: ecosystem.tooling
type: qa
step: 9
---
## Q
资深工程师怎样配置格式化、检查和测试流程？通用规则是什么，Go、Java、Rust、Python、C++ 各自怎么落实，何时破例？

## A
**通用规则**：
1. **自动化的事不靠人**：格式化在保存或提交时自动执行；CI 只做**检查**（有差异就失败），不做修改。
2. **工具版本钉死**：格式化器和 linter 的版本不同，输出就可能不同，会造成“本地通过、CI 失败”。
3. **检查器分级**：真缺陷（正确性）是错误，风格是警告；刚引入时对旧代码用“基线”，只对新增代码严格。
4. **测试快、独立、确定**；慢测试单独分层。
5. **把警告当错误**，否则警告会无限积累。

按语言：
- **Go**：CI 里 `gofmt -l .` 输出非空就失败；`go vet ./...` 和 `go test -race ./...`；需要更多检查用 `golangci-lint` 并固定版本；表驱动测试（table-driven）是惯用法。
- **Java**：Spotless 插件接进 `mvn verify`，`spotless:check` 在 CI，`spotless:apply` 在本地；Error Prone 当编译器插件；JUnit 5 加 AssertJ；不要让检查只存在于某人的 IDE 配置里。
- **Rust**：CI 里 `cargo fmt --check`、`cargo clippy -- -D warnings`、`cargo test`；团队在 `Cargo.toml` 的 `[lints]` 表里统一 lint 等级；`cargo deny` 管依赖。
- **C++**：`clang-format` 加 `.clang-format` 进仓库，CI 里 `--dry-run -Werror`；编译用 `-Wall -Wextra -Werror`；`clang-tidy` 分级开检查；测试在 CI 里至少跑一遍 ASan 加 UBSan，涉及线程再跑 TSan；这些检查代替的是 Rust 编译器替你做的那部分。
- **Python**：`pyproject.toml` 里配置 `ruff`（检查加格式化）和类型检查器，`pre-commit` 钩子在提交前运行，CI 里 `ruff check`、`ruff format --check`、`mypy` 或 `pyright`、`pytest`；用 `uv` 固定工具版本。

**何时破例**：个人脚本和一次性代码不用全套；遗留代码库一次性开全部检查会淹没团队，应渐进收紧；性能敏感或生成的代码可以局部关闭某条检查，但必须写明原因（`#[allow(...)]` 加注释，`# noqa: XXXX` 带规则号）。
