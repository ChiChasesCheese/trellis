---
id: pl-dyncheck-table
node: engineering.dynamic-checkers
type: qa
step: 6
---
## Q
Go、Java、Rust、Python 各自靠什么动态检查器？为什么它们能发现静态类型系统发现不了的问题？

## A
| 语言 | 主要工具 | 检查什么 | 代价与局限 |
|---|---|---|---|
| Go | `go test -race` / `go run -race` | 数据竞争；`-asan` 只用于 `cgo` | 慢约 2 到 20 倍，内存多 5 到 10 倍；只在执行到的路径上发现 |
| Java | jcstress；`-Xcheck:jni` | 内存模型层面的可见性与重排序；JNI 的误用 | jcstress 要单独写测试，结果是统计性的；JVM 本身无需 ASan |
| Rust | Miri（nightly）；nightly 上的 ASan、TSan | `unsafe` 代码的未定义行为、别名违规；内存错误 | Miri 慢一到两个数量级，不支持 FFI；sanitizer 需要 nightly |
| Python | `python -X dev` 开发模式；用 ASan、TSan 构建的解释器 | 开发模式开启更多运行时检查（分配器调试钩子、`faulthandler`、资源警告）；C 扩展的内存错误 | 对纯 Python 逻辑帮助有限；C 扩展调试需要特殊构建的解释器 |

**为什么能发现静态检查发现不了的问题**：静态类型系统要对**所有**可能的执行给出保证，所以必须保守，凡是证明不了的就禁止或放弃。动态检查器只看**这一次**真实的执行，面对的是具体的地址、具体的线程交错，不需要推理所有可能性，因此能看到类型系统根本表达不了的东西：这个指针此刻是否指向已释放的内存，这两个线程之间有没有同步。

**规律**：内存管理越是交给运行时（Java、Python），动态检查器越集中在并发和本地扩展；越是把责任交给程序员（Rust 的 `unsafe`、C 和 cgo），越需要 ASan 与 Miri 这类工具来替程序员复核担保。Go 把 `-race` 做成一个编译选项，反映它「并发是日常、工具必须顺手」的态度；Rust 把最严格的检查（Miri）留给 `unsafe` 的少数模块，因为安全代码已经由编译器负责。
