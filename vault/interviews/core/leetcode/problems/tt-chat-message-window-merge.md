---
slug: tt-chat-message-window-merge
---
## Q
**聊天消息窗口合并（get_chat_messages）**｜Medium

多次调用 `get_chat_messages(id)` 得到多个按 `id` 升序、可能重叠的消息窗口（消息是 `{"id": int, "text": str}`）。写 `merge_windows(windows)`，合并成按消息顺序排列、不重复的列表。

## A
**一句话。** 窗口各自有序，用 `heapq.merge` 按 `id` 做 k 路归并，再对相邻同 `id` 的消息只留第一条。

```python
def merge_windows(windows):
    by_id = itemgetter("id")
    merged = heapq.merge(*windows, key=by_id)   # k 路归并
    return [next(g) for _, g in groupby(merged, key=by_id)]
```

**复杂度。** 时间 `O(N log k)`，额外空间 `O(k)`。

**易错点。**
- 按窗口出现次序拼接：`[窗口(125), 窗口(103)]` 会把 `120..129` 排在 `100..108` 前面。
- 拼接后只用 `groupby` 去重：它只合并相邻的相同键，`[窗口(108), 窗口(103)]` 里 `103..108` 重复出现。要先归并成有序流。
- `heapq.merge` 不传 `key`：字典不能比较，抛 `TypeError`。

**追问。**
- 要标出窗口间的空洞？：合并后扫一遍，`id` 不等于前一条 `id + 1` 就开新段。
- `id` 不连续（有消息被删）？：对每个窗口的 `[首 id, 末 id]` 做区间合并（LC 56）。

**同模式。** LC 56 合并区间、LC 88 合并两个有序数组、LC 23 合并 K 个升序链表、LC 986 区间列表的交集
