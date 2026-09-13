# int02 · Payments Reconciliation：分页拉 charge → 退避重试 → 幂等退款对账 → webhook 验签，练的是"生产级 HTTP 客户端该有的四个边界处理"

> [!tldr]
> - 这题考的是：写一个真的会发 HTTP 请求的对账客户端——cursor pagination、429/5xx 退避重试、`Idempotency-Key`
>   幂等退款、webhook HMAC 验签，四个 part 递进叠加，不含任何算法
> - 三步套路：先把"发一次请求"的最小闭环跑通（起 mock server + 一次不分页的 GET）→ 再把四个边界处理模式各
>   自写成几行代码 → 最后把它们正确地串起来并测到位
> - 最值得带走的一个模式：**把"怎么发一次 HTTP 请求"收敛成一个独立的薄函数，业务逻辑只调用它、不碰
>   `urllib`/`requests` 的细节**——这样分页循环、退款、webhook 处理各自只剩"这一步该做什么判断"，而不是
>   到处重复 `urllib.request.Request(...)`

## 1. 题目在说什么（人话版）
Stripe 内部经常要拿"我方系统的记录"去对"Stripe 侧的记录"，比如商户后台余额 vs charges API。这题让你写一
个最小可行的对账客户端：连一个 Stripe 风格的假 payments API，把全部 charge 拉下来（对方分页返回，一页可
能拿不全）、和本地一份 CSV 账本比对，找出三类差异；同时要处理真实 HTTP 客户端在生产环境必须处理的事——
请求会被限流（429）、服务器会偶尔挂掉（5xx）、网络重试可能让同一个操作被执行两次（所以退款要幂等）、
webhook 回调可能是伪造的或重复投递的（所以要验签+去重）。**没有一行算法**，考的是你有没有在生产代码里
处理过"网络会失败、请求会重复、事件会乱序"这类边界情况的直觉。

小例子（Part 1，`limit=2` 强制分两页）：
```
第一页 GET /v1/charges?limit=2        -> {"data":[c1,c2],"has_more":true}
第二页 GET /v1/charges?limit=2&starting_after=c2 -> {"data":[c3],"has_more":false}
fetch_all_charges(...) 返回 [c1, c2, c3]
```

## 2. 读题：把文字变成模型
- **实体**：`charge`（远端记录，字段 `id`/`amount`/`status`）、本地账本行（字段名不同：`amount_cents`）、
  `refund`（幂等操作的结果）、webhook `event`（要验签+去重的外部输入）。
- **输入长什么样**：Part 1/2 是 HTTP 响应 JSON（`{"data": [...], "has_more": bool}`）；Part 3 多一份本地
  CSV；Part 4 是一个签名 header 字符串 + 一段 payload 字节。四个 part 的"输入"形状完全不同，这是这题和纯
  算法题最大的区别——你要读的是 API 文档，不是题面里的一个数组。
- **输出要什么**：Part 1 是一个 list；Part 2 是一次带重试的调用结果；Part 3 是三个排好序的差异列表；
  Part 4 是一个 `bool`。
- **状态**：`with_retry` 要记"这是第几次尝试"（决定退避时长）；`refund` 要在每次重试里带**同一个**
  `Idempotency-Key`（状态是"这次逻辑操作的身份"，不是请求本身的状态）；`handle_event` 要维护一个跨调用
  复用的 `set`（已处理过的 `event.id`）。
- **一句话建模**：这是一道**分层的 HTTP 客户端工程题**——一个薄的"发一次请求"函数在最底层，上面叠三个
  几乎相互独立的边界处理模式（pagination、backoff、idempotency）+ 一个不碰网络的纯函数（HMAC 验签）。

> [!note] 为什么先抽"发一次请求"这一层
> 候选做法是每个 part 各自拼 `urllib.request.Request(...)`，或者先写一个 `_request(method, path, ...)`
> 让所有 part 调用它。差异不在复杂度（两种写法逻辑上等价），而在**改动半径**：面试官如果追问"如果要加一
> 个通用的 timeout 参数/统一加个 header 呢"，前者要改三处，后者改一行。这是"深模块"的直觉在这题里的具体
> 体现——把易变的细节（怎么发请求）藏进一个函数，让业务逻辑（分页判断、退款决策）只依赖它的返回值和抛出
> 的异常类型。

## 3. 下笔顺序（60 分钟怎么分配）
这题最容易的失败模式是"上来就写 `with_retry` 想把重试逻辑一次写对"，结果 35 分钟过去了 happy path 还没跑
通。按下面的时间盒走，先让数据能进能出，再补边界：

- **0–5 读题确认**：把 API 文档过一遍，确认几个决定代码结构的细节——`starting_after` 是"上一页最后一条的
  id"不是 offset；429 直接读 `Retry-After` 照做（不指数增长），5xx 才是你自己估算的指数退避；`refund` 的
  `Idempotency-Key` 必须在**每一次**重试里都带同一个值；`verify_webhook` 的容忍度边界是 `<=`（300 秒仍
  有效，301 秒失效）。这些是问出来比自己猜省时间的细节。
