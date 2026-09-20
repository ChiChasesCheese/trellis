---
nodes: [problems.foundations.object-storage]
url: https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-muralidhar.pdf
tags: []
---
# f4: Facebook's Warm BLOB Storage System

值得读：OSDI 2014 的学术论文，是"用宽纠删码替代三副本，在真实生产规模上到底省
多少存储"这个问题最权威的第一手数据——Reed-Solomon(10,4) 把有效副本倍数从
Haystack 的三副本+RAID-6（3.6×）降到单区域 2.8×、跨区域加 XOR 编码后 2.1×，
报告的部署规模是从 65PB 逻辑数据中省下 53PB 物理存储。题解「深入探讨」第 3 节的
纠删码参数（RS(10,4)）和倍数取自这篇论文，但耐久性概率本身是题解按 Backblaze 的
实测年故障率自行用二项分布计算的简化模型，不是论文里给出的数字，这一点在正文中
明确区分。
