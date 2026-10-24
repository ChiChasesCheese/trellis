---
id: pl-eco-modules-best-practice
node: ecosystem.modules
type: qa
step: 9
---
## Q
资深工程师怎样组织模块与包？通用规则是什么，Go、Java、Rust、Python、C++ 各自怎么做，何时破例？

## A
**通用规则**：
1. **默认私有，对外承诺要少**。公开的每一个名字都是以后要维护的 API。
2. **按职责与变化原因分，不按技术层次分**（避免 `controllers/`、`utils/` 这类杂物抽屉）。
3. **依赖方向单向**：高层依赖低层，领域代码不依赖框架。
4. **把「内部」用语言机制标出来**，不要只靠文档。

按语言：
- **Go**：包名短而小写，名字体现用途（`http`、`bytes`），避免 `util`、`common`；把不想承诺的放进 `internal/`；用接口在使用方（消费者）定义，来解开循环；一个 module 里放可执行入口在 `cmd/`。
- **Java**：新项目至少按功能分包而非按层分包；库作者提供 `module-info.java` 来声明 `exports`，哪怕调用方仍在类路径上，也能获得封装；用 ArchUnit 把分层规则写成测试。
- **Rust**：默认私有，需要 crate 内共享用 `pub(crate)`；公开 API 通过 `lib.rs` 里的 `pub use` 重新导出，隐藏内部目录结构；大项目用 workspace 拆成多个 crate。
- **C++**：头文件只放接口，实现放 `.cpp`；头文件自己包含自己需要的头（能独立编译），并加 include guard 或 `#pragma once`；能用前置声明就不 `#include`；内部符号放匿名命名空间或隐藏符号可见性（`-fvisibility=hidden`）；用 CMake 的 `PRIVATE`/`PUBLIC` 目标依赖表达边界；新项目可评估 C++20 模块，但要先确认工具链支持。
- **Python**：包的 `__init__.py` 只重新导出公共 API，并定义 `__all__`；绝对导入优先；循环导入通过抽第三个模块解决，延迟导入只是权宜；项目布局用 `src/` 目录避免当前目录遮蔽已安装包；不要给自己的文件起标准库的名字（`random.py`、`logging.py`、`types.py`）。

**何时破例**：脚本和一次性工具，一个文件装下全部就好；过早拆分的代价（跳转、命名、样板）常比耦合更高。拆分的时机是第二个变化原因出现时。
