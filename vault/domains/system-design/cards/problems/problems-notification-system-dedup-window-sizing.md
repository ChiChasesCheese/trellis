---
id: problems-notification-system-dedup-window-sizing
node: problems.social.notification-system
type: qa
step: 4
tags: [grown]
---
## Q
How should the retention window for a notification system's dedup records be sized, and given that Twilio documents messages can sit in its per-account queue for up to 10 hours before being dropped, what dedup window does that imply?

## A
The dedup retention window must exceed the longest retry or queuing delay of every downstream hop that could resend the same logical notification — otherwise a legitimate delayed retry arrives after the dedup record has expired and is treated as new, producing a duplicate send. With Twilio's documented 10-hour maximum message-queue retention as the longest known downstream window, a dedup window of at least 11 hours (10 hours plus a 1-hour safety margin) is needed; sizing it to a shorter, arbitrary value like 1 hour would let a legitimately delayed SMS retry slip through as an undeduplicated duplicate.

## Q zh
通知系统去重记录的保留窗口应该怎么定size？已知 Twilio 文档说明消息在其账号级队列里最长可保留 10 小时才会被丢弃，这意味着去重窗口应该是多少？

## A zh
去重保留窗口必须超过所有可能重发同一条逻辑通知的下游环节里最长的重试/排队延迟——否则一次合法的延迟重试会在去重记录过期之后才到达，被当作新请求处理，产生重复发送。以 Twilio 文档记载的 10 小时账号级消息队列最长保留时长作为已知最长的下游窗口，去重窗口至少需要 11 小时（10 小时加 1 小时安全余量）；如果把它定成更短的任意值（比如 1 小时），一次合法的延迟短信重试就会绕过去重、造成重复。
