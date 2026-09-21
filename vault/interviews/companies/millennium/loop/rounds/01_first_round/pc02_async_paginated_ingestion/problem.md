# pc02 · Async Paginated API Ingestion — 顺序翻页 → 并发限流保序 → 退避重试 + 幂等去重

> Millennium LEaD 第一轮（45 min：15 min 背景 + 30 min 实时编码，Webex + HackerRank）。Part 1、
> Part 2 是一手报道的原题机制；Part 3 **(reconstructed)**。

## 背景

PracHub 报道 Millennium 技术筛选（2025-09-06）出过"Implement paginated API ingestion"，同一渠道
2025-10-24 又报道一题"Debug missing output in Python async HTTP flow"；LeetCode Discuss 7423863
（Round 2）独立确认"Asyncio — write working code and explain how coroutines work"；1point3acres
thread-1124751 有异步编程追问的讨论。HackerRank 沙箱不能真的发网络请求，所以三条报道共同指向同一个
抽象：把"HTTP 客户端"换成一个可注入的 async 函数

```python
async def fetch_page(page: int) -> dict  # {"items": list[str], "total_pages": int}
```

`total_pages` 只在**第一页**的返回里才有意义地被"发现"——这和真实分页 API 把总数放在首个响应体或
响应头里是同一回事；后续页原样带回它，调用方不需要特判"我是不是已经拿到 total_pages 了"。
"Debug missing output" 那道题的典型 bug——并发抓取时按协程完成顺序往列表里 append，导致输出顺序
和页码对不上、看起来像"丢了数据"——正是 Part 2 要求"保持输出顺序稳定"所防的那个坑。

## API 契约（英文签名）

```python
class TransientError(Exception): ...

async def fetch_all_sequential(fetch_page: FetchPage) -> list[str]
async def fetch_all_concurrent(fetch_page: FetchPage, max_concurrency: int) -> list[str]
async def fetch_all_with_retry(
    fetch_page: FetchPage,
    max_concurrency: int = 1,
    max_retries: int = 3,
    base_delay: float = 0.1,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> list[str]
```
`FetchPage = Callable[[int], Awaitable[dict]]`：给定 1-based 页码，返回
`{"items": list[str], "total_pages": int}`。`max_concurrency < 1` 或 `max_retries < 0` →
`ValueError`；`fetch_page` 返回的 `total_pages < 1` → `ValueError`。

## 规则

### Part 1 — 顺序翻页（一手原题的基本形状）

从第 1 页开始，`await fetch_page(page)` 依次拿到每一页，读出 `total_pages` 后一路翻到最后一页，
按到达顺序拼接 `items`。没有并发，输出顺序天然就是页码顺序。

### Part 2 — 并发限流、保持输出顺序稳定（一手原追问 + "missing output" 的修复）

先取第 1 页拿到 `total_pages`（这是唯一能知道总页数的办法），再用 `asyncio.Semaphore(max_concurrency)`
把第 2..total_pages 页一起丢给 `asyncio.gather` 并发抓取。**输出必须按页码顺序拼接，不能按协程完成
顺序**——用一个按页码索引、预先留好位置的列表收结果，而不是在每个协程里直接 `append` 到共享列表。

### Part 3 — 指数退避重试 + 幂等去重 **(reconstructed)**

在 Part 2 的并发流水线上叠两件事：
- `fetch_page` 抛出 `TransientError`（模拟超时/5xx）时重试，最多 `max_retries` 次，退避时长
  `base_delay * 2**attempt`（通过可注入的 `sleep` 参数等待，测试不会真的等）；抛出其它异常**不
  重试**，直接向上传播。
- **幂等去重**：最终结果按页码顺序、页内按首次出现顺序合并；一个已经出现过的 item（不管是来自更
  早的页，还是同一页因重试而被重复交付）不再被计入第二次。

## Worked examples（全部由 `solution.py` 实际运行得出，不手算）

**例 1（Part 1，`total_pages=3`）**
```python
lines = ["3", "a,b", "c", "d,e"]
part1(lines)
```
→ `['a', 'b', 'c', 'd', 'e']`

**例 2（Part 2，`max_concurrency=2`，各页延迟不同：第 2 页最慢、第 1/4 页最快，输出仍按页码排）**
```python
lines = ["4 2", "p1", "p2", "p3", "p4"]
part2(lines)
```
→ `['p1', 'p2', 'p3', 'p4']`（用真实的 `fetch_page` 注入延迟 `{1:0, 2:0.05, 3:0.01, 4:0}` 验证过：
即使第 3、4 页比第 2 页先返回，输出依然是 `p1,p2,p3,p4`，不是完成顺序 `p1,p4,p3,p2`）

