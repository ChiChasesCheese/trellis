---
id: hl-cq-q38-script
node: cpp-questions.i-low-latency
type: qa
step: 15
---
## Q
用英文 60 秒回答：What is branch prediction? How does it show up in code?

## A
结构：预测与 15–20 周期的误判代价 → 只有不可预测的数据相关分支才是问题（47 ms 随机、8 ms 排序、6 ms 无分支）→ 对策：可预测化、无分支、冷路径外移，用 `perf stat` 验证。

- The CPU pipeline fetches ahead, so at a branch it **predicts** the direction. A correct guess is nearly free; a misprediction flushes the pipeline and costs on the order of 15 to 20 cycles.
- Predictable branches are fine; the problem is **unpredictable, data-dependent** ones. Same loop, 20 million random bytes: with a branch it took 47 ms on random data and 8 ms once the data was sorted; a **branchless** version - always write, advance the cursor by the comparison result - took 6 ms on random data.
- So I either make branches predictable, restructure into branchless arithmetic or conditional moves when the data is random, or keep rare paths cold. I'd confirm with `perf stat` branch-misses, not guess.
