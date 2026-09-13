# q25 · 发票对账（把收到的付款匹配到未结发票）

> `problems/q25_invoice_reconciliation/` · 4 个 part
> **主题：候选集的选择规则 + "点名了就绝不外溢" + 幂等应用。**

## 一句话题意

给一批发票和一批付款（带 memo），把付款匹配到发票上。
P1 memo 必须严格；P2 memo 是自由文本，取"提到的"发票；P3 一笔付款可以覆盖多张发票；P4 输出审计流水。

## 核心考点

`S02` 解析 · `S03` 按 id 建记录 · **`S05` 精确 vs 宽松匹配** · `S06` 整数分 ·
`S08` 确定性顺序 · `S09` 格式 · **`S11` 幂等应用** · `S19` 增量

## 解题思路

### Part 1 — 严格 memo

memo 必须**恰好**是 `Paying off: <invoice_id>`（id 周围空格容忍，**其余什么都不能有**），
且该发票存在、未付、**金额相等**。否则忽略。
**已付发票的第二笔付款忽略**（不重复应用）。

### Part 2 — 宽松 memo

```python
tokens = re.split(r"[^A-Za-z0-9_-]+", memo)          # 非 [A-Za-z0-9_-] 都是分隔符
mentions = [t for t in tokens if t in invoices]
candidates = mentions if mentions else all_invoices   # ★ 有点名就只用点名的
```

在候选中选**到期最早的、未付的、金额相等的**那张。
**没有合格候选就忽略** —— **点名了就绝不回落到没点名的发票**。

### Part 3 — 一笔覆盖多张

候选集同 P2，但金额不必相等。按**到期顺序（最早在前）**倾倒：
每张拿 `min(剩余付款, 该发票欠款)`，直到付款用完。

- 全部付款处理完后仍欠钱的发票 → `PARTIAL (remaining r)`；没被碰过的 → `UNPAID`。
- 最后一张候选之后还剩的钱 → `<payment_id>: UNAPPLIED <left>`，**绝不外溢到未点名的发票**。
- 金额 ≤ 0 的付款**忽略，且不产生任何行**。

### Part 4 — 审计流水

匹配规则同 P3。在发票状态行**之前**，按应用发生的顺序打印
`<payment_id> -> <invoice_id> <cents_applied>`，然后发票状态行，最后 `UNAPPLIED` 行。

## 坑

1. **已付发票的第二笔付款不能重复应用。**
2. P1 的 memo 是严格的：`Paying off: invoiceA today` 或单独的 `invoiceA` **都不匹配**。
3. P2 的 token 匹配是**整 token**：memo 里的 `invoiceAB` **不算**提到 `invoiceA`。
4. memo 里可能有逗号（`Paying off: invoiceA, thanks`）→ **行只切前两个逗号**。
5. **到期时间平手 → 发票的输入顺序**；**输出永远按发票输入顺序**，不是按到期顺序。
6. P3 边界：付款 == 欠款 → `PAID`；少 1 → `PARTIAL (remaining 1)`；多 1 → `UNAPPLIED 1`。
7. **点名的付款绝不外溢**；未点名的付款按到期顺序铺开到所有发票。
8. 金额 0 / 负 → 忽略，**不产生 `UNAPPLIED` 行**。
9. 10^12 分的金额要精确（整数）。
10. 空发票列表 → 空输出；没有付款 → 每张发票 `UNPAID`。

## 变体

- **集成风格**：同样的规则包在 HTTP 风格的 API 后面（`POST /payments`、`GET /invoices/{id}`）——
  P4 的审计流水就是它的替身。
- 返回 `{invoice_id: status}` 而不是 stdout。
- memo 只用数字后缀引用发票（`#123`）—— 改一下 tokenizer。

## Code Core 节点

**`algorithms.settlement`**（FIFO 倾倒） · **`model.idempotency`** · `rules.money` ·
`input.normalization`（tokenize memo） · `output.ordering` · `chrono.arithmetic`（到期序）

## 自测清单

- [ ] 已付发票的第二笔付款
- [ ] P1 的严格 memo 的三种反例
- [ ] `invoiceAB` 不算提到 `invoiceA`
- [ ] memo 里有逗号
- [ ] 到期平手 → 输入序；输出按输入序
- [ ] P3 的 `==` / `-1` / `+1` 三个边界
- [ ] 点名的付款不外溢
- [ ] 金额 0 / 负
- [ ] 空发票列表 / 无付款
