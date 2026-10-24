---
id: pl-rt-deploy-pitfall-cgo-glibc
node: runtime.deployment
type: qa
step: 9
---
## Q
“本地构建、服务器运行”最常见的几种翻车是什么？静态二进制放进最小镜像时为什么会 `not found`？

## A
根因都是：**构建环境里的某个隐含依赖，在运行环境里不存在或版本不同。**

**1. 以为是静态的，其实动态链接了 C 库。** Go 只要使用了 cgo（比如依赖 SQLite 的某些驱动、旧版的 `net` 在特定条件下），就会动态链接 libc。把这种二进制复制进 `scratch` 或 Alpine 镜像：
- `scratch` 里没有任何库，运行时报 `exec /app: no such file or directory`，文件明明存在，缺的是它的**动态链接器**（interpreter）；
- Alpine 用 musl libc，glibc 构建的二进制找不到 `libc.so.6`。
检查方法：Linux 上 `ldd ./app` 应该显示 `not a dynamic executable`（macOS 上用 `otool -L`）。

**2. 交叉编译遇到 cgo。** 本机实验里在 macOS 上 `GOOS=linux CGO_ENABLED=1 go build` 失败：
```
# runtime/cgo
gcc_clearenv.c:16:2: error: implicit declaration of function 'clearenv'
```
而 `CGO_ENABLED=0` 的纯 Go 版本，同一个用到 `net` 的程序成功编出约 3.1 MB 的 Linux 静态可执行文件。

**3. Rust 的 glibc 版本。** 在较新的发行版上构建的二进制，引用了新版 glibc 的符号，在旧系统上报 `version 'GLIBC_2.xx' not found`。解决：在较旧的环境构建，或用 musl 目标。

**4. Python wheel 与平台不匹配。** 在 Mac 上 `pip install` 的 numpy 是 macOS ARM64 的 wheel；把整个 `venv` 目录复制到 Linux 无法运行，因为 `venv` 里是平台相关的二进制和写死的路径。在 Linux 容器里重新安装依赖才对。Alpine（musl）上很多 wheel 没有预编译版本，会退回到源码编译，慢且需要编译器。

**5. Java 的 JVM 版本。** 用新版本编译的类文件在旧版 JVM 上报 `UnsupportedClassVersionError`；用 `--release 17` 约束字节码级别。

**预防**：构建环境和运行环境的操作系统、libc、架构一致（或都用容器）；CI 里在最终镜像上跑一次冒烟测试。
