---
id: problems-email-service-spam-classifier-fail-open
node: problems.media.email-service
type: qa
step: 6
tags: [grown]
---
## Q
An email service runs spam/phishing classification as an asynchronous second stage after a message is already accepted at the SMTP edge. If that async classifier becomes unavailable, should the design fail open (deliver messages to the inbox unfiltered until it recovers) or fail closed (hold or reject messages until it recovers), and why?

## A
The design should fail open. Failing closed would mean either rejecting or indefinitely holding legitimate mail whenever the classifier is down, which directly violates the inbound path's availability target — a sender's message being bounced or stuck because of an unrelated internal component outage is a worse outcome than a temporary reduction in spam-filtering accuracy. Failing open only degrades one property (some spam or phishing that would have been caught temporarily reaches the inbox instead of the spam folder) and that degradation is recoverable after the fact: once the classifier is back, messages that were delivered during the outage can be re-scored and retroactively moved into the spam folder, while a bounced legitimate email cannot be un-bounced.

## Q zh
一个邮件服务把垃圾/钓鱼邮件分类放在消息已经被 SMTP 边缘接受之后的异步第二阶段执行。如果这个异步分类器不可用，设计应该「失败即放行」（分类器恢复前先不过滤地投递到收件箱）还是「失败即拒绝」（分类器恢复前暂扣或拒绝邮件）？为什么？

## A zh
应该选择「失败即放行」。「失败即拒绝」意味着分类器故障期间要么拒收、要么无限期暂扣合法邮件，这直接违反入站路径的可用性目标——一个发件人的邮件因为一个与它无关的内部组件故障而被退信或卡住，是比「垃圾邮件过滤准确率暂时下降」更差的结果。「失败即放行」只会降级一个属性（分类器故障期间，一部分本该被拦截的垃圾/钓鱼邮件暂时进了收件箱而不是垃圾邮件文件夹），而且这个降级是事后可挽回的：分类器恢复后，可以对故障期间投递的邮件重新打分，把判定为垃圾的信事后移入垃圾邮件文件夹；但一封被退信的合法邮件无法被撤回退信。
