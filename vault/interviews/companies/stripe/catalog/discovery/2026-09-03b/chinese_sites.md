# 中文站点扫描 + 小红书可行性（2026-09-03）

排查环境：本仓库 Claude Code 沙箱容器，出口走 `agent proxy`（很可能是云服务商/数据中心 IP 段，不是住宅 IP——这一点是下面小红书结论的关键证据）。全部结论遵循 `catalog/SOURCES.md` 的三条纪律：不编 URL、找不到写"未找到"+检索式、不绕过登录/验证码/反爬签名。

---

## 小红书结论（最前面，用户最关心）

### 1. 取正文：机制没死，但**在这个环境里用不了**

结论：`/home/user/quant-stroller/src/quant/scout/social.py` 的设计（移动端 UA 直拉分享链接 → 服务端把笔记 SSR 进 `window.__INITIAL_STATE__`，无需登录）**在原理上依然成立**，但今天从这台机器实测，**11 条分享链接无一例外全部失败**——不是"没有笔记数据"，而是每次都被重定向到 `https://www.xiaohongshu.com/404/sec_XXXXXXXX?source=xhs_sec_server&...`（小红书自己的"安全校验"拦截页），`__INITIAL_STATE__` 里只有 App 配置，没有任何 `noteId`。

实测明细（全部 2026-09-03，移动端 UA `iPhone/17_0 Safari/604.1`）：

| 链接 | 来源 | 结果 |
|---|---|---|
| `http://xhslink.com/o/6vPAOBgun34` | WebSearch 命中 | → `/404/sec_fCDilxgj` |
| `http://xhslink.com/fOSTob` | WebSearch 命中 | → `/404/sec_pDwacXZM` |
| `https://www.xiaohongshu.com/discovery/item/67b97405...`（无 token，Facebook 帖子里截断的） | WebSearch 命中 | → `/404/sec_SPooYnVA`（缺 `xsec_token`，符合预期会被拒） |
| `http://xhslink.com/o/7cTgAqCp1d0` | threads.com 今日帖子，**token 完整** | → `/404/sec_JwmOvZup` |
| `http://xhslink.com/o/3HTkBc3rTCx` | threads.com 今日帖子，**token 完整** | → `/404/sec_AkovEXkb` |
| `http://xhslink.com/o/6syJpGyZLaN` | threads.com 今日帖子，**token 完整** | → `/404/sec_BjmDyKwY` |
| `http://xhslink.com/o/5PmXoGUN37b` | threads.com 今日帖子，**token 完整** | → `/404/sec_acMIUEgd` |
| `http://xhslink.com/o/3iOyik9WaJb` | threads.com 今日帖子，**token 完整** | → `/404/sec_cepDcOow` |
| `http://xhslink.com/o/EAWrJtDe9X` | threads.com 今日帖子，**token 完整** | → `/404/sec_zuGRvlNx` |
| `http://xhslink.com/m/3FQ3mH71TL2` | threads.com 帖子 | → 直接跳首页（短链已失效） |
| 用上面第 4 条重定向里解出的完整 `xiaohongshu.com/discovery/item/...?xsec_token=...` 原文直接请求（绕开 xhslink 短链这一跳） | 同上 | 依然 → `/404/sec_pQuBUDHB` |

也就是说：**换了 6 个不同的、当天刚发的、`xsec_token` 完整没截断的分享链接，结果完全一致**——这不是"某条链接过期了"，而是这台机器本身在小红书的风控名单上。

**证据链**（找到直接原因，不是瞎猜）：dev.to 文章《How to scrape RedNote (Xiaohongshu) with Python in 2026》明确写道，小红书 2026 年的反爬有三层：TLS/JA3 指纹识别、`x-s`/`x-t`/`x-s-common` 请求签名（约每月轮换一次）、以及**"对来自 AWS / GCP / Azure / DigitalOcean 等数据中心 IP 的请求几分钟内封锁"**（住宅代理也只能撑到每 IP 每分钟 10-20 次请求）。本沙箱的出口正是走 agent proxy，几乎肯定落在会被命中的 IP 段——这与"headers 全对、token 完整，但每次都被 302/跳到 sec 校验页"的现象完全吻合。

