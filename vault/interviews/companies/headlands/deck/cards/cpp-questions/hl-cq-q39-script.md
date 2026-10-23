---
id: hl-cq-q39-script
node: cpp-questions.i-low-latency
type: qa
step: 20
---
## Q
用英文 60 秒回答：Exceptions vs error codes vs `std::optional`/`std::expected`: what do they cost, and what do trading systems do?

## A
结构：零开销模型（不抛免费）但一次抛出 3–4 µs、约比返回码慢 30 倍 → 可预期失败用返回值（`[[nodiscard]]` 错误码、`optional`、`expected`）→ 交易代码库常关异常，仅冷路径用 → `noexcept` 移动、析构不抛、RAII。

- Exceptions in C++ follow the **zero-cost model**: when nothing is thrown, the code is as fast as with error codes, because the unwinding tables are only consulted on a throw. But a **throw is expensive** - about 3 to 4 microseconds in my test, roughly 30 times a return code - so exceptions are for truly exceptional conditions.
- Expected failures like parse errors or a missing key I return as values: an error code with `[[nodiscard]]`, `std::optional` when no reason is needed, or `std::expected` when it is.
- Many trading codebases compile with exceptions disabled and keep them only on cold initialization paths.
- Related: mark move constructors **`noexcept`**, never throw from destructors, and rely on RAII for exception safety.
