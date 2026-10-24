---
id: pl-rt-deploy-found-static
node: runtime.deployment
type: qa
step: 2
---
## Q
Go 和 Rust 的“单个静态二进制”是什么？静态链接与动态链接有什么区别？在 Mac 上怎样编出 Linux 服务器能跑的程序？

## A
**链接（linking）**是把你的目标代码和它用到的库拼成可执行文件的步骤。
- **静态链接**：库的机器码直接复制进可执行文件。文件大，但自包含，运行时不需要找库。
- **动态链接**：可执行文件只记录“我需要 `libc.so.6`、`libssl.so.3`”，运行时由系统的动态链接器找到并加载。文件小、库可共享可单独升级，但目标机器必须有对应版本的库。

**Go**：默认把运行时和所有 Go 依赖静态链接进一个文件；只要不使用 C 库（`CGO_ENABLED=0` 或没有 cgo 依赖），整个程序不依赖系统库。**Rust** 默认静态链接 Rust 依赖，但仍动态链接系统的 C 库（Linux 上是 glibc），想完全静态要选 `musl` 目标。

**交叉编译**：Go 把目标平台当成两个环境变量，不需要额外工具链。真实例子（在 macOS ARM 上，一次测量）：
```
GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -ldflags="-s -w" -o hello_linux hello.go
```
产物是一个 Linux/ARM64 的静态可执行文件，约 1.5 MB；一个用到 `net` 包的程序是约 3.1 MB。直接复制到 Linux 服务器就能运行。

但只要开启 cgo（程序里用了 C 代码或依赖 C 库的包），交叉编译就要求目标平台的 C 编译器和头文件，否则失败，真实报错（节选）：
```
# runtime/cgo
gcc_clearenv.c:16:2: error: implicit declaration of function 'clearenv'
```
原因是 cgo 要用本机的 C 编译器编译面向 Linux 的 C 代码，macOS 的编译器和头文件不适用。

Rust 交叉编译需要先 `rustup target add <target>`，并配置对应的链接器；纯 Rust 项目简单，依赖 C 库的项目麻烦，与 Go 的 cgo 同理。

所以“单文件部署”有一个前提：**不碰 C 世界**，或者在目标平台上构建（容器里构建）。