`quant-stroller` 代码本身没有问题：它的单元测试全部用 `httpx.MockTransport`（零网络），docstring 里"2026-07-13 已实测"应该是作者在自己电脑（住宅 IP）上验证的，跟这次在沙箱里测到的情况不矛盾——**结论是环境限制，不是设计过时**。

### 2. 按关键词搜索：不能，逐个方案都试过

| 方案 | 结果 |
|---|---|
| Bing `site:xiaohongshu.com stripe 面经` | 200，但页面里所有 `xiaohongshu.com` 字样都只是回显查询词，**0 条真实结果**；换成不带 `面经` 的 `site:xiaohongshu.com stripe`，Bing 直接放弃 site: 限定，退化成泛网页结果（stripe.com、wikipedia），同样 **0 条小红书笔记** |
| WebSearch 工具 + `allowed_domains: ["xiaohongshu.com"]`，query 分别试了「stripe 面经 OA 算法题」「stripe interview 算法 小红书笔记」 | 两次都只命中小红书的**招聘官网/条款页/App 内问答页**，无一条是用户笔记 |
| DuckDuckGo `html.duckduckgo.com/html/?q=site:xiaohongshu.com...` | 返回验证码墙（"Select all squares containing a duck"），**未绕过** |
| 小红书官方 web 搜索入口 `xiaohongshu.com/search_result?keyword=...` | 桌面 UA 和移动 UA 结果一致：301 到 `search_result/`（带斜杠）后 **404**，说明网页版搜索本身就要求登录/App 环境，不是"能搜到但没结果" |
| RSSHub `/xiaohongshu/...` 路由 | 查了 RSSHub 文档 + GitHub PR #17228：现有路由是 `/xiaohongshu/user/:user_id/notes`（按**已知用户 ID** 拉该用户笔记列表），**没有关键词全文搜索路由**；就算是这条按用户走的路由，要拿到笔记全文也需要配置 `XIAOHONGSHU_COOKIE`（PR 原文："获取详情需要 cookie 登录"）——绕不开登录这一步。公共实例 `rsshub.app` 本身也被 Cloudflare 挡了（"Just a moment..." 人机校验），未绕过 |
| 第三方镜像/数据站 | 未找到任何免登录、可关键词检索小红书笔记的镜像站 |

结论与题目背景一致：**搜索引擎确实没有索引小红书的 Stripe 面经**，而且小红书自己的搜索、以及生态里唯一现成的开源桥（RSSHub）都在登录墙后面。

### 3. 如果需要用户配合：具体操作步骤

这是唯一能拿到 XHS Stripe 面经正文的路，请按这几步做：

1. 手机上打开**小红书 App**（不是网页版），在顶部搜索栏输入关键词，比如「stripe 面经」「stripe oa」「stripe 面试」「stripe 算法」，多试几个词。
2. 点开看着像候选人面经的笔记，点笔记右下角的**分享图标**。
3. 在分享面板里选**「复制链接」**（不是"复制口令"——口令格式是给站内跳转用的，外部工具解析支持差，容易出问题）。
4. 把复制到的**一整段文本**（包括前面那句"XX发布了一篇小红书笔记，快来看吧！"之类的提示语和后面的 `http://xhslink.com/...` 链接）**原样、完整**粘贴发给我们——**不要自己截断或删减**，尤其是链接里的 `xsec_token` 参数：这是唯一的访问凭证，少一个字符整条链接就废了（实测：上面第 3 条就是因为 token 被截断，直接变成 404）。
5. **要新鲜的**：今天实测下来，即使 token 完整、链接是当天发的，站方仍可能因为访问方（也就是我们这边）的 IP 而挡下来；所以复制后请**尽快**发过来，不要放几天再发——放几天大概率会连原始短链一起失效（上面 `xhslink.com/m/3FQ3mH71TL2` 那条已经直接跳回首页了）。
6. **诚实的预期管理**：就算链接新鲜、token 完整，我们这边（沙箱环境）之前 6 次尝试**全部失败**，原因是这个环境本身被小红书判定为数据中心/风控 IP。也就是说，就算你按上面步骤发来一条完美的链接，我们**仍有很大概率读不出来**——如果发生这种情况，唯一的下一步是你自己在手机上把笔记正文（含截图里的文字，因为很多面经的关键内容在配图里）复制/截图直接发给我们，而不是发链接。

