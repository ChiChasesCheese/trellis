---
id: amz-rate-limiter-what-and-three-questions
node: amazon.amz-rate-limiter
type: qa
step: 1
tags: [grown]
---
## Q
限流器（Rate Limiter）要你设计什么？开场先问哪三个澄清问题？

## A
限流器在请求进来时判断「这个调用方此刻还能不能放行」，超额就拒绝。三问：(1) 按什么维度限（用户、IP、接口）——决定状态的 key；(2) 单进程还是多机共享额度——决定状态放内存还是外部存储；(3) 被拒时只回 bool，还是要回剩余额度和多久后重试——决定返回值是 `Decision` 而不是裸 bool。
