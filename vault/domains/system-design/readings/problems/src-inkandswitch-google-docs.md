---
nodes: [problems.media.google-docs]
url: https://www.inkandswitch.com/peritext/
tags: [paper]
---
# Peritext: A CRDT for Collaborative Rich Text Editing

值得读：Ink & Switch 与剑桥大学合作的学术论文，系统化定义了富文本协同编辑必须处理的"交错
异常"（interleaving anomaly，两个用户并发在同一位置插入一段文字时被错误地按字符交替拆散）
和格式续写语义（粗体在区间末尾续写应扩展、超链接不应扩展），并给出了把格式区间锚定到稳定
字符标识而非数值下标的 CRDT 解法。本题解虽然选择中心化 OT 而非 CRDT 作为主算法，但在「深
入探讨」第 3 节直接借用了这篇论文对交错异常问题的形式化定义，并说明同样的"格式锚定稳定标
识"思路在 OT 实现里同样适用——论文本身只在 CRDT 语境下给出解法，是本题解与它的分歧点。
