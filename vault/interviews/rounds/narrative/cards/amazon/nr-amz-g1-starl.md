---
id: nr-amz-g1-starl
node: amazon.outline
type: qa
step: 46
---
## Q
<p class="title">一个自信的错数字<span class="meta">02 提纲</span></p>

适用 LP、开场 hook 和 STAR-L 提纲

## A
- 主 LP：Dive Deep；备用：Insist on the Highest Standards、Earn Trust（对读者负责）。

**Hook：「I re-derived the number with a script instead of trusting how confident it sounded.」**

- **S · Situation**
    - I'm building a **system-design study bank**: about **50 problems**, drafted by **Claude Code subagents**.
    - A learner **memorizes** those numbers, so a wrong one is a **shipped defect**.
- **T · Task**
    - I **own correctness**: the agent drafts, and **I** make sure nothing wrong gets through.
- **A · Action**
    - On the **first pilot problem**, the article stated a hash-collision probability of **38 percent**.
    - I **re-derived** it with a one-line script: the real answer was **certainty**, the exponent off by **six orders of magnitude**.
    - The wrong figure was **already in a flashcard**, so I fixed the **article first, then the card**.
    - I stopped treating it as one bug and wrote a **rule** into the shared agent instructions: every number is **computed, never recalled**.
    - Second rule: a number you **couldn't verify** never goes into a card.
    - **Later**, a second article had correct arithmetic on **two contradicting assumptions** (a **1,560x** peak ratio), so I added: assumptions must **agree with each other**.
- **R · Result**
    - All **49** problems passed the gate; **two** were redone for design substance.
    - **Four lessons** now live in the instruction file.
- **L · Learning / Mechanism**
    - The model's **confidence tells you nothing**; arithmetic is cheap, so **check it by machine**.

<div class="sources"><b>表达 · business English</b><br>• <b><i>sanity-check</i></b> — 快速核对是否合理<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I sanity-checked the 38 percent with a one-line script before it reached anyone.”</span><br>• <b><i>root cause, not symptom</i></b> — 修根因而不是修表象<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I fixed the root cause by writing a rule, not just the one wrong figure.”</span><br>• <b><i>close the loop</i></b> — 把事情闭环<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I fixed the article, then the card, to close the loop for the reader.”</span></div>
