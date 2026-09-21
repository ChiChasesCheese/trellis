# pc09 · Price Data Store — upsert/latest/as-of → OHLC/VWAP → 多币种换算

> 45 分钟第一轮编码常见题；Part 1 是一手原题（"price data design problem"），Part 2 为其自然延伸，Part 3 **(reconstructed)**。

## 背景

LeetCode Discuss 7423863（Quant Dev-Python，Millennium LEaD 第一轮 R5，重开的技术轮）报道了一道 **"price data design problem"**；同一岗位候选人在 PracHub（2026-02-12）被口头问到"how would you model stock price prediction"，指向同一类"时间序列价格存储"话题；QuantVault 的 Millennium OA 题单里还有一道 "multi-currency PnL"，需要把不同币种的价格换算成统一基础货币。三个 part 是同一个考点的递进：**用一个按时间排序的数组做二分，而不是用一个只按插入顺序 `append` 的 dict-of-list**——后者在写入乱序到达时会悄悄把"as-of 查询"和区间聚合全部做错。

## API 契约（英文签名）

```python
class PriceStore:
    def __init__(self) -> None: ...
    def upsert(self, symbol: str, ts: int, price: int | str | Decimal, volume: int | str | Decimal = 0) -> None: ...
    def latest(self, symbol: str) -> Decimal: ...
    def as_of(self, symbol: str, ts: int) -> Decimal: ...
    def ohlc(self, symbol: str, t0: int, t1: int) -> tuple[Decimal, Decimal, Decimal, Decimal]: ...
    def vwap(self, symbol: str, t0: int, t1: int) -> Decimal: ...

class FXTable:
    def __init__(self) -> None: ...
    def upsert(self, pair: str, ts: int, rate: int | str | Decimal) -> None: ...
    def rate_as_of(self, pair: str, ts: int) -> Decimal: ...

def price_in_base(store: PriceStore, fx: FXTable, symbol: str, ts: int, symbol_ccy: str, base_ccy: str) -> Decimal: ...
```

- **金额一律 `Decimal`**：`upsert`/`FXTable.upsert` 的 `price`/`volume`/`rate` 只接受 `int`、`str`、`Decimal` 三种类型；传 `float` 一律 `ValueError`（金额不能靠浮点累加，CONVENTIONS.md 的规则；候选人真在 HackerRank 上被要求这样做的概率不高，但这题刻意把它做成一个可测的边界）。
- `symbol`/`pair`/`symbol_ccy`/`base_ccy` 必须是非空 `str`，否则 `ValueError`；`ts`/`t0`/`t1` 必须是 `int`（`bool` 不算），否则 `ValueError`。
- 所有方法内部返回**未四舍五入的精确 `Decimal`**；四舍五入只发生在展示层（见下方"输出格式"），不发生在存储或计算里。
- 未知 `symbol`/`pair` → `KeyError`；查询范围内没有数据 → `LookupError`（例如 `as_of` 查询的 `ts` 早于该 symbol 第一条记录，或 `ohlc`/`vwap` 的区间里一条记录都没有）。这两种"没找到"用不同的异常类型，是故意的：`KeyError` 对应"这个 key 从没出现过"，`LookupError` 对应"key 存在，但这个时间点/区间没有数据"。

## 规则

### Part 1 — `upsert` / `latest` / `as_of`

`upsert(symbol, ts, price, volume=0)` 写入一条 tick；同一个 `(symbol, ts)` 再写一次是**覆盖**（后写的赢）。写入顺序不保证按 `ts` 递增（乱序到达是常态，这正是这题不能用"只 `append` 的 list"的原因）。

`latest(symbol)` 返回该 symbol **目前记录过的最大 `ts`** 对应的价格——不是"最后一次调用 `upsert` 写入的那条"，两者在乱序写入时不是一回事。

`as_of(symbol, ts)` 返回**时间戳 `<= ts` 里最新的一条**价格（不存在则 `LookupError`）。

实现要点：每个 symbol 维护一个**始终按 `ts` 排序**的时间戳列表（`bisect.insort` 插入），配合 `ts -> price` 的字典。`latest`/`as_of` 都是对这个有序列表的二分查找/取尾，不需要扫描整个历史。

### Part 2 — 区间聚合：`ohlc` / `vwap`

`ohlc(symbol, t0, t1)` 返回闭区间 `[t0, t1]` 内的 `(open, high, low, close)`：`open`/`close` 按**时间顺序**取区间内第一条/最后一条（不是按插入顺序）；`high`/`low` 是区间内的最大/最小价。`t0 > t1` → `ValueError`；区间内没有数据 → `LookupError`。

