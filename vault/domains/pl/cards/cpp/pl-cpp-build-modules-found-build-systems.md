---
id: pl-cpp-build-modules-found-build-systems
node: cpp.build-modules
type: qa
step: 5
---
## Q
C++ 的构建系统（CMake 等）做什么？为什么语言标准本身不管构建，工程师日常怎样管理依赖？

## A
**构建系统要解决的事**：知道有哪些源文件，用什么编译选项（标准版本、优化、警告、宏定义、头文件搜索路径），哪些目标依赖哪些目标，如何生成可执行文件和库，哪些文件改了需要重编。

**C++ 标准不管这些**：ISO 标准只定义语言和标准库，不定义"源文件怎么组织、怎么编译、依赖放哪里"。各平台、各编译器的命令行、库格式都不同，标准无法也不愿统一。

**现实中的方案**：

| 工具 | 角色 |
|---|---|
| **CMake** | 事实标准。写一份 `CMakeLists.txt` 描述目标和依赖，生成 Ninja、Makefile、Visual Studio、Xcode 的工程文件 |
| **Ninja** | 快速的底层构建执行器，通常由 CMake 调用 |
| **Bazel** | 大型单体仓库用，强调可复现、远程缓存、增量构建（Google 系） |
| **Meson** | 语法更简洁的替代品 |
| **vcpkg、Conan** | 第三方包管理器，下载、编译、锁定版本 |

**CMake 的核心概念**是"目标"（target）：库或可执行文件，带有它自己的编译选项和**传递性**的使用要求（`PUBLIC`/`PRIVATE`/`INTERFACE`）。现代 CMake（3.x）的原则是围绕目标写，不再设置全局变量。

**依赖管理的现实**：
1. 系统包管理器（apt、brew）提供的版本固定且与系统绑定；
2. 把源码作为子目录或 git submodule 引入，用 `FetchContent` 在配置时下载；
3. vcpkg/Conan 按清单（manifest）管理版本，缓存预编译的二进制；
4. 大公司自己 vendoring（把依赖的源码拷进仓库）并用 Bazel 构建。

**与其他语言对比**：Rust 有 `cargo`，Go 有 `go build`/`go mod`，Python 有 `pip`/`uv`，Java 有 Maven/Gradle，它们都是语言的一部分或官方推荐的单一工具，一个 `cargo build` 搞定。C++ 没有，所以每个项目要做一组选择，新人入门成本高，跨项目复用也难。

**日常实践**：
- 用 CMake + Ninja，目标化写法；
- `CMAKE_EXPORT_COMPILE_COMMANDS=ON` 生成 `compile_commands.json`，给 `clang-tidy`、clangd 用；
- 选一个包管理器并锁版本；
- CI 里用 `ccache` 缓存编译。

**要记住的一点**：在 C++ 里，"构建与依赖"是项目自己的基础设施，不是语言给的；新项目的第一个技术选型常常就是这个。
