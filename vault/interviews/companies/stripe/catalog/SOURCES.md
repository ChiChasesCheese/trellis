# 来源登记表 —— 这些结论是从哪来的，将来怎么复验

> 机器可读的登记表在 `catalog/sources.json`；维护它的工具是 `tools/refresh_check.py`。
> 本文件解释**为什么这么分层**、**每一层信到什么程度**、**过期了该怎么复查**。

题库里每一条"这题考过、这题是这么问的"，最终都挂在一个 URL 上。时间一长，真正的风险不是
"当初没写来源"，而是**当初的来源今天还在不在、有没有被改过、有没有更新**。Stripe 从 2024 年起
加速轮换题库，我们这份 catalog 冻结于 **2026-08-25**——它每过一个月就更旧一点。这份登记表
的全部意义就是：**让"这份题库是不是还新"变成一条可以随时跑的命令，而不是一次性的信仰。**

## 怎么用

```bash
python3 tools/refresh_check.py rebuild   # 重扫仓库 md，刷新 URL 清单（人工维护的 sites 段会保留）
python3 tools/refresh_check.py stale     # 按各站复验周期，列出到期该复查的来源
python3 tools/refresh_check.py ping      # 真发 HTTP 请求探活，回写状态码
python3 tools/refresh_check.py report    # 打印中文汇总表 + 探活异常清单
```

## 分层：信到什么程度

| 层级 | 是什么 | 信到什么程度 | 复验周期 |
|---|---|---|---|
| **T1** | 一手面经：候选人本人发的帖（Blind / LeetCode Discuss / 一亩三分地 / Reddit / Glassdoor），以及候选人上传的解法仓库与真实库 issue | **最高**。发帖人没有 SEO 动机。缺点是匿名、无法追问、记忆会失真 | 30 天（GitHub 上已关闭的历史 issue 属既成事实，90 天即可） |
| **T2** | 聚合站与代面站：PracHub / InterviewDB / csoahelp / programhelp / oavoservice / linkjob / extrabrain / 各培训站 | **中等**。有日期、有结构化题面时很有用（本轮 C7、C27 就是靠 PracHub 复原的），但它们互相抄，**计 `#refs` 时必须去重**；游戏化的"多少人做出来"无法验证 | 30–90 天 |
| **T3** | 官方与背景：docs.stripe.com、stripe.com 的 JD 与 Operating Principles、levels.fyi | 事实层面**高**，但它描述的是公司，不是题 | 90–180 天 |
| **T9** | **已判定不可信**：lodely.com、vervecopilot.com | **零**。AI 生成的题目农场，内容与所有一手来源矛盾。命中即排除，正文一律不采信 | 365 天（只为记住它们不可信） |

## 怎么才抓得动：每个站各有各的门

这一节是 2026-09-03 实测出来的，**别按直觉猜**。同一个 URL 换个 header 就能从 403 变 200。

| 站点 | 脚本能不能抓 | 怎么抓 |
|---|---|---|
| **teamblind.com** | **能**（实测 12/12 返回 200） | 必须带**浏览器 User-Agent**。带 `bot/1.0` 之类的老实 UA 一律 403。`refresh_check.py` 默认就用浏览器 UA |
| **leetcode.com** | discuss 的 HTML 页 403，但**有活路** | 用 GraphQL 端点：`POST https://leetcode.com/graphql`（实测可用）。正文走 API 取，不要去啃 HTML |
| **raw.githubusercontent.com** | 能 | 取仓库文件走 raw 域名 |
| **github.com**（HTML 仓库页） | 在受限出口下 403 | 换 raw 域名，或人工打开 |
| **1point3acres.com** | **不能** | 结构性不可达：WebFetch / curl / r.jina.ai 三种方式都被 Cloudflare 拦。只能人工登录翻。**这是本题库最大的检索缺口** |
| **medium.com** | **不能** | 浏览器 UA 也 403，人工打开 |
| **reddit.com** | **能（走 RSS）** | HTML 页是 JS 壳、`.json` 接口 403，但 **`.rss` 可用**：`r/<sub>/search.rss?q=...&restrict_sr=1&sort=new` 每次 25 条；单帖 `/comments/<id>/.rss` 连**评论全文**一起给。只能按 subreddit 搜（全站 search.rss 返回 0 条）。工具：`tools/harvest.py` |
| PracHub / InterviewDB / csoahelp / programhelp / oavoservice | 能 | 直接抓。本轮 C7、C12、C27 的题面就是从 PracHub 抓回来的 |
| **xiaohongshu.com** | **正文能，搜索不能** | 桌面 UA 会 302 到 `/login`；**移动端 UA** 直拉分享链接则免登录吐 SSR，完整笔记在 `window.__INITIAL_STATE__` 里。**但站内搜索要登录，而搜索引擎几乎不索引小红书**——所以笔记 URL 必须由人提供（App 内分享→复制链接，**保留 `xsec_token`**）。工具：`tools/harvest.py xhs <链接>` |
| nowcoder.com（牛客） | 能 | 中文面经，catalog 此前完全没覆盖 |
| 1o24bbs.com | **连不上** | 本容器内 000（DNS/网络层不可达），与站点反爬无关 |

