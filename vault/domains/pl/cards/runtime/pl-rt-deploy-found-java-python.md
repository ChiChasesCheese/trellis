---
id: pl-rt-deploy-found-java-python
node: runtime.deployment
type: qa
step: 3
---
## Q
Java 的 JAR 和 Python 的虚拟环境（venv）、wheel 各是什么？部署它们时目标机器上必须有什么？

## A
**Java**：
- **JAR**（Java Archive）是一个 zip 文件，里面是编译好的 `.class` 字节码和资源。字节码与 CPU、操作系统无关，同一个 JAR 可在任何装有兼容 JVM 的机器运行。
- **Fat JAR / uber JAR**：把你的代码和全部依赖的 JAR 合并成一个，`java -jar app.jar` 即可运行。
- 目标机器必须有**版本合适的 JVM**。完整的 JDK 约 294 MB（本机 Temurin 25）；`jlink` 可以只打包需要的模块，做出最小运行时，例如只含 `java.base` 的运行时约 45 MB。
- 字节码跨平台，但依赖里的本地库（JNI）仍然是平台相关的。

**Python**：
- 部署的是**源码**，运行时需要**解释器**和**依赖包**。依赖包有两种形态：纯 Python 包（源码，平台无关）和含 C 扩展的包，后者以 **wheel**（预编译的二进制分发包）发布，文件名里写着适用的 Python 版本、操作系统、CPU 架构（如 `manylinux_2_28_x86_64`）。
- **虚拟环境（venv）**：一个独立目录，里面有解释器的链接和该项目专用的 `site-packages`，避免不同项目的依赖互相冲突。它**不是**可移植的产物：里面的路径和二进制绑定了创建它的机器。
- 本机观察（一次测量）：Python 3.14 基础安装约 76 MB；同一个 `numpy` 的 macOS ARM64 wheel 装好后约 22 MB，Linux x86-64 的 manylinux wheel 装好后约 56 MB（自带 OpenBLAS 等库）。

所以：
- Java 的“编译一次，到处运行”只对纯字节码成立，且要求目标机有 JVM。
- Python 部署的单位是“**解释器 + 源码 + 与目标平台匹配的二进制依赖**”，在不同平台上必须重新解析并安装依赖，常用锁定文件（`uv.lock`、`requirements.txt` 加哈希）保证可复现。
