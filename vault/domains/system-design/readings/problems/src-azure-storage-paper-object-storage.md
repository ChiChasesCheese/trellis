---
nodes: [problems.foundations.object-storage]
url: https://azure.microsoft.com/en-us/blog/sosp-paper-windows-azure-storage-a-highly-available-cloud-storage-service-with-strong-consistency/
tags: []
---
# Windows Azure Storage: A Highly Available Cloud Storage Service with Strong Consistency

值得读：SOSP 2011 论文（及其 2012 年 USENIX ATC 的纠删码后续篇）第一手描述了
Partition Layer（可扩展索引、事务顺序、强一致性）与 Stream Layer（数据复制、
按存储块流管理容错）的分层，以及局部重构码（LRC）用局部校验降低单分片重建读放大
的设计。题解「深入探讨」第 1 节的元数据-数据分离和第 3 节 LRC(12,2,2) 的存储倍数
计算（16/12 ≈ 1.33×）都以此为依据，但没有采用论文里完整的容错域（fault domain）
与升级域（upgrade domain）布局细节，是一个简化版本。

%% trellis:begin %%
## Source
[Open the original ↗](https://azure.microsoft.com/en-us/blog/sosp-paper-windows-azure-storage-a-highly-available-cloud-storage-service-with-strong-consistency/)
%% trellis:end %%
