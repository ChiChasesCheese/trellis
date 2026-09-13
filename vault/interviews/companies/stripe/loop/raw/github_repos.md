# Stripe 面试 Loop —— GitHub / 开源侧原始资料（repo、题解、bug squash 素材、integration 素材）

> 范围：Stripe OA 之后的轮次（technical phone screen → onsite：bug squash / integration / coding / system design → HM/behavioral）在 GitHub / 开源生态中能找到的题解 repo、可复刻的 bug squash 素材、integration 练习素材、system design 参考实现。
> 采集日期：2026-09-01。方法：GitHub Search API（`api.github.com/search/repositories`、`search/code`）+ WebSearch + WebFetch（gist、raw.githubusercontent.com、issue tracker）。GitHub 未登录检索限速 60 次/小时，按需分批。
> 可信度分级：**[一手]** = 面试者本人写的题解/复刻；**[二手]** = 转载/聚合；**[代码]** = 可直接读到的源码/commit/issue；**[未验证]** = 检索到但未能打开确认。
> 体例：每条事实后附 `[来源 / URL / 日期]`。题名、API、代码、repo 名保留英文，其余中文。

---
## 0. 速览（最有用的 10 个 repo，一行一个）

1. `github.com/femisowems/stripe-interview-questions` · 6 道 HackerRank 风格题（Company Name Checker / Card Range Obfuscator / Fraud Detector / Store Closing Time Penalty / Subscription Notification Scheduler / Payment Card Validation）逐题 Java+JS+Python 三实现 + `Problem*.md` 题面 + `sample_input.txt`/`expected_output.txt` + `run_tests.sh` · 最后更新 2026-05-01 · **[一手，可信度高，最值得抄]**。[来源 / https://github.com/femisowems/stripe-interview-questions / 2026-09-01]
2. `github.com/joeytor/StripeInterview` · 一份「从网上收集的题目清单」README，按 Phone/Onsite Coding/Integration/Bug Squash/System Design 分类，且 `src/main/java/` 下有 9 道题的 Java 实现（含 `BikeMap.java` 用 Gson+OkHttp 读写 JSON、发请求）· 最后更新 2022-03-10 · 4 星/17 fork（题解被广泛借用）· **[二手汇总 + 一手代码]**。[来源 / https://github.com/joeytor/StripeInterview / 2026-09-01]
3. `github.com/Shivam5022/Interview-Experiences` · 181 星、23 fork，众包面经合集（非 Stripe 专属，但含 Stripe 帖引用）· 最后更新 2025-06-08 · 需在 README 内搜索 "Stripe" 关键词定位 · **[二手，高热度]**。[来源 / https://github.com/Shivam5022/Interview-Experiences / 2026-09-01]
4. `github.com/sahaia1/Stripe_Pyhton_libraries` · 8 个 Python 脚本（`capital.py`、`radarrules.py`、`invoicer.py`、`money_transfer.py`、`graph_currency.py` 等），文件名直接对应常见 Stripe 面试题 · 最后更新 2024-08-13 · **[一手个人练习，代码较薄]**。[来源 / https://github.com/sahaia1/Stripe_Pyhton_libraries / 2026-09-01]
5. `gist.github.com/aranibatta/ffa87e94d117a86fc05b6940e626ee56` · 见第 1 节详情。
6. `gist.github.com/stealthbomber10/d85d44776ad58ba66d84ff76fd5be736` · 见第 1 节详情。
7. `gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1` · 见第 1 节详情。
8. `github.com/stripe-mock`（官方）· API mock server，可用来搭 integration 本地练习环境 · 见文件 2 第 5 节。
9. GitHub code search `accept-language stripe interview` / `currency conversion stripe interview` · 见第 1 节。
10. Bug squash 目标库真实 issue（`FasterXML/jackson-core`、`square/moshi`、`yaml/snakeyaml`、`psf/requests`）· 见第 2 节。

## 1. 面经/题解 repo

### 1.1 官方 `stripe-interview` org（招聘方发给候选人的环境搭建 repo，**非题目本身**）

`github.com/stripe-interview` 组织下 10 个 repo，全部是招聘流程里 Stripe 发给候选人的「面试前环境准备」仓库，用来让候选人在面试前把语言工具链/IDE 调好，**不含题目内容**，但依赖清单/README 能反推出面试用什么库、什么姿势写代码：

| repo | 语言 | 最后更新 | star | 内容 |
|---|---|---|---|---|
| `python-interview-prep` | Python | 2024-09-17 | 122 | README 讲 venv+`interview_requirements.txt`；依赖仅 `six`、**`requests`**、`urllib3`——印证 Integration 轮多半用 `requests` 发 HTTP。[https://github.com/stripe-interview/python-interview-prep] |
| `javascript-interview-prep` | JS | 2026-08-20（近期仍在维护！） | 7 | `hello-world.mjs` 用 `node-fetch` 调开放 API；自带 VSCode `launch.json` 调试配置。[https://github.com/stripe-interview/javascript-interview-prep] |
| `java-interview-prep` | Java | 2025-07-14 | 47 | Maven `pom.xml`，依赖 `guava`+`junit`；`src/` 目录给出标准工程骨架。[https://github.com/stripe-interview/java-interview-prep] |
| `cpp-interview-prep` | C++ | 2026-07-28（近期维护） | 9 | CMake 工程骨架。[https://github.com/stripe-interview/cpp-interview-prep] |
| `csharp-interview-prep` | C# | 2024-01-22 | 11 | — |
| `scala-interview-prep` | Scala | 2021-02-25 | 9 | SBT 示例工程 |
| `ruby-interview-prep` | Ruby | 2021-11-11 | 6 | — |
| `android-kotlin-interview-prep` | Kotlin | 2025-10-20 | 1 | — |
| `react-native-interview-prep` | TS | 2025-06-24 | 0 | — |
| `ml-python-interview-prep` | Python | 2023-06-19 | 0 | 专供 ML 岗 |

结论：这批 repo 更新频率（JS/CPP 2026 仍在更新，Python/Java 2024–2025）说明 Stripe **至今仍在用同一套面试基础设施**，语言选项集合本身就是候选人可选编程语言的权威清单。[来源 / https://api.github.com/orgs/stripe-interview/repos / 2026-09-01]

### 1.2 一手题解/题库 repo

**`github.com/femisowems/stripe-interview-questions`**（Java：53 KB，0 星，最后更新 2026-05-01——**是目前找到的最新的题解 repo**）
- 作者自述"为即将到来的 Stripe 面试准备"，README 引用了 `linkjob.ai` 的 Stripe HackerRank OA 页面作为题源。
- 逐题：
  1. **Company Name Checker**（公司名归一化匹配，判断"重复注册"）——三语言实现 + `Problem1.md` + `sample_input.txt`/`expected_output.txt` + `run_tests.sh`，题面/代码/测试均完整。
  2. **Card Range Obfuscator**（BIN 卡号区间合并/补洞）——同上，题面/代码/测试均完整。
  3. **Fraud Detector**（按次数/百分比阈值判定商户欺诈，含 dispute 冲正逻辑）——同上。
  4. **Store Closing Time Penalty**（`BEGIN`/`END` 包裹的多店日志，求最优打烊时间使罚分最小）——与本节 1.3 中 pkafel gist、`en_forums.md` 已收录的 LeetCode Discuss 2585038 题面完全对应，可交叉验证正确性；题面/代码/测试均完整。
  5. **Subscription Notification Scheduler**（订阅生命周期事件调度：开始/临期/过期/换plan/续订，需按时间线重算）——同上。
  6. **Stripe Payment Card Validation System**（VISA/MASTERCARD/AMEX 前缀+长度识别 + Luhn 校验 + 通配符 `*` 补全计数 + `?` 纠错恢复原卡号，搜索空间较大）——同上。
- 顶层 `npm test` 一键跑全部 6 题、3 语言、对拍 `expected_output.txt`。**这是目前找到的结构最完整、可直接拿来练手的题解 repo**。[来源 / https://github.com/femisowems/stripe-interview-questions / commit 2026-05-01]

**`github.com/joeytor/StripeInterview`**（无主语言标注，19 KB，4 星/17 fork，最后更新 2022-03-10）
- README 明确分区：
  - **Phone Interview**：Stripe Capital、Compress URL、HTTP Header Parser、Mutual Rank、Server Penalty、User Points。
  - **Virtual Onsite / Coding**：Money Transfer、Load Balancer、Invoicer、Rate Limiter。
  - **Virtual Onsite / Integration**：**Request Replay**（读 JSON 里的 request/response，重放请求校验状态码是否一致，需维护旧→新 response id 映射）、**Bike Map**（读 JSON 打印信息 + 向 URL 发请求并把响应存本地文件；Java 文件里有基础 JSON 读写方法；README 提示查 `GSON`+`OKHTTP`）。
  - **Bug Swash**：`FasterXML/jackson-core`、`square/moshi`。
  - **System Design**：Payment Webhook（引用 stripe.com/docs/webhooks + tianpan.co 参考设计）、Counter Logging System（参照 AWS/Azure/GCP metrics）、IAM System、Ledger（消息队列摄入交易，按 merchant 账户订阅消费，NoSQL 存储，周期性聚合算余额）。
- `src/main/java/` 下 9 个 `.java` 实现文件对应上述题目（`BikeMap.java`、`Compress.java`、`HttpHeaderParser.java`、`Invoicer.java`、`LoadBalancer.java`、`MoneyTransfer.java`、`MutualRank.java`、`ServerPenalty.java`、`StripeCapital.java`、`UserPoints.java`）。`BikeMap.java` 用 `Gson`（`GsonBuilder().setPrettyPrinting()`）+ `OkHttpClient` 实现读文件/读 JSON 字符串/读 JSON 数组/发 HTTP 请求的基础方法，是 Integration 轮 Bike Map 题的直接参考实现骨架（非完整解，是工具方法集合）。
- 注意：题目年代较早（2022 前），Server Penalty/Card Range 等题名与新版（femisowems 2026）题目高度相似但细节可能已迭代，交叉参考即可，**不要假设题面完全没变**。[来源 / https://github.com/joeytor/StripeInterview / 2026-09-01]

**`github.com/sahaia1/Stripe_Pyhton_libraries`**（9 KB，1 星，最后更新 2024-08-13，作者自称"Stripe interview prep"）
- 8 个 Python 脚本，文件名即题名：`capital.py`（对应 Stripe Capital 题）、`radarrules.py`（对应 Radar Rules 引擎题）、`invoicer.py`（对应 Invoicer 题）、`money_transfer.py`（对应 Money Transfer 题）、`graph_currency.py`（疑似汇率图/货币换算题）、`code1.py`、`python_learn_datetime.py`（练习脚本非题解）、`stripe_example_api.py`（调用 Stripe API 示例，可能是自测 SDK 用法而非面试题）。代码量小（单文件多在几十行），偏个人刷题笔记而非完整题解，仅供交叉验证题名存在性。[来源 / https://github.com/sahaia1/Stripe_Pyhton_libraries / 2026-09-01]

**`github.com/Shivam5022/Interview-Experiences`**（181 星/23 fork，最后更新 2025-06-08，众包面经合集非 Stripe 专属）——单文件 `Readme.md`，体量大、需按公司名搜索定位 Stripe 相关段落；因是众包合集，Stripe 相关内容多为文字面经链接而非代码，价值在于交叉验证轮次结构而非题解本身。[来源 / https://github.com/Shivam5022/Interview-Experiences / 2026-09-01]

### 1.3 Gist 题解（phone screen 经典题，均为 Stripe "Server Naming/Allocator" 系列 + Store Closing Time 系列）

- **`gist.github.com/aranibatta/ffa87e94d117a86fc05b6940e626ee56`**——"Interview Code Written for Stripe (9/1/2016)"，作者 Arani Bhattacharyay。`tracker.py`：**Server Number Allocator**（`next_server_number`：给定已分配编号列表，返回最小可用正整数）+ 未完成的 `Tracker` 类（`allocate`/`deallocate` 按 host_type 拼编号生成/回收 hostname，代码有语法错误未跑通——`class Tracker` 缺冒号、`has_key` 是 Py2 遗留写法）。**年代久远（2016），仅作历史参考，反映 Stripe phone screen 题目多年沿用同一题干**。[来源 / https://gist.github.com/aranibatta/ffa87e94d117a86fc05b6940e626ee56 / 创建 2016-09-01，更新 2019-04-26]
- **`gist.github.com/stealthbomber10/d85d44776ad58ba66d84ff76fd5be736`**——"stripe interview"，含**完整题面注释**（`next_server_number` 函数级题面 + 6 组 example + 后续 **Tracker 类**（`allocate(host_type)`/`deallocate(hostname)`，含边界样例如特殊字符 host_type `"#$@%"`）的完整题干）。这是目前找到的**题面最完整**的 Server Naming 系列 gist，可直接当作练习题干使用。[来源 / https://gist.github.com/stealthbomber10/d85d44776ad58ba66d84ff76fd5be736 / 创建 2018-10-10，更新 2024-12-24]
- **`gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1`**——"Solution to Stripe phone interview questions"，明确引用 **LeetCode Discuss 2585038**（`en_forums.md` 第 126 行已收录同一题源）。Kotlin 实现 **Store Closing Time Penalty**：`computePenalty`（给定打烊时间点算罚分）+ `findBestClosingTime`（暴力枚举求最优）+ `getAllClosingTimesOrderByBegin`（用栈解析嵌套 `BEGIN`/`END` 多店日志，对每家店求最优打烊时间，按开店顺序输出）。三段实现与 `femisowems` repo 的 `question4`（Store Closing Time Penalty）题干完全吻合，可交叉核对算法正确性。[来源 / https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1 / 创建 2023-10-15，更新 2024-12-24]

### 1.4 更多零散 repo（本轮新检索到，价值参差）

- **`github.com/SabihaNazKhan/StripePhoneScreen24Nov25`**（Java，3 KB，最后更新 2025-09-27，含义"2025-11-24 Stripe Phone Screen"）——`src/Solution.java` **完整保留了 Part 1 题面注释**：**Shipping Cost Calculator**——电商订单（`country`+`items[{product, quantity}]`）× 国家/商品运费矩阵，求订单总运费；样例 `calculate_shipping_cost(order_us, shipping_cost) == 16000`。这就是已知起点提到的"SabihaNazKhan（shipping cost）"，**已核实存在且题面完整**，只有 Part 1（129 行，无 Part 2 注释，可能候选人只写到这里）。[来源 / https://github.com/SabihaNazKhan/StripePhoneScreen24Nov25 / 2026-09-01]
- **`github.com/premjm-67/stripe-interview-questions`**（Java，4 KB，1 星，最后更新 2026-01-02）——README 仅一行标题，5 个单字母命名文件（`B.java`/`CF.java`/`ED.java`/`MP.java`/`PL.java`）**均为标准 LeetCode 原题**（`ED.java`=LeetCode 399 Evaluate Division 图算法；`PL.java`=LeetCode 2050 Parallel Courses III 拓扑排序；`MP.java` 的 `bestClosingTime` 疑似 LeetCode 1191/2483 风格题，与 Stripe "Store Closing Time" 题**同构但不确定是否为同一题**）。**价值较低**——像是个人 LeetCode 刷题记录被贴上"stripe-interview-questions"标签，而非 Stripe 专属题，标注为 **[未验证/可能是标题误导]**。[来源 / https://github.com/premjm-67/stripe-interview-questions / 2026-09-01]
- **`github.com/kwang101/PracticeForStripe`**（Java，1 KB，最后更新 2022-01-18，描述"Practice for Stripe onsite"）——`src/PalindromicDate.java` + 空的测试桩 `tst/PalindromicDateTest.java`（`doSomeTest` 方法体是占位符，未实现）。**回文日期**是常见 phone screen 类型题但本 repo 代码基本是空壳，**价值低**，仅确认"回文日期"曾作为 Stripe 练习题被提及。[来源 / https://github.com/kwang101/PracticeForStripe / 2026-09-01]
- 搜索 `stripe+onsite`/`stripe+bug+squash`/`stripe+integration+interview` in:name,description 命中的其余仓库（`nancyz-stripe/design_onsite`、`ash-bd/s2-stripe-onsite`、`blackpearls0985/SyncSpace` 等）经核实**与本次目标（Stripe SWE bug squash/integration/coding 题解）无关**（分别是无内容占位仓、PHP 老古董、Stripe 支付集成的其他公司作业），不予收录。

## 2. Bug squash 素材：被报道过的 repo 与真实 bug

> 方法：对 `en_forums.md`/`cn_forums.md` 已确认的 6 个库（`requests`、`Mako`、SnakeYAML、`Jackson`、`Express`、Ruby `Sass`）+ `joeytor` README 提到的 `Moshi`，逐个用 GitHub Search Issues API 定位 2015–2024（+ 近期）区间内、描述吻合候选人转述的**真实已修复 bug**，标注 issue/PR 链接、根因一句话、修复 diff 大小，供复刻练习。

### 2.1 Python — `requests`（`psf/requests`）

- **Issue #2589「Can't post BytesIO file-like object」**（提交 2015-05-04，已关闭）——根因：`requests` 在处理 multipart 文件字段时，若传入的是纯 `io.BytesIO()`（无 `.name`/`len` 属性的文件类对象）而非磁盘文件，`super_len()`/编码逻辑处理不一致，导致上传失败或数据损坏。与英文面经"一位候选人遇到 BytesIO 相关 bug"（`en_forums.md:199`）**高度吻合，是目前找到的最佳复刻候选**。[来源 / https://github.com/psf/requests/issues/2589 / 2015-05-04]
- **Issue #3532「Passing seekable objects without len to super_len causes .getvalue() which copies them just to get the length」**（2016-08-23，已关闭）——同一族 BytesIO/文件类对象长度探测 bug，可作为 #2589 的补充/进阶版本（性能问题而非功能性 bug：大对象被不必要地整体拷贝一次）。[来源 / https://github.com/psf/requests/issues/3532 / 2016-08-23]
- **Issue #3369「TypeError in iter_slices() when slice_length=None」**（2016-07-01，已关闭）——`iter_slices` 在 `slice_length` 为 `None` 时抛 `TypeError` 而非优雅处理，属于典型"边界值未判空"的 bug squash 风格问题，代码量小、根因单一，适合改编成练习。[来源 / https://github.com/psf/requests/issues/3369 / 2016-07-01]

### 2.2 Python — `Mako`（`sqlalchemy/mako`，早期在 Bitbucket，现镜像/主仓在 GitHub）

- **Issue #434「slash handling issue in template URI normalization」→ 修复 commit `e05ac61`（对应 CVE 修复）**（2026-04-14 提交，已关闭）——根因：`Template.__init__` 只剥离**单个**前导斜杠，而 `TemplateLookup.get_template()` 会剥离**所有**前导斜杠，两处不一致导致形如 `"//../../secret.txt"` 的 URI 能绕过目录穿越（path traversal）检查。**修复 diff 极小**：`mako/template.py` 仅 1 行新增/3 行删除 + 41 行新测试（`test/test_lookup.py`），**是理想的 bug squash 复刻素材**——bug 本身是路径处理逻辑不一致，修复只改 1 行代码。与英文面经"Mako path handling"描述（`en_forums.md:200`）完全对应。[来源 / https://github.com/sqlalchemy/mako/issues/434 / commit https://github.com/sqlalchemy/mako/commit/e05ac61989a7fb9dd7dcde6cfd72dc48328719a3 / 2026-04-14]
- **Issue #435「backslash handling issue in template URI normalization on Windows」→ 修复 commit `72e10c5`**（2026-04-28 提交，已关闭；对应 CVE-2026-44307）——根因：URI 规范化用 `posixpath`（把反斜杠当字面字符），但 Windows 上 `os.path.isfile()` 把反斜杠当路径分隔符，导致 `"\..\secret.txt"` 能绕过目录穿越检查。修复 diff：`mako/lookup.py`/`mako/template.py` 各 1-2 行 + 40 行新测试。**与 #434 是同一族"path handling"bug 的两个变体**，两个都极小、根因清晰，适合直接拿来做 bug squash 练习（甚至可以只教一半、让候选人自己发现另一半）。[来源 / https://github.com/sqlalchemy/mako/issues/435 / commit https://github.com/sqlalchemy/mako/commit/72e10c573ca0fbcbddd4455abca8ce92a61780d7 / 2026-04-28]

### 2.3 Java — `SnakeYAML`（`snakeyaml/snakeyaml`，现镜像自 Codeberg，GitHub 侧 issue 检索为空）

- GitHub Search Issues API 对 `repo:snakeyaml/snakeyaml` 返回 **0 条结果**——该项目 2022 年后主仓库迁至 **Codeberg**（`codeberg.org/snakeyaml/snakeyaml`），GitHub 仅为镜像，issue 功能可能被禁用或未同步。**[未能直接验证具体 issue 链接，标注为未能访问]**。
- 但 SnakeYAML 的"boolean-like scalar 解析异常"是 **YAML 1.1 规范的知名坑（俗称"Norway Problem"）**：`on`/`off`/`yes`/`no`/`y`/`n` 等字符串在 YAML 1.1 下会被隐式解析成布尔值（比如国家代码 `NO`（挪威）被解析成 `false`），这是**语言/规范层面的已知行为而非单个 bug**，可以直接用官方文档 + Stack Overflow 上大量真实案例（如配置文件里 `enabled: on` 被错误转型）复刻成 bug squash 练习：让候选人发现"为什么 `flag: on` 读出来是 Java `Boolean` 而不是 `String`"。**[推断，需候选人自行到 Codeberg 或 SnakeYAML 官方 issue 历史核实原始 issue 编号]**。

### 2.4 Java — `Jackson`（`FasterXML/jackson-core` / `jackson-databind`）

- **`jackson-core` Issue #649「Bug in FilteringParserDelegate」→ PR #650「Fix failing tests」**（issue 2020-11-07 提交，PR 2020-11-08 合并）——`FilteringParserDelegate` 是 Jackson 用于流式过滤 JSON 内容的组件，此 bug 涉及过滤逻辑在特定 token 序列下产生错误结果。**修复 diff**：3 个文件，+40/-26 行，规模适中，适合 30-45 分钟 bug squash。[来源 / https://github.com/FasterXML/jackson-core/issues/649 / PR https://github.com/FasterXML/jackson-core/pull/650 / 2020-11-08 合并]
- **`jackson-core` Issue #582「`FilteringGeneratorDelegate` bug when filtering arrays (in 2.10.1)」**（2019-11-29，已关闭）——同族"过滤器组件对数组处理有误"的 bug，可作为 #649 的姊妹题。[来源 / https://github.com/FasterXML/jackson-core/issues/582 / 2019-11-29]
- **`jackson-databind` Issue #3228「[BUG] Inconsistent Parsing of JsonArray while reading multiple values from a source」**（2021-08-02，已关闭）——从同一数据源连续读取多个 JSON 值时解析结果不一致，属"状态未正确重置"类 bug，根因定位需要读一部分 `JsonParser` 内部状态机代码，难度略高于典型 bug squash，适合 Senior 候选人。[来源 / https://github.com/FasterXML/jackson-databind/issues/3228 / 2021-08-02]

### 2.5 Java — `Moshi`（`square/moshi`）

- **Issue #470「Bug parsing @Json(name="2")」**（2018-03-29，已关闭）——当 `@Json(name=...)` 注解值是纯数字字符串（如 `"2"`）时解析出错，根因大概率是字段名到 JSON key 的映射逻辑对"看起来像数字"的 key 做了错误的类型推断/转换。**代码量小、根因单一**，是较理想的 Moshi bug squash 候选。[来源 / https://github.com/square/moshi/issues/470 / 2018-03-29]
- **Issue #1171「require(parameter == null || parameter.type == property.returnType) has bug」**（2020-07-08，已关闭）——Kotlin 反射相关的参数类型断言在特定继承/泛型场景下误报，涉及 Moshi 的 Kotlin adapter 生成逻辑，难度中等偏高。[来源 / https://github.com/square/moshi/issues/1171 / 2020-07-08]
- **Issue #624「@Json-annotated fields have set accessible called on them no matter what, bug or feature?」**（2018-08-15，已关闭）——反射字段访问权限处理的边界行为，讨论中澄清了"bug 还是设计如此"的争议，适合作为"读代码 + 判断预期行为"类型的 bug squash 变体（不是纯粹改代码，还要读 issue 讨论理解设计意图）。[来源 / https://github.com/square/moshi/issues/624 / 2018-08-15]

### 2.6 JavaScript — `Express`（`expressjs/express`）与 `Day.js`（`iamkun/dayjs`）

- `expressjs/express` 历史 bug 数量大（搜索 "bug" in:title 命中 59 条），但多数是路由中间件边界情况；未在英文面经里看到候选人转述具体 issue 编号，只能给出"路由/中间件类真实 bug 广泛存在，可挑一个中等规模的自行改编"的**方向性结论**，不点名具体 issue（避免过度推断）。**[推断为主]**
- 用户方原始指令提到 "React async race" 描述对应 `en_forums.md:180`「Fix an Async Race Condition in a React Data Fetching Component（`resourceId`...）」，这是候选人自己描述的题目（可能是 Stripe 自造的练习代码而非真实开源库 bug），**不对应某个具体开源 repo 的 issue**，无法在 GitHub 上找到"真实历史 bug"对应物，只能作为自造练习题参考。
- `Day.js`（`iamkun/dayjs`）虽未在已知面经中被点名为 Stripe bug squash 库，但作为轻量日期库，其真实 bug（如 #3068「+00:00 timezone bug」、#3015「undocumented Y and YYY tokens fall through to ZZ formatting」）体量小、根因清晰，**可作为"未被证实用过、但结构上很适合改编成 bug squash 练习"的补充库**，仅供参考不代表 Stripe 实际用过。[来源 / https://github.com/iamkun/dayjs/issues/3068 / 2026-05-23]、[https://github.com/iamkun/dayjs/issues/3015 / 2026-03-12]

### 2.7 Ruby — `Sass`（`sass/ruby-sass`，已归档，Ruby 版 Sass 已停止维护多年）

- **PR #97「Fix more whitespace stripping bugs」**（2018-11-07，已合并）——空白字符处理相关的多个小 bug 修复合集，规模小、可拆成单个练习。[来源 / https://github.com/sass/ruby-sass/pull/97 / 2018-11-07]
- **Issue #48「Bug with handling / in interpolation」**（2018-04-06，**仍处于 open 状态**，未修复）——`/` 在字符串插值中的处理有歧义 bug；因为**未修复**，不适合直接当"改一次就过"的练习，但可以用作"候选人只需要诊断根因、不必给出完美修复"的高难度变体。[来源 / https://github.com/sass/ruby-sass/issues/48 / 2018-04-06]
- 注：Ruby Sass 官方已于 2020 年 EOL，仓库为历史存档，`git clone` 仍可用但生态（gem 依赖）可能过时，复刻练习时建议锁定 Ruby/Bundler 版本。

### 2.8 社区自练方案

- **"注入 bug 的 repo" / bug-squash-practice 类项目**：GitHub 上没有找到与 Stripe 直接关联、专门"预先注入 bug"的公开练习仓库（多数面经作者是**自己 fork 热门开源库后手动引入 bug** 来计时练习，如 `en_forums.md:234` 所述"自己 clone 热门开源库（express/axios/lodash/requests 等）注入 bug 计时练习"）。这是目前最推荐的自练方法：挑选本节列出的任一小型真实 bug，**回退到 bug 引入前的 commit**（即修复 PR 的父 commit）作为练习起点，隐藏修复 PR，计时 30-45 分钟尝试独立定位+修复，再对比真实修复 diff。
- **Coditioning / InterviewCoder 的练习法**（`en_forums.md` 已引用 Coditioning 关于 bug squash 形式的文章，`https://www.coditioning.com/blog/804/stripe-swe-bug-squash-interview`）：核心方法论是"给一个失败的单测 + clone 的仓库，在自己 IDE 里定位并修复"，与本节素材可以直接组合使用——用上面任一真实 bug 的"引入前 commit + 修复 PR 里新增的单测"组合出一个可执行的练习环境。

## 3. Integration 素材

### 3.1 BikeMap —— 目前找到的最完整复刻信息（未找到公开 repo/gist 直接给出 `ride-simple.json` 原文，但流程被多篇文章逐 part 还原）

- **未能找到**任何公开 GitHub repo/gist 直接托管 Stripe 官方 `ride-simple.json` 原始文件或题面原文——这是私有出题仓库，候选人不允许下载/复制题干（`cn_forums.md:87` 已确认"需求写在 GitHub issue 里，故意设置为不可复制/不可直接粘贴"）。**标注为未能直接获取原始素材**。
- 但 **oavoservice.com 的逐 part 拆解文章**给出了目前找到的最详细复刻蓝图：
  - **数据**：`ride-simple.json` 是标准 **GeoJSON**，约 500 个 GPS 点，层级结构 `FeatureCollection → features[] → feature.geometry.coordinates[]`（坐标顺序是 **[经度, 纬度]**，这是 GeoJSON 标准顺序，容易搞反）。
  - **Part 1** 解析 GeoJSON，取前 10 个坐标点按要求格式输出——要点：文件路径可配置、异常处理健壮、正确识别数据层级。
  - **Part 2** 向给定 URL **发 POST 请求**（JSON body），把返回的 **PNG 地图图片**存到本地——要点：正确 headers、JSON 序列化、网络异常处理。
  - **Part 3** 用 **`staticmap`** 库把骑行路线连成线、画在底图上并导出图片——要点：坐标顺序不能搞反。
  - **Part 4** 在地图上标注地标（landmark），计算离骑行路线**最近的地标**——可选用 KD-Tree 等空间数据结构优化。
  - **Part 5**（"几乎没人做完"）：批量处理多条路线、缓存地图请求、把脚本模块化成可复用 CLI。
  - 关键库：`json`（内置）、`requests`（HTTP）、`staticmap`（渲染）、`math`（距离计算）。
  - 一小时格式，Stripe 更看重**前几个 part 的实现质量、代码整洁度、对未知需求的应对**而非做完全部 5 part。
  [来源 / https://oavoservice.com/en/articles/stripe-integration-bikemap-geojson-http-staticmap-nearest-landmark / 访问 2026-09-01]（与 `en_forums.md:257-259`、`cn_forums.md:87` 交叉一致）
- **`staticmap` PyPI 库**（`github.com/komoot/staticmap`）用法要点：
  ```python
  from staticmap import StaticMap, CircleMarker, Line
  m = StaticMap(300, 400)                                   # 宽高（+可选 padding_x/padding_y）
  m.add_line(Line([(13.4, 52.5), (2.3, 48.9)], 'blue', 3))  # 坐标是 (lon, lat)，颜色，线宽
  m.add_marker(CircleMarker((13.4, 52.5), 'red', 12))       # 坐标，颜色，直径
  image = m.render()
  image.save('map.png')
  ```
  颜色支持 Pillow 能识别的任意颜色定义。[来源 / https://github.com/komoot/staticmap（README） / 2026-09-01]
- `github.com/joeytor/StripeInterview` 的 `BikeMap.java`（见第 1.2 节）是 Java 版最基础的工具方法骨架（读文件/读 JSON），可作为 Java 语言候选人的起点，但**不含**发 HTTP 请求存 PNG、画路线、找最近地标等核心逻辑，仅第一步。

### 3.2 其他被报道的 integration 任务的公开复刻

- **Request Replay / Request Replayer**（`en_forums.md:257` 附近、`cn_forums.md:168`）——读 JSON 文件里保存的历史 request/response 对，重放请求，校验响应状态码/内容是否一致，需要维护"旧 response id → 新 response id"的映射。`joeytor/StripeInterview` README 有题干描述（见 1.2 节），但**没有找到独立公开复刻 repo**，只有该 README 里的一段文字描述，无代码实现。
- **Review Assignment via Git Diff + CSV Owners（JGit）**（`cn_forums.md:181`）——给一个 git diff（用 `JGit` 库解析）+ 一份 CSV 格式的代码 owner 清单，输出这次 diff 应该分配给谁 review。**GitHub 上搜索 `reviewer assignment jgit`/`code owners jgit diff` 均为 0 命中**，没有公开复刻。可以自己搭：用 `org.eclipse.jgit:org.eclipse.jgit` Maven 依赖 + `DiffFormatter`/`TreeWalk` API 解析 diff 涉及的文件路径，再按 CSV（路径前缀 → owner）做最长前缀匹配分配。[来源 / GitHub Search API 检索 0 命中 / 2026-09-01]
- **Payment Reconciliation（支付对账，对接清算服务 API）**（`cn_forums.md` 附近）与 **multi-JSON ETL** 类任务（读多个 JSON 源、清洗/合并/写出）——**均未找到公开复刻 repo**；这类题目结构上是"读若干结构不同的 JSON/CSV 数据源 → 按规则做 ETL（提取/转换/加载）→ 输出报表或写入存储"，可以用任意开源的小型 ETL 教程项目（如 `pandas` 读多个 JSON + `merge`/`groupby`）自行改编练习，没有必要专门找"最像"的开源项目。

### 3.3 可用来搭本地 mock 服务器的轻量方案（一句话评价）

| 方案 | 语言/生态 | 一句话评价 |
|---|---|---|
| Python `http.server`（标准库） | Python | 零依赖、几行代码起一个静态/自定义 handler 服务，适合"发 POST 拿 PNG"这类简单场景自己搭假后端，但要自己写路由和 JSON 处理逻辑。 |
| `json-server`（npm） | Node.js | 给一个 JSON 文件就能起一个支持增删改查的假 REST API，**最适合快速模拟 Bikemap/Request Replay 这类"读 JSON 数据 + 发 HTTP 请求"题型的后端**，零代码。 |
| WireMock（`github.com/wiremock/wiremock`） | Java（也有 standalone/容器/云版本） | 功能最全（录制回放、JSON 匹配、故障注入），适合 Java 候选人练 Integration 轮时本地起一个"真实感更强"的 mock 服务；比 `json-server` 重，但更贴近生产级 mock 测试实践。 |
| Python `responses` 库 | Python（`requests` 专用） | 在单测里 monkey-patch `requests` 库的调用，不起真实端口，适合给 bug squash/integration 代码写单测时 mock 外部 HTTP 调用，是 `stripe-interview/python-interview-prep` 官方依赖 `requests` 场景下的自然搭配。 |
| Python `respx` 库 | Python（`httpx` 专用） | 与 `responses` 类似但服务于 `httpx`（同步+异步都支持），如果练习代码用 `httpx` 而非 `requests` 就选它。 |

[来源 / WebSearch 综合 wiremock.org / json-server 官方文档 / 访问 2026-09-01]

## 4. System design 素材（GitHub 上的 Stripe 相关设计文档、参考实现）

- `github.com/joeytor/StripeInterview` README 的 **System Design** 分区（见 1.2 节）列了 4 道被报道过的题：Payment Webhook（引用 `stripe.com/docs/webhooks` + `tianpan.co/notes/166-designing-payment-webhook` 参考设计博客）、Counter Logging System（参照公有云 metrics 系统）、IAM System、**Ledger**（消息队列摄入交易 + 按商户账户订阅消费 + NoSQL 存储 + 周期性聚合算余额）。这是目前找到的**唯一**直接把 Stripe SD 题目和设计要点连在一起的 GitHub 素材。
- **`tianpan.co/notes/166-designing-payment-webhook`**（非 GitHub，但被 `joeytor` README 引用为 Payment Webhook 的参考设计博客）——建议在文件 2（官方侧资料）里与 Stripe 官方 webhook 文档一起交叉阅读。
- 未找到专门"Stripe ledger/webhook/idempotency/rate-limiter 参考实现"的 GitHub repo（即拿真实代码实现这几个系统的开源项目），这类内容更多以博客/文档形式存在，见文件 2 第 4 节（Stripe 官方工程博客）。
- 幂等/限流器相关的通用参考实现（非 Stripe 专属，但可作为 SD 轮候选人自己动手实现的参考）：`stripe/smokescreen`（见文件 2 第 5 节，SSRF 防护，webhook 追问常涉及）本身就是可读的真实生产级 Go 代码，是**唯一一个能在 GitHub 上直接读到 Stripe 生产代码风格**的相关项目。

## 5. 各题解 repo 的代码质量/坑

- **`femisowems/stripe-interview-questions`**——**质量最高**，三语言实现思路一致、测试齐全、题面完整，**直接可用**。唯一要注意：仓库很新（2026-05），暂无其他人验证过正确性（0 星、无 fork），建议自己跑一遍 `run_tests.sh` 核对 `expected_output.txt` 再信任。
- **`joeytor/StripeInterview`**——README 的题目分类和描述价值高（**在轮次归类上最系统**），但 `src/main/java/` 里的实现**多为半成品/工具方法骨架**（如 `BikeMap.java` 只有读文件/读 JSON 的辅助方法，没有主逻辑），**不要当作"标准答案"**，只当作起点脚手架。题目年代较早（2022 前提交），不排除部分题目细节已随 Stripe 出题库迭代而变化。
- **`sahaia1/Stripe_Pyhton_libraries`**——代码量太小、多是单文件脚本，**不建议作为学习模板**，只用来交叉确认题名存在性（如 `radarrules.py`/`capital.py` 佐证 Radar Rules、Stripe Capital 类题目确实被出过）。
- **`SabihaNazKhan/StripePhoneScreen24Nov25`**——**题面（Part 1 Shipping Cost）本身价值高**，但代码只写到一半（无测试、无 Part 2），仅可当题干抄录来源，不可当题解参考。
- **`premjm-67/stripe-interview-questions`**、**`kwang101/PracticeForStripe`**——**明确判定为低价值/可能标题误导**：前者是贴牌为"stripe interview"的通用 LeetCode 刷题集合（Evaluate Division / Parallel Courses III 等经典题，与 Stripe 出题风格不符）；后者代码是空壳。**不建议纳入复习材料**，仅在本文档存档以避免读者重复发现后误判为新线索。
- **`stripe-interview` 官方 org 的 10 个语言 prep repo**——**权威性最高但信息量最少**：只是环境搭建脚手架，不含任何题目内容，价值在于"确认面试支持哪些语言"和"依赖清单里透露的技术栈线索"（如 Python 侧预装 `requests`），**不要指望在这些 repo 里找到题目**。

## 附：来源清单 + 未能访问

**已成功访问/验证的来源：**
- GitHub REST API（`api.github.com/repos/...`、`/orgs/stripe-interview/repos`、`/search/issues`、`/search/repositories`）—— 约 40 次调用。
- `raw.githubusercontent.com` 直接读取 README/源码 —— 约 20 次。
- Gist 三个（aranibatta、stealthbomber10、pkafel）全部成功读取原文。
- WebFetch：`oavoservice.com` BikeMap 拆解文章、`komoot/staticmap` README、PyPI `staticmap` 页面。
- WebSearch：GitHub repo 关键词检索（`stripe phone screen`/`stripe bug squash`/`stripe integration interview`/`stripe onsite`/`stripe-interview-questions`）、mock server 生态对比、BikeMap 相关关键词。

**未能访问 / 检索为空：**
- GitHub `search/code`（code search API）——未认证请求返回 `401 Requires authentication`，无法用它检索"`ride-simple.json`""`accept-language stripe`"等代码片段级关键词，只能退化为 `search/repositories`（仓库级）+ WebSearch。
- `codeberg.org/snakeyaml/snakeyaml` 的原始 issue 历史——GitHub 镜像仓库检索为空，未直接访问 Codeberg 站点核实 boolean 解析 bug 的具体 issue 编号。
- JGit reviewer assignment、Payment Reconciliation、multi-JSON ETL 类 integration 题的公开复刻 repo——GitHub 检索 0 命中，判定为不存在公开复刻（这类任务通常基于 Stripe 私有出题仓库，候选人无法留存题干）。
- 部分 GitHub Search Issues API 调用受每小时 60 次核心请求限速影响，节流后完成，未出现数据丢失，但搜索广度受限（每个库仅取前 10 条结果排序方式为按创建时间）。

## 6. 附：femisowems 仓库两道代表题的完整题面原文摘录（供直接练习）

> 之所以完整摘录这两道，是因为它们分别代表"字符串/日志解析"和"数学/组合爆搜"两类 Stripe 出题风格，且题面在 repo 里保存得最完整、可直接使用；其余 4 题（Company Name Checker、Card Range Obfuscator、Fraud Detector、Subscription Notification Scheduler）题面结构类似，见 1.2 节摘要，完整原文可直接访问对应 `question*/Problem*.md`。

### 6.1 Problem 4 — Store Closing Time Penalty（与本文 1.3 节 pkafel gist、`en_forums.md:126` LeetCode Discuss 2585038 为同一题族）

原始英文题面（`question4/Problem4.md`）：店铺按小时记录是否有顾客（`Y`/`N`）；关店时间点 `closing_time`（0 到 n）的**罚分**定义为：开着但没顾客的每小时 `+1`（浪费），关了但有顾客的每小时 `+1`（错失机会）。
- **Part 1**：给定 log 和 closing_time，算总罚分。
- **Part 2**：求使罚分最小的 closing_time；并列时取最小的 closing_time。
- **Part 3**：员工可能把多天日志记在一个文件里，用 `BEGIN`/`END` 包裹；规则：不能嵌套、可跨多行、一行可能有多段、无效/未闭合的片段要忽略；按顺序对每个合法 log 输出最优 closing_time。
- 样例（含 `GARBAGE` 干扰文本的多段解析）：输入两段 `BEGIN...END`，输出 `4` 和 `7`。
[来源 / https://github.com/femisowems/stripe-interview-questions/blob/master/question4/Problem4.md / 2026-09-01]

### 6.2 Problem 6 — Stripe Payment Card Validation System

原始英文题面（`question6/Problem6.md`）：
- 支持网络：VISA（16 位，`4` 开头）、MASTERCARD（16 位，`51`–`55` 开头）、AMEX（15 位，`34`/`37` 开头）。
- Luhn 校验算法：从最右位起，每隔一位翻倍，翻倍后大于 9 则减 9，求和，能被 10 整除则有效。
- 输入格式：第一行 `Q`（查询数），每行以下四种形式之一：
  - `P1 card_number`——基础 VISA 校验，输出 `VISA` 或 `INVALID_CHECKSUM`。
  - `P2 card_number`——多网络校验，输出 `VISA`/`MASTERCARD`/`AMEX`/`INVALID_CHECKSUM`/`UNKNOWN_NETWORK`。
  - `P3 redacted_card`（含 1–5 个 `*` 通配符）——统计每个网络下有多少种合法补全，按网络名字母序输出 `NETWORK,count`。
  - `P4 corrupted_card?`（观测到的卡号恰好有一处错误，以 `?` 结尾）——恢复所有可能的合法原卡号，按数值升序输出 `card_number,NETWORK`。
- 样例含 9 组查询，展示 `P1`-`P4` 四种输出格式的完整对拍数据。
[来源 / https://github.com/femisowems/stripe-interview-questions/blob/master/question6/Problem6.md / 2026-09-01]

### 6.3 补充检索：其余关键词（本轮均为 0 命中或与 Stripe 面试无关，记录以避免重复检索）

以下 GitHub 仓库级关键词检索（`search/repositories`）均未找到与 Stripe SWE 面试相关的新素材，命中的全部是 Stripe 官方产品/Connect/Capital 的商业 demo 或无关同名项目：`stripe+capital+in:name,description`（10 命中，全部是 Stripe Capital 产品的第三方 demo/финансовые 项目）、`http+header+parser+stripe`（2 命中，均为通用 rate-limit header 解析库，非面试题）、`mutual+rank+stripe`（0）、`money+transfer+stripe+interview`（0）、`currency+conversion+stripe+interview`（0）、`accept-language+stripe`（0）。这些关键词更适合用 GitHub **code search**（需要登录 token，本次环境未认证，`search/code` 返回 `401`）去检索题解**代码片段**而非仓库名/描述，若后续有 token 可授权访问，建议优先对这几个关键词重跑 code search。[来源 / GitHub Search Repositories API / 2026-09-01]

### 6.4 femisowems 六题官方风格题名与业务背景对照表（比 README 摘要更精确的 `Problem*.md` 标题原文）

| 题号 | `Problem*.md` 精确标题 | 业务背景一句话 |
|---|---|---|
| 1 | **Atlas Company Name Check** | Stripe Atlas 远程注册公司时校验"公司名是否可用"，需按归一化规则（大小写、`&`/`,` 转空格、空格折叠等）判断与已注册名是否等价。 |
| 2 | **Card Range Obfuscation** | 卡号 8–19 位，前 6 位是 BIN；Stripe 卡片元数据 API 对一个 BIN 区间可能只返回部分覆盖的品牌区间（有 gap），需要补全区间使其无缝覆盖整个 BIN 段，防止被用于探测有效卡号。 |
| 3 | **Catch Me If You Can: Fraud Detection** | 对商户交易流按 **MCC（Merchant Category Code，商户类别码）** 做欺诈模型：支持按次数阈值、按百分比阈值，以及 dispute（拒付）冲正特定 charge 的欺诈判定。 |
| 4 | **Store Closing Time Penalty** | 见 6.1 节完整题面。 |
| 5 | **Subscription Notification Scheduler** | 订阅生命周期邮件调度：`send_schedule` 把相对天数偏移映射到邮件类型（`"start"`/负数偏移/`"end"`），要求在正确日期打印邮件。 |
| 6 | **Stripe Payment Card Validation System** | 见 6.2 节完整题面。 |

这张表比 README 的简短摘要更有价值的地方：**题 1 明确点名 Stripe Atlas**、**题 3 明确用 MCC 这个 Stripe/支付行业真实术语**——说明这批题目的业务包装并非泛泛而写，而是紧贴 Stripe 具体产品线（Atlas、Radar/Fraud、卡片元数据 API、Billing/订阅），复习时可以顺带补一下这几个产品的官方术语（见文件 2 第 6 节术语表）。[来源 / https://github.com/femisowems/stripe-interview-questions/tree/master / 2026-09-01]

