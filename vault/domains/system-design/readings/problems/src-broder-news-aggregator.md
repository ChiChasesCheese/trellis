---
nodes: [problems.search.news-aggregator]
url: https://cs.brown.edu/courses/cs253/papers/nearduplicate.pdf
---
# Identifying and Filtering Near-Duplicate Documents

值得读：Andrei Z. Broder（AltaVista）本人撰写的第一方论文，定义了 shingle（连续词窗口/
q-gram）和用最小独立置换族（min-wise independent permutations）估计 resemblance 的
MinHash 技术，并披露了真实生产经验——用几百字节的"sketch"对超过 3,000 万篇文档做相似度
聚类（50% 以上 resemblance 判定），聚类耗时与 `m log m` 成正比而不是 `m^2`；到 1999 年
中，AltaVista 已经日爬超过 2,000 万页。本题解「深入探讨」第 2 节引用了论文披露的"几百
字节/文档"sketch 体积作为方案一（Shingling+MinHash+LSH banding）的成本基准，并把它和
方案二（SimHash 的 8 字节指纹）做直接对比，得出本设计选择方案二的具体理由——原文本身
没有做这个跨技术的内存占用对比，因为论文写作时 SimHash 技术尚未发表。

%% trellis:begin %%
## Source
[Open the original ↗](https://cs.brown.edu/courses/cs253/papers/nearduplicate.pdf)

## Archived copy
![[src-broder-news-aggregator-clip]]
%% trellis:end %%
