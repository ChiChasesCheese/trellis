---
id: pl-data-maps-intro-go
node: data.maps-collections
type: qa
step: 4
---
## Q
Go 的内建 `map` 有哪些行为需要知道？随机迭代顺序、nil map、并发写分别是什么，为什么这样设计？

## A
**是什么**：Go 内建了唯一的映射类型 `map[K]V`，是哈希表（Go 1.24 起内部改为 Swiss Table 设计，一种开放寻址的紧凑哈希表）。键类型必须是可比较的（可以用 `==`），切片、`map`、函数不能当键。集合用 `map[T]struct{}` 或 `map[T]bool` 模拟。

**三个必须知道的行为**：
1. **迭代顺序故意随机化**。Go 从 1.0 起每次 `range` 的起点随机，目的是让程序员不要依赖顺序。对 12 个整数键的映射连续迭代三次，真实输出分别是 `12 1 2 4 11 3 ...`、`4 11 3 5 6 ...`、`3 5 6 7 ...`，起点不同。需要稳定顺序，就先取出键、排序再遍历。
2. **nil map 可读不可写**。`var m map[string]int` 声明了但没有 `make`，读 `m["x"]` 返回零值 `0`，`len(m)` 是 0，但写入会 panic：`assignment to entry in nil map`。
3. **并发写是致命错误**。多个 goroutine 同时写（或一读一写）同一个 map，运行时会检测并直接终止整个程序：`fatal error: concurrent map writes`。它不是 panic，`recover` 不住。需要并发就加 `sync.Mutex`，或用 `sync.Map`。

**设计理由**：Go 偏爱简单：只给一种映射，没有泛型集合类。随机顺序是预防措施：如果顺序稳定，大家的程序会悄悄依赖它，将来改实现就会破坏兼容。并发检测是主动选择快速失败：与其让数据悄悄损坏，不如立刻崩溃。

**读取用逗号 ok 形式**：`v, ok := m[k]` 区分「键不存在」和「值恰好是零值」。
