---
id: pl-sig-choosing-evolution-hybrid
node: signatures.choosing
type: qa
step: 8
---
## Q
语言选型的格局最近十年怎样变化？“多语言系统”、Rust 内核和 WebAssembly 等趋势说明什么？

## A
**趋势一：分层的多语言成为常态**。大型系统通常是“**易写的外壳，快速的内核**”：Python 的 NumPy、PyTorch、Polars、Pydantic 核心是 C++ 或 Rust；JavaScript 工具链（esbuild、SWC、Biome）用 Go 或 Rust 重写；Python 的 `ruff` 与 `uv` 用 Rust 写成。选择语言变成“**选界面的语言**和**选内核的语言**”。

**趋势二：Rust 进入原本由 C/C++ 占据的领域**。Linux 内核、Android、Windows 的部分组件、浏览器引擎、云基础设施（Firecracker、Cloudflare 的代理）。采用方式是渐进式的：新模块用 Rust，旧代码保持，边界上用 FFI。

**趋势三：Go 成为云基础设施的默认语言**。Docker、Kubernetes、Terraform、Prometheus 等使 Go 成为该领域的“官方语言”，招聘和工具都围绕它形成。

**趋势四：Java 保持企业核心，同时现代化**。虚拟线程、`record`、模式匹配、GraalVM 原生镜像缩小了与 Go 在并发和部署上的差距。

**趋势五：Python 站稳数据与 AI，同时补性能**。自由线程、JIT、类型系统、`uv` 与 `ruff` 让它在工程化上更成熟。

**趋势六：WebAssembly 作为可移植的二进制目标**。Rust、Go、C 都可以编译到 Wasm，在浏览器、边缘和插件系统里运行，使“用什么语言写的”与“在哪里运行”进一步解耦。

**趋势七：AI 辅助编码改变成本结构**。生成样板代码的成本下降，使“语言冗长”（Java、Go 的样板）相对不那么痛，也让团队更容易同时维护多种语言。但验证代码正确性的成本没有下降，一种常见的判断是：这会提高带更强静态保证的语言（Rust、带类型检查的 Python）的相对价值。

**说明什么**：语言选型从“选一个统一的栈”变成“**设计一个由边界、协议和多种语言组成的系统**”。资深工程师的能力，越来越体现在划分边界、选择接口和控制多语言的复杂度上，而不是在单一语言里的技巧。

**给学习者的建议**：精通一门语言，熟悉另外两到三门的核心思想，理解它们之间怎样互操作。
