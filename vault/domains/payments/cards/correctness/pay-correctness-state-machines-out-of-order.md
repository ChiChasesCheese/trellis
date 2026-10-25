---
id: pay-correctness-state-machines-out-of-order
node: correctness.state-machines
type: qa
step: 4
---
## Q
渠道的 webhook 乱序到达：先收到 captured，后收到本该更早的 authorized，状态机怎么处理才不会倒退？

## A
**乱序原因**：渠道重试、多线程发送、网络路径不同，webhook 不保证顺序。

**处理方法**
1. **状态阶位**（rank）：给每个状态一个单调递增的阶位：created 0，requires_action 1，authorized 2，captured 3，refunded 4。收到事件对应的目标状态阶位**低于或等于**当前阶位时，视为过期事件，忽略（但记录）。
2. **事件携带的时间或序号**：渠道事件通常有创建时间或序列号；按它们判断新旧，旧的丢弃。
3. **跳过的中间状态要补**：先收到 captured（当前状态 created），意味着中间的 authorized 已经发生。允许从 created 直接到 captured，并补记中间状态的历史，账务上同时补 authorized 和 captured 两步的必要分录。
4. **以主动查询为准**：对于关键状态，收到事件后调渠道查询接口获取当前真实状态，再按阶位推进。事件只是触发，不是真相。

**例子**
- 当前 created，收到 captured（阶位 3 > 0）：直接推进到 captured，补记 authorized。
- 随后收到迟到的 authorized（阶位 2 < 3）：忽略，不倒退，记录一条 ignored_stale_event。
- 再收到重复的 captured（阶位 3 = 3）：幂等忽略。

**注意**：忽略不等于丢弃事件本身，原始事件要完整保存在收件箱，便于排查和重放。