由此得到两条工作方式：

- **靠搜索引擎摘要拿到的内容，置信度最多 medium**，且必须标注「WebSearch 摘要，原页 403」。
- 抓不动的站（1p3a / medium / reddit）在 `sources.json` 里标 `access: manual`，`ping` 会跳过，`stale` 单列一栏。**不要拿"跳过"当"来源已死"。**

> 更正记录（两次，都留着）：
> 1. 本文件最初写的是"teamblind / leetcode / 1point3acres 三站一律 403"。实测后只有
>    1point3acres 属实——teamblind 换 UA 即可，leetcode 有 GraphQL 端点。
> 2. 2026-09-03 复测又推翻了一条：**reddit 不是"全站 403"**，HTML 页确实没用，但 `.rss`
>    完全可用，连评论全文都给。此前把 reddit 记为不可达，代价是漏掉了整个 r/leetcode
>    的一手面经流。**教训是同一个：不要用一次失败的抓取方式给一个站点定终身。**
>    一个站"抓不动"要具体到**哪条路径**抓不动，并把试过的路径写下来。

## 另一条容易被误读的事实：403 有两种成因

`ping` 打回来的 403 有两种完全不同的意思，**混为一谈就会得出"来源全死了"的错误结论**：

1. **站点反爬** —— 上表里标"不能"的那几个。这是站点行为，换机器也一样。
2. **你这台机器的出口被限制** —— 在沙箱 / CI 容器里跑时，连 `github.com` 的普通仓库页
   都会 403。这种 403 跟链接死活毫无关系。

所以 `sources.json` 里每条探活结果都记了 `checked_from`（机器标签），`report` 会按标签
分组并给出警告。**2026-09-03 首轮探活是在受限容器（`claude-code-sandbox`）里跑的**：
200/202 的结果可信；403 里含大量 GitHub 与 Medium，属于环境限制，不能当作链接失效。
要拿准数，请在自己的机器上跑：

```bash
python3 tools/refresh_check.py ping --recheck --label mac
```

## 复验协议（将来做"最新性证明"就按这个走）

1. `refresh_check.py rebuild` —— 先让 URL 清单跟上正文的变化
2. `refresh_check.py stale` —— 看哪些站到期了；**先做 T1，再做 T2**
3. 可脚本复验的：`refresh_check.py ping --domain <站点>`，`report` 会把 4xx/5xx 单列出来
4. 只能人工复验的三站：按 `sources.json` 里每站的 `recheck` 字段去手动翻，重点看**上次冻结日之后**的新帖
5. 有新发现 → 写进 `catalog/discovery/<年-月>/`，**先落排查报告，再改 CATALOG.md**；报告里每条必须带 URL + 访问日期 + 原文摘录 + 置信度
6. 改完 CATALOG.md，把对应站点的 `last_verified` 更新掉

## 记账的三条纪律

这三条是这份题库能不能长期可信的全部：

1. **不编 URL。** 只写实际抓取过、或搜索结果里真实返回过的链接。
2. **不把猜测写成事实。** 找不到就写"未找到"，并把试过的检索式记下来——省得下次重复走同一条死路。
3. **转引要标明。** 复用旧材料时标注"复用 + 原采集日期"，**不冒用今天的访问日期**。一条 2025 年的证据不会因为今天被引用一次就变新。

## 与"重建题"的关系

排查完仍然只有标题、没有题面的题，会被做成**重建题**放进题库训练用。每一道重建题的
`problem.md` 第一段都有一个显著的警示块，写明"规则、输入输出格式、part 划分全部是本仓库编的"。

这条边界不能糊：**重建题是拿来练知识点的，不是拿来背答案的。** 把自拟的输出格式当成真题格式去背，
比不练更糟——真题里格式错一个逗号就挂。
