---
id: delivery-aws-origin-access
node: delivery.aws
type: qa
---
## Q
CloudFront serves private S3 content correctly, but the S3 object URL is publicly reachable. What boundary is broken?

## A
The origin is exposed, so clients can bypass CDN authorization, logging, rate limits, and signed delivery. Make the bucket private, grant the distribution's origin access identity/control only the required actions and prefixes, block public access, and test direct-origin denial. Edge protection is not a security boundary if the origin remains public.

## Q zh
CloudFront 正确提供 private S3 content，但 S3 object URL 可被公开访问。哪个 boundary 被破坏？

## A zh
origin 已暴露，因此 client 可以绕过 CDN authorization、logging、rate limit 和 signed delivery。应把 bucket 设为 private，只向 distribution 的 origin access identity/control 授予必要 action 和 prefix，block public access，并测试 direct-origin denial。如果 origin 仍公开，edge protection 就不是 security boundary。
