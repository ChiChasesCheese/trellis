# 00-essentials · 阅读顺序

> 读者画像：PayPal 后端 1.5 年（Java/Kotlin/Snowflake SQL、Kafka、Spark），SQL 管线强，限时算法/类设计弱。五篇覆盖电面 coding、OOD、OA、SD 四类技术轮；非技术轮（recruiter/HM/Chakra/team matching）见 `../../fit.md`、`../../03-chakra-playbook.md`、`../../04-answer-bank.md`。

| 顺序 | 文件 | 对应轮次 | 先修 |
|---|---|---|---|
| 1 | `01-solving-framework.md` | 全部技术轮的地基：40 min 电面编码 / 45 min OOD / 120 min OA 三套时间框架、出声模板、follow-up 四种形状 | 无，先读这篇 |
| 2 | `02-dp-patterns.md` | OA（`q02` `q04` `q05` `q09`）+ 电面（`q01`） | 读完 1 |
| 3 | `03-graph-tree-patterns.md` | 电面 coding（`pc01` `pc02` `pc04` `pc06`）+ OA（`q03` `q07` `q08` `q10`） | 读完 1 |
| 4 | `04-class-design-and-concurrency.md` | OOD 轮（`od01`–`od09`，od07 未建题）| 读完 1 |
| 5 | `05-sd-framework-snowflake-primitives.md` | SD 轮（`sd01`–`sd12`、`sd22`）；配合 `../20-cards/sd_checklist.md`（45 min 分钟表 + 五维 rubric，不重复） | 读完 4（构件与 OOD 的锁/租约概念相通） |

**其余先修材料**：Java→Python 面试写法见 `../00-prereq/01-python-for-interviews.md`；并发基础见 `../00-prereq/02-concurrency-basics.md`（04 篇引用它）；分布式词汇见 `../00-prereq/03-distributed-systems-vocab.md`（05 篇引用它）；用你自己的 Snowflake 使用经验讲原语见 `../00-prereq/04-snowflake-primitives.md`（05 篇引用它）。

**建议顺序**：先扫一遍 `00-prereq/` 四篇（如果 Python/并发/分布式术语不熟，1–2 小时），再按 1→5 顺序读本目录。每篇读完立刻去 `../../loop/mock.py` 或 `drill.py` 跑对应题目，不要五篇连读完再练习——`01` 里的出声模板必须在做题时同步练习才会内化。
