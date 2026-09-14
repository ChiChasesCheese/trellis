# 05 · Onsite · Integration（60 min）

> 事实层在 `loop/LOOP_GUIDE.md` §5。本章讲练法。

## 这轮到底考什么

**不考算法。** 考：读文档的速度、HTTP 客户端的错误处理、对陌生数据结构的警惕、以及代码在"需求还会继续加码"时的模块化程度。

形式是 **open-book**：私有 repo（README、boilerplate、示例数据、API 文档）→ 本地跑起来 → 4–5 个递进 part。**可联网查文档，禁 AI**。需求有时写在 GitHub issue 里且**不可复制**。

一手评价点破了这轮的性质：

> "very easy api calling but easy for everyone so you have to be perfect"

**简单，所以不允许出错。**

## 通过线（这轮的通过线出奇地低）

2/5、2.5/5（有提示）、3/5、3.9/5 都有人过。共识是：

> **integration 没做完 或 bug squash 差，二选一还能过；两个都弱必拒。**

但**定级会受影响**：有候选人因为没做完 Part 3 从 L3 降到 L2。

多数候选人 60 分钟内做不完 5 个 part。**Part 1–2 的实现质量、代码整洁度比"做完几个 part"更被看重。**

## ⚠️ 先说一件比时间表更重要的事：60 分钟可能只有 35 分钟写代码

2026-04 一位 4 YOE 候选人的一手复盘（他因此只做完 2/4 part）：

> "interviewer gave me **35 minutes only**, told he would use **10 minutes in the end for discussion,
> 10 minutes in starting for setting up my IDE and github account** for integration round.
> (Also the interviewer kind of **arrived late 4-5 minutes**)"

开场那 10 分钟是**唯一你能自己拿回来的**。进场前必须已经就绪并跑过一次：
**IDE · GitHub 登录 · SSH key · clone 目录 · 语言 runtime · 一个能跑的 hello world**。

## 60 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–5 | 读题，**确认输出格式**，问清假设 |
| 5–15 | 跑通项目，定位要改的代码在哪 |
| 15–35 | happy path 打通 |
| 35–48 | 错误处理 / 边界 |
| 48–55 | 清理（命名、拆函数、删调试代码） |
| 55–60 | 总结：做到哪、剩下的会怎么做 |

**保守版（实测更接近这个）**：装环境 0–10（提前做掉就是白赚 10 分钟）· 读题 + happy path 10–30 ·
错误处理 30–42 · 清理 42–48 · 讨论 48–60。

**5–15 这一段是最容易失控的。** 环境跑不起来能吃掉 20 分钟。提前拿 recruiter 发的 sample repo 演练一次。

## ⭐ 真实的四段式结构（2025-08 Dublin senior 一手，逐字）

> "there's **4 sub-rounds**. To begin with, you're given a **hello world boiler plate code** and you're expected to
> **call an API and print the response**. The request parameters are expected to be **read from a file — so file
> parsing is essential**. In the second one, you're asked to **parse the response and use it to call yet another
> API**. The subsequent rounds follows suit by increasing complexity in terms of forming the request and parsing
> the response. Use of an ide is permitted. The challenge here is **time** since **requirements change across
> sub-rounds** and thus **if the code is modular enough from the beginning, it helps**."

三条直接可操作的：

1. **part 1 就拆成三个函数**：`build_request()` / `call()` / `parse()`。别写成一个 `main`。
   需求每个 sub-round 都变，不拆就是每轮重写——这是他原话里唯一给出的"打法"。
2. **请求参数是从文件里读的**，不是硬编码 URL。文件解析在 part 1 就要用上。
3. **part 数不固定**：这位是 4 段，London 那位是 5 part，Dublin 另一位只有 3 part。别按固定数排时间。

## 八个挂点（extrabrain 整理）

