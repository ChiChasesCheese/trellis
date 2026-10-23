---
id: hl-cq-q24-tsan-and-others
node: cpp-questions.f-ub-debug
type: qa
step: 8
---
## Q
两个线程对同一个 `int` 做 `++counter`，ThreadSanitizer 会报什么？怎么修？另外 LSan、MSan、Valgrind、UBSan 的 recover 行为各有什么特点？

## A
- **TSan**：报 `WARNING: ThreadSanitizer: data race`，列出两个写操作所在的线程和代码行；用 `std::mutex` 或 `std::atomic` 修好后警告为 0。
- **LSan** 查泄漏：Linux 上随 ASan 启用；Apple Silicon 上提示 `detect_leaks is not supported on this platform`。
- **MSan** 查未初始化读：仅 Linux。
- **Valgrind**：不用重编译，但慢几十倍。
- **UBSan** 默认打印后继续；加 `-fno-sanitize-recover=undefined` 让它直接终止。
