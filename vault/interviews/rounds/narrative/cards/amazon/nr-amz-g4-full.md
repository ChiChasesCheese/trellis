---
id: nr-amz-g4-full
node: amazon.full
type: qa
step: 19
---
## Q
<p class="title">什么时候信任 LLM<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：并行跑了几个月的代理之后，我需要一条比「感觉对」更好的规则。
- 目标：针对每个任务决定该信任输出到什么程度，并且写下来。
- 我做了什么：规则有两个输入，一是有没有 oracle（编译器、测试、可重跑的脚本），二是错了的代价有多大。有 oracle 且爆炸半径小，我信任并用机器验证，比如有绿测试保护的重构、脚手架、必须能编译的示例。
- 没有 oracle 时我不信任数字、关于外部系统的论断和二手信息；有个例子是代理把一个数字标成「官方披露」，实际只来自一个备考网站。代价高的代码，比如涉及钱的代码，无论如何我都读每一个 diff。盲区是「合理假设上的错误结论」，闸门只查形状，只有阅读才查实质，所以我先读代理自己列的「最不确定」清单。
- 结果与学到：缺陷在闸门或评审时暴露，而不是被读者发现；例如编译了所有教材示例后抓到了一个根本编译不过的 Java 例子。信任是模型周围验证机制的属性，不是模型本身的属性。

<span class="label">英文口述（60–90 秒）</span>

After months of running agents in parallel, I needed a rule better than it feels right. I wanted to decide per task how much to trust the output, and write it down. The rule has two inputs: is there an oracle, like a compiler, a test or a re-runnable script, and what does a wrong answer cost? With an oracle and a low blast radius, I trust and verify by machine: refactors under green tests, scaffolding, examples that must compile. With no oracle, I don't trust numbers, claims about external systems, or anything secondhand. For example, an agent labelled a figure officially disclosed, but it came from a single prep site. For high-cost code, like money code, I read every diff myself regardless. The blind spot is a wrong conclusion on a plausible assumption, because gates check shape and only reading checks substance, so I read the agent's own least-sure list first. As a result, defects surface at the gate or in review, not with the reader. For instance, a Java example that would not compile was caught when I compiled every textbook example. Trust is a property of the verification around the model, not of the model.

<div class="sources"><b>表达 · business English</b><br>• <b><i>blast radius</i></b> — 出错时影响的范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“With a low blast radius and a green test, I trust the agent&#x27;s refactor.”</span><br>• <b><i>trust but verify</i></b> — 信任但要验证<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“With an oracle in place, I trust but verify by machine.”</span><br>• <b><i>secondhand</i></b> — 二手的、非一手来源的<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I don&#x27;t trust anything secondhand without checking the source.”</span></div>
