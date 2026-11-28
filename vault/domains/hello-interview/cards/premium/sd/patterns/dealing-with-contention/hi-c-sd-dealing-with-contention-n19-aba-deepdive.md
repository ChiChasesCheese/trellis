---
id: hi-c-sd-dealing-with-contention-n19-aba-deepdive
node: sd.patterns.dealing-with-contention.notes
type: qa
step: 20
---
## Q
**处理竞争 · 追问：乐观并发里的 ABA 问题**｜摘要 · 追问

什么是 ABA 问题？用 `review_count` 当版本为什么会出错，怎么修？

## A
- **现象：** 值在你读和写之间从 A 变 B 又变回 A，相等检查看不到这一来回。
- **例子：** 餐厅点评数读到 100；期间删一条（99）又来一条（100），你的"版本还是 100 吗"检查通过，悄悄覆盖了中间的更新。
- **最稳的修法：** 专用版本列，每次更新都加一，不管业务数据有没有变：`SET avg_rating=..., version=version+1 WHERE id=? AND version=42`。
- **没法加列时：** 把读到的所有字段都放进 WHERE，整行没变才写，笨重但能抓到任何变化。
- **替代：** 有的数据库提供内置行版本，例如 Postgres 的系统列 `xmin`。
