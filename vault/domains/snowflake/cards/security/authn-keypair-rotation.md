---
id: authn-keypair-rotation
node: security.authn-mfa-sso
type: qa
tags: [grown]
---
## Q
使用密钥对认证（key-pair authentication）的服务账号需要轮换密钥时，怎样做到不中断正在运行的作业？

## A
Snowflake 允许一个用户同时挂两个公钥（`RSA_PUBLIC_KEY` 和 `RSA_PUBLIC_KEY_2`）。轮换时先把新公钥设到空闲的那个槽位，让客户端切换到新私钥，确认都已切换后再清除旧公钥。两把钥匙并存的窗口期内，新旧私钥签发的 JWT 都能通过验证，所以作业不会中断。
