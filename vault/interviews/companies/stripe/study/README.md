# study/ — 中文题解与通用精华

这个目录是 `stripeoa` 仓库的**学习面**：把 `problems/` 里 53 道题的英文规格，翻译、拆解、
提炼成中文的**考点**、**解题思路**、**语法与语义细节**，以及一套**可迁移到任何公司 OA 的通用打法**。

目标只有一个：**读完 `00-essentials/` 之后，随便翻开一道 `problems/qNN_*/problem.md`，
你能看懂题、说出考点、独立写出通过全部隐藏测试的代码。**

## 怎么用（推荐顺序）

| 步骤 | 做什么 | 花多久 |
|---|---|---|
| 1 | 通读 `00-essentials/01` → `11`，不背，只求"知道有这回事" | 3–4 小时 |
| 2 | 打开 `10-solutions/q01_fraud_mcc_disputes.md`，只读「题意」「考点」两节，合上，自己写 | 60 分钟 |
| 3 | 写完再读该篇的「思路」「骨架」「坑」，对照 `problems/q01_*/solution.py` | 20 分钟 |
| 4 | 把没答上来的点，去 SystemDesign 仓库的 **Code Core** 牌组里找对应卡片，加进复习队列 | — |
| 5 | 按 `INDEX.md` 的顺序刷完 Top 10，再刷算法组 qA01–qA13 | — |

**第 2 步是重点。** 题解是用来验收的，不是用来读着爽的。先写，再看。

## 目录

```
study/
  README.md                       本文件
  INDEX.md                        53 题 × 考点 × Code Core 节点 的映射总表
  00-essentials/                  通用精华 —— 与公司无关，与题目无关，只有可迁移的东西
    01-solving-framework.md       60 分钟通用解题框架
    02-core-topics.md             核心考点总纲（S01–S24 / A01–A16 中文详解）★ 主文件
    03-python-cheatsheet.md       Python 语法 · 标准库 · 惯用法速查
    04-money-and-rounding.md      金额、精度、舍入、费率、分摊
    05-time-and-intervals.md      时间、日期、窗口、区间
    06-ordering-and-output.md     排序、tie-break、字节级输出
    07-pitfalls.md                陷阱总清单（从 53 道题里抽出来的）
    08-algorithm-patterns.md      算法模式识别 + 模板代码
    09-debug-and-selftest.md      无调试器调试 + 自测清单
    10-communication.md           与面试官沟通（phone screen / onsite）
    11-readiness-checklist.md     "能独立做出来"的验收清单
  10-solutions/                   53 篇中文题解，文件名 = problems/ 下的目录名
    q01_fraud_mcc_disputes.md
    ...
    qA13_lc2483_minimum_penalty_for_a_shop.md
```

## 与 Code Core 牌组的关系

姊妹仓库 `SystemDesign` 里有一个新领域 **`code-core`**（Anki 牌组 *Code Core*，86 个节点）。
分工是清楚的：

- **这里（stripeoa/study）** = 中文、具体、面向这 53 道题。读一遍，做一遍。
- **那里（code-core 牌组）** = 英中双语、抽象、面向所有 OA。每天几分钟，反复复习。

每篇题解末尾的「Code Core 节点」一节，把这道题的考点映射到牌组的叶子节点上，
所以做错一道题之后你知道该去复习哪几张卡，而不是"再刷十道题"。

## 这个项目会长大

Stripe 只是第一个 starter。后面接进来的 Amazon OA、quant OA、各家 onsite，
都按同一个模式：**具体题目留在自己的仓库，通用规律升到 `code-core` 的叶子上**。
`code-core` 里的 `transfer.*` 分支就是为此预留的接口 —— 新公司的一轮面试是一个叶子，
不是一个新领域。
