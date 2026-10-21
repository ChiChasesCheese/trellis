---
id: nr-amz-s9-senior-2
node: amazon.followups
type: qa
step: 43
---
## Q
<p class="title">Amex 出款延迟事故<span class="meta">03 senior 追问</span></p>

*"Why not revert the effective-date change, given that it was the fastest way to stop the bleeding?"*

## A
<span class="label">面试官在探</span> 面试官在探：你怎么权衡速度、风险和长期正确性，而不是只追快。

<span class="label">回答框架</span>

- 先承认 revert 的优势：最快、改动面最小
- 再说它的代价：会把为 EU 合规做的改动一并撤掉，合规风险回来
- region 条件让 EU 与 US 语义独立，修的是真正的原因
- 代价是 UDTF 里多一个分支和对应测试，我会明说并补上覆盖

<span class="label">为什么这是最佳实践</span>

revert 把两个本来独立的需求绑在一起：撤销 US 的错误，同时撤销 EU 的合规。事故里的快路径如果制造新的合规风险，就不是真正的快。条件分支让每个区域有自己的语义，今后再改一边不会牵动另一边；代价是多一个分支，所以必须配测试，这是一个有意识的取舍。

<div class="sources"><b>表达 · business English</b><br>• <b><i>blast radius</i></b> — 影响范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A revert had a bigger blast radius because it also undid the EU compliance work.”</span><br>• <b><i>decouple</i></b> — 解耦<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The region conditional decouples EU and US behavior.”</span></div>