`vwap(symbol, t0, t1)` 返回区间内的成交量加权均价 `Σ(price·volume) / Σ(volume)`。区间内有数据但**总成交量为 0**（例如全部记录都没传 `volume`）→ `ValueError`（除数为零，均价无定义），这和"区间没数据"的 `LookupError` 是两种不同的失败模式。

### Part 3 — 多币种换算 **(reconstructed)**

`FXTable` 是另一个 as-of 存储，但"symbol"是货币对（如 `"GBPUSD"` 表示 1 GBP 等于多少 USD），存的是汇率而不是价格——和 `PriceStore` 同一套二分技巧,只是换了一层皮。`rate` 必须 `> 0`，否则 `ValueError`。

`price_in_base(store, fx, symbol, ts, symbol_ccy, base_ccy)`：先用 `store.as_of(symbol, ts)` 拿到原始价格；若 `symbol_ccy == base_ccy` 直接返回，不查汇率表。否则先找**正向**货币对 `symbol_ccy + base_ccy`（价格乘汇率），找不到再找**反向**货币对 `base_ccy + symbol_ccy`（价格除以汇率——因为报价台未必两个方向都发布）；两个方向都没有 → `LookupError`。

## 输出格式

三个 part 的每条查询输出，展示前一律 `quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)` 到 4 位小数（半进位，`x.xxxx5` 一律进位，不做"银行家舍入"）；`ohlc` 的四个数字用一个空格连接在同一行。

## Worked examples（全部由 `solution.py` 实际运行得出）

**Part 1**（乱序写入 + 同 ts 覆盖）
```python
store = PriceStore()
store.upsert("AAPL", 100, "150.00")
store.upsert("AAPL", 105, "151.25")
store.upsert("AAPL", 102, "150.75")   # 乱序：102 写在 105 之后
store.latest("AAPL")                  # -> Decimal('151.25')，取的是最大 ts=105
store.as_of("AAPL", 103)              # -> Decimal('150.75')，ts<=103 里最新的是 ts=102
store.as_of("AAPL", 99)               # -> LookupError('AAPL: no price at or before ts=99')
store.upsert("AAPL", 100, "149.50")   # 覆盖 ts=100 的旧值
store.as_of("AAPL", 100)              # -> Decimal('149.50')，不是 '150.00'
```

**Part 2**
```python
s = PriceStore()
s.upsert("MSFT", 1, "300", "10")
s.upsert("MSFT", 2, "305", "5")
s.upsert("MSFT", 3, "295", "20")
s.upsert("MSFT", 4, "310", "5")
s.ohlc("MSFT", 1, 4)   # -> (Decimal('300'), Decimal('310'), Decimal('295'), Decimal('310'))
s.vwap("MSFT", 1, 4)   # -> Decimal('299.375')   ((300*10+305*5+295*20+310*5)/(10+5+20+5) = 11975/40)
```

**Part 3**
```python
store = PriceStore(); fx = FXTable()
store.upsert("VOD", 10, "100.00")     # VOD 价格以 GBP 计价
fx.upsert("GBPUSD", 5, "1.2500")
price_in_base(store, fx, "VOD", 10, "GBP", "USD")   # -> Decimal('125.000000')  (100.00 * 1.2500)
price_in_base(store, fx, "VOD", 10, "USD", "USD")   # -> Decimal('100.00')      (同币种，不查汇率表)

fx2 = FXTable(); fx2.upsert("USDGBP", 5, "0.8000")   # 只发布了反向货币对
price_in_base(store, fx2, "VOD", 10, "GBP", "USD")   # -> Decimal('125')        (100.00 / 0.8000)

fx3 = FXTable()  # 完全没有汇率
price_in_base(store, fx3, "VOD", 10, "GBP", "USD")
# -> LookupError('no FX rate for GBP->USD at or before ts=10')
```

## `main()` 命令流

每行一个命令，`UPSERT`/`FX` 不产生输出，其余命令各输出一行（展示层四舍五入到 4 位小数）：

```
PART 1                          PART 2                              PART 3
UPSERT AAPL 100 150.00          UPSERT MSFT 1 300 10                UPSERT VOD 10 100.00
UPSERT AAPL 105 151.25          UPSERT MSFT 2 305 5                 FX GBPUSD 5 1.2500
UPSERT AAPL 102 150.75          UPSERT MSFT 3 295 20                INBASE VOD 10 GBP USD
LATEST AAPL                     UPSERT MSFT 4 310 5
ASOF AAPL 103                   OHLC MSFT 1 4
                                 VWAP MSFT 1 4
→ 151.2500                      → 300.0000 310.0000 295.0000 310.0000    → 125.0000
  150.7500                        299.3750
```

