---
id: tlc-tt-chat-message-window-merge-0-whole
node: b.tt-chat-message-window-merge
type: qa
---
## Q
**聊天消息窗口合并（get_chat_messages）**｜Medium · TikTok 高频

已有函数 `get_chat_messages(chat_message_id)`：传入一个聊天消息 ID，返回以该消息为中心、上下各 `5` 条（含它自己，所以最多 `11` 条，靠近会话开头或结尾时不足）、按消息顺序排列的消息列表。对多个消息 ID 各调用一次，得到多段可能重叠的结果。写函数 `merge_windows(windows)`，把这些响应合并成一个按消息顺序排列、不重复的消息列表。消息是字典 `{"id": int, "text": str}`，`id` 随消息先后严格递增，同一个 `id` 对应同一条消息；每个窗口内部已按 `id` 升序；窗口之间可能重叠、相邻、不相交，同一个窗口也可能出现多次。窗口数不超过 `10^4`，所有窗口的消息总数不超过 `1.1 * 10^5`。例：会话 `id` 为 `100` 到 `129`，以 `103`、`108`、`125`、`108` 为中心的四个窗口 → 合并后是 `100` 到 `113` 以及 `120` 到 `129`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每个窗口本来就有序，用 `heapq.merge` 按 `id` 做 `k` 路归并，得到全局有序的流；同一条消息的副本在流里必然相邻，再用 `itertools.groupby` 按 `id` 分组，每组只取第一条。`O(N log k)` 时间，归并本身是惰性的。

**识别。** 「多个有序序列合并成一个」是 `k` 路归并（LC 23、LC 88 的思路）；「重叠、重复」不需要区间运算，只要按唯一的 `id` 去重；排序依据是 `id`，所以窗口之间的相对次序没有任何意义，不能按窗口出现的顺序拼接。

**推导。** 暴力：把所有消息放进 `dict`（`id -> 消息`）去重，再按 `id` 排序，`O(N log N)`，简单可靠，也是正确的备选 → 浪费：输入已经是 `k` 段有序序列，全部重排丢掉了这个信息 → 洞察：`heapq.merge` 每次只比较各窗口当前的队头，`O(N log k)`；归并输出按 `id` 有序，重复的 `id` 一定相邻，用 `groupby` 一遍过滤即可，不需要额外的集合。

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

运行：上面的例子 → `id` 依次为 `100, 101, ..., 113, 120, 121, ..., 129`（共 `24` 条）；`[]` → `[]`；`[[]]` → `[]`；只有一个窗口 `[100..105]`（中心是会话第一条）→ 原样返回。

**复杂度。** 时间 `O(N log k)`，`N` 为消息总数，`k` 为窗口数；除结果外额外空间 `O(k)`（堆里每个窗口一个队头）。

**易错点。**
- 窗口顺序不等于消息顺序：按窗口出现的次序拼接并去重，`[窗口(125), 窗口(103)]` 会得到 `120..129` 在前、`100..108` 在后，顺序是错的。
- 拼接后只用 `groupby` 去重：它只合并相邻的相同键。`[窗口(108), 窗口(103)]` 拼接后 `103..113` 之后跟着 `100..108`，`103..108` 重复出现。必须先归并成有序流再去重。
- `heapq.merge` 不传 `key`：消息是字典，字典之间不能比较大小，抛 `TypeError: '<' not supported between instances of 'dict' and 'dict'`。

**追问。**
- 需要标出窗口之间的空洞：合并后再扫一遍，`id` 与前一条的 `id + 1` 不相等就开新的一段，返回 `list[list[Message]]`。
- `id` 不连续（有消息被删除）：不能用 `id + 1` 判断相邻，改成对每个窗口的 `[首 id, 末 id]` 做区间合并（LC 56）。
- 减少接口调用：把待查的中心 `id` 排序，若某个中心已经落在前一个窗口覆盖的范围里，就不必再调用 `get_chat_messages`。

**同模式。** LC 56 合并区间、LC 88 合并两个有序数组、LC 23 合并 K 个升序链表、LC 986 区间列表的交集、LC 57 插入区间。
