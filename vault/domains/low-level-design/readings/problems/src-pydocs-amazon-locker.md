---
nodes: [problems.machines.amazon-locker]
url: https://docs.python.org/3/library/secrets.html
---
# secrets — 生成安全随机数用于管理密钥

值得读：一页文档撑起这道题里最容易被轻描淡写带过的一处。文档开篇就写明 `secrets` 应当优先
于 `random` 用于"密码、账号认证、安全令牌和相关机密"——取件码正是这样的用途：它是持有即
凭证，猜中了就能打开一个装着别人包裹的柜门。而 `random` 背后的 Mersenne Twister 是可预测的，
观察到足够多输出就能反推内部状态，文档自己在 `random` 那一页也写了"不应用于安全目的"。
本题解用 `secrets.choice` 从 31 个去掉了 0/O/1/I/L 的字符里取 8 位——可读性也是安全性的一
部分，让人在小键盘上输错的码是白白消耗的爆破额度。同页的 `secrets.token_hex` 和
`compare_digest` 在"把码哈希后落库"那一步会用上。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/secrets.html)

## Archived copy
![[src-pydocs-amazon-locker-clip]]
%% trellis:end %%
