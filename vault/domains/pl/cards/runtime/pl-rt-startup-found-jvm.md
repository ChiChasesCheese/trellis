---
id: pl-rt-startup-found-jvm
node: runtime.startup-footprint
type: qa
step: 2
---
## Q
启动一个 Java 程序时，JVM 具体做了什么？类数据共享（CDS）和 AOT 缓存是什么，一个最小的 Hello World 要多久、占多少内存？

## A
**JVM 启动流程**（从零理解）：Java 程序被编译成 `.class` 文件（字节码）。运行 `java Hello` 时：
1. 操作系统启动 `java` 可执行文件，它加载 JVM 动态库，建立堆、元空间、线程、GC、JIT 编译器等内部结构。
2. JVM 加载并初始化几百个 JDK 自带的核心类（`Object`、`String`、`System`……），每个类要经过读取、解析、校验、链接、初始化。
3. 加载你的 `Hello` 类，找到 `main`，用**解释器**逐条执行字节码。热点之后才被 JIT 编译。

第 2 步最费时间：类是延迟加载的，但核心类必须先就位。

**类数据共享**（CDS，Class Data Sharing）：JDK 随发行版带一个预处理好的归档文件，里面是已解析好的核心类元数据，启动时直接用 `mmap` 映射进内存，省掉读取与解析。默认就开着。
**AOT 缓存**（JDK 24 起的新特性，由 Leyden 项目推进）：用一次“训练运行”记录程序加载了哪些类、链接了什么，生成一个缓存文件，之后启动直接复用。命令形如 `java -XX:AOTCacheOutput=app.aot ...` 生成，再用 `-XX:AOTCache=app.aot` 运行。

实测（Apple Silicon，一次测量，20 次取中位数）：
- `java Hello`：约 24 毫秒，最大常驻内存（RSS）约 40 MB；
- 关掉 CDS（`-Xshare:off`）：约 34 毫秒，说明默认归档省了约 10 毫秒；
- 一个用到 `HttpClient`、正则、Stream、`CompletableFuture` 的小程序：默认约 496 毫秒，使用 AOT 缓存约 443 毫秒，约省 11%。

结论：JVM 的基线是“几十毫秒、几十 MB”，应用类越多、框架越重（扫描、反射、代理），启动越慢；Spring 类应用的启动常达数秒。
