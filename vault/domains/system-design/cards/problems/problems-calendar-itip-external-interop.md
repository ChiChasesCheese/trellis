---
id: problems-calendar-itip-external-interop
node: problems.realtime.calendar
type: qa
step: 6
tags: [grown]
---
## Q
When a calendar system's organizer invites an attendee whose email belongs to a completely different calendar product, why does sending a standard iTIP object (RFC 5546, `METHOD:REQUEST`) over email or CalDAV work better than building a bespoke integration with that other product, and how does an organizer's later edit (e.g. changing the meeting time) get recognized as an update rather than a brand-new invitation?

## A
A standard iTIP object is understood by any compliant calendar client, so the inviting system never needs to know anything about the recipient's backend implementation — it only needs to correctly produce and parse one open format, turning an N-way integration problem (one integration per external product) into a single protocol implementation. When the organizer edits the event, the system resends a `REQUEST` with an incremented `SEQUENCE` property; the recipient's client compares this to the sequence number it already has and recognizes it as an update to the existing invitation rather than a separate new one.

## Q zh
当日历系统的组织者邀请一个使用完全不同日历产品的参会人时，为什么通过邮件或 CalDAV 发送标准 iTIP 对象（RFC 5546，`METHOD:REQUEST`）比为那个其他产品单独构建定制集成更好？组织者之后的编辑（比如改会议时间）是如何被识别成「更新」而不是一次全新邀请的？

## A zh
标准 iTIP 对象能被任何符合规范的日历客户端理解，所以发起邀请的系统完全不需要了解接收方后端的实现细节——它只需要正确生成和解析一种开放格式，把一个「N 个外部产品对应 N 次集成」的问题，变成「只需要实现一套协议」的问题。组织者编辑事件时，系统重新发送一个 `SEQUENCE` 属性递增的 `REQUEST`；接收方客户端把这个值和自己已有的序号比较，识别出这是对已有邀请的更新，而不是一次独立的新邀请。
