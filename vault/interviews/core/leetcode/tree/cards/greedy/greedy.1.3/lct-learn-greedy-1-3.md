---
id: lct-learn-greedy-1-3
node: greedy.1.3
type: qa
step: 1
---
## Q
**贪心算法 › 贪心策略 › 双序列配对**｜学习卡

套路是什么？

## A
**一句话。** 两个序列各自排序，用双指针一一配对：小的需求配刚好够的资源，不够的资源丢掉，够了就配对。

下图：LC 455，两边都升序，每块饼干给当前最小的胃口，不够就丢掉。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="14" y="38" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">胃口 g</text>
<rect x="80" y="20" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="105.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="20" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="155.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="180" y="20" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="14" y="118" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">饼干 s</text>
<rect x="80" y="100" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="105.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="100" width="50" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="155.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="180" y="100" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="205.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="105.0" y1="48" x2="105.0" y2="98" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="105.0,48.0 108.0,54.3 102.0,54.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="155.0" y1="48" x2="205.0" y2="98" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="155.0,48.0 161.6,50.4 157.4,54.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="155.0" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不够：丢</text>
<text x="250" y="50" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">都升序</text>
<text x="250" y="66" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">饼干够最小胃口</text>
<text x="250" y="82" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">就配对</text>
</svg>

```python
def find_content_children(g, s):
    g.sort()                         # 胃口升序
    child = 0
    for size in sorted(s):           # 饼干升序
        if child < len(g) and size >= g[child]:
            child += 1               # 这块刚好满足最小胃口
    return child
```

**要点。**
- 为什么对？：最小的胃口都满足不了的饼干，对后面更大的胃口也没用，丢掉；够了就配最小胃口，大饼干留给后面更大的胃口。
- LC 2561 怎么改？：两篮数量差凑成待换列表，只处理较小的一半，每次花 `min(x, 2 * 全局最小值)`（借最便宜的水果中转两次）。

**易错点。**
- 不排序、按输入顺序发：`g = [1,2]`、`s = [2,1]` 时大饼干被小胃口拿走，得 `1`，应为 `2`。
- LC 2561 忘了借中转：`[100,100,1]` 与 `[200,200,1]` 借 `1` 换两次只花 `2`，直接换花 `100`。
- LC 2561 累加了待换列表的全部元素：一次交换同时解决两个水果，只取较小的一半。

**对应题目。** LC 455 分发饼干、LC 2561 重排水果
