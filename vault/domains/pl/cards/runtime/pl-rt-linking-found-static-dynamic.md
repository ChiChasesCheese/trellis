---
id: pl-rt-linking-found-static-dynamic
node: runtime.linking-abi
type: qa
step: 3
---
## Q
同一个“hello world”，Go、Rust、C 编译出来的可执行文件分别多大、依赖哪些动态库？为什么 macOS 上的 Go 程序也要依赖 `libSystem`？

## A
一次测量（macOS ARM64，各自默认构建）：

| 程序 | 大小 | `otool -L` 依赖 |
|---|---|---|
| C（clang -O2，动态链接 libc） | 约 33 KB | `libSystem.B.dylib` |
| Rust（`rustc -O`，标准库静态链入） | 约 470 KB | `libSystem.B.dylib` |
| Go（`go build`） | 约 2.4 MB | `libSystem.B.dylib`、`libresolv.9.dylib` |

大小的差别，来自**谁带着运行时**：C 的 `printf` 在系统的共享库里，可执行文件里只有一个引用；Rust 把用到的那部分标准库（格式化、锁、栈回溯等）拷进了可执行文件；Go 还把垃圾回收器、调度器、完整的 `fmt` 与反射带进去，所以最大，但也最“自足”。

**动态链接和加载**：`otool -L` 列出的是启动时要加载的共享库（Linux 上对应 `ldd`）。加载器把它们映射进进程地址空间，并把可执行文件里的未定义符号绑定到库里的地址。

**为什么 macOS 上的 Go 也依赖 libSystem**：操作系统内核的系统调用号在 macOS 上不是稳定接口，只有 `libSystem` 提供的 C 函数（如 `write`）才被承诺稳定。Go 1.11 起在 macOS 上通过 libSystem 调用系统，所以“纯 Go 程序”也有动态依赖。在 Linux 上，系统调用接口本身稳定，纯 Go（不用 cgo）的程序可以完全静态：没有任何动态依赖，拷到任何发行版上都能跑，这就是 Go 在容器里常用 `scratch` 镜像的原因。

**静态 vs 动态的决策**：
- 静态：部署是拷一个文件，行为与构建时一致；但 OpenSSL 出安全补丁时，每个静态链接了它的程序都要重新构建发布。
- 动态：补一个 `.so` 全机生效，但版本错配会在启动时失败（缺符号、缺 `GLIBC_2.xx`）。
