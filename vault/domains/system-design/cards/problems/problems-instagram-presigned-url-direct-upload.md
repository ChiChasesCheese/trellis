---
id: problems-instagram-presigned-url-direct-upload
node: problems.social.instagram
type: qa
step: 2
tags: [grown]
---
## Q
In a photo/video sharing app's upload path, why does routing every upload through the application server (client uploads to app server, app server forwards to object storage) waste resources compared to using pre-signed URLs for direct client-to-object-store upload?

## A
Proxying uploads through the application server means every media byte is received once and forwarded again, so the application tier's compute fleet has to be sized to absorb upload bandwidth even though that work is pure byte-forwarding, not business logic. With pre-signed URLs, the application server only issues a short-lived, scoped credential (valid for one specific object key and a limited time window) and the client uploads chunks directly to the object store, so the application tier's scaling is decoupled from upload bandwidth entirely, while the credential's narrow scope avoids the security risk of handing out long-lived storage credentials.

## Q zh
在一个图片/视频分享应用的上传路径中，为什么让每次上传都经过应用服务器（客户端上传到应用服务器，应用服务器再转发到对象存储）比用预签名 URL（pre-signed URL）让客户端直接上传到对象存储更浪费资源？

## A zh
通过应用服务器代理上传意味着每一个媒体字节都要被接收一次、再转发一次，导致应用层的计算集群必须按上传带宽来配置容量，即使这部分工作只是纯粹的字节转发，不是业务逻辑。用预签名 URL 时，应用服务器只签发一个限时、限权限（只对某一个具体的对象 key 生效）的凭证，客户端直接向对象存储分片上传，应用层的扩容完全和上传带宽解耦；凭证权限范围窄，也避免了发放长期存储凭证带来的安全风险。
