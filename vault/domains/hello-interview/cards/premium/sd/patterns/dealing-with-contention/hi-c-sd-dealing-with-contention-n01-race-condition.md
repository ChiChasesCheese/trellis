---
id: hi-c-sd-dealing-with-contention-n01-race-condition
node: sd.patterns.dealing-with-contention.notes
type: qa
step: 1
---
## Q
**处理竞争 · 竞态条件**｜摘要 · 必会

最后一张票被两个人同时买，为什么会卖出两张、库存变成负数？问题出在哪一步？

## A
- **朴素写法：** 先 `SELECT` 读出剩余座位数，应用判断大于 0，再 `UPDATE` 减一。单人使用完全正确。
- **出错过程：** Alice 读到 1，Bob 在 Alice 写回之前也读到 1；两人都认为有座，都去扣款，Alice 提交后库存为 0，Bob 再减一变成 -1，两张确认邮件指向同一个座位。
- **根因：** 读和写是两个独立步骤，中间有缝隙，Bob 拿着已经过期的数字做决定。缝隙在内存里是微秒，跨网络是毫秒，但足够两个请求都判定自己赢了。
- **放大：** 并发用户越多（比如一万人抢同一资源），缝隙撞上的概率越高；系统跨多个节点后协调更难。所以必须引入某种同步（synchronization）。
