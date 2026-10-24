---
id: tlc-tt-chat-message-window-merge-2-code
node: a.tt-chat-message-window-merge
type: qa
step: 2
---
## Q
**聊天消息窗口合并（get_chat_messages）**｜写出 Python 实现

`windows` 是若干个消息窗口（`list[list[Message]]`，窗口数不超过 `10^4`），消息是 `{"id": int, "text": str}`，每个窗口内按 `id` 升序，不同窗口可能重叠或重复。返回一个按 `id` 升序、每个 `id` 只出现一次的消息列表。

## A
**思路。** 用 `heapq.merge` 按 `id` 把所有窗口归并成一个有序流；重复的消息在流里相邻，用 `groupby` 按 `id` 分组，每组取第一条。

```python
import heapq
from itertools import groupby
from operator import itemgetter
from typing import Any

Message = dict[str, Any]          # {"id": int, "text": str, ...}，窗口内按 id 升序


def merge_windows(windows: list[list[Message]]) -> list[Message]:
    by_id = itemgetter("id")
    merged = heapq.merge(*windows, key=by_id)                    # k 路归并：每个窗口本来就有序
    return [next(group) for _, group in groupby(merged, key=by_id)]   # 相邻同 id 只留第一条
```

运行：中心为 `103`、`108`、`125`、`108` 的四个窗口（会话 `id` 为 `100` 到 `129`）→ `[100, 101, ..., 113, 120, 121, ..., 129]`；`[]` → `[]`；`[[]]` → `[]`；单个窗口 `100..105` → 原样返回。

**复杂度。** 时间 `O(N log k)`；额外空间 `O(k)`（不含结果）。

**写法要点。** `heapq.merge` 的 `key` 参数（Python 3.5 起）让不可比较的字典也能按 `id` 归并，并且是惰性的：一次只推进被选中的那个窗口；相同键的元素按传入窗口的先后稳定输出，所以 `next(group)` 取的是最早出现的那个副本；`groupby` 只合并相邻的相同键，这里恰好利用归并输出有序；`next(group)` 取每组第一个元素，丢弃组内其余；`itemgetter("id")` 比 `lambda m: m["id"]` 更快，也更清楚。
