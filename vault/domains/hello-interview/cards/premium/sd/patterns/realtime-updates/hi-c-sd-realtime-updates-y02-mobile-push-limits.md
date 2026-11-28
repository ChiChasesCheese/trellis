---
id: hi-c-sd-realtime-updates-y02-mobile-push-limits
node: sd.patterns.realtime-updates.beyond
type: qa
step: 6
---
## Q
**实时更新 · 系统推送靠不住的地方：存储合并、静默推送限流、令牌失效**｜拓展 · 追问

用户关机两天，期间来了 50 条消息，各推送一次。开机后他会收到几条通知？静默推送（background push）能保证把 App 叫醒去同步吗？推送服务返回令牌无效，或者限流，该怎么处理？

## A
**一句话。** 设备离线时，APNs 对每个 App 只存一条通知（通常是最新的），FCM 对不可折叠消息最多存 100 条、超出就全部丢弃；静默推送被系统当作低优先级，可能被限流、延迟甚至不送；所以推送只能当"门铃"，真正的消息靠 App 上线后按游标同步。令牌失效就删除，限流就退避重试。

**离线期间的存储。**
- **APNs：** 设备离线时，APNs 按 `apns-expiration` 最多存 30 天，但每个 App（bundle ID）只存一条；连续发多条，通常只保留最新那条，且不保证。`apns-expiration: 0` 表示只尝试一次、不存。
- **FCM 可折叠消息：** 带同一个 `collapse_key` 的新消息替换还没送达的旧消息；每台设备同时最多保留 4 个不同的折叠键。通知类消息总是可折叠的。
- **FCM 不可折叠消息：** 每个 App 实例最多为离线设备存 100 条；超过就丢掉全部已存消息，设备重新上线时 SDK 会回调 `onDeletedMessages`，App 应据此做一次全量同步。默认和最长存活时间都是 4 周。
- **合并的写法：** 给同一会话的通知设同一个 `apns-collapse-id`（不超过 64 字节）或 `collapse_key`，内容写"3 条新消息"，而不是每条一个通知。

**静默推送。**
- **iOS 后台通知：** `content-available: 1`、`apns-push-type: background`、优先级必须是 5。系统把它当低优先级，不保证送达，太多会被限流，官方建议每小时不超过两三条；App 被用户强制退出后，系统丢弃挂起的后台通知。
- **iOS 可见通知加扩展：** 需要在显示前取数据或解密时，发可见通知并设 `mutable-content: 1`，由通知服务扩展（Notification Service Extension）在约 30 秒内改写内容；它只对会显示提醒的通知生效。
- **Android：** FCM 高优先级可以把休眠（Doze）中的设备叫醒；如果高优先级消息总是不产生用户可见的通知，FCM 会降低这个 App 的优先级。

**错误处理。**
- **令牌无效：** APNs 返回 410（`Unregistered`，令牌不再对这个主题有效），FCM 返回 `UNREGISTERED`（404）。删除这个令牌，不要再发。
- **限流和服务端错误：** FCM 的 `QUOTA_EXCEEDED`（429）要指数退避，初始至少 1 分钟；`UNAVAILABLE`（503）要遵守 `Retry-After` 并退避。
- **重复：** 推送服务自己的重试可能让同一通知到两次；用 collapse ID 让重复的通知互相替换。

**面试里这样说。** 「离线设备我只发一个带会话 ID 的可见通知，用 collapse ID 合并；推送可能被合并、丢弃或延迟，所以 App 上线后按游标从收件箱补齐。410 和 UNREGISTERED 就删令牌。」
