---
id: hi-c-sd-dealing-with-contention-x07-aba-version
node: sd.patterns.dealing-with-contention.exam
type: qa
step: 7
---
## Q
**处理竞争 · 用点评数当版本**｜考点 · 必会

更新餐厅平均分时，你用 `review_count` 当乐观并发的版本。为什么这有时会悄悄丢更新？怎么改？

## A
- **原因：** 点评数可以先减后增回到原值（删一条又来一条），你的"版本没变"检查通过，覆盖了中间的更新（ABA）。
- **改法：** 专用的 `version` 列，每次写都加一；写入条件 `WHERE id=? AND version=读到的值`。
- **替代：** 无法加列时，把读到的所有字段放进 WHERE；或用数据库内置的行版本（如 Postgres 的 `xmin`）。
- **什么时候业务值可以当版本：** 只朝一个方向变化的值，比如拍卖只涨不降的最高出价。
