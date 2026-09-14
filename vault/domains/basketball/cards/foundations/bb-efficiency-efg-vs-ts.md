---
id: bb-efficiency-efg-vs-ts
node: foundations.efficiency
type: qa
---
## Q
Player A shoots 50% from the field, all twos. Player B shoots 42%, but half his attempts are threes and he draws fouls. Which shooting metrics separate them, what does each one include, and which should you quote?

## A
- **FG%** treats every make as equal, so it cannot compare a three-point shooter to a rim finisher. By FG% alone A looks better, which is wrong.
- **eFG% = (FGM + 0.5 × 3PM) / FGA** — credits a made three with the extra half-basket it is actually worth. On 100 shots, B's 42 makes split evenly across 50 threes and 50 twos gives eFG% ≈ 52.5%, already ahead of A's 50%.
- **TS% = PTS / (2 × (FGA + 0.44 × FTA))** — adds free throws. The 0.44 is an estimate of how many *possessions* a free-throw attempt represents, since and-ones, three-shot fouls and technicals mean FTAs do not map one-to-one onto trips.
- **Quote TS%** when comparing scorers, because drawing fouls is a scoring skill that eFG% ignores entirely. B's advantage grows again once his free throws count.
- Neither metric says anything about **shot creation or volume**. A spot-up shooter's TS% is inflated by shots someone else made easy; efficiency has to be read together with usage.

## Q zh
球员 A 投篮命中率 50%，全是两分。球员 B 命中率 42%，但一半出手是三分，而且能造犯规。哪些投篮指标能把两人区分开？每个指标包含什么？你应该引用哪一个？

## A zh
- **FG%** 把每次命中都当作等价，所以无法比较三分射手和终结者。只看 FG% 会觉得 A 更好，这是错的。
- **eFG% =（FGM + 0.5 × 3PM）/ FGA** — 给命中的三分记上它实际多出的半个球。以 100 次出手计，B 的 42 次命中平均分布在 50 次三分和 50 次两分上，eFG% ≈ 52.5%，已经超过 A 的 50%。
- **TS% = PTS /（2 ×（FGA + 0.44 × FTA））** — 再把罚球算进来。0.44 是对"一次罚球出手代表多少个**回合**"的估计，因为 and-one、三分犯规和技术犯规意味着 FTA 和上罚球线的次数并非一一对应。
- 比较得分手时**引用 TS%**，因为造犯规是一项 eFG% 完全忽略的得分技能。把罚球算进去后，B 的优势会再度扩大。
- 两个指标都不说明**创造出手的能力和使用率**。定点射手的 TS% 被别人喂出来的轻松球抬高了；效率必须和 usage（使用率）一起读。
