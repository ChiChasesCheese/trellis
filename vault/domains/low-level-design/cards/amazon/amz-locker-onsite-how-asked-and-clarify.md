---
id: amz-locker-onsite-how-asked-and-clarify
node: amazon.amz-locker-onsite
type: qa
step: 1
tags: [grown]
---
## Q
快递柜（Amazon Locker）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是一个放在街角的自助取件柜：快递员把包裹投进尺寸合适的空柜格，系统发一个取件码，收件人凭码取走，码过期后柜格要能收回。代码常常只写在记事本上、不运行，靠手工推演（dry run，在纸上逐行走一遍）验证。三问：(1) 柜格尺寸是固定档位还是以后会加；(2) 取件码多久过期、过期后包裹去哪；(3) 一个网点还是多个，是否多快递员并发。
