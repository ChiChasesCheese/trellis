---
id: nr-amz-g1-followups
node: amazon.followups
type: qa
step: 76
---
## Q
<p class="title">一个自信的错数字<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **How did you notice?**
    - 用 `python3 -c` 复算（review 规则：每个数字复算），不是「感觉不对」。
    - 【待补：这一次是你本人复算的，还是 review 步骤里发现的？照实说】
- **Is that really a hallucination?**
    - 定义：流畅、自信但没有依据的内容。
    - 这是算术 / 数量级错误，更准确叫 **confident wrong claim**；主动说出区分是加分项。
- **What did you change so it doesn't recur?**
    - 规则进共享指令文件（每个被发现的缺陷变成一条规则）。
    - 一个 review 辅助脚本 + 一个验收脚本。
- **Why not just use a better model?**
    - 更强的模型降低频率，不提供 oracle。
    - 检查成本（一行脚本）远低于模型升级，且对未来的模型同样有效。
- **Did a wrong number reach a learner?**
    - 在卡片发布前被抓到（推送到 Anki 是最后一步）。
    - 【待补：是否有已进入 Anki 复习的卡片后来被纠错？没有就说没有】
- **What would you do differently?**
    - 在 pilot 之前就把「数字必须脚本复算」写进指令。



<div class="sources"><b>表达 · business English</b><br>• <b><i>confident wrong claim</i></b> — 说得笃定但其实错的论断<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d call it a confident wrong claim rather than a hallucination, since it was an arithmetic error.”</span><br>• <b><i>raise the floor</i></b> — 抬高下限，让最差情况也不差<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A better model raises the floor, but only a script gives me an oracle.”</span><br>• <b><i>bake it into the process</i></b> — 把做法固化进流程<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Every defect I find gets baked into the instruction file as a rule.”</span></div>
