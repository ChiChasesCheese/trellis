# q01 · 按 MCC 判定欺诈商户（CHARGE / DISPUTE 事件流）

> `problems/q01_fraud_mcc_disputes/` · 5 个 part · OA 旗舰题（8 个独立来源，最近 2026-07）
> **这是刷题顺序的第 1 题。它把这类 OA 的全部套路演示了一遍。**

---

## 一句话题意

给一串商户配置行和 CHARGE/DISPUTE 事件行，按每个 MCC 各自的欺诈容忍度（**计数**或**比例**），
输出当前被标记为欺诈的账户 id 列表。

---

## 输入 / 输出

**输入**（逗号分隔，空行忽略，逗号周围空格容忍）：

```
MERCHANT,<account_id>,<mcc>        商户 → MCC（重复出现时后者覆盖）
THRESHOLD,<mcc>,<value>            3 → 计数阈值；0.25 / 1.0 → 比例阈值
FRAUD_CODES,<code>[,<code>...]     欺诈码集合（可重复出现，取并集）
MIN_COUNT,<n>                      比例阈值生效前的最小笔数（默认 0）
STICKY                             可选：一旦标记永久保持
CHARGE,<charge_id>,<account_id>,<amount>,<code>
DISPUTE,<charge_id>                指向之前的某笔 CHARGE
```

**setup 行（前 5 种）先于所有事件生效，不管它出现在文件哪一行。**

**输出**：默认一行 —— 欺诈账户 id **按普通字符串序**升序、`,` 连接、无空格；
没有则输出字面量 `NONE`。`PART 1`/`PART 2`/`PART 3` 有各自的输出格式。

---

## 核心考点

`S01` 读全 spec · `S02` 解析 · `S03` 每商户两个计数器 · **`S05` 阈值语义（计数 vs 比例、`>=`、最小量门槛）** ·
`S08` 确定性排序 · `S09` `NONE` 格式 · **`S10` 事件流 + 反向事件** · **`S11` 幂等（重复 dispute）** ·
`S18` 未知 id / 未知 MCC · `S19` 增量设计

---

## 解题思路

### 状态形状（从 Part 4/5 倒推 —— 这题的关键决定）

```python
@dataclass
class Charge:
    account: str
    is_fraud: bool
    alive: bool = True          # 被 dispute 之后置 False

charges: dict[str, Charge] = {}                    # charge_id → 原始记录 ★
merchant_mcc: dict[str, str] = {}
thresholds: dict[str, tuple[str, int, int]] = {}   # mcc → ("count", v, 1) | ("ratio", num, den)
fraud_codes: set[str] = set()
min_count: int = 0
totals: dict[str, int] = defaultdict(int)
frauds: dict[str, int] = defaultdict(int)
ever_flagged: set[str] = set()                     # STICKY 用
```

**★ 必须保留每一笔 charge。** Part 4 的 `DISPUTE,<charge_id>` 要求"这笔 charge 从未发生过"，
你必须知道那一笔属于哪个账户、是不是欺诈 —— 只存计数器就死定了。

### 两遍扫描

```python
setup_kinds = {"MERCHANT", "THRESHOLD", "FRAUD_CODES", "MIN_COUNT", "STICKY"}
for line in lines:                # 第一遍：只处理 setup
    if kind(line) in setup_kinds: apply_setup(line)
for line in lines:                # 第二遍：只处理事件
    if kind(line) not in setup_kinds: apply_event(line)
```

题面明确说 setup "applied **before** any event, wherever they appear"。
单遍循环按出现顺序处理会挂。

### Part 1 — 解析 setup

**唯一的难点：靠字面量的形状区分计数和比例。**

```python
def parse_threshold(lit: str):
    if "." not in lit:
        return ("count", int(lit), 1)
    whole, frac = lit.split(".")
    den = 10 ** len(frac)
    return ("ratio", int(whole) * den + int(frac or 0), den)   # 0.25 → (25, 100)
```

`1.0` 是**比例**（100% 欺诈才触发），`1` 是**计数**（一笔就触发）。
存成 `num/den` 的整数对，全程不碰浮点。

### Part 2 — 累计

```python
def apply_charge(cid, acct, code):
    if cid in charges and charges[cid].alive:      # 重复 id → 忽略（幂等）
        return
    ch = Charge(acct, code in fraud_codes)
    charges[cid] = ch
    totals[acct] += 1
    frauds[acct] += ch.is_fraud
```

