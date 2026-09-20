---
id: problems-google-docs-interleaving-anomaly-stable-anchor
node: problems.media.google-docs
type: qa
step: 5
tags: [grown]
---
## Q
In a rich-text collaborative editor, what is the 'interleaving anomaly,' and how does anchoring formatting spans to stable per-character identifiers (instead of numeric offsets) help avoid both it and incorrect format-inheritance at span boundaries?

## A
The interleaving anomaly happens when two users concurrently insert separate runs of text at the same position, and a naive character-by-character merge scrambles the two runs together instead of keeping each run contiguous. Anchoring a formatting span (e.g. bold) to the stable identifiers of its first and last characters, rather than to numeric positions that shift with every concurrent edit, lets insertions and deletions simply move or shrink the span's endpoints without corrupting run ordering, and lets each format declare whether typing at its boundary should extend the span (bold continuing) or not (a hyperlink or comment not silently absorbing new text).

## Q zh
在富文本协同编辑器中，什么是「交错异常」（interleaving anomaly），把格式区间锚定到稳定的逐字符标识（而不是数值偏移量）如何同时避免这个异常和区间边界处错误的格式继承？

## A zh
交错异常指的是两个用户并发在同一位置各自插入一段连续文字时，简单的逐字符合并会把两段文字错误地拆散、交替穿插在一起，而不是让每一段保持连续。把一个格式区间（如加粗）锚定到其首尾字符的稳定标识，而不是随每次并发编辑都会变动的数值位置，就能让插入/删除只需要平移或收缩区间端点而不会打乱两段文字的顺序，并且让每种格式能声明在其边界处续写是否应该扩展该区间（加粗应续写扩展，超链接或评论不应默默吸收新输入的文字）。
