---
id: pl-rt-startup-best-practice
node: runtime.startup-footprint
type: qa
step: 8
---
## Q
在 CLI、Serverless、容器化服务里，资深工程师怎样控制各语言的启动时间和内存占用？

## A
**先测量。** 启动时间用多次运行取中位数（冷缓存和热缓存分开看），内存看 RSS 峰值，不看“堆大小”配置值。

**Java**：
- 容器里**显式设堆**：`-XX:MaxRAMPercentage=70`（按容器限额的比例）或 `-Xmx`；别让 JVM 凭默认值占满宿主机，同时给堆外内存（线程栈、元空间、直接内存、代码缓存）留余量。本机实验里同样负载，默认 G1 峰值 2.1 GB，限定 `-Xmx300m` 约 201 MB。
- 短命进程：用 AOT 缓存/AppCDS 缩短类加载（本机小程序省约 11%）；`-XX:TieredStopAtLevel=1` 少花 JIT；考虑原生镜像。
- 框架：避免启动时的类路径扫描、重型反射；选择编译期依赖注入的框架。
- 长期服务：不必为启动时间牺牲峰值吞吐；用预热和滚动发布代替。

**Go**：
- 内存受限时设 `GOMEMLIMIT`（软上限，回收更积极）并按需调 `GOGC`；本机实验里 `GOMEMLIMIT=250MiB` 把峰值从约 510 MB 压到约 243 MB。
- 用 `go build -ldflags="-s -w"` 去掉符号可缩小二进制（本机 hello 从 2.3 MB 到 1.5 MB）。
- 避免在 `init()` 里做重工作，包初始化顺序不易管理。

**Rust**：
- 发布构建用 `strip`、`lto`、`opt-level="s"` 等控制体积；注意泛型膨胀。
- 基线内存最小，要小心的是无上限的缓冲和缓存。

**Python**：
- 用 `python -X importtime` 找慢导入，把重模块导入移进函数内；CLI 里别在顶层导入 `pandas`/`numpy`（本机导入 pandas 约 121 毫秒）。
- 容器里提前编译 `.pyc`（`python -m compileall`），避免每个实例重新编译。
- 内存里的小对象开销大：用生成器、`__slots__`、数组/NumPy。

**通用**：资源限制（CPU、内存）要在运行环境里显式设置，并让运行时感知（容器感知的 JVM、Go 的 GOMEMLIMIT/GOMAXPROCS）。
