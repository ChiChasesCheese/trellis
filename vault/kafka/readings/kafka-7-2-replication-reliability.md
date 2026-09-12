---
nodes:
- reliability.guarantees
title: 复制如何支撑可靠性
corpus: kafka-2e
section: 071-7-2
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 复制如何支撑可靠性

本节从可靠性角度重新审视复制机制，具体列出跟随者副本被判定为同步副本需要满足的时间窗口条件(心跳、复制延迟)，并说明副本减少如何降低有效复制系数、增大数据丢失风险。是把第6章的复制协议与本章可靠性保证联系起来的桥梁。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
