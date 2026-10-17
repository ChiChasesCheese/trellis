# Story × LP 覆盖矩阵

听到 LP 问题，先在下面的第二张表找该 LP 的「先用哪个故事」，再用「备选」换角度。同一轮、同一面试官面前不要重复讲同一个故事；每个故事的「换个 LP 讲」写了换角度时该强调哪一段。

## Story × LP（P = 主答案，S = 支撑 / 换角度）

故事：S1 Amex 管线 · S2 Quality-check 框架 · S3 ACH NULL 事故 · S4 AU 退款费 · S5 interchange 切换 · S6 anomaly go/no-go · S7 schema pool · S8 Terraform RCA · S9 Amex 出款延迟 · S10 退款费复盘 · S11 实习事件流 · R1 Quant-Stroller · R2 AI 迁移 · R3 Aiki · M1 带新人

| Story | 1 CO | 2 OWN | 3 IS | 4 ARAL | 5 LBC | 6 HD | 7 IHS | 8 TB | 9 BFA | 10 FRU | 11 ET | 12 DD | 13 HB | 14 DR | 15 BE | 16 SSBR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S1** |  | P | S |  |  |  | S |  |  | S |  | S |  | P |  |  |
| **S2** |  |  | P | S |  | S | P | S |  | P | P |  | S |  |  |  |
| **S3** | S | P |  |  |  |  | P |  | S |  | S | P | P | S |  |  |
| **S4** | P | S |  | S |  |  |  |  |  |  | P | P | S |  |  |  |
| **S5** | S | P | S | P |  |  | S | S | S | S |  | S |  | P |  |  |
| **S6** |  | P | S | P |  |  | S |  | S | S |  | P | P | S |  |  |
| **S7** |  | P | P |  | S |  |  | S | P | S |  |  |  |  |  |  |
| **S8** |  | S |  |  |  |  | S |  | P |  | S | P |  | S |  |  |
| **S9** | P | S |  |  |  |  | S |  |  |  | S | S | S | S |  |  |
| **S10** | S | S |  | P |  |  | S |  |  |  | P | P |  |  |  |  |
| **S11** |  |  |  |  | S |  | S |  |  |  |  | S |  | S |  |  |
| **R1** |  | S | P | P | P |  | P | P |  |  |  | S |  | S |  |  |
| **R2** |  |  | S |  | P |  | S |  | P |  |  |  |  | S |  |  |
| **R3** | P | S | S |  | S |  |  |  |  |  |  |  |  | S |  |  |
| **M1** |  | S |  |  |  | P | S |  |  |  | S |  |  |  | S |  |

## 每条 LP：先用哪个故事 / 备选

| # | LP | 先用 | 备选 |
|---|---|---|---|
| 1 | Customer Obsession | S4、S9 | R3 / S3、S5、S10 |
| 2 | Ownership | S1、S3、S5、S6、S7 | S4、S8、S9、S10、R1、R3、M1 |
| 3 | Invent and Simplify | S2、S7 | R1 / S1、S5、S6、R2、R3 |
| 4 | Are Right, A Lot | S5、S6、S10 | R1 / S2、S4 |
| 5 | Learn and Be Curious | R1、R2 | S7、S11、R3 |
| 6 | Hire and Develop the Best | M1 | S2 |
| 7 | Insist on the Highest Standards | S2、S3 | R1 / S1、S5、S6、S8、S9、S10、S11、R2、M1 |
| 8 | Think Big | R1 | S2、S5、S7 |
| 9 | Bias for Action | S7、S8 | R2 / S3、S5、S6 |
| 10 | Frugality | S2 | S1、S5、S6、S7 |
| 11 | Earn Trust | S2、S4、S10 | S3、S8、S9、M1 |
| 12 | Dive Deep | S3、S4、S6、S8、S10 | S1、S5、S9、S11、R1 |
| 13 | Have Backbone; Disagree and Commit | S3、S6 | S2、S4、S9 |
| 14 | Deliver Results | S1、S5 | S3、S6、S8、S9、S11、R1、R2、R3 |
| 15 | Strive to be Earth's Best Employer | 无主故事：M1 做薄支撑 | M1 |
| 16 | Success and Scale Bring Broad Responsibility | 无故事 | 见待补 |

## 待补

- 【待补：LP13 Have Backbone / Disagree and Commit：找一次建议被否决（尤其被资深同事/经理）后仍全力执行的例子；先从 S5（选 A/B 时有没有资深同事倾向 A）、S9（revert vs conditional）、S2 评审里挖；没有就如实说没有完整故事】
- 【待补：LP6 Hire and Develop：被带的工程师现在独立 own 什么；onboarding doc 帮了几个人；一次你给出具体设计意见、对方改了的例子；是否参与过面试/评级（M1 是唯一主故事）】
- 【待补：LP8 Think Big：S2 框架被几个团队使用；S7 工具被谁采用；一次你把小任务重新定义成更大平台并说服别人投入（现在只有个人项目 R1 撑着）】
- 【待补：LP5 Learn and Be Curious：S11 实习起点与学习路径；S7 为什么去研究零拷贝克隆 / Deployments API；R1 学 DSR / PBO 的路径（现在没有雇主工作的主故事）】
- 【待补：LP10 Frugality：真实成本数字：S1 的 `STREAM_HAS_DATA` 省多少 warehouse 时间；S2 方案 D 避免多少新基础设施；S7 克隆相对全量拷贝省多少（S2 是唯一主故事）】
- 【待补：LP9 Bias for Action：S5 暗发布时在信息不全下决定上线的那一刻：风险、可逆性、谁反对；S8 事后两个同形风险是否推动了修复】
- 【待补：LP1 Customer Obsession：S4 AU 漏掉的退款费金额；S9 商户最终拿到钱的时间与是否直接沟通；一次没人要求时因商户影响升级优先级】
- 【待补：LP14 Deliver Results：S1 / S5 里一个具体障碍及怎么绕过；对齐 S1 美元口径】
- 【待补：LP15 / LP16：为同事创造更安全/更包容环境的例子，或评估行动对第三方/用户副作用并因此改变做法的例子；S3 commit 前考虑对商户的二阶影响、S10 避免按错误谓词过度补偿，可作候选，需你确认真实动机】
- 【待补：简历「$600B+ annual transaction volume」与 S1 的 ~22M 笔相差两个数量级，面试前把简历和口播的范围统一】
- 【待补：简历 "Spearheaded net settlement project … hundreds of millions in working-capital savings" 与 S5 口播 "I own the fee side" 不一致，统一说法并准备 baseline】
- 【待补：各 S / R / M 文件里的 influence 细节（谁评审、谁反对、谁复用），见各故事的「待补」】
