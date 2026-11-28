---
id: hi-c-sd-large-blobs-x02-who-validates
node: sd.patterns.large-blobs.exam
type: qa
step: 2
---
## Q
**大文件 · 谁来验证签名**｜考点 · 必会

S3 预签名 URL 和 CloudFront 签名 URL 在验证方式上有什么本质区别？

## A
- **S3 预签名：** 存储服务用它持有的、你的云凭证重新计算签名并比较。
- **CloudFront 签名：** 你持私钥签名，边缘节点用对应公钥在本地验证，不用回源或回调你的服务器。
- **意义：** CDN 的校验可以发生在全球任意边缘节点，没有额外往返。
- **使用提示：** 通过 CDN 分发时要签的是 CDN URL，而不是存储 URL。
