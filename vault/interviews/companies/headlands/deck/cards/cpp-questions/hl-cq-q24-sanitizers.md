---
id: hl-cq-q24-sanitizers
node: cpp-questions.f-ub-debug
type: qa
step: 5
---
## Q
面试题：什么是 sanitizer？AddressSanitizer、UBSan 和 ThreadSanitizer 各抓什么？
What are sanitizers? What do AddressSanitizer, UBSan and ThreadSanitizer catch?

## A
Sanitizer 是编译器插桩的**运行时检查器**。
- **ASan**（AddressSanitizer）：堆 / 栈 / 全局缓冲区溢出、use-after-free、重复释放。
- **UBSan**：有符号溢出、移位越界、未对齐访问等。
- **TSan**（ThreadSanitizer）：数据竞争。
- **MSan**：读未初始化内存（仅 Linux）。
- 编译时加 `-fsanitize=...`，加 `-g` 让报告带行号；ASan 约慢 2 倍，TSan 慢得多，所以用于测试而非生产。