---

## 各站可达性台账

| 站点 | 状态 | 能否搜索 | 拿到多少 Stripe 内容 |
|---|---|---|---|
| **nowcoder.com（牛客）** | 200（真正的搜索接口是 `/search/all?type=all&query=...`，直接打 `/search?type=post&query=...` 会经过两跳 301 才到） | 能，站内搜索 API 直接可用 | 极少：67 条命中里只有 **1 条**真正跟 Stripe 公司面试相关（其余是 PAT/Codeforces 里恰好叫"stripe"的题、或提及 Stripe API 的技术教程），且这 1 条只是流程复盘，不含具体题面（见下） |
| **CSDN** | 200，`so.csdn.net/api/v3/search` 直接返回 JSON | 能，且好用 | **最丰富**，但混杂大量疑似 AI 内容农场文章（见下方专门说明），需要甄别 |
| **掘进 juejin.cn** | 200，`api.juejin.cn/search_api/v1/search` 直接可用 | 能 | **0**——查了「stripe 面经」「Stripe OA」两轮，全是 Stripe 支付集成/收款教程，没有任何面试相关内容 |
| **知乎 zhihu.com** | 直连 403 | 只能靠 WebSearch 域名限定查询绕着看摘要 | **0**——两轮查询命中的都是"大厂面试算法题"通用文章，没有一条提到 Stripe |
| **博客园 cnblogs.com** | `zzk.cnblogs.com` 302 到 `zzkx.cnblogs.com`，200 | **不能**——搜索页返回"请完成人机验证"（图形验证码墙），**未绕过** | 0（搜索被墙，无法判断站内是否有内容） |
| **V2EX** | 200 | **不能**——V2EX 自己没有站内全文搜索，搜索页直接跳转到一篇说明帖《搜索引擎技术研究》，站方明确建议用外部搜索引擎；WebSearch 域名限定查询也没有命中 Stripe 相关内容 | 0 |
| **脉脉 maimai.cn** | 直连 403 | 只能靠 WebSearch 域名限定查询绕着看摘要 | **0**——命中的全是字节/腾讯/Shopee 等其他公司的面经，没有 Stripe |
| **微信公众号文章**（经搜索引擎） | — | WebSearch 试了 `site:mp.weixin.qq.com stripe 面经/OA` 和不带 site: 限定的中文查询 | **0**——命中的公众号文章都是别的公司面经或 Stripe 支付接入教程，没有 Stripe 面试内容 |
| 1point3acres.com | 403，结构性不可达（Cloudflare，复用题目给定结论，未重复实测） | — | — |
| 1o24bbs.com | 000，容器内连不上（复用题目给定结论，未重复实测） | — | — |

---

## 牛客收割结果

唯一命中的真实帖：**《Stripe OA+VO详细面经分享》**
- URL：`https://www.nowcoder.com/discuss/768684111849402368?sourceSSR=search`
- 访问日期：2026-09-03
- 发帖时间：2025-06-29（帖子内 `createTime` 时间戳 1751140574000）
- 置信度：medium（候选人第一人称叙述，但只是流程复盘，不含具体题目文本/样例）

原文摘录（简体，已核对与站内 JSON 字段一致）：

> "Hackerrank：有60分钟做一道题。不是Leetcode风格，没有复杂的算法，更多是数据处理。我45分钟就通过了所有测试用例。2小时后就收到了技术面试的邀请。技术面试：60分钟做一个四部分的题目...VO面试：3个一小时的环节...第一部分是Coding...第二部分是找bug...第三部分是集成...最后一轮是与hr的bq面试"

**结论：这条帖子不含可提取的具体题目，只是对 CATALOG.md 已有的流程结论（HackerRank 60 分钟 / VO 三个一小时环节：Coding + Bug + Integration）做了一次独立的第三方佐证，可作为新增 #ref 挂在这套流程描述下，但不产出新题目行。** 牛客站内没有其他有效命中——已尝试的查询：`stripe`、`stripe oa`、`stripe hackerrank`、`stripe 面经`、`stripe 面试`，均已在正文中列出结果。

---

## 已收录题目的新增细节

