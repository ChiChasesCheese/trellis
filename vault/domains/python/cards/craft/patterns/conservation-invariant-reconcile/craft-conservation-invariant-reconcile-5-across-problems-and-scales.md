---
id: craft-conservation-invariant-reconcile-5-across-problems-and-scales
node: craft.patterns.conservation-invariant-reconcile
type: qa
step: 5
---
## Q
**守恒不变式与对账 · 账本、钱包、取款机、券商里的同一个自检，放大到支付对账**｜模式

账本的分录为零、钱包的缓存与账本一致、取款机的钞票总量、券商的现金与股票总量，各自检查什么？放大到真实的支付系统，对账长什么样？

## A
**要点。** 同一个思路：找出系统里一个**永远不变的量**，写成一个只读的断言，在测试里、运行时定期、事故后各检查一遍。违反它说明某处记账有漏洞，哪怕所有功能看起来都正常。

```python
# double-entry-ledger：每个币种全部余额之和恒为 0
def total(self, currency): return sum(v for (_, c), v in self._bal.items() if c == currency)
# digital-wallet：缓存余额必须等于账本推导，不等就用账本覆盖
derived = self._ledger.derived_balance(account_id)
# atm：装入的钱要么还在机器里，要么被客户拿走了
return self.loaded == self.in_cassette + self.on_tray + self.in_reject_bin + self.collected
# stock-brokerage：撮合是零和搬运，总现金只被入金改变
return sum(a.cash for a in self._accounts.values())
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

**见于。** double-entry-ledger、digital-wallet、atm、stock-brokerage。

**不变的。** 变化只通过「成对的搬运」发生；不变量是只读查询，不参与业务；真相（账本）与投影（缓存）分开，冲突时真相覆盖投影。**变化的。** 守恒的量（币种余额、钞票、现金与股票）和检查的时机（写入时校验、定时对账、测试收尾）。

**信号。** 需求里出现「钱」「库存」「额度」「份额」「不能多也不能少」；或者你在写一个会被多个路径改动的总数。

**尺度对照。** 力扣：没有直接对应；最接近的是 Optimal Account Balancing（LC 465）里「每个人的净额之和为零」。低层设计：分录为零校验、缓存对账、性质测试。分布式：支付平台每天把自己的账本和银行、卡组织的结算文件逐笔对账，差异分类处理（漏记、重复、金额不符）；分账与分润必须守恒，余数分配规则要确定且可复现。变化：单机里一次校验就保证了守恒，跨系统时没有共同的事务，所以对账是**事后**的、周期性的，差异会真实出现，系统要有处理差异的流程（调整分录，而不是改历史），这也是为什么账本只追加。
