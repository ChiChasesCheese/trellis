---
nodes: [problems.search.search-engine]
url: https://www.barroso.org/publications/TheTailAtScale.pdf
---
# The Tail at Scale (Dean & Barroso, CACM 2013)

值得读：Jeff Dean 与 Luiz André Barroso 提出了"扇出放大长尾延迟"的核心模型——一次请求
扇出到 n 个后端，只要任一后端变慢，整体请求就变慢，且这个概率随 n 增长而迅速逼近 1——
以及对冲请求（hedged request）作为缓解手段。本题解在「深入探讨」第 1、2 节直接使用了
这个结构性论点和对冲请求这一机制，但论文原文给出的具体数字示例未能逐字核实（原始 PDF
内容未能完整解析），本题解给出的全部具体数字（32/480 个分片、27.5%/99.2%/4.7% 的长尾
命中概率）都是本题解按自己的分片规模和假设的单分片超时概率重新计算得出，不是照抄论文
里的示例数字。
