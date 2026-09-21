# pc02 · Async Paginated API Ingestion：练的是"并发下怎么保证顺序"

> [!tldr]
> - 这题考的是：用 `asyncio` 翻一个分页 API，从顺序翻页升级到并发限流，还要顺序不能乱
> - 三步套路：顺序翻页拿到最小可用版 → 加 `Semaphore` 限并发但按页码装配结果 → 加重试与去重
> - 最值得带走的一个模式：**并发时"谁先完成"和"最终顺序"是两件事**——按索引写入预先留好的位置，
>   永远不要在并发任务内部直接 `append` 到共享列表

## 1. 题目在说什么（人话版）

有一个分页 API，每次请求返回当前页的数据和"一共有多少页"。顺序翻到最后一页很容易；但如果要求
用并发加速（限制同时在途的请求数），输出还必须和顺序翻页时一模一样，不能因为哪一页先返回就排到
前面。

```
输入（模拟 4 页，每页 1 个 item，第 2 页故意最慢）：
fetch_page(1) -> {"items": ["p1"], "total_pages": 4}
fetch_page(2) -> {"items": ["p2"], "total_pages": 4}   # 延迟最大
fetch_page(3) -> {"items": ["p3"], "total_pages": 4}
fetch_page(4) -> {"items": ["p4"], "total_pages": 4}   # 最快返回

并发抓取（限并发 4），输出仍然是：
["p1", "p2", "p3", "p4"]     # 不是按完成顺序的 ["p1","p4","p3","p2"]
```

## 2. 读题：把文字变成模型

- **实体**：一个可注入的 async 函数 `fetch_page(page) -> {"items": [...], "total_pages": n}`，
  面试环境不能真发网络请求，这就是它的替身。
- **输入长什么样**：`page` 是 1-based 页码；`total_pages` 只有第一页的返回值才靠谱。
- **输出要什么**：所有页 `items` 按页码顺序拼接成一个列表。
- **状态**：Part 1 不需要额外状态（顺序 await）；Part 2 需要一个**按页码索引、预先留好位置**的
  列表，外加一个 `Semaphore` 限流；Part 3 再加一个"已重试次数"和一个"已见过的 item"集合。
- **一句话建模**：这是一个**并发扇出、按原始顺序收拢结果**的问题——map-reduce 里"map 并发跑、
  reduce 阶段必须对齐原始索引"的最小版本。

> [!note] 为什么不能在协程里直接 append
> 直接 `results.append(await fetch_page(p))` 在并发下顺序等于完成顺序，不等于页码顺序——这正是
> 报道里"missing output"那个 bug 的真身：不是数据丢了，是顺序乱了导致看起来像丢了。用页码当下标
> 写入一个预先分配好长度的列表，才能保证顺序和请求发出的顺序一致，与完成时间无关。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`main()` 读入 → 按 part 分发 → `asyncio.run(...)` → 打印。
2. **Part 1 最小可用**：`await fetch_page(1)` 拿 `total_pages`，`for page in range(2, total_pages+1)`
   依次 `await`；每次样例自测。
3. **Part 2 叠加**：把"顺序 for 循环"换成"`asyncio.Semaphore` + `asyncio.gather`"，但结果写进一个
   按页码索引的列表，不是普通 `append`；先说清楚这个设计，再动手写。
4. **Part 3 叠加**：给 `fetch_page` 包一层重试（`try/except TransientError` + 指数退避
   `sleep`），最外层加一个 `seen` 集合去重。
5. **收尾**：`max_concurrency < 1`、`max_retries < 0`、非 `TransientError` 异常不重试，逐条过一遍。

## 4. 代码怎么组织

```
fetch_all_sequential(fetch_page) -> list[str]                     # Part 1
fetch_all_concurrent(fetch_page, max_concurrency) -> list[str]    # Part 2
fetch_all_with_retry(fetch_page, max_concurrency, max_retries,
                      base_delay, sleep) -> list[str]              # Part 3，sleep 可注入方便测试
part1/2/3(lines) -> list[str]      # 从文本构造一个内存里的 fake fetch_page，再调用上面的函数
main(stdin, stdout)                # 分发
```
`sleep` 作为参数注入是这份 kit 的通用写法（限流器、TTL 缓存都这么干）：测试不需要真的等
`2**attempt` 秒，换一个立刻返回的假 `sleep` 就能秒级跑完重试逻辑的断言。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
async def fetch_all_concurrent(fetch_page, max_concurrency):
    first = await fetch_page(1)                    # 唯一能知道 total_pages 的办法
    total_pages = first["total_pages"]
    pages_items = [first["items"]] + [[] for _ in range(total_pages - 1)]  # 按页码预留位置

    semaphore = asyncio.Semaphore(max_concurrency)
    async def _fetch(page):
        async with semaphore:
            result = await fetch_page(page)
            pages_items[page - 1] = result["items"]  # 按下标写，不是 append

    await asyncio.gather(*(_fetch(p) for p in range(2, total_pages + 1)))
    items = []
    for page_items in pages_items:                  # 按页码顺序拼接
        items.extend(page_items)
    return items
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「I'll model the HTTP client as an injectable async function `fetch_page(page)` that
  returns items plus `total_pages`, since I can't make a real network call here.」
- 写 Part 2 时：「I'm writing results into a list indexed by page number rather than appending
  inside each task, because completion order under concurrency isn't the same as page order —
  that's the bug the 'missing output' report was actually describing.」
- 交付时：「Sequential and concurrent versions agree on the same fake data; if time allows, I'd add
  retry with exponential backoff and de-dup for at-least-once delivery.」

## 7. 常见跑偏（方法层面，3 条）

- 一上来就写 `results.append(await fetch_page(p))` 在 `asyncio.gather` 里——这是"missing output"
  报道里那个 bug 本身，先讲清楚"完成顺序 ≠ 页码顺序"再动手。
- 忘记 `await`：`fetch_page(page)` 不加 `await` 拿到的是协程对象，不是结果，后续操作会在不同地方
  报错，排查起来比直接崩溃更烦。
- 把"重试延迟"写死成 `time.sleep`（同步阻塞）而不是 `await asyncio.sleep`——会卡住整个 event
  loop，其它协程也跟着停摆。

## 8. 同族题 / 延伸

- 本 kit `pc09_price_data_store`（若已建）：同样有"迟到数据/乱序到达"的讨论。
- `../../stripe/problems/q27_payment_ledger/`：同一个"客户端会重试，处理逻辑必须幂等"母题，换成
  了支付账本场景。
- `../../snowflake/loop/rounds/03_phone_coding/pc03_recent_event_stream/`：追问 3 提到并发写入的
  加锁讨论，和本题"并发下的顺序/一致性"是同一类问题。
- 练习命令：`python3 loop/mock.py start pc02`
