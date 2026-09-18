# 故事 × 8 条价值观 覆盖矩阵（recruiter / expertise / HM / team matching 四轮共用）

> 故事本体在 [[Core]]（[[S1]]–[[S9]]，含诚实红线）；逐题答案在 [[Answers]]（[[Answers#Q1]]–[[Answers#Q24]]）；英文口述稿在 `../00_ai_screen/stories.md`（[[S1]]–[[S10]] + 追问版）与 `../../../04-answer-bank.md`。**这里不复制故事，只做映射与检查表。**
> 用法：`mock.py bq hm -n 5` 抽完后，在下表勾掉命中的格子；一组 5 题至少覆盖 3 个故事、3 条价值观。

## 矩阵

| 故事 | Own It | Get It Done | Integrity Always | Put Customers First | Be Excellent | Think Big | Make Each Other the Best | Embrace Differences |
|---|---|---|---|---|---|---|---|---|
| **[[S1]]** AMEX GRRCN 管线（22M 笔 / $138.6B） | ● 端到端 | ● 18 个月生产 | | | ● 幂等 + 急停 | ○ | | |
| **[[S2]]** Quality-check 框架 + ADR | ● 自己修自己的缺陷 | | ● 三个被否方案 | | ● 复用 8 次 | | ○ 定标准 | |
| **[[S3]]** ACH fee RCA（196 merchants / $11.3M/day） | ● 自己转发 pager | ● | | ○ | | | | |
| **[[S4]]** AU Amex refund（1,079,627 vs 0） | | | ○ | ● 给 PM 同一份证据 | | | ● 跨团队 | ○ |
| **[[S5]]** Net settlement（$55B TPV / 13.7M 行 / 0.224%） | ● 两年 owner | ● | | | ● shadow-run | ● | | ● 三方三语言 |
| **[[S6]]** Anomaly detector go/no-go | | ○ | ● 叫停、写下数字 | | | | | |
| **[[S7]]** snowglobe-tools（schema pool） | ● 自发 | | | | ○ | ○ | | |
| **[[S8]]** Terraform 7 分钟 RCA | | ● | | | | | ● unblock 他人 | |
| **[[S9]]** DoorDash 出款事故（SLA 权威） | ● 被点名 owner | | ○ | ● | | | | |
| **Ziyang**（domain-ownership 框定） | | | | | | | ● 定 contract | |
| **Onboarding doc**（2024→2026） | | | | | | | ● | |
| **Quant-Stroller**（66K 行 / 470 测试文件） | | | | | | ● | | |

● 主用 · ○ 可带到

## 红线提醒

- 不说 $600B；说 138B / 22M / 13.7M / 0.224%。
- Ziyang 只讲领域所有权，不编 PR review / 1:1 细节。
- Sentry 只说 ingestion 层 error tracking；主讲 Datadog。
