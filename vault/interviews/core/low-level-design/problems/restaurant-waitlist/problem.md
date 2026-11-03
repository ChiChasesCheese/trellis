# 餐厅候位（Restaurant Waitlist）

一家餐厅有几张大小不同的桌子，客人成桌到来：有空桌就直接入座，没有就排队。桌子空出来时，安排队伍里第一个坐得下的人。前台还要能告诉排队的客人"大概还要等多久"。不需要界面，只写 `Restaurant` 类，时间由注入的时钟提供。

**分关要求**（做完一关再看下一关）
- 第 1 关（约 20 分钟）：入座、排队、离开。
  - `Restaurant(table_sizes: Sequence[int], clock: Callable[[], datetime], dining_time: timedelta = 60 分钟, max_overtakes: int | None = None)`：`table_sizes[i]` 是 i 号桌的容量。桌子为空或有容量小于 1 的桌子抛 `ValueError`。`clock`、`dining_time` 从第 2 关起使用，`max_overtakes` 从第 3 关起使用。
  - `join(party_id: str, size: int) -> int | None`：有桌就立刻入座并返回桌号，否则排到队尾返回 `None`。入座时在容量够的空闲桌里选最小的（大桌留给大团），容量相同取编号小的。
  - `leave(party_id) -> None`：排队的客人走了；不在排队（包括已入座）抛 `UnknownPartyError`。同一个 id 之后可以重新 `join`。
  - `finish(party_id) -> list[tuple[str, int]]`：用餐结束，桌子空出来；从队首往后，第一个坐得下的人入座，前面坐不下的留在队里、保持相对顺序。返回新入座的 `(party_id, 桌号)`。不在用餐抛 `UnknownPartyError`。
  - `queue() -> list[str]`、`table_of(party_id) -> int | None`。
  - 错误：`size < 1` 抛 `InvalidPartyError`；`size` 超过最大的桌子抛 `PartyTooLargeError`（`InvalidPartyError` 的子类）；`party_id` 正在排队或用餐抛 `DuplicatePartyError`。失败时不改变状态。
  - 例：桌 `[2,4]`，`a(2)` 坐桌 0，`b(4)` 坐桌 1，`c(4)`、`d(2)` 排队。`finish("a")` 返回 `[("d", 0)]`：桌 0 容量 2，`c` 坐不下，`d` 是第一个坐得下的。
- 第 2 关（约 20 分钟）：等位估计。
  - `estimate_wait(party_id) -> timedelta`：排队客人预计还要等多久；已入座返回 `timedelta(0)`；不认识抛 `UnknownPartyError`。
  - `quote(size) -> timedelta`：此刻来一桌 `size` 人（排到队尾）预计要等多久，不改变任何状态；`size` 不合法的错误同 `join`。
  - 推演规则：每张忙桌空出的时刻 = 入座时间 + `dining_time`，已经超时的算"现在就空"；桌子空出时用和实际完全相同的规则安排队伍。
  - 例：桌 `[2,4]`，18:00 `a(2)`、`b(4)` 入座，`c(4)`、`d(2)`、`e(2)` 依次排队。18:00 时 `c`、`d` 都是 60 分钟，`e` 是 120 分钟；到 18:30 分别是 30、30、90。
- 第 3 关（约 15 分钟）：防饿死。
  - `max_overtakes` 不为 `None` 时：一个人被排在他后面的人插队（后来者先入座）达到 `max_overtakes` 次之后，就挡在所有后面的人前面——他没入座之前，后面的人即使有空桌也不能坐。`0` 表示严格先来先坐。`None` 保持第 1 关的行为。
  - 被挡住的人在挡路者入座或离开之后，于同一次调用里被安排（`finish` 可以一次返回多个入座）。`estimate_wait` 和 `quote` 要遵守同样的规则。
  - 例：桌 `[2,6]`，`a(6)` 占 6 人桌，`b(6)` 排队，`c(2)` 坐桌 0（插队 1 次）。`max_overtakes=1` 时，`c` 结束后新来的 `d(2)` 只能排队，直到 `a` 结束：`finish("a")` 返回 `[("b",1),("d",0)]`。
- 第 4 关（选做）：改人数。
  - `change_size(party_id, size) -> list[tuple[str, int]]`：排队中的客人改人数，位置和被插队次数不变；返回因此新入座的 `(party_id, 桌号)`（改小后可能立刻坐下，也可能带动后面被挡住的人）。
  - 不在排队抛 `UnknownPartyError`；新人数不合法同 `join`，且失败时保持原样。

**评分点**
- "谁坐哪张桌"的规则只写在一个地方（一个不依赖实例状态的函数），实际入座和等位推演共用它，所以预测不会和现实不一致。
- 入座选最小够用的桌，能说出这样做保住大桌的理由，以及它不是全局最优。
- 每个会改变状态的入口（`join`、`leave`、`finish`、`change_size`）最后都跑同一个"能坐的都安排上"的步骤，而不是各写各的。
- 推演在复制品上进行，不污染真实状态；超时的桌子有明确的处理规则。
- 防饿死的规则以参数形式加入，默认值不改变前面的行为；能说出代价（桌子空着但有人在等）。
- 失败的调用不留半成品：重复 id、人数非法、改人数失败时队伍原样。
- 用注入的时钟，测试里不 `sleep`。
- 能讲清为什么不用优先队列：规则是"第一个坐得下的人"，队伍要保持相对顺序并支持中间删除。