- **5–15 跑通项目**：`python3 loop/mock.py serve int02 --port 0` 起 mock server，用 `curl` 或几行 Python
  发一次**不带分页参数**的 `GET /v1/charges?limit=5`，确认 `Authorization: Bearer sk_test_...` header 对、
  能拿到 JSON。这一步的唯一目标是把"我能和这个 API 说上话"这件事先验证掉，不要一上来就写分页循环。
- **15–35 happy path**：四个 part 的主线逻辑各写一遍，先不管错误处理。`with_retry` 先写成 `return fn()`
  占位；`fetch_all_charges` 写 `while True` 分页循环；`refund`/`load_ledger`/`reconcile` 写对账主线；
  `verify_webhook`/`handle_event` 写签名校验和去重的主干。每写完一个 part 立刻拿 worked example 或一次真
  实请求自测，不要攒到最后一起调。
- **35–48 错误处理**：回到 `with_retry` 补 429（读 `Retry-After`）、5xx（指数退避+抖动）、非 429 4xx（直
  接抛不重试）、`max_attempts` 耗尽（重新抛出最后一次异常）四个分支；补 `verify_webhook` 对畸形 header、
  篡改 payload、错误密钥、过期时间戳的防御性返回 `False`。这一段是本题真正的得分区——四个来源材料反复强
  调"只取第一页""无限重试无退避""静默失败"是最常见的失败模式。
- **48–55 清理**：把重复的 `urllib.request.Request(...)` 收敛成一个 `_request` 函数、检查函数是否
  ≤ 40 行、补类型标注和一句话 docstring、把裸 `except:` 换成具体异常类型。
- **55–60 总结**：把 problem.md 里的 worked examples 全部跑一遍核对，口头总结做了哪些简化（比如没有实现
  断点续传：`fetch_all_charges` 中途失败会直接抛异常，不会记住已经拉到第几页）。