来源全部是 CSDN 搜索 API（`so.csdn.net/api/v3/search`）返回的 `description`/`body` 字段，**未直接抓取 `blog.csdn.net` 正文页**（正文页有反爬 JS 混淆挑战，遇到即止，未尝试逆向或执行该 JS——见下方"失败的检索式"）。`body` 字段本身还带有 CSDN 自己做的字符级混淆（比如 "Stripe"→"Sipe"、"Coding"→"Codig"，系统性丢字母，应是防止直接复制转载），因此下面引用一律标注"经反混淆整理，非逐字原文"。

**重要提醒**：`programhelpoa`（笔名 `ProgramHelpOa`）这个 CSDN 账号，从命名和写作风格看就是 `programhelp.net`（catalog 里已有的 T2 聚合站）自己的 CSDN 镜像号，**不算独立新来源**，只在此处引用其补充细节，不计入 `#refs`。`2611_95078937`、`2301_81532744` 这两个账号风格是典型面试培训机构广告文（"长期整理北美一线大厂真实面经...提供面试前针对性 Mock..."），归为 T2 级、medium 置信度，同样不计独立 #refs，仅供细节交叉参考。

- **A25 Money Transfer / rebalancing（LC 465 twin）**：三篇 CSDN 文章（`2611_95078937` 2026-01-28 id=157480076、`2611_95078937` 2026-02-27 id=158472151、`2301_81532744` 2026-05-27 id=161463306）都独立复述了同一套三段式结构：账户余额调平（构造可行解，不要求最优）→ follow-up 1「最少交易次数」（贪心：最大债主配最大债务人 / DFS+剪枝）→ follow-up 2「审计」。**新增细节**：审计 follow-up 的标准答案表述是"dry-run 模拟执行 + 与实际转账日志比对 + 幂等 ID 设计"，比 CATALOG 现有的"audit / best-effort"描述更具体。访问日期 2026-09-03，置信度 medium（T2，多篇互相印证但同源风险高）。
- **A32 PaymentLedger class**：CSDN `2611_95078937` 2026-01-26（id=157400215，标题《Stripe 2026 Summer Intern VO 面经分享｜Coding + Integration》）的摘要给出比 CATALOG 现有条目更细的方法覆盖：**去重、全额/部分退款、时间范围查询、时序异常处理、持久化**。与 A32 已知的 `add_payment`/`add_refund`/`get_total_revenue`/`get_payments_by_date` 四方法 + partial refund/time-range/bad timestamp follow-up 完全对得上，属于同题的独立复述。置信度 medium。
- **A2 Jupyter/WebSocket Load Balancer**：CSDN `programhelpoa` 2026-03-16/03-17（id=159132253、159164730）两篇复述了五阶段流程（基础分配→DISCONNECT→SHUTDOWN→单服连接数限制→全链路整合），**新增一个格式细节**："服务器索引从 1 开始编号"。因为发帖账号即 programhelp 自己，不计独立 #ref，只记细节。
- **C29 Bug Squash**：
  - 上述 157480076/158472151/161463306 三篇里，Mako 调试轮的两个 bug 描述（"路径未校验是否为目录"+"缺失某 AST 节点访问函数导致崩溃"）与 CATALOG 现有 C29 记录的 Mako 两个 bug **完全一致**，是独立复述而非新 bug。
  - **但 161463306（`2301_81532744`，2026-05-27）额外给出一个此前未记录的具体 bug 范例**（非 Mako，是一个约 150-200 行的"简化版但很真实的内部业务代码"）：退款逻辑里"先把订单状态更新为 `REFUNDED`，再校验退款金额是否超过原交易金额——顺序反了，导致状态污染"。这是一个新的、可直接拿来当训练案例的具体 bug，建议后续收进 `loop/LOOP_GUIDE.md` §4 的 bug squash 案例池。置信度 medium（单一 T2 来源）。
