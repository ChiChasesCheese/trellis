---
id: mlp-coding-pc11-followups
node: coding.pc11
step: 2
type: qa
---
## Q
**订单簿撮合引擎：追问与变体**｜编程轮

订单簿写完后，面试官会往哪些方向追问？

## A
- **改单（amend）要不要保留排队位置：** 行业惯例是只减量、价格不变时保留位置；改价或加量等于撤旧单、下新单，排到同价位队尾。原因是加量或改价如果还保留位置，就能用小单先占位再改大，对后面排队的人不公平。

```python
def amend(b, oid, new_id, new_price, new_qty):
    side, price, qty = b.orders[oid]
    if qty == 0:
        return False
    if new_price == price and new_qty <= qty:
        b.orders[oid][2] = new_qty              # 只减量：留在原队位
        return True
    b.cancelOrder(oid)                           # 改价或加量：撤旧单，新 id 重下，排队尾
    b.placeOrder(new_id, side, new_price, new_qty)
    return True
```

- **前五档（top 5 levels）：** 每个价位返回总挂单量。最直接的写法是把有效价位排序取前 5 个，再对每个价位累加剩余量；价位很多时，改成每个价位额外维护一个 `level_qty` 数字（成交、撤单时同步增减），取前五档用 `heapq.nsmallest(5, …)`，不必每次扫全部订单。
- **撤单特别多、订单上百万：** 惰性删除让撤单 O(1)，但废单会占内存，挤在队首之外的不会被清理。做法是周期性重建，或某个价位废单比例超过一半就整队压缩；另一种做法是每个价位用双向链表加 `id -> 节点` 的字典，撤单当场 O(1) 摘掉，没有废单残留，代价是内存和指针开销更大。
- **多个交易品种：** 每个 symbol 一个独立的订单簿，互不影响，所以可以按 symbol 分片，每片一个线程或进程，不用加锁。
- **崩溃恢复：** 引擎是确定性的（同样的输入顺序得到同样的结果），所以只要把每条收到的指令先写进追加式日志（WAL，先记日志再改内存，重启时重放），再定期保存快照；恢复时加载最近快照，重放之后的日志即可，成交记录也是重放出来的，不必单独持久化。
- **会多花一个测试用例的边界：** 市价单遇到空盘（什么也不成交，剩余作废）；同价多笔按先后成交；一笔大单跨多个价位；撤已成交或不存在的单（返回 False）；卖单价格正好等于买一价（算交叉，要成交）；买单价格等于卖一价同理；数量为 0 或负数的单（先拒绝）。

**英文答法。**
- "On amend, **only a size decrease at the same price keeps queue position**; anything else is cancel plus a new order."
- "The engine is **deterministic**, so I log every command and replay it from the last snapshot after a crash."
- "With millions of cancels I'd switch to a **linked list per level** so cancel is O(1) and nothing stale is left behind."