1. 没搞清**输出格式**就写
2. 环境配置太久
3. 忽视错误处理
4. 过度设计
5. 忘跑面试官给的测试
6. 硬编码样例特判
7. 轻视支付安全细节
8. 卡住沉默

第 1 条是头号杀手，而且最好防：**开场就问"输出格式能给我一个样例吗"**。

## 手速要练到什么程度

这些必须**不用查文档**就能写：

```python
# POST JSON
req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                             headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.loads(r.read().decode())

# 二进制落盘（注意 "wb"）
with open(path, "wb") as f:
    f.write(r.read())

# 游标分页拉全量
while True:
    page = get(f"{url}?limit=100" + (f"&starting_after={cursor}" if cursor else ""))
    yield from page["data"]
    if not page["has_more"]:
        break
    cursor = page["data"][-1]["id"]
```

`urlopen` 对 4xx/5xx **抛 `HTTPError` 而不是返回** —— 这个不熟会让你的第一次错误处理写歪。

完整清单见 `loop/study/20-cards/http_json.md`（44 张）。

## 必须背下来的 Stripe API 语义

Integration 轮直接考这些（详见 `loop/study/20-cards/stripe_api.md`）：

- **幂等**：同一个 key 重放会返回**原来那个响应，包括 500**；改了参数用同 key 会报 `idempotency_error`；网络错误重试**要**沿用原 key
- **分页**：游标（`starting_after` / `ending_before`，互斥），`has_more` 判尾，`limit` 默认 10 上限 100
- **429**：先读 `Retry-After`；退避要加**抖动**；**不是所有 429 都该退避**——`lock_timeout` 是抢锁不是限流
- **webhook 验签**：`Stripe-Signature` 是 `t=...,v1=...`，HMAC-SHA256 签 `f"{t}.{raw_body}"`，**常数时间比较**，容忍度 5 分钟且**不能设 0**，必须用 **raw body**
- **金额**：整数最小单位，永不用 float

## 一个真实的坑（int01 埋了它）

**GeoJSON 的坐标是 `[lng, lat]`（经度在前）**，而多数渲染 API 的 `points` 用人类习惯的 `[lat, lng]`。两者相反。这是 bikemap 题最经典的死法。

推而广之：**拿到陌生数据结构，先打印一条真实记录看清楚**，别按直觉假设字段顺序。

## 明天怎么练（具体到命令）

```bash
# 终端 A
python3 loop/mock.py serve int01
# 终端 B
python3 loop/mock.py start int01 -m 60
```

顺序：**int01（bikemap，最高频）→ int02（分页/限流/幂等，语义最密）→ int03（多 JSON ETL）→ int04（subprocess 调 git）**。

int01 **完整跑通两遍**。第一遍你会花时间在"怎么发请求"上，第二遍才是真的在练这轮。

## 自检清单

- [ ] 我能闭眼写 `urllib` 的 POST JSON 和二进制落盘
- [ ] 我知道 `urlopen` 对 4xx 是抛异常不是返回
- [ ] 我能背出游标分页的循环写法
- [ ] 我知道退避要加抖动，也知道哪些 429 不该退避
- [ ] 我能手写 webhook 验签四步，且知道为什么要用 raw body、为什么容忍度不能设 0
- [ ] 我开场第一件事是确认输出格式
- [ ] 我的错误处理不是 `except: pass`
- [ ] 我提前在自己机器上跑通过一次陌生 repo（环境不吃时间）

## 对应材料

- 题目：`loop/rounds/05_integration/int01`–`int04`
- 卡片：`loop/study/20-cards/http_json.md`、`stripe_api.md`
- 前置：`loop/study/00-prereq/06-HTTP与API`
- **模板**：`loop/study/00-prereq/07-模板-常用模式.md` + `templates/`
- mockserver：`loop/mockserver/`（分页 / 429 / 幂等 / 签名都实现了，可以对着读）
- 事实与来源：`loop/LOOP_GUIDE.md` §5
