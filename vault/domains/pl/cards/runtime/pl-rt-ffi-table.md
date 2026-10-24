---
id: pl-rt-ffi-table
node: runtime.ffi
type: qa
step: 7
---
## Q
Java、Go、Rust、Python 在 FFI 的“易用性 / 安全性 / 性能 / 构建复杂度”上各选了什么，为什么？

## A
| 语言 | 主要机制 | 易用性与安全 | 性能 | 构建 |
|---|---|---|---|---|
| Java | JNI（旧，要写 C 胶水）；FFM API（22 起，纯 Java 描述） | FFM 易用，受限方法需显式授权；越界有检查 | 约 3 纳秒 / 次 | FFM 不用 C 编译；JNI 要编译分发动态库 |
| Go | cgo | 语法嵌入 C 代码，字符串要拷贝；GC 与 C 内存边界要小心 | 约 13 纳秒 / 次 | 需要 C 编译器，失去简单交叉编译与静态链接 |
| Rust | `extern "C"` + `unsafe`，bindgen/cbindgen | 编译器不检查 C 契约，靠安全封装；所有权能表达归属 | 约 1 纳秒 / 次，等同普通调用 | 要链接 C 库；交叉编译需配置 |
| Python | ctypes；C API / Cython；PyO3/pybind11 | ctypes 易用但无类型检查；C API 易崩溃；PyO3 较安全 | ctypes 约 147 纳秒；扩展更快 | wheel 需按平台预编译发布 |

背后的逻辑：
- **运行时越重，进出边界越贵**：Rust（无运行时）最便宜，Go（自己的调度器和栈模型）最贵，Java 居中，Python 的解释器开销在 ctypes 上最明显。
- **FFI 的难度取决于“谁拥有内存”**：GC 语言要解决“对象会移动 / 被回收”，所以需要拷贝（Go 的 `CString`）、固定（pinning）或原生内存作用域（Java 的 `Arena`）；Rust 用所有权，Python 用引用计数，可以更自然地表达。
- **语言对 FFI 的态度**：Python、Rust 把它当作核心能力（Python 是胶水，Rust 要替换 C/C++ 并与之共存）；Go 倾向避开（“cgo 不是 Go”），因为纯 Go 的构建与部署体验更重要；Java 长期用 JNI 的难用来“劝退”，直到 FFM 才正面解决。
