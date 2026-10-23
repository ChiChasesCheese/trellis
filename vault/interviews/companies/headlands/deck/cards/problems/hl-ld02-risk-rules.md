---
id: hl-ld02-risk-rules
node: problems.ld02-trading-ood
type: qa
step: 7
---
## Q
交易前风控 `RiskEngine.check` 的七条规则、检查顺序和边界是什么？为什么要 fail closed、顺序要确定？

## A
订单发出前必须通过的一组规则：出了交易所错单就是真金白银（著名事故如 2012 年 Knight Capital，45 分钟亏约 4.4 亿美元；美国 SEC 市场准入规则 15c3-5 要求预交易风控）。

**检查顺序 = `RiskReason` 的声明顺序**，报告**第一条**违反的；顺序不固定（如遍历 `HashMap` 的规则）则两次运行报告的原因可能不同，重放不一致。
1. `HALTED`：熔断（kill switch）中，拒绝一切，包括减仓单；
2. `NO_REFERENCE_PRICE`：没设过参考价 ⟹ 拒绝（**fail closed**：无法判断价格带就不放行，不是 fail open）；
3. `QTY_LIMIT`：`qty > maxOrderQty`（`==` 通过）——防多打几个 0；
4. `NOTIONAL_LIMIT`：`px*qty > maxOrderNotional`（`==` 通过）；乘法**溢出也算** `NOTIONAL_LIMIT`，不能回绕成小数而通过；
5. `PRICE_BAND`：`|px − ref| / ref > bps/10000` 拒绝，边界等于通过——防「胖手指」（150 打成 15）。整数交叉相乘 `|px − ref| * 10_000 <= ref * priceBandBps`，不做除法没有舍入（5% = 500 基点；参考价 3 或 10007 时除法会错）；
6. `OPEN_ORDERS_LIMIT`：`orders.openCount() >= maxOpenOrders`（所有标的合计；`PENDING` 也算；这一单尚未登记）；
7. `POSITION_LIMIT`：最坏情况净仓（见下一张卡）。

```java
if (halted) return reject(HALTED);
Long ref = refPx.get(o.symbol());
if (ref == null) return reject(NO_REFERENCE_PRICE);
if (o.qty() > limits.maxOrderQty()) return reject(QTY_LIMIT);
try {
    if (Math.multiplyExact(o.px(), o.qty()) > limits.maxOrderNotional()) return reject(NOTIONAL_LIMIT);
    long dev = Math.multiplyExact(Math.abs(o.px() - ref), 10_000L);
    if (dev > Math.multiplyExact(ref, limits.priceBandBps())) return reject(PRICE_BAND);
} catch (ArithmeticException overflow) { return reject(NOTIONAL_LIMIT); }
```
`check` **只读**，不改任何状态，可在登记之前调用；`setReferencePrice(px <= 0)` → IAE。样例：限额 `(1000, 1_000_000, 5000, 3, 500)`，参考价 100：买 100@105 通过（+5.00% 恰好等于带宽）；100@106 → `PRICE_BAND`；标的 B 无参考价 → `NO_REFERENCE_PRICE`。

边界：每条规则的 `==` / `+1`；价格带 ref 很小或不整除（10007、3）；未知标的；同时违反多条的确定顺序；halt 拒绝减仓单。