## 4. 代码怎么组织
```
_request(base_url, method, path, api_key, body=None, extra_headers=None) -> dict   # 唯一碰 urllib 的地方
with_retry(fn, max_attempts=5, sleep=..., rng=...)                                  # 429/5xx 判断，不碰 urllib
fetch_all_charges(base_url, api_key, ...) -> list[dict]                             # 分页循环，调 with_retry(_request)
refund(base_url, api_key, charge_id, amount, idempotency_key, ...) -> dict          # 调 with_retry(_request)
load_ledger(path) -> list[dict]                                                     # 只管 CSV 解析
reconcile(local_rows, remote_charges) -> dict                                       # 纯函数，不碰网络
verify_webhook(payload, sig_header, secret, now, tolerance=300) -> bool             # 纯函数，不碰网络
handle_event(event, store) -> bool                                                  # 纯函数，不碰网络
main(stdin, stdout)                                                                 # 只做分发
```
拆分原则：**只有一层碰网络**。`_request` 是全文件唯一出现 `urllib.request.Request`/`urlopen` 的地方（本题
最终版本里 `fetch_all_charges` 的分页循环、`refund`、`main()` 的 `PART 2` 分支全都调用它，而不是各自拼
一份请求）；`with_retry` 只认识"`fn()` 抛不抛 `HTTPError`、状态码是多少"，完全不知道请求长什么样，这让它
能同时服务 GET 分页和 POST 退款两种完全不同的调用。`reconcile`/`verify_webhook`/`handle_event` 则是另一
个极端——纯函数，输入输出都是内存里的数据结构，单测时不需要起 mock server。这种"网络层 / 重试层 / 业务纯
函数层"三层分离，是这题从"能跑"到"面试官满意"的分水岭：陌生人看到 `refund` 函数体里没有一行 `urllib`，
立刻就知道"网络怎么发"和"这次操作幂等键怎么用"是两件事。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：一层薄的请求函数 + 分页循环 + 退避判断。省略解析、docstring、边界处理。
def _request(base_url, method, path, api_key, body=None, extra_headers=None):
    headers = {"Authorization": f"Bearer {api_key}"}
    headers.update(extra_headers or {})
    req = urllib.request.Request(base_url.rstrip("/") + path, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def with_retry(fn, max_attempts=5, sleep=time.sleep, rng=random.random):
    attempt = 0
    while True:
        attempt += 1
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if attempt >= max_attempts:
                raise
            if e.code == 429:                                    # 服务端说了要等多久，照做
                sleep(float(e.headers.get("Retry-After", 1)))
            elif 500 <= e.code < 600:                              # 服务端没说，自己估 + 抖动
                base = 0.05 * (2 ** (attempt - 1))
                sleep(base + rng() * base)
            else:
                raise                                              # 其他 4xx：重试没意义，立刻抛

def fetch_all_charges(base_url, api_key, limit=100, sleep=time.sleep):
    charges, starting_after = [], None
    while True:
        qs = f"limit={limit}" + (f"&starting_after={starting_after}" if starting_after else "")
        page = with_retry(lambda p=qs: _request(base_url, "GET", f"/v1/charges?{p}", api_key), sleep=sleep)
        charges.extend(page["data"])
        if not page.get("has_more"):
            return charges
        starting_after = page["data"][-1]["id"]

def refund(base_url, api_key, charge_id, amount, idempotency_key, sleep=time.sleep):
    body = json.dumps({"charge": charge_id, "amount": amount}).encode()
    headers = {"Content-Type": "application/json", "Idempotency-Key": idempotency_key}  # 每次重试都带同一个值
    return with_retry(lambda: _request(base_url, "POST", "/v1/refunds", api_key, body, headers), sleep=sleep)
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认几个会影响代码结构的细节：`starting_after` 是游标不是 offset；429 我直接读
  `Retry-After` 照做，5xx 才是我自己估算指数退避；`Idempotency-Key` 要在每次重试里带同一个值，漏了就会重
  复退款。」
- 写 `_request` 时：「我先抽一个只管『怎么发一次请求』的函数，GET 分页和 POST 退款都调它——这样
  `with_retry` 和业务逻辑都不用知道 header 怎么拼。」
- 写 `with_retry` 时：「429 和 5xx 我分开处理：429 服务端已经告诉我准确的等待时间；5xx 它没说，我自己估
  一个会随尝试次数翻倍的时长，再加点抖动防止一堆客户端同时重试撞在一起。」
- 写 `refund` 时：「这个函数会被 `with_retry` 包一层，意味着同一个 POST 可能真的被发出去两次——我把
  `Idempotency-Key` 放进 header dict，闭包每次重试都用同一份，不会在重试时换成新 key。」
- 写 `verify_webhook` 时：「我用 `hmac.compare_digest` 而不是 `==`，因为逐字节比较存在时序侧信道；任何格
  式不对的 header 我都返回 `False` 而不是抛异常，因为 webhook 端点必须对畸形/伪造请求保持健壮。」
- 交付时：「四个 part 都过了；我没做断点续传——如果分页中途失败到 `max_attempts` 耗尽，目前是异常直接抛
  出、已经拉到的部分丢弃，时间允许的话可以改成返回已拉到的数据 + 记住游标。」

## 7. 常见跑偏（方法层面，3 条）
- **一上来就死磕 `with_retry` 的完整重试逻辑**：429/5xx/其他 4xx 三个分支 + 抖动 + `max_attempts`，一次
  写全很容易卡住。先让它 `return fn()` 占位，把 Part 1/3/4 的主线跑通，最后 10 分钟回来集中补退避——这是
  这题四个 part 互相独立、可以乱序推进的地方，不必按 1→2→3→4 严格顺序写。
- **业务逻辑里散落 `urllib.request.Request(...)`**：GET 分页写一份、POST 退款写一份，两份高度相似但字段
  略有出入，改一处（比如加超时）容易漏改另一处。先抽出"发一次请求"这一层，其余函数只依赖它的返回值和抛
  出的异常类型，不知道请求是怎么发出去的。
- **把"能跑通 happy path"当成"做完了"**：这题的分值密度在错误路径上——429 有没有真的读 `Retry-After`、
  4xx 有没有被误当成可重试、`Idempotency-Key` 重试时有没有漏发、webhook 畸形输入有没有被吞成异常而不是
  返回 `False`。四个模式各自的核心逻辑都很短（分页循环本体约 10 行，`with_retry` 的 429+5xx 两个分支加
  一起约 20 行，`Idempotency-Key` 的关键动作只是"把这一行 header 放进闭包里、不要在重试时换掉"，
  `verify_webhook` 拼签名+比较的核心三行——`signed_payload`、`hmac.new(...).hexdigest()`、
  `hmac.compare_digest(...)`），难的从来不是单个模式本身，而是把它们正确串起来、每条错误路径都有对应测
  试。

## 8. 同族题 / 延伸
- 同一轮：int01 BikeMap 的 Part 3（PNG 魔数校验）和这题的 `verify_webhook` 是同一种"防御性解析、畸形输入
  一律返回失败值而不是抛异常"模式。
- 延伸思考：把 `fetch_all_charges` 改成支持"从上次失败的 `starting_after` 继续"的断点续传，只需要把游标
  作为可选参数传入、异常时把已拉到的数据和游标一起返回给调用方，不需要改 `with_retry`/`_request`。
- 同一模式换皮：任何"调用第三方分页 API + 遵守限流 + 保证重试幂等"的题都是这四个模式的排列组合（比如
  GitHub API 的 `Link` header 分页、AWS 的 `NextToken` 分页），语法不同，骨架一样。
- 练习命令：`python3 loop/mock.py serve int02 --port 0`（起 mock server 手动 `curl` 试探 API）；
  `rtk proxy python3 -m pytest loop/rounds/05_integration/int02_payments_reconciliation`（跑参考解测试）。
