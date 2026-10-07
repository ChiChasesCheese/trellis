# Team Interviews · VOICE 价值观 · 题库（10 题）

> 来源：官方 how-we-hire（O-14："meet a cross-functional group of people … explore values fit, how you collaborate"）· VOICE 原文（O-10）· "You might not thrive here if…"（O-11）· how-we-work（O-13）· AI 条款（O-15："What doesn't land: Generic, polished responses that read like they came straight from a prompt"）。题目本身是**按官方价值观构造的 (reconstructed)**——没有面经报道过具体的 team 面题。
> 练：`python3 loop/mock.py bq team -n 4 -m 2`。每题 60 秒，先给结论，再给一个具体例子，最后一句"我从中学到/现在怎么做"。

| # | 题 | VOICE | 主故事 | 一句话要点 |
|---|---|---|---|---|
| 1 | Tell me about a time you shipped something quickly and it went wrong. What did you own? | **V**elocity（"owning our mistakes"） | [[S3]] fail loudly · [[S10]] | 快不是问题，静默失败才是；我加了"响亮失败"的守卫 |
| 2 | Give an example of stepping into a problem that wasn't yours. | **O**wnership（"moving on purpose, not permission"） | [[S7]] schema pool · [[S8]] | 没人分配，但每个人都被它拖慢 |
| 3 | Tell me about a time you were wrong and changed your mind publicly. | **I**ntellectual honesty（"facts over ego … disagree, commit, move forward"） | [[S10]] 推翻自己 10× | 用数据推翻自己的估算并主动更正 |
| 4 | Tell me about a disagreement where you committed to a decision you didn't agree with. | Intellectual honesty（"disagree, commit"） | [[S9]] | 讲清我的主张、最后的决定、我如何全力执行 |
| 5 | How do you make sure what you build is actually useful to the customer? | **C**ustomer obsession（"never do work that holds no customer value"） | [[S4]] · [[S6]]（告警量 = 分析师的痛） | 先问谁会看这个输出、误报的代价是谁付 |
| 6 | What's a bar you raised on your team? | **E**xcellence | [[S2]] 质量门禁 · [[S1]] 校验 UDTF | 把"对不对"变成自动门禁 |
| 7 | How do you work when there's no process for what you need to do? | O-11 "rigid rules … the open-endedness" · O-13 "When the path isn't clear, you're expected to make one" | [[S6]] · [[S5]] | 先写下已知/未知，提出方案，设可回滚点，推进 |
| 8 | How has AI changed the way you work in the last six months? | O-12 "rethink your work around what AI makes possible" | [[S7]] | 不是更快写同样的代码，而是做以前不值得做的事（clone 池、on-call copilot） |
| 9 | How do you give and receive feedback? | Excellence（"raise the bar in our work, our feedback"） | [[S2]] 接受批评 | 具体、基于证据、对事 |
| 10 | What would make you leave a job? | fit | — | 不能 own 结果、离用户太远（真诚，短） |

## 跨职能面（PM / 设计 / 安全分析师）可能的角度

- 安全分析师："How would you want analysts to tell you a detection is wrong?"——回答里要有**反馈回路**（cb03 t3 的思路：用 disposition 数据，但别让攻击者"洗白"）。
- PM："How do you decide v1 scope?"——"the smallest thing a reviewer can act on, with the assumptions written down and a metric that tells us if it's wrong"。
- 任何人："What questions do you have for us?"——`../../../06-questions-to-ask.md`。
