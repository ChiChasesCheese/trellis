# CODE_GUIDE — fetchrace

给第一次读 `asyncio` 代码的人看的导览。讲代码在做什么、模块怎么互相调用、以及并发代码里最容易
想岔的几个点。**不讲这道题的 bug 在哪** —— 那是练习本身要你去找的东西。

## 数据流

```
  urls: ["url1", "url2", ...]
        │
        ▼
  crawler.py  fetch_all(urls, concurrency=N)
        │  为每个 url 建一个 fetch_one() 任务，一起丢给 asyncio.gather()
        │  一个 Semaphore(N) 保证同一时刻最多 N 个任务真正在做网络请求
        ▼
  crawler.py  fetch_one(sem, url, fetcher)  ← 每个 url 一份
        │  await sem.acquire()  拿到"许可"才能继续
        ▼
  retry.py    fetch_with_retry(url)
        │  失败就退避重试几次，每次等更久
        ▼
  http_client.py  fetch_url(url)
        │  真正发 HTTP 请求（丢给线程池执行，因为它本身是阻塞的）
        ▼
  （本地测试用的 http.server，见 tests/support/server.py）
        │
        │ 每个 url 的结果：一个 FetchResult，或者一个 Exception
        ▼
  crawler.py  aggregate(raw_results)  →  Stats(total, succeeded, failed, errors, bodies)
```

## 逐模块

### `http_client.py` — 最底层，发一次 GET
`urllib.request.urlopen` 是阻塞调用（发出去之后整个线程会卡住，直到收到响应），`asyncio` 的协程
不能直接 `await` 一个阻塞函数。`fetch_url` 的做法是把它扔进事件循环自带的线程池
（`loop.run_in_executor`），然后 `await` 那个线程池任务——真正卡住的是线程池里的某个工作线程，
执行 `fetch_url` 这个协程本身所在的那条"主线"（事件循环线程）在 `await` 的这一刻是空出来的，
可以去处理其他协程。任何非 2xx/3xx 状态码或网络层面的失败，都会被包装成 `FetchError` 抛出来。

### `retry.py` — 失败了就退避重试
`fetch_with_retry` 包了一层重试逻辑：调 `fetch(url)`，失败就 `await asyncio.sleep(delay)` 等一
会儿再试，每次失败后等待时间翻倍（指数退避），试够 `retries` 次还失败就把最后一次的异常继续往上
抛。`fetch` 参数默认是 `http_client.fetch_url`，但可以换成任何"给个 url、返回 bytes"的协程函数——
测试里经常传一个假的 `fetch`，跳过真实网络请求。

### `crawler.py` — 限流 + 聚合
这是三个模块里最重要的一个，分三块看：

- `fetch_one(sem, url, fetcher)`：处理**一个** url。先 `await sem.acquire()` 拿到一个"名额"，
  再调 `fetcher(url)`（正常情况下就是 `retry.fetch_with_retry`），最后把名额还回去
  （`sem.release()`），返回一个 `FetchResult(url, body)`。
- `fetch_all(urls, concurrency, fetcher)`：给每个 url 建一个 `fetch_one` 任务，一次性交给
  `asyncio.gather(*tasks, return_exceptions=True)` 去跑。`return_exceptions=True` 的意思是：某个
  任务内部抛了异常，`gather` **不会**把这个异常继续往外抛、也不会取消其他还在跑的任务——它会把
  这个异常对象本身，原封不动地放进返回列表里那个位置，当成一个普通的返回值。
- `aggregate(raw_results)`：把 `gather` 返回的那个"有的位置是 `FetchResult`、有的位置是
  `Exception`"的列表，翻译成一份汇总（`Stats`）：总数、成功数、失败数、失败的异常列表、成功的
  响应体字典。

### `Semaphore` 的语义
`asyncio.Semaphore(N)` 内部维护一个从 N 开始的计数器。`acquire()` 会把计数器减一，如果减到负数
（也就是已经有 N 个人拿着"名额"没还）就阻塞，直到有人 `release()` 把计数器加回来。`release()`
把计数器加一。这套机制存在的唯一意义就是：**每一次 `acquire()` 都必须最终对应恰好一次
`release()`**，不管中间那段代码是正常跑完、还是半路抛了异常——少 `release()` 一次，"名额"就永久
少了一个，多 `release()` 一次，限流形同虚设。

## 读并发代码时容易误解的地方

这几点不是这道题专属的坑，是读任何 `asyncio` 代码之前都该先弄清楚的机制。

**1. `await` 是"让出执行权"的那一刻，不是"什么都没发生"。** `asyncio` 是单线程协作式调度：同一
时刻只有一个协程在真正执行 Python 代码，但每次遇到 `await` 一个还没完成的东西（网络 I/O、
`asyncio.sleep`、另一个协程），当前协程就把控制权交还给事件循环，事件循环转而去推进其他就绪的
协程。这意味着两次 `await` 之间的代码是"原子"的（不会被别的协程插进来打断），但**跨越一个
`await` 的两段代码之间**，任何共享状态都可能已经被其他协程改过——`await` 本身就是并发交错真正
发生的地方。

**2. `asyncio.gather()` 返回结果的顺序，是你传入协程的顺序，不是它们完成的顺序。** 哪怕
`tasks[2]` 比 `tasks[0]`先跑完，`gather(*tasks)` 返回的列表里，第 0 个位置永远对应 `tasks[0]`
的结果。这是很多人第一次写并发抓取代码时会搞反的地方：以为结果列表反映的是"谁先跑完"，实际上
反映的是"你当初怎么排列输入"。

**3. `return_exceptions=True` 只是把异常从"会中断 gather"变成"会出现在结果列表里"，不会替你
把它和正常结果区分开。** 拿到结果列表之后，每一项到底是真实返回值还是一个 `Exception` 实例，
需要调用方自己用 `isinstance(item, Exception)` 去判断——`gather` 本身不会做这件事，也不会告诉你
"第几项失败了"，它就是把两种东西放进同一个列表里，形状看起来一模一样。

**4. `Semaphore`/锁这类"需要成对操作"的资源，跟异常处理是强绑定的两件事。** `acquire()` 之后
如果中间那段代码可能抛异常，"归还"这个动作就必须写在 `try/finally` 里，而不能写在正常执行路径
的最后一行——写在最后一行意味着"只有没出错才会归还"，这在逻辑上等于说异常路径永远不归还。这不是
`asyncio` 独有的问题（`threading.Lock`、数据库连接池的 `checkout`/`checkin` 都是同一个道理），
只是 `asyncio` 里因为 I/O 密集、异常常见（超时、连接失败），这类 bug 格外容易被真实网络问题
触发出来。

**5. `asyncio` 的并发 bug 通常是"逻辑上必然发生"的，不是"运气不好才发生"的。** 因为同一时刻只有
一个协程在执行代码（不像多线程真的有 CPU 级别的并行），只要你能构造出同样的一组输入（同样的 url
列表、同样谁失败谁成功），交错方式就是确定的、可重复的——这也是为什么 `asyncio` 版本的并发 bug
往往比 `threading` 版本更容易写出"每次跑都必现"的失败用例，不需要 `Barrier` 或人工加
`sleep` 去赌运气。

---
练到第二遍就别再看这份指南了——真实面试现场没有人会给你一张"这个模块负责什么"的说明书。
