---
id: hl-oa01-followup-exceptions
node: problems.oa01-job-chain
type: qa
step: 15
---
## Q
追问：校验错误为什么用异常，而不是 `Optional` 或错误码？在 C++ 里怎么回答同一个问题？

## A
**Java 回答**：校验分散在多层（解析、拼链、格式化），异常让中间层不必层层转发错误，只在 `analyze` 这**一个边界**统一转成值（`Outcome`）。异常较贵（要抓栈），但只在出错时抛一次，不在热路径。

**C++ 回答**：非法输入是少数情况时，异常让正常路径不带错误检查，一个 `catch` 就能把所有校验失败统一成 `Malformed`。如果坏行是常态（每秒百万行里很多坏行），异常每次约几微秒，就改用返回值：`std::optional`、`std::variant<Job, Error>`，或 C++23 的 `std::expected<Job, Error>`。

关键是能说出取舍：错误稀少用异常，错误常见用返回值。
