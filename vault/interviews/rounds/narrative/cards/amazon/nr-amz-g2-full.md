---
id: nr-amz-g2-full
node: amazon.full
type: qa
step: 17
---
## Q
<p class="title">不依赖 agent 自述的正确性<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：我用并行的 Claude Code subagent做了约 100 份面试准备材料：49 道系统设计题和 45 道低层设计题。一个给自己打分的模型每次都会说「完成了」。
- 目标：让正确性不取决于代理自己怎么说，并且在代理数量增加时不需要我把所有东西重读一遍。
- 我否决了什么：我否决了「自述加抽查」，也否决了「代理互相审查」，因为有个代理自己又拉起了审查代理，破了我的并发上限，于是「不许再启动别的代理」成了规则。每个代理只负责一个目录，同时最多三个。
- 我做了什么：先于任何内容写好验收命令，参考解必须通过，空模板必须失败。每次返回后我自己重跑验收、重算每个数字、先读代理列出的最弱论断，每个缺陷都变成一条规则。后来为了测试这些测试，我用了变异：一道题里拼接 key 的 bug 通过了全部 10 个测试，我补上了缺失的断言，现在测试套件能杀掉 11 个手写变异中的 11 个。
- 结果与学到：45 道低层设计题全部通过，约 900 个测试，九份草稿返工。验证必须是机制，而不是一种心情。

<span class="label">英文口述（60–90 秒）</span>

I produced about a hundred interview-prep artifacts, 49 system-design and 45 low-level-design problems, using parallel Claude Code subagents. A model that grades its own work says done every time, so I had to make correctness independent of the agent's word, and make it scale without me re-reading everything. I rejected self-reports plus a spot check. One agent owns one directory, three at a time. I wrote the acceptance gate as a command before any content: the reference solution must pass and the empty starter must fail. I also rejected agents reviewing agents, because one spawned a reviewer and broke my cap, so never start another agent became a rule. After each return I re-run the gate myself, re-derive every number, and read the agent's weakest-claims list, and every defect becomes a rule. Later, to test the tests, I used mutation: on one kata, a concatenated-key bug passed all ten tests. I added the missing assertion, and the suite now kills 11 of 11 hand-written mutants. All 45 low-level-design problems and about 900 tests passed, and nine drafts went back for rework. Verification has to be a mechanism, not a mood.

<div class="sources"><b>表达 · business English</b><br>• <b><i>independent of the agent&#x27;s word</i></b> — 不依赖代理自己的说法<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I made correctness independent of the agent&#x27;s word.”</span><br>• <b><i>mechanism, not a mood</i></b> — 是机制而不是感觉<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Verification has to be a mechanism, not a mood.”</span><br>• <b><i>scale without re-reading</i></b> — 扩展规模而不用重读全部<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The design had to scale without me re-reading everything.”</span></div>
