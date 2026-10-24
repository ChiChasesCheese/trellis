---
id: pl-eco-compat-best-practice
node: ecosystem.compatibility
type: qa
step: 9
---
## Q
资深工程师怎样面对语言与依赖的版本演进？通用规则是什么，Go、Java、Rust、Python、C++ 各自怎样做，何时破例？

## A
**通用规则**：
1. **跟着节奏升级，小步多次**：每次升级的破坏有限，积压三年再升则是一场迁移项目。
2. **把弃用警告当缺陷**：在 CI 里让它们失败，在还有时间时修掉。
3. **库作者对公共 API 负责**：遵守 semver，删除前先弃用，写变更日志。
4. **在 CI 里同时测试最低支持版本和最新版本**。
5. **工具链版本进入仓库**，让所有人和 CI 一致。

按语言：
- **Go**：`go.mod` 的 `go` 行跟着团队实际使用的最低版本；每个 Go 发行后尽快升级（旧版本只支持最近两个发行版）；用 `go vet` 与 `go fix` 的迁移工具；发布库用 `gorelease` 检查是否破坏 API；需要破坏时发布新的主版本，导入路径加 `/v2`。
- **Java**：以 LTS 版本（长期支持，如 21、25）为升级节点；`mvn -Dmaven.compiler.release=N`；CI 里开 `-Xlint:deprecation,removal`；用 `jdeps --jdk-internals` 找依赖 JDK 内部 API 的代码；库作者标记 `@Deprecated(forRemoval=true, since="x")`。
- **Rust**：定期 `cargo fix --edition` 迁移；固定 `rust-toolchain.toml`；库声明最低支持的 Rust 版本（MSRV）并在 CI 里测试；`cargo-semver-checks` 检查公共 API 变化。
- **C++**：在构建系统里钉死 `-std=c++XX` 和编译器版本，CI 里用至少两个编译器（Clang 与 GCC）和 `-Wall -Wextra`；升级标准时用 clang-tidy 的 `modernize-*` 检查机械改写旧写法；库的头文件用特性检测宏（如 `__cpp_lib_span`）而不是版本号判断；公共库边界保持 `extern "C"` 或稳定的 ABI。
- **Python**：CI 加 `-W error::DeprecationWarning`；跟着当前和前一个 Python 版本测试矩阵；库在 `pyproject.toml` 里声明 `requires-python`；用 `pyupgrade`/`ruff` 的 `UP` 规则机械升级语法。

**何时破例**：生命周期很短的原型不必追求；有认证或合规约束必须固定在某个版本的系统，需要计划好**安全补丁**怎样拿到，而不是永不升级。冻结版本是选择，不是默认。
