---
id: hi-sd-dropbox-10-security
node: sd.problem-breakdowns.dropbox
type: qa
step: 10
---
## Q
**Dropbox：文件安全**｜系统设计 · 问题拆解

Dropbox 的文件安全要考虑哪几层？授权用户把下载链接发到公开论坛怎么办？

## A
**三层。**
- 传输加密：全程 HTTPS
- 静态加密：S3 服务端加密，每个对象用独立密钥，密钥与文件分开存放
- 访问控制：sharelist 或分享表就是基本 ACL，只给有权限的用户发下载链接

**链接泄露。** 用有效期很短（如 5 分钟）的签名 URL。CloudFront 的做法是：服务器用私钥签名，签名里包含路径、过期时间和可选限制，分发给授权用户；CDN 收到请求后用已注册的公钥验证签名和过期时间，合法才返回内容。

**易错。** 签名 URL 本质是持有者令牌（bearer token），谁拿到有效 URL 谁就能下载，短有效期只是限制暴露窗口。更高安全要求可再加 IP 绑定，或要求同时带认证 Cookie。
