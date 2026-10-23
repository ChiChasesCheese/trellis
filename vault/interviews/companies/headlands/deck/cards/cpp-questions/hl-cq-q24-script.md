---
id: hl-cq-q24-script
node: cpp-questions.f-ub-debug
type: qa
step: 10
---
## Q
用英文 60 秒回答：What are sanitizers? What do AddressSanitizer, UBSan and ThreadSanitizer catch?

## A
结构：三种 sanitizer 各抓什么与 `-g -fsanitize` → 读 ASan 报告三步（错误类型、出错帧、分配/释放历史）→ TSan 修好后无警告 → 成本：ASan 慢 2 倍、TSan 更慢，只用于测试。

- Sanitizers are compiler instrumentation that checks at run time. **AddressSanitizer** catches heap, stack and global buffer overflows, use-after-free and double free; **UBSan** catches signed overflow, bad shifts and misaligned access; **ThreadSanitizer** catches **data races**. I build with `-g -fsanitize=...` and run my tests under them.
- Reading an ASan report: first line is the **error kind**, the first frame is the **faulting line**, and "allocated by" and "freed by" tell the object's history. For example, a dangling `string_view` showed up as heap-use-after-free pointing at the destructor of the string.
- TSan flagged two threads incrementing a plain `int`, and was silent after I fixed it with a mutex.
- They are 2x slower for ASan and much slower for TSan, so they're for testing, not production.
