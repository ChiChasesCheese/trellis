---
id: pl-rt-ffi-best-practice
node: runtime.ffi
type: qa
step: 9
---
## Q
设计和使用跨语言边界时，资深工程师遵循哪些原则？

## A
1. **边界要窄、要粗。** 暴露少量粗粒度的函数，一次调用做一大块事（传数组、传批量请求），不要在热循环里每个元素过一次边界。边界成本是十到百纳秒，计算量应远大于它。
2. **在边界上做转换和校验，内部保持纯净。** 把外部数据一次性转成本语言的类型，校验长度、空指针、编码，再进入内部逻辑。
3. **明确内存所有权。** 谁分配谁释放，或者用约定好的 `create/destroy` 配对函数。Go 里用 `C.CString` 就要 `C.free`；Java 用 `Arena` 的作用域；Rust 用 `Box::into_raw`/`from_raw` 配对，或让 `Drop` 封装；Python 扩展要正确增减引用计数。
4. **不要让 panic / 异常穿过边界。** C 的 ABI 没有异常：Rust 的 panic 穿过 `extern "C"` 函数边界会让进程直接中止（较老版本是未定义行为），应使用 `catch_unwind` 转成错误码，Java 的异常要在原生层之前转成返回值，Python 扩展要设置错误并返回 NULL。错误用返回码或明确的错误结构传递。
5. **线程模型要想清楚。** 回调从 C 线程进入 Java/Python/Go 时，Python 要先拿 GIL，Java 要附加（attach）线程，Go 的回调需要特殊处理。优先让原生库不创建线程或由宿主语言管理线程。
6. **优先选高层、受检的绑定。** Python 用 PyO3/pybind11/cffi 而不是裸 C API；Java 用 FFM 而不是 JNI；Rust 用 bindgen 生成声明，不手写。
7. **能纯语言实现就别 FFI。** 评估：是否有成熟的纯 Go/纯 Java/纯 Rust 实现？FFI 的长期成本包括构建矩阵、发布平台数、崩溃的诊断难度、安全审计。
8. **测试跨边界**：用 ASan/Valgrind 检查内存错误，跨平台 CI 构建全部目标。

什么时候值得用 FFI：已有成熟的、性能关键的原生库（加密、压缩、BLAS、GPU）；或在遗留 C/C++ 系统里渐进引入 Rust。
