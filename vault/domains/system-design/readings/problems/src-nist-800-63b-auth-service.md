---
nodes: [problems.foundations.auth-service]
url: https://pages.nist.gov/800-63-3/sp800-63b.html
tags: [reference]
---
# NIST SP 800-63B — Digital Identity Guidelines: Authentication and Lifecycle Management

值得读：美国 NIST 官方数字身份指南，要求验证方把连续失败登录尝试限制在不超过 100
次，并给出指数级退避（30 秒到一小时）、IP 白名单、风险自适应认证等补充手段；同时
明确反对传统的密码复杂度强制规则，只在检测到凭证已泄露的证据时才要求改密码。本题
解「深入探讨」第 4 节的登录防滥用设计比这份文档更进一步的地方在于：它把"单账号限
流"本身论证为对撞库（credential stuffing）无效，需要舰队级信号作为主要防线，而不
是把账号级失败次数上限当作唯一防护手段。

%% trellis:begin %%
## Source
[Open the original ↗](https://pages.nist.gov/800-63-3/sp800-63b.html)

## Archived copy
![[src-nist-800-63b-auth-service-clip]]
%% trellis:end %%
