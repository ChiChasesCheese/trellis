# ByteStyle：六条价值观和你的故事

- ByteStyle 是 ByteDance 官方的六条价值观；使命是「Inspire Creativity, Enrich Life」。它不是公布的评分表，是 HM 听你讲故事时用的透镜。TikTok 的岗位说明还写着：以好奇、谦逊和产生影响的愿望来领导，保持 **Always Day 1** 的心态。
- 用法：每条价值观对应一个故事和一句话；讲故事时让这个词自然出现一次，不要背诵价值观。
- 缺口用 【待补：…】 标出；补不出来就不要硬凑。

| 价值观 | 故事 | 你要说的那一句 |
|---|---|---|
| Always Day 1 | S7、S8 | I built it **before anyone asked** |
| Champion Diversity and Inclusion | S9、S4 | I **deferred** where others knew more |
| Be Candid and Clear | S10、S3 | I **retracted** my own number |
| Seek Truth and Be Pragmatic | S3、S10 | I **sliced the data** until one row explained it |
| Be Courageous and Aim for the Highest | S6、S5 | I **stopped** a launch; I chose the harder, cleaner design |
| Grow Together | S2、S7 | **Other engineers** build on what I made |

## 1 · Always Day 1

- **官方含义**：保持创业心态，不靠资源或过去的成就；追求效率和简洁，减少不必要的流程；拒绝自满，保持开放和谦逊。
- **故事**：[[S7_schema-pool-and-why-a-clone-is-fast|S7 schema pool]]（没人要的工具）· [[S8_fix-one-then-scan-the-repo|S8]]（修一个，再扫整个仓库）。
- **一句话**：「Nobody assigned it: two engineers, or two AI agents, collided on DDL, so I built a pool of **two-second** clones.」
- **S8 的备用句**：「I'd rather own '**here's the next one**' than just the one that paged.」
- **别说**：S7 是团队标准；它是个人仓库里的工具。

## 2 · Champion Diversity and Inclusion

- **官方含义**：重视个体差异和各自的长处；放眼全球；默认善意、默认信任，促进有效协作。
- **故事**：[[S9|S9 出款延迟事故]]（多 owner 事故，我是 SLA 的权威，部署让给同事）· [[S4|S4 AU Amex 退款费]]（三个团队 50 条回复，用数据拉回共同事实）。
- **一句话**：「I took the part I was the **authority** on, and let the others land the **deploy**.」
- **S4 的备用句**：「It **predated** our migration」把指责变成共同事实。
- 【待补：和不同时区或文化的团队（中国、新加坡）协作的真实例子；没有就不硬凑】

## 3 · Be Candid and Clear

- **官方含义**：直言不讳，暴露问题，不「managing up」；准确、简洁、直接，少用术语；用数据和事实下结论，而不是假设或情绪。
- **故事**：[[S10_retract-own-number|S10 撤回自己的数字]]（最强）· [[S3_silent-null-root-cause|S3]]（拒绝把 ACH 加进例外清单）。
- **一句话**：「I'd rather **retract my own number in public** than have a remediation sized off a bad predicate.」
- **S3 的备用句**：「Adding ACH to the exclusion list would turn a **loud** detector **silent**.」
- **清晰**：每个故事 60 秒内出现「我的决定」；一个名词后面跟一个「因为……」。

## 4 · Seek Truth and Be Pragmatic

- **官方含义**：独立思考，追到根上；深入事实，要第一手数据；脚踏实地，关注真实影响。
- **故事**：[[S3_silent-null-root-cause|S3]]（没有报错的 bug）· [[S10_retract-own-number|S10]]（重审谓词）· [[S4|S4]]（查数据，不查组织架构）。
- **一句话**：「I **sliced** the missing rows, found **one row** with a NULL, and **walked back** to the function with two overloads.」
- **S4 的备用句**：「I pulled the **data**, not the org chart: **1,079,627** rows vs **0**.」
- **Pragmatic**：S6：「per-row cost × peak rows」的算术，比争论更务实。

## 5 · Be Courageous and Aim for the Highest

- **官方含义**：有计算的冒险，看投入产出；在更大的范围里探索替代方案；坚持高标准，不只是完成。
- **故事**：[[S6_per-row-cost-times-peak-rows|S6]]（叫停一个会半夜报警的上线）· [[S5_cutover-with-the-production-query|S5]]（选更干净的静态拆分，不是更聪明的 fallback）。
- **一句话（S6）**：「I'd rather **stop** than ship something that **pages at 3 a.m.**」
- **一句话（S5）**：「In a revenue path the source of truth should be a **fact**, not a runtime decision.」
- **Highest**：S5 的做法：用生产查询本身验证，默认关的发布，把窗口的风险**写在代码旁边**。
- 【待补：一个更大的赌注，带投入产出的论证；如果没有，就讲 S5 的「选 B」】

## 6 · Grow Together

- **官方含义**：被使命驱动；面对短期波动有耐心和韧性；一起解决问题；持续学习。
- **故事**：[[S2|S2 质量检查框架]]（别人往上接）· [[S7_schema-pool-and-why-a-clone-is-fast|S7]]（相邻团队用上了 on-call copilot）。
- **一句话**：「Adding a check went from a **new task** to a **config row**; other engineers onboard onto it.」
- **带教**：我写了团队的 **onboarding doc**（2024），一个新同事的三个模块接到我的平台上，我先定**契约**。
- **学习**：说一个你正在补的真实缺口（例如 Go、性能剖析）。【待补：这周你实际做了什么】
- **韧性**：【待补：一次重组、req 变化或项目被砍后你怎么继续的例子；没有就不讲】

## 面试里怎么用

- 不要说「我符合 Always Day 1」；讲 S7，词自然出现一次。
- HM 问「你为什么适合 TikTok」时，选**一条**价值观，用它的故事回答，不要列六条。
- 被问「你怎么看和同事意见不同」：Be Candid and Clear（S10、S3）。
- 被问「你怎么处理模糊的项目」：Seek Truth（S3）或 Be Courageous（S6）。
- 被问「你怎么带别人」：Grow Together（S2，加 onboarding doc）。
