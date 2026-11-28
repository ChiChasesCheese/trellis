---
id: hi-c-sd-fb-live-comments-b04-reconnect-merge
node: sd.problem-breakdowns.fb-live-comments.beyond
type: qa
step: 4
---
## Q
**Facebook 直播评论 · 断线补发：合并 HTTP 补拉与实时流**｜拓展 · 加分

重连时同时有一份 HTTP 补拉的历史和一条新建立的实时流，两边有重叠，怎么合并才不重复也不漏？

## A
```python
from typing import Iterable

def merge_streams(last_id: str, catchup: Iterable[tuple[str, str]], live: Iterable[tuple[str, str]], limit: int = 100) -> list[tuple[str, str]]:
    # 评论 ID 可按时间排序：补拉和实时流里同一个 ID 只保留一份，丢掉 last_id 及更早的
    merged: dict[str, str] = {}
    for cid, text in list(catchup) + list(live):
        if cid > last_id:
            merged[cid] = text
    return sorted(merged.items())[-limit:]   # 有界回放：只保留最近 limit 条
```
- **顺序很重要：** 先建立 SSE 并把到达的事件暂存起来，再发 HTTP 补拉；两者都完成后合并。如果先补拉再建流，两步之间到达的评论既不在补拉结果里，也没被流收到，就会出现空洞。
- **验证：** 上次看到 c04，补拉得到 c05–c07，实时流里有 c07 和 c08，合并结果是 c05 到 c08，每条一份；上次看到 c07 则只剩 c08；限制 2 条时只留 c07、c08。
- **前提：** 评论 ID 全序且与发布时间一致（如 ULID、雪花 ID），否则字符串比较无法判断先后。
- **有界回放的取舍：** 超过上限就丢最旧的并提示"你错过了更多"，不要为了完整而把几千条灌给客户端。
- **模式。** 先订阅后补拉：先让增量通道开始缓冲，再读取快照，最后按 ID 合并，才能不漏不重。
