---
id: nr-amz-g4-starl
node: amazon.outline
type: qa
step: 49
---
## Q
<p class="title">什么时候信任 LLM<span class="meta">02 提纲</span></p>

适用 LP、开场 hook 和 STAR-L 提纲

## A
- 主 LP：Are Right, A Lot（判断力 + 找反证）；备用：Ownership、Learn and Be Curious。

**Hook：「Trust depends on whether an oracle can say the output is wrong.」**

- **S · Situation**
    - After months of **running agents in parallel**, I needed a rule better than "it **feels right**".
- **T · Task**
    - Decide **per task** how much to trust the output, and **write it down**.
- **A · Action**
    - The rule has two inputs: is there an **oracle** (compiler, test, re-runnable script), and what does a wrong answer **cost**?
    - Oracle plus **low blast radius**: I **trust and verify by machine** — refactors under green tests, scaffolding, examples that must compile.
    - **No oracle**: I **don't trust** numbers, claims about external systems, anything **secondhand**.
    - Example: an agent labelled a figure **officially disclosed**; it came from a **single prep site**.
    - **High cost**, like money code: I **read every diff** myself regardless.
    - The blind spot is a **wrong conclusion on a plausible assumption**: gates check **shape**, only reading checks **substance**.
    - So I read the agent's own "**least sure**" list first.
- **R · Result**
    - Defects surface at the **gate or in review**, not with the reader.
    - Example: a Java example that **would not compile**, caught when I **compiled every textbook example**.
- **L · Learning / Mechanism**
    - Trust is a property of the **verification around the model**, not of the model.
- 信任矩阵（口述用）：
    - 有 oracle + 错的代价低 → 信任 + 机器验证：脚手架、重构、样例代码。
    - 有 oracle + 错的代价高 → 信任 + 机器验证 + 我读 diff（money code）。
    - 无 oracle + 代价低 → 当草稿用，我改写。
    - 无 oracle + 代价高 → 不信任：数字、外部系统事实、安全、权限、二手来源；先造 oracle，或自己做。

<div class="sources"><b>表达 · business English</b><br>• <b><i>decision framework</i></b> — 决策框架<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I wrote a two-input decision framework instead of going on gut feel.”</span><br>• <b><i>write it down</i></b> — 写下来固化<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I wrote the rule down so it doesn&#x27;t depend on my mood.”</span><br>• <b><i>least-sure list</i></b> — 最不确定清单<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I read the agent&#x27;s least-sure list before anything else.”</span></div>
