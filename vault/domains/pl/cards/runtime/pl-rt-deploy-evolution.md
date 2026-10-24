---
id: pl-rt-deploy-evolution
node: runtime.deployment
type: qa
step: 10
---
## Q
软件交付形态经历了怎样的演变？语言工具链现在往哪里走？

## A
**交付形态的演变**：
1. **直接部署源码或二进制到服务器**：手工装依赖、配环境，机器“雪花化”，同样的程序在不同机器上行为不同。
2. **平台打包**：Java 的 WAR/EAR 放进应用服务器，Python 的 `virtualenv`，系统包（deb/rpm）。
3. **容器镜像**（Docker，2013 年起）：把应用和环境一起打包，镜像成为通用的交付单位，Kubernetes 以此为基础编排。
4. **更小、更快、更安全的变体**：`distroless`、`scratch`、`jlink`、Native Image、Wasm 模块、microVM（Firecracker 之类，用于 Serverless）。
5. **供应链安全**：SBOM（软件物料清单）、签名、可复现构建、依赖漏洞扫描成为交付的一部分。

**语言工具链的趋势**：
- **Python**：`uv` 等新一代工具把依赖解析、虚拟环境、Python 版本管理合一，并推动 `pyproject.toml` 和锁文件标准；PEP 723 允许单文件脚本声明依赖。
- **Java**：从应用服务器走向“可执行 JAR + 容器”，再到 GraalVM 原生镜像、CRaC 快照、AOT 缓存，缩小启动与体积。
- **Go**：内置的 `go build` 与模块代理已经够用；趋势是更小的二进制、更快的链接、PGO；`go tool` 与 `embed` 让静态资源也进二进制。
- **Rust**：Cargo 生态、`cargo-dist`/`cross` 简化多平台发布；对静态链接与 Wasm 的支持不断改进。
- **共同点**：**可复现构建**与**锁定依赖**成为默认期望；“一份产物走遍所有环境”成为原则。

**WebAssembly（Wasm）作为另一种可移植形态**：和字节码类似，一个 `.wasm` 模块可以在浏览器、边缘节点、服务器端的运行时里执行，带沙箱，启动极快；Go、Rust 可直接编译到 Wasm，Python 和 Java 的支持仍在发展。它代表“比容器更轻的交付单位”的方向，但生态尚未成熟。

判断规律：**交付单位越小越自包含，启动与密度越好，但对语言和库的约束越多**，每一步演进都在这条轴上移动。
