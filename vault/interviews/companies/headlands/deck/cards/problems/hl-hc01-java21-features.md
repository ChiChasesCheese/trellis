---
id: hl-hc01-java21-features
node: problems.hc01-stock-trading-dp
type: qa
step: 16
---
## Q
买卖股票实现里用到哪些 Java 21 特性？`Trade`、`Plan`、`Move`、`reversed()` 各自解决什么？

## A
```java
public record Trade(int buyDay, int sellDay) {
    public Trade { if (buyDay < 0 || sellDay <= buyDay) throw new IllegalArgumentException(...); }
}
public record Plan(long profit, List<Trade> trades) {
    public Plan { trades = List.copyOf(trades); }
}
public sealed interface Move permits Buy, Sell {}
```
- **record 紧凑构造器**：`Trade` 保证买入日 < 卖出日，非法值构造不出来；测试直接 `assertEquals(List.of(new Trade(1,2)), plan.trades())`。
- **`Plan` 防御性拷贝**：`List.copyOf` 得到不可变拷贝，外部再改原列表不影响；没有它字段虽 `final`，列表仍可被改，「不可变」是假的。
- **`Rules` record** 把 k / fee / cooldown 打包：121 = `atMost(1)`，122 = `unlimited()`，309 = `unlimited().withCooldown(true)`，714 = `unlimited().withFee(f)`——六道题是同一函数的六组参数。
- **sealed `Move` + 模式匹配 switch + `case null`**：不需要 `default`，新增 `Rest` 时所有 `switch` 编译失败；`case null` 免去先判空。
- **Sequenced Collections**：`list.reversed()` 是倒序视图，不拷贝、不改原列表；`getLast()` 取代 `get(size()-1)`。
- `enum` 的 `switch` 表达式要求覆盖所有取值。
