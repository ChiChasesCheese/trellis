---
id: nr-amz-g1-full
node: amazon.full
type: qa
step: 16
---
## Q
<p class="title">一个自信的错数字<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：我在做一个系统设计学习题库，约 50 道题，由 Claude Code subagent起草。读者会把里面的数字背下来，所以一个错数字就是一个已经交付的缺陷。
- 我的角色：正确性由我负责。代理负责起草，我负责保证错的东西不会流出去。
- 触发：第一道试点题的文章里写了哈希碰撞概率 38%。我没有因为它说得很笃定就接受，而是用一行脚本复算，结果是必然碰撞，指数差了六个数量级。
- 我做了什么：这个错数字已经进了一张闪卡，所以我先改文章再改卡片。然后我不把它当成一个孤立的 bug，而是在共享的代理指令里写了规则：每个数字都要计算，不能凭记忆；没法验证的数字不进卡片。后来另一篇文章算术都对，但用了两个互相矛盾的假设（峰值比 1,560 倍），我又加了一条：假设之间必须一致。
- 结果与学到：49 道题全部通过验收，两道因为设计实质问题重做，四条教训写进了指令文件。模型的笃定程度说明不了任何事，算术很便宜，所以交给机器检查。

<span class="label">英文口述（60–90 秒）</span>

I'm building a system-design study bank, about fifty problems drafted by Claude Code subagents. A learner memorizes those numbers, so a wrong one is a shipped defect, and I own correctness: the agent drafts, I make sure nothing wrong gets through. On the first pilot problem, the article stated a hash-collision probability of 38 percent. It sounded confident, but I re-derived it with a one-line script, and the real answer was certainty. The exponent was off by six orders of magnitude. The wrong figure was already in a flashcard, so I fixed the article first, then the card. Then I stopped treating it as one bug and wrote a rule into the shared agent instructions: every number is computed, never recalled, and a number you couldn't verify never goes into a card. Later, a second article had correct arithmetic on two contradicting assumptions, a 1,560x peak ratio, so I added a rule that assumptions must agree with each other. All 49 problems passed the gate, two were redone for design substance, and four lessons now live in the instruction file. The takeaway: a model's confidence tells you nothing, and arithmetic is cheap, so check it by machine.

<div class="sources"><b>表达 · business English</b><br>• <b><i>shipped defect</i></b> — 已经交付到用户手里的缺陷<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Learners memorize these numbers, so a wrong one is a shipped defect.”</span><br>• <b><i>own correctness end to end</i></b> — 对正确性端到端负责<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The agent drafts, but I own correctness end to end.”</span><br>• <b><i>off by orders of magnitude</i></b> — 差了好几个数量级<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The article&#x27;s collision figure was off by six orders of magnitude.”</span></div>
