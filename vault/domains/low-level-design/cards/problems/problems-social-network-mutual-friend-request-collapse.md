---
id: problems-social-network-mutual-friend-request-collapse
node: problems.social.social-network
type: qa
step: 2
tags: [grown]
---
## Q
社交网络里，如果 A 给 B 发了一条待处理的好友请求，此后 B 也主动给 A 发一条好友请求，第二条请求应该怎么处理？

## A
直接让它生效，两人立刻成为好友，而不是留下两条互相矛盾的待处理请求。判断依据：两个方向的意愿本来就一致——A 想加 B、B 也想加 A——没有理由制造一次多余的“请再确认一下”。实现上是 `send_friend_request` 先查有没有反方向的待处理请求，有就直接走接受流程：
```python
mirror = self._pending_request(to_id, from_id)
if mirror is not None:
    self._accept(mirror)
    return mirror
```
这条不变量必须被测试覆盖，否则很容易实现成“各自留一条待处理请求”，用户体验上会显得系统没有反应。