**例 3（Part 3，第 2 页失败 2 次后成功；第 1、2 页有一个重叠 item `"b"`，只输出一次）**
```python
lines = ["2 2 3", "a,b|0", "b,c|2"]
part3(lines)
```
→ `['a', 'b', 'c']`（不是 `['a','b','b','c']`；`"b"` 按首次出现——第 1 页——保留一次）

## `main()` 命令流

```
PART 1              PART 2                  PART 3
3                   4 2                     2 2 3
a,b                 p1                      a,b|0
c                   p2                      b,c|2
d,e                 p3
                    p4
→ a                 → p1                    → a
  b                    p2                      b
  c                    p3                      c
  d                    p4
  e
```
每页一行：`-` 表示空页（没有 item）；Part 3 每页是 `<items>|<fail_times>`，`fail_times` 是这一页
在成功前要先抛几次 `TransientError`。

## 边界清单

- 空页（该页 0 个 item，行内容是 `-`）——不能让输出跳过整页导致后续页错位
- `total_pages = 1`：Part 2/Part 3 不需要任何并发调度，第 1 页本身就是全部结果
- 页数与声明的 `total_pages` 不一致（页行数 ≠ `total_pages`）→ `ValueError`
- `max_concurrency < 1`、`max_retries < 0` → `ValueError`
- `fetch_page` 抛出非 `TransientError` 的异常（比如 `RuntimeError`）→ **不重试**，立即向上传播，
  且不应该消耗任何 `sleep` 调用
- 重试次数刚好耗尽（`fail_times == max_retries`）仍应成功；`fail_times == max_retries + 1` 应该
  最终把 `TransientError` 抛给调用方
- 并发限流的硬约束：任意时刻同时在途的 `fetch_page` 调用数不超过 `max_concurrency`
- 跨页重叠 item 的去重按**首次出现（页码优先，页内序号其次）**保留，不是"后来者覆盖"
- 输出为空（`total_pages=1` 且该页也是空页）

## 追问

1. **coroutine 和 thread 的区别？**——协程是单线程内的协作式调度，`await` 主动让出控制权；线程是
   抢占式调度，操作系统随时可能切换。asyncio 的并发靠"I/O 等待时让出"，不靠多核。
2. **event loop 在哪？**——`asyncio.run()` 创建并驱动一个事件循环，所有 `await` 点都是它调度协程
   的机会；本题里 `asyncio.gather` 把多个协程交给同一个循环交替推进。
3. **"missing output" 的典型 bug 是什么？**——在每个并发任务内部直接 `results.append(...)`，输出
   顺序变成"谁先返回谁先出现"，业务上看起来像"数据丢了/错位了"，其实是顺序没保证；修法是按页码
   索引写入预先留好的位置。
4. **漏写 `await` 会怎样？**——`fetch_page(page)` 不加 `await` 得到的是一个 coroutine 对象而不是
   结果，后续对它做 `.extend()`/下标访问会直接抛类型错误或悄悄拿到空值，取决于哪一步先出错。
5. **超时怎么加？**——`asyncio.wait_for(fetch_page(page), timeout=...)`，超时可以包装成
   `TransientError` 复用同一套重试逻辑。

## 来源与置信度

- **HIGH**：PracHub Millennium 页面"Implement paginated API ingestion"（Technical Screen，
  2025-09-06）+ "Debug missing output in Python async HTTP flow"（2025-10-24）。
- **HIGH（一手）**：LeetCode Discuss 7423863（2025-12，Quant Developer-Python，Round 2）
  "Asyncio — write working code and explain how coroutines work"。
- 1point3acres thread-1124751：异步编程追问（协程/事件循环/漏写 await 的典型 bug）的独立佐证。
- Part 3（指数退避重试 + 幂等去重）为重建：三条来源都指向"异步分页抓取"这个核心机制，但都没有
  给出完整的重试/去重规则，按"分页抓取题最常见的下一层追问"补全。

## 考什么

asyncio 基本模型（event loop、协程 vs 线程）· `asyncio.Semaphore` 限并发 · 并发下的顺序保证
（按索引写入而不是按完成顺序 append）· 指数退避重试与"哪些异常该重试"的判断 · 幂等/去重。
