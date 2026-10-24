---
id: pl-rt-deploy-best-practice
node: runtime.deployment
type: qa
step: 8
---
## Q
资深工程师怎样为各语言设计构建和镜像，才能做到可复现、小体积、安全？

## A
**通用原则**：
1. **构建环境固定、依赖锁定、产物不可变**：同一份提交总是产出同一份产物；锁文件进版本库；镜像用具体版本标签或摘要，不用 `latest`。
2. **多阶段构建**：编译环境和运行环境分开，最终镜像只含运行必需的东西。
3. **最小权限、最小面**：不以 root 运行；最终镜像里没有编译器、包管理器、shell（或尽量少）。
4. **同一个产物走完所有环境**：测试通过的就是上线的，不在每个环境重新构建。
5. **可观测与优雅关闭**：处理 SIGTERM，健康检查，日志写标准输出。

**Go**：`CGO_ENABLED=0 go build -trimpath -ldflags="-s -w"`，放进 `scratch` 或 `distroless/static`；需要 CA 证书和时区数据时把它们复制进去。本机实测 hello 的镜像是 2.22 MB。如果必须用 cgo，在目标发行版上构建，别指望交叉编译。

**Rust**：用 `cargo build --release`；需要静态链接时选 `x86_64-unknown-linux-musl`，注意 musl 的内存分配器性能比 glibc 慢，必要时换 `jemalloc`/`mimalloc`；用 `cargo-chef` 之类缓存依赖层。

**Java**：用 JRE 精简镜像或 `jlink` 做最小运行时；分层 JAR 让依赖层缓存；设好 `MaxRAMPercentage`；需要极速启动的服务评估原生镜像和 AOT 缓存。固定 JDK 的小版本。

**Python**：
- 用 `uv`/`pip` 生成锁文件并带哈希；镜像里只装锁定的依赖，`--no-cache`；
- 多阶段：builder 阶段装编译依赖构建 wheel，运行阶段只复制 `site-packages`；
- 用与目标平台一致的基础镜像（避免 wheel 与 libc 不匹配，比如 musl 与 manylinux 的坑）；
- 提前编译 `.pyc`。

**什么时候打破**：快速原型和内部工具可以直接在服务器上 `uv run`；但一旦服务有多人维护或多环境，就要回到不可变产物。
