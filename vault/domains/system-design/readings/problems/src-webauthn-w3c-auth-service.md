---
nodes: [problems.foundations.auth-service]
url: https://www.w3.org/TR/webauthn-3/
tags: [reference]
---
# Web Authentication: An API for accessing Public Key Credentials Level 3

值得读：W3C 官方 WebAuthn 规范，规定公钥凭证按 RP ID 严格限定作用域（只有注册时的
那个 RP 能在认证仪式中使用该凭证），并说明签名计数器（signature counter）机制在
同步（synced）多设备凭证下的克隆检测语义已经弱化。本题解「深入探讨」第 5 节在此
基础上补充了这道题规模特有的落地约束——RP ID 必须选可注册域后缀（如
`example.com` 而非 `app.example.com`），因为几亿账号规模下一旦选错域名归属，事
后无法批量迁移已注册的 passkey。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.w3.org/TR/webauthn-3/)
%% trellis:end %%