- 未知码 = 非欺诈。
- 没有 `MERCHANT` 行的账户**照样计数**（Part 2 要输出它），只是永远不判定。

### Part 3 — 判定

```python
def is_fraudulent(acct) -> bool:
    mcc = merchant_mcc.get(acct)
    if mcc is None:            return False        # 没有 MERCHANT 行
    th = thresholds.get(mcc)
    if th is None:             return False        # MCC 没有阈值
    total = totals[acct]
    if total == 0:             return False        # 全被撤销了 → 不判定，不是 0/0
    kind, num, den = th
    if kind == "count":
        return frauds[acct] >= num                 # 非严格
    return total >= min_count and frauds[acct] * den >= num * total   # 整数交叉相乘 ★
```

**★ `frauds * den >= num * total`** —— 这一行是整道题的核心。
用 `frauds/total >= num/den` 的浮点写法，在 `1/3` vs `0.33` 上就错了。

### Part 4 — 撤销

```python
def apply_dispute(cid):
    ch = charges.get(cid)
    if ch is None or not ch.alive:     # 未知 id / 重复撤销 → no-op
        return
    ch.alive = False
    totals[ch.account] -= 1
    frauds[ch.account] -= ch.is_fraud
```

和 `apply_charge` **逐字对称**。

### Part 5 — 边界（题面列出的全部）

见下面的「坑」。

---

## 坑（隐藏测试专门抓的）

1. **`>=` 不是 `>`**：计数阈值 2、恰好 2 笔欺诈 → 标记。比例 0.5、恰好 1/2 → 标记。
2. **`1.0` 是比例，`1` 是计数。** 判据是小数点，不是值。
3. **`total == 0` 不判定**（全部被 dispute 之后），不是除零，也不是"比例为 0"。
4. **撤销一笔非欺诈的 charge 会让比例上升**，可能把账户推**过**阈值。反直觉，必测。
5. **重复 `DISPUTE` 同一个 id → no-op**（不是再减一次）。
6. **`DISPUTE` 未知 id → 忽略**（不是报错）。
7. **`MIN_COUNT` 只作用于比例阈值**，计数阈值没有量的门槛。门槛用 `>=`。
8. **没有 `MERCHANT` 行 / MCC 没有 `THRESHOLD` 的账户**：Part 2 要输出，判定时永不标记。
9. **输出 `NONE` 而不是空行。**
10. **普通字符串序**：`acct_10` 排在 `acct_2` **前面**。
11. **`STICKY`**：一旦标记过就永久在输出里，即使后来被撤销回来。是完全不同的一套输出。
12. 澄清（仓库的 adversarial review）：一个 charge id 被 dispute 之后**再次出现**，算**新的一笔**；
    重复一个仍然存活的 id 才是忽略。

---

## 变体（题面 "Variants" 一节）

- **3-part 版**（linkjob 2025-09、extrabrain 2026-02）：P1 计数阈值、P2 比例+最小量且**永久标记**、
  P3 dispute 把该笔**标为非欺诈**但**不移出总数**（`dispute_removes_charge=False`）。
- 计数阈值用严格 `>`（"exceeds"）的说法也出现过。本仓库主线用 `>=`，
  代码里留了一个常量可切换 —— **规格含糊时就该这么做**。

---

## Code Core 节点

`round.reading` · `input.line-protocols` · `input.numbers` · `model.records` · `model.entity-state` ·
`model.event-stream` · **`model.reversal`** · **`model.idempotency`** · **`rules.thresholds`** ·
**`rules.exact-ratio`** · `output.ordering` · `output.sentinels` · `correctness.edge-catalog`

---

## 自测清单（写完逐条跑）

- [ ] 题面三个 worked example，逐字节
- [ ] 计数阈值：`N-1` / `N` / `N+1` 三个用例
- [ ] 比例阈值：恰好 1/2 vs 0.5
- [ ] `1/3` vs `0.33`（应为**上方**）和 vs `0.34`（下方）
- [ ] `MIN_COUNT` 恰好命中 / 差一
- [ ] 全部 dispute 后 total = 0
- [ ] dispute 一笔非欺诈 → 比例上升 → 新标记
- [ ] 重复 dispute / 未知 id dispute
- [ ] 无 MERCHANT 行的账户出现在 PART 2、不出现在默认输出
- [ ] 空输入 → `NONE`
- [ ] `acct_10` / `acct_2` 的排序
- [ ] STICKY 开 / 关两套输出
