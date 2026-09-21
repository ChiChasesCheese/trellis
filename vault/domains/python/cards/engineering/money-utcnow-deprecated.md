---
id: money-utcnow-deprecated
node: engineering.money-time
type: qa
source: python-docs
---
## Q
从 Python 3.12 起，为什么 `datetime.utcnow()` 被标记为弃用（deprecated），该用什么替代？

## A
`datetime.utcnow()` 返回的是一个 `tzinfo` 为 `None` 的 naive 对象——它的时钟值是 UTC，但很多 `datetime` 方法会把 naive 对象当作本地时间处理，容易在下游被静默地按错误时区解读。应改用 `datetime.now(timezone.utc)`（或 3.11+ 的 `datetime.UTC` 常量），得到一个真正携带 UTC 时区信息的 aware 对象。
