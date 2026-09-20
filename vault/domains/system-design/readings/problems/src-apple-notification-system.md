---
nodes: [problems.social.notification-system]
url: https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html
---
# Communicating with APNs

值得读：APNs 官方文档，给出推送通知的权威限制和语义——payload 大小上限（常规 4 KB，
VoIP 5 KB）、`apns-priority`/`apns-expiration`/`apns-collapse-id` 头的确切行为、以及
`410 Unregistered`、`429 TooManyRequests` 等错误码的含义。比其他二手资料更精确的地方
在于它明确区分了"立即发送"和"省电发送"两档优先级的强制要求（priority=10 且只有
content-available 会报错），本题解的提供商错误语义归一化直接对照这些官方错误码设计。

%% trellis:begin %%
## Source
[Open the original ↗](https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html)

## Archived copy
![[src-apple-notification-system-clip]]
%% trellis:end %%