- **C30 System design prompts**：161463306 里第三轮系统设计题目是**"简化版退款/支付方式更新服务"**（允许发起退款、支持部分退款、记录所有变更用于对账；追问：下游银行超时怎么办、失败重试策略、向后兼容、幂等）——这是一个 CATALOG 现有 C30 列表（Webhook delivery / Counter-metrics / IAM / Ledger service / subscriptions / rate limiter）里**没有的新标题**，建议补进 C30 的候选列表。置信度 medium。
- **HM/behavioral 轮**：161463306 明确写出面试官问题逐条对应 Stripe 官方 Operating Principles（"Care about the mission"→线上 P0 故障 hold 住新功能发布；"Disagree and commit"+"Optimize for the long term"→跨团队分歧；"Write high-quality code"+"Obsess over details"→工程质量项目）。这与 CATALOG 现有"Stripe Operating Principles 官方文案无变化"的结论一致，补充了一份 HM 轮如何具体考察这些原则的候选人自述范例。
- **C15 MLE track**：CSDN `programhelpoa` 2026-04-09（id=159997219，标题《Stripe MLE OA 高频题分享》）描述 MLE OA 四大高频题：欺诈商户检测（对应 A4）、卡号区间混淆（对应 A8）、多阶段负载均衡（对应 A2）、ML 集成调试（sklearn pipeline + 典型 bug）。这与 CATALOG C15 已有的"MLE NG OA 2026: PyTorch 分类器 + pandas"是**不同的一次 MLE OA 描述**（说明 MLE track 题库也在复用 SWE track 的 A2/A4/A8），建议合并进 C15 作为补充细节，不新开条目。置信度 medium。

## 疑似线索（置信度低，仅供交叉参考，未建题）

- CSDN `weixin_73559547` 2025-12-10（id=155790187，标题《Stripe店面题库》）摘要提到四类题：运费计算（固定/阶梯/混合计费，对应 A22）、支付账单匹配（精确与容差匹配，对应 A30）、账户数据验证（KYC 规则，对应 A7）、**用户权限系统（父子账号角色继承）**——最后一条与 CATALOG 里 C6「RBAC Role Resolver」的线索（"算账户层级链上的有效权限"）方向一致，是对 C6 的又一条弱佐证，但账号命名模式（`weixin_`+随机数字）与下面提到的"疑似 AI 内容农场"高度相似，**不提升 C6 的置信度等级**，只记录在案。

## ⚠️ CSDN 上一批高度疑似 AI 内容农场的文章（不采信）

同一批查询里还命中了一组标题都叫《Stripe面试全解析：xxx与xxx实战》《Stripe SDE面试全攻略》之类的文章，账号全部是 `weixin_` 开头的随机数字（`weixin_33937913`、`weixin_30279671`、`weixin_34082695`、`weixin_30564901`、`weixin_33811539`、`weixin_30696427` 等），**但 CSDN 记录的发布日期是 2012、2014、2016、2017、2018、2019 年**——而内容却在讨论"Stripe 2026 OA"、`requires_action` 支付状态、Saga 补偿模式等 2025-26 年才会出现的具体细节。日期与内容自相矛盾，这是典型的 AI 生成 + 回填发布时间的 SEO 农场特征，与 CATALOG.md 里 T9 级的 lodely.com / vervecopilot.com 是同一类问题。**本报告不采信这批文章的任何具体细节，只记录"CSDN 上存在这类内容，交叉核对题目时要注意甄别日期"这一事实。**

## 新题

**本轮没有找到一个"从未出现过"的、有完整题面/样例/规则的全新题目。** 上面列出的都是对已收录条目（A2、A25、A32、C15、C29、C30）的增量佐证或补充细节，新题数 = **0**。如实报告：中文站这一轮的价值主要在小红书可行性的确认性结论（能/不能，以及为什么）和牛客/CSDN 的可达性台账，而不是新增题目。

---

## 失败的检索式

