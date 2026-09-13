# q16 · 拒付记录解析（跳过损坏行 · 撤回的争议整组消失）

> `problems/q16_chargeback_parsing/` · 3 个 part
> **主题：逐字段的校验策略 + 最小货币单位的多币种格式化。**

## 一句话题意

解析卡组织发来的拒付记录，跳过损坏行并计数，
最后：**任何一组 `(network, transaction_id)` 里只要有一行 reason 是 `withdrawn`，整组都不输出。**

## 输入 / 输出

```
PART n
network,transaction_id,amount,currency,reason,date
visa,txn_123,2500,usd,fraudulent,2024-01-05
```
`network ∈ {visa, mastercard, amex, discover}`（输入大小写不敏感）；
`amount` 是**最小货币单位**的整数；`currency` 是小写 ISO 4217；`date` 是 `YYYY-MM-DD`。最多 2·10^5 行。

输出（输入序）：

```
[NETWORK] transaction_id: <money> CURRENCY - reason (YYYY-MM-DD)
```

`<money>` 三种情况：
- 两位小数币种：符号 + `x.xx`（`usd` → `$25.00`，`eur` → `€19.99`，`gbp` → `£50.00`）
- **零小数**币种（`jpy`、`krw`）：整数无小数（`¥2500`、`₩2500`）
- 其他币种：`x.xx` **无符号**（`12.34 CAD`）

Part 2–3 最后**总要**打印 `SKIPPED: n`（哪怕是 `SKIPPED: 0`）。

## 核心考点

`S02` 分隔符解析 + 畸形行 · **`S06` 最小单位 + 零小数币种** · `S09` 精确格式 ·
**`S11` 成对事件的去重/撤销** · `S12` 日期校验 · **`S18` 校验与错误路径** · `S24` 争议词汇

## 解题思路

### 损坏行的判定（逐条对照）

```python
def parse_row(line):
    f = [x.strip() for x in line.split(",")]
    if len(f) != 6:                                   return None   # 字段数不对
    net, tid, amt, cur, reason, date = f
    if net.lower() not in NETWORKS:                   return None
    if not tid or not cur or not reason:              return None
    if not amt.isdigit():                             return None   # 非整数 / 负数 / 空 / "25.00"
    try:  d = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:                                return None
    return Row(net.lower(), tid, int(amt), cur, reason, d.strftime("%Y-%m-%d"))
```

- `amt.isdigit()` 一次挡住 `25.00`、`abc`、`-1`、空串（`"-1".isdigit()` 是 `False`）。
- `strptime` 一次挡住 `2024-02-30`、`2024-13-01`、`01/05/2024`。
- **合法日期要重新规范化输出**：`2024-2-3` 被 `strptime` 接受，输出成 `2024-02-03`。
- **空行不是行，不计入 `SKIPPED`。**

### Part 3 — 撤回

```python
withdrawn = {(r.net, r.tid) for r in valid if r.reason == "withdrawn"}
survivors = [r for r in valid if (r.net, r.tid) not in withdrawn]
```

**两遍**：先收集所有被撤回的组，再过滤。
撤回行在原始行之前还是之后**都一样**（题面明说"到达顺序无所谓"）。
一组里有两个 withdrawn、或只有一个 withdrawn 而没有原始行，同样整组消失。

**同一个 `transaction_id` 在不同 network 上是不同的争议**，互不影响。
**被撤回的行不计入 `SKIPPED`**（只有损坏行计）。**损坏的 withdrawn 行不能取消任何东西**
（它在第一步就被丢掉了，进不了 `valid`）。

## 坑

1. 金额：`5` → `$0.05`，`100` → `$1.00`，`0` → `$0.00`，`123456789` → `$1234567.89`。
2. **JPY 永不显示小数**；未知币种**无符号**。
3. 损坏行的六种：字段数不对、`25.00`、负数、空 amount、`2024-02-30`、未知 network。
   **大写 `VISA` 是接受的**（输入大小写不敏感）。
4. **`2024-2-3` 被接受**，且要输出成 `2024-02-03`。
5. **`SKIPPED: 0` 也要打印**；空输入时 Part 2/3 只打印 `SKIPPED: 0`（Part 1 什么都不打）。
6. 撤回在原始行之前、两个撤回、只有撤回没有原始、同 id 不同 network（只有被撤回那个 network 消失）、
   **损坏的撤回行不取消任何东西**。
7. **输出按输入序，不排序**；非撤回争议的重复行**打印两次**。
8. 字段周围空白、空行、末尾换行。

## 变体

- 原题说"一个或多个文件"并汇总；这里把文件拼接到 stdin 上。
- programhelp 2025-08-08 把同样三个 part 讲成"退款/争议数据"，损坏行描述为"无法解析成 dispute 对象的行"。

## Code Core 节点

**`input.malformed`** · **`rules.money`**（最小单位 / 零小数币种） · `chrono.parsing`（`strptime` 当校验器） ·
**`model.idempotency`**（成对事件抵消） · `output.formatting` · `output.sentinels`

## 自测清单

- [ ] 三种金额格式（含符号 / 零小数 / 无符号）+ `5` / `0` / 大额
- [ ] 六种损坏行各一次 + 大写 network
- [ ] `2024-2-3` 的规范化输出
- [ ] `SKIPPED: 0` / 空输入
- [ ] 撤回在前 / 两个撤回 / 只有撤回 / 跨 network
- [ ] 损坏的撤回行不取消
- [ ] 重复的非撤回行打印两次
