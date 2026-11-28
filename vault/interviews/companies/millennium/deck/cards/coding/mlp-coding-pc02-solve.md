---
id: mlp-coding-pc02-solve
node: coding.pc02
step: 1
type: qa
---
## Q
**异步分页拉取：题与解**｜编程轮

有一个分页接口，`await fetch_page(page)`（页码从 1 开始）返回 `{"items": [...], "total_pages": n}`。写代码拉完所有页，要求并发拉取、同时在途的请求不超过 `max_concurrency`，输出顺序必须和按页码顺序翻页完全一致。再加一层：遇到临时错误（超时、5xx）要重试。

## A
**一句话思路。** 先拉第 1 页（只有它能告诉你一共几页），再用信号量（Semaphore，限制同时进入临界区的协程数）限流并发拉其余页；结果按页码下标写进预先留好位置的列表，而不是在协程里 `append`，这样完成顺序再乱，输出也按页码排。

```python
import asyncio

class TransientError(Exception):
    pass   # 模拟超时、5xx 这类值得重试的错误

async def fetch_all(fetch_page, max_concurrency, max_retries=3, base_delay=0.1,
                    sleep=asyncio.sleep):
    # sleep 作为参数注入：测试里换成立刻返回的假函数，不用真等
    async def fetch_retry(page):
        attempt = 0
        while True:
            try:
                return await fetch_page(page)       # 漏掉 await 只会拿到协程对象
            except TransientError:
                if attempt >= max_retries:
                    raise                           # 次数用完，把错误交给调用方
                await sleep(base_delay * 2 ** attempt)   # 指数退避：0.1, 0.2, 0.4 ...
                attempt += 1
            # 其他异常不捕获，直接向上传播，不重试

    first = await fetch_retry(1)
    total = first["total_pages"]
    if total < 1:
        raise ValueError("total_pages must be >= 1")
    pages = [first["items"]] + [[] for _ in range(total - 1)]   # 按页码预留位置
    sem = asyncio.Semaphore(max_concurrency)

    async def worker(page):
        async with sem:                              # 最多 max_concurrency 个同时在途
            pages[page - 1] = (await fetch_retry(page))["items"]   # 按下标写，不 append

    await asyncio.gather(*(worker(p) for p in range(2, total + 1)))

    out, seen = [], set()
    for items in pages:                              # 按页码顺序合并，顺便去重
        for it in items:
            if it not in seen:
                seen.add(it)
                out.append(it)
    return out

async def demo():
    data = {1: ["a", "b"], 2: ["b", "c"], 3: ["d"]}
    calls = {2: 0}
    async def fetch_page(p):
        if p == 2 and calls[2] < 2:                  # 第 2 页先失败两次
            calls[2] += 1
            raise TransientError()
        await asyncio.sleep(0.01 * (4 - p))          # 后面的页反而先返回
        return {"items": data[p], "total_pages": 3}
    print(await fetch_all(fetch_page, 2, base_delay=0))   # ['a', 'b', 'c', 'd']

asyncio.run(demo())
```

**复杂度。** 请求次数 N（页数），总耗时约 N / max_concurrency 个往返；内存 O(总条目数)。

**边写边讲。**
- "I'll model the HTTP client as an **injectable async function**, since I can't make real calls here."
- "I write results into a list **indexed by page number**; completion order under concurrency is not page order."
- "A **semaphore** caps in-flight requests, and I retry only **transient** errors with exponential backoff."
