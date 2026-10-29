---
id: tlc-tt-chat-message-window-merge-4-followup
node: b.tt-chat-message-window-merge
type: qa
step: 4
---
## Q
**聊天消息窗口合并（get_chat_messages）**｜追问

面试官接着问：（1）合并后的消息之间如果有空洞（两个窗口不相连），要能看出来；（2）消息 `id` 并不连续（有消息被删除）；（3）调用 `get_chat_messages` 很贵，怎样少调几次？

## A
1. **标出空洞**：先用 `merge_windows`（按 `id` 归并并去重，返回升序列表）得到合并结果，再顺序扫描，当前消息的 `id` 不等于上一条的 `id + 1` 就开一段新的，返回连续的若干段。

```python
def merge_into_segments(windows: list[list[Message]]) -> list[list[Message]]:
    segments: list[list[Message]] = []
    for msg in merge_windows(windows):
        if segments and msg["id"] == segments[-1][-1]["id"] + 1:
            segments[-1].append(msg)          # 紧接着上一条：同一段
        else:
            segments.append([msg])            # 有空洞：另起一段
    return segments
```

会话 `id` 为 `100` 到 `129`，中心 `103`、`108`、`125` 的窗口 → 两段，分别是 `100..113` 和 `120..129`。
2. **`id` 不连续**：`id + 1` 不再表示「相邻」。改成对每个窗口的 `[首 id, 末 id]` 做区间合并（LC 56）：两个窗口的区间重叠就属于同一段，不重叠就有空洞；窗口是接口返回的，窗口内部不会漏消息。
3. **少调接口**：把待查的中心 `id` 排序，维护已覆盖的最右边界；中心已经落在已覆盖范围里的，就不必再调用；重复的中心先用集合去掉。并发调用时，各窗口互相独立，可以并行拿到再合并。

**Python 提醒**：`heapq.merge` 返回的是一次性的惰性迭代器，不能遍历两次；需要多次使用时先 `list()`。上面 `merge_into_segments` 里 `merge_windows` 已经返回列表，所以安全。
