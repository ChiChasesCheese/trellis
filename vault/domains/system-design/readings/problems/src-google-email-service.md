---
nodes: [problems.media.email-service]
url: https://support.google.com/mail/answer/81126
---
# Email sender guidelines — Gmail Help
值得读：Google 官方发布的批量发件人可执行门槛——每天超过 5,000 封信的发件人必须
同时配置 SPF/DKIM/DMARC，Postmaster Tools 举报率必须低于 0.3%（建议 0.1% 以下）。
本题解「深入探讨」第 3 节把这两个数字直接用作入站过滤按信誉分车道的设计输入，
文档本身只是合规清单，没有给出"信誉是连续变量、决定检查强度"这一层设计推理。

%% trellis:begin %%
## Source
[Open the original ↗](https://support.google.com/mail/answer/81126)

## Archived copy
![[src-google-email-service-clip]]
%% trellis:end %%