| 站点/方式 | 检索式 | 结果 |
|---|---|---|
| DuckDuckGo | `html.duckduckgo.com/html/?q=site:xiaohongshu.com+stripe+面经` | 验证码墙（"Select all squares containing a duck"），未绕过 |
| 博客园 zzkx.cnblogs.com | `/s?w=stripe 面经` | 返回"请完成人机验证"图形验证码，未绕过 |
| rsshub.app | `/xiaohongshu/fulltext/stripe 面经`、直接访问首页 | Cloudflare "Just a moment..." 人机校验，未绕过 |
| blog.csdn.net 正文页 | 直接 GET 7 篇候选文章的 URL（158472151/157480076/161463306/159771517/157400215/159164730/159132253） | 全部返回 521 + JS 混淆挑战脚本，未尝试逆向/执行，未绕过 |
| xiaohongshu.com 网页版搜索 | `/search_result?keyword=stripe`（桌面 UA）、`/search_result?keyword=stripe 面经`（移动 UA） | 均 301→`/search_result/`（带斜杠）→404，说明前台搜索需要登录/App 环境 |
| xhslink.com 分享短链（11 条，见"小红书结论"第 1 节完整列表） | 直接 resolve | 全部 → `/404/sec_XXXXXXXX` 安全校验页，或短链本身已失效直接跳首页 |
| Bing | `site:xiaohongshu.com stripe 面经`、`site:xiaohongshu.com stripe` | 0 条真实小红书笔记结果 |
| WebSearch（domain-restricted to xiaohongshu.com） | `stripe 面经 OA 算法题`、`stripe interview 算法 小红书笔记` | 只命中招聘官网/条款页/App 内问答，无笔记 |
| WebSearch（domain-restricted to zhihu.com） | `Stripe 面试 算法题 OA` | 无 Stripe 相关命中 |
| WebSearch（domain-restricted to maimai.cn） | `Stripe 面经 面试` | 无 Stripe 相关命中（全是其他公司） |
| WebSearch（domain-restricted to v2ex.com） | `Stripe 面试 OA 算法` | 无 Stripe 相关命中 |
| WebSearch | `Stripe 面经 OA site:mp.weixin.qq.com`、`"Stripe" 面试 微信公众号 面经` | 无 Stripe 面经类公众号文章命中（命中的都是 1point3acres/csoahelp/其他公司面经） |
| nowcoder.com 站内搜索 | `stripe`、`stripe oa`、`stripe hackerrank`、`stripe 面经`、`stripe 面试` | 除 1 条真实帖外，其余全部是无关内容（PAT/Codeforces 题目或 Stripe 支付技术文章） |
| juejin.cn 搜索 API | `stripe 面经`、`Stripe OA` | 0 条面试相关内容，全是支付集成教程 |

---

## 来源登记（供 SOURCES.md）

| 来源 | 层级 | 可抓取性 | 备注 |
|---|---|---|---|
| nowcoder.com | T1（唯一相关帖是候选人第一人称） | 能，需走 `/search/all?type=all&query=...` 这个最终端点（中间两跳 301 会分别指到 `/search/post` 和该端点，直接打最终端点最快） | 搜索结果里"stripe"命中大量噪音（PAT 题、无关技术文章），需要人工/规则过滤 |
| CSDN so.csdn.net | T2（搜索接口本身可信，但站内内容质量参差，含疑似 AI 农场） | 能，`so.csdn.net/api/v3/search?q=...&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&U=` 直接返回 JSON，含 `description` 摘要，部分高相关结果会带完整 `body`（但 `body` 字段有系统性字符混淆，需谨慎引用） | 正文页 `blog.csdn.net/.../article/details/<id>` 有反爬 JS 挑战，未绕过；发布日期字段不可全信，出现过日期与内容年份矛盾的农场文章 |
| juejin.cn | T2（但对 Stripe 面试无覆盖） | 能，`api.juejin.cn/search_api/v1/search`（POST，`{"key_word":...,"sort_type":0,"cursor":"0","limit":10,"search_type":0}`） | 全站内容是技术教程导向，不是面经站，不建议作为长期监控源 |
| xiaohongshu.com / xhslink.com | 结构性受限于本环境 IP | 移动 UA + 分享链接的 SSR 机制原理仍成立，但数据中心/云 IP 会被安全校验拦截；需要住宅 IP 或真机复验 | 复验方式见"小红书结论"第 3 节 |
| zhihu.com / maimai.cn | 直连 403 | 只能靠 WebSearch 域名限定摘要，看不到正文 | — |
| cnblogs.com（zzkx 搜索子域） | 验证码墙 | 未绕过 | — |
| v2ex.com | 站点可达但无站内全文搜索 | — | 站方自己建议用外部搜索引擎 |
| 1point3acres.com / 1o24bbs.com | 复用既有登记（`catalog/sources.json`） | 不可达（Cloudflare / 容器连不上） | 本轮未重复实测，直接沿用题目给定结论 |