## 边界清单

- 空输入（没有任何命令）→ 无输出
- 单条记录（`latest`/`as_of` 只有一条数据可选）
- 同一 `(symbol, ts)` 重复 `upsert`（覆盖，后写的赢）
- 乱序写入（`ts` 不按递增顺序到达）——`latest`/`as_of`/`ohlc`/`vwap` 都要对，不能假设插入即时间序
- `price`/`volume`/`rate` 传 `float` → `ValueError`；传负数 `price`/`volume` → `ValueError`；`rate <= 0` → `ValueError`
- `symbol`/`pair` 为空字符串，或 `ts`/`t0`/`t1` 不是 `int`（含 `bool`）→ `ValueError`
- 查询不存在的 `symbol` → `KeyError`；`as_of` 查询早于该 symbol 第一条记录的 `ts` → `LookupError`
- `ohlc`/`vwap` 的 `t0 > t1` → `ValueError`；区间内没有任何记录 → `LookupError`
- `vwap` 区间内有记录但总成交量为 0 → `ValueError`（除零，不是"没数据"）
- `ohlc` 区间内只有一条记录 → `open == high == low == close`
- Part 3：请求币种与计价币种相同 → 不查汇率表，直接返回原价；只有反向货币对时用 `1/rate`；两个方向都没有 → `LookupError`
- 大规模（10 万条 tick，近似递增写入，符合实盘行情流的到达模式）：`upsert` + 二分查询仍 < 2 s（见"性能与规模"）

## 性能与规模

存储用"每个 symbol 一个按 `ts` 排序的列表（`bisect.insort` 维护）+ `ts -> price` 字典"。`bisect.insort` 单次插入是 O(n)（要挪动比它大的元素），但**对递增到达的实盘行情流，新 `ts` 几乎总是插在末尾**，退化成 O(1) 摊还；只有真正乱序的写入才会触发 O(n) 的挪动。`latest`/`as_of`/`ohlc`/`vwap` 都是二分或切片，O(log n) 或 O(log n + 命中数)。性能测试：10 万条近似递增写入的 tick + 1000 次 `as_of` 查询 + 一次全区间 `ohlc`/`vwap`，本机 < 2 s（实测约 0.3 s，见 `test_perf_100k_upserts`）。

## 追问

1. **为什么不用 `dict[symbol] -> list` 直接 `append`？** `append` 只保证插入顺序，乱序到达时列表就不再按 `ts` 排序，`as_of`/`ohlc`/`vwap` 的二分/切片全部失效——这是这题的核心考点。
2. **内存**：每个 tick 占用一个 `ts`（int）+ 一个 `Decimal` price + 一个 `Decimal` volume；百万级 tick 级别要考虑按时间分桶、冷数据落盘。
3. **迟到数据**：如果一条 `ts` 很旧的记录在很晚才到达（比如回填历史数据），`bisect.insort` 仍然正确地把它插到该在的位置，只是这一次插入是 O(n)——这和"乱序写入"是同一个问题的两种说法。
4. **持久化**：现在是纯内存结构；真实系统会加一个 WAL 或者定期把有序列表 snapshot 到列式存储（比如按 `(symbol, 日期)` 分区的 Parquet），重启时重放。
5. **为什么 `latest` 不是 O(1) 直接存一个变量？** 因为乱序写入可能把一条更早的 `ts` 写进来，此时"最后一次 `upsert`"和"`ts` 最大的那条"不是同一条记录；本题选择正确性（对 `ts` 排序取尾）而不是想当然的 O(1)。

## 来源与置信度

- **HIGH（一手）**：LeetCode Discuss 7423863（Quant Dev-Python，Millennium LEaD 第一轮 R5，重开的技术轮）"price data design problem"，未给出完整题面细节，仅有题名。
- PracHub（2026-02-12，Millennium，Technical Screen，口头）："How would you model stock price prediction?"——同一时间序列价格话题的独立佐证，但不是同一道编码题。
- QuantVault Millennium OA 题单："multi-currency PnL"，指向 Part 3 的多币种换算需求。
- Part 1、Part 2 的具体 API（`upsert`/`latest`/`as_of`/`ohlc`/`vwap`）与全部 worked examples 均为按题名重建 **(reconstructed)**；Part 3 的 `FXTable`/`price_in_base` 设计同样 **(reconstructed)**。

## 考什么

用有序结构 + 二分代替"只 append 的 list"，支撑 as-of 查询与区间聚合 · 乱序写入下的正确性（不能假设插入顺序 = 时间顺序）· 金额用 `Decimal`、舍入规则只在展示层生效一次 · 两种"没找到"（`KeyError` vs `LookupError`）的语义区分。
