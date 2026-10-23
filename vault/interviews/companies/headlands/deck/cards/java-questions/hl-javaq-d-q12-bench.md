---
id: hl-javaq-d-q12-bench
node: java-questions.d-memory
type: qa
step: 8
---
## Q
拷贝 64 MB 数组，`arraycopy`、手写 for 循环、`Arrays.copyOf` 在预热期和稳态各是多快？为什么结论仍是"一般用 arraycopy"？

## A
- **第 1 轮（预热期）**：arraycopy 约 4 ms，for 循环约 5 ms，`Arrays.copyOf` 约 11 ms。
- **稳态**：arraycopy 约 1 ms，for 循环约 1 ms，`Arrays.copyOf` 约 3 ms。
- 稳态下循环和 arraycopy 一样快——C2 能把简单拷贝循环识别并替换成同样的拷贝（据计时判断，没看汇编）。
- 但预热期（解释器里）循环慢得多，所以**一般仍用 `arraycopy`**：意图清晰、预热期也快、检查齐全。
- `Arrays.copyOf` 慢，是因为多了分配和清零。
