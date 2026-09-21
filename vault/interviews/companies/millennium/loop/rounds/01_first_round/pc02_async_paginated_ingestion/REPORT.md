# pc02 Async Paginated API Ingestion — report

## Summary
Millennium LEaD 第一轮实时编码，三条独立报道共同指向的"异步分页抓取"题：PracHub 的
"Implement paginated API ingestion" + "Debug missing output in Python async HTTP flow"，与
LeetCode Discuss 的"Asyncio — write working code and explain how coroutines work"。3-part：
Part 1 顺序翻页（一手基本解）→ Part 2 `asyncio.Semaphore` 限并发、按页码而非完成顺序拼接结果
（一手原追问，同时是"missing output"报道的修复）→ Part 3 指数退避重试 + 幂等去重
**(reconstructed)**。

## Sources & confidence
HIGH：PracHub Millennium 页面（Technical Screen，2025-09-06 + 2025-10-24）；LeetCode Discuss
7423863（2025-12，Quant Developer-Python，Round 2）。1point3acres thread-1124751 为异步追问的
独立佐证。Part 3 为重建。

## Approach by part
1. `fetch_page(1)` 先拿到 `total_pages`，再 `for page in range(2, total_pages+1)` 依次
   `await`；没有并发，输出天然按页码顺序。
2. 同样先取第 1 页；第 2..total_pages 页用 `asyncio.Semaphore(max_concurrency)` +
   `asyncio.gather` 并发抓取，但写入一个按页码预先留好位置的列表，最后按索引顺序拼接——不是按
   协程完成顺序 `append`。
3. 在 Part 2 的流水线外包一层 `_fetch_with_retry`：捕获 `TransientError`，重试
   `base_delay * 2**attempt` 秒（通过可注入的 `sleep` 参数），最多 `max_retries` 次；其它异常
   直接向上抛。最终合并时用一个 `seen` 集合按首次出现去重。

## Pitfalls hidden tests target
- 并发下输出顺序必须是页码顺序，不是完成顺序（`test_part2_order_stable_under_variable_latency`：
  故意让第 2 页最慢、第 4 页最快）
- 并发上限是硬约束：任意时刻同时在途的调用数不超过 `max_concurrency`
  （`test_part2_concurrency_is_bounded` 用 in-flight 计数器断言峰值恰好等于限流值）
- Part 1 必须真的是顺序的，不能偷偷并发（`test_part1_calls_are_strictly_sequential` 断言峰值
  in-flight == 1）
- 非 `TransientError` 的异常不重试、不消耗任何 `sleep` 调用（`test_part3_non_transient_exception_not_retried`）
- 退避时长精确等于 `base_delay * 2**attempt`（`test_part3_exponential_backoff_delays` 用注入的
  spy sleep 断言具体数值 `[1.0, 2.0]`）
- 重试次数恰好耗尽 vs 多一次的边界（`test_part3_retry_succeeds_within_budget` /
  `test_part3_retries_exhausted_raises`）
- 跨页重叠 item 按首次出现去重，不是"后来者覆盖"（`test_part3_dedup_preserves_first_seen_order`）
- 空页（`-`）不能让后续页错位（`test_part1_empty_page_does_not_shift_alignment`）
- `max_concurrency < 1`、`max_retries < 0`、声明页数与实际页行数不一致 → 均 `ValueError`

## Complexity & measured cost
Part 1：O(total_pages) 次顺序 `await`，总耗时 ≈ Σ每页延迟。Part 2/3：O(total_pages / max_concurrency)
批次，总耗时 ≈ 批次数 × 单页延迟（远小于顺序耗时）。
实测：200 页、每页模拟 10ms 延迟、`max_concurrency=50`，`fetch_all_concurrent` 端到端 0.057s
（顺序版理论上要 2s）；10 页、`max_concurrency=3`、每页 20ms 延迟，实测峰值同时在途调用数恰好是
3（`test_part2_concurrency_is_bounded`），验证限流生效。`test_part2_perf_200_pages_bounded_concurrency`
断言 < 2.0s。

## Test inventory
22 tests（`grep -c "def test"`，23 collected including 1 组 2 值参数化）— part1 7（含 1 io）·
part2 7（含 1 perf、1 io）· part3 8（含 2 组参数化非法输入、1 io）；edge 15 · perf 1 · io 3。

## Skills exercised
S07 asyncio 并发模式（`Semaphore` 限流、`gather` 保序）· S08 复杂度/并发权衡（顺序 vs 并发的耗时
对比）· S04 重试与幂等（指数退避、区分可重试/不可重试异常、去重）。
