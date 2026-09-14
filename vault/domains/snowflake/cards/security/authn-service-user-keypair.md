---
id: authn-service-user-keypair
node: security.authn-mfa-sso
type: qa
tags: [grown]
---
## Q
一个 ETL 程序需要每晚无人值守地连接 Snowflake。为什么不该给它用“用户名 + 密码 + MFA（多因素认证）”，而应该用密钥对认证（key-pair authentication）？

## A
MFA 需要人去手机上确认推送或输入验证码，自动化程序无法完成这一步；而把密码写进配置又容易泄露，且密码可被拿去交互式登录。密钥对认证是给用户注册一个 RSA 公钥，客户端用本地私钥对一个短期 JWT（JSON Web Token）签名来证明身份：服务端只存公钥，私钥从不上网传输，也不需要人参与，因此适合机器人账号。
