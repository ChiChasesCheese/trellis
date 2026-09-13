# q05 · 卡号校验（Luhn · 卡组识别 · `*` 掩码 · `?` 单处损坏）

> `problems/q05_card_validation_luhn/` · 4 个 part
> **主题：先形状后校验的检查顺序 + 掩码上的小规模组合。**

## 一句话题意

判断卡号是否合法（长度+前缀决定卡组，Luhn 决定校验），并在两种残缺输入上做枚举：
`*` 表示被涂掉的一位（数每个卡组有多少种合法补全），
`?` 表示有**恰好一处**错误（一位被改 或 相邻两位被交换），列出所有合法原号。

## 卡组表与 Luhn

| 卡组 | 长度 | 前缀 |
|---|---|---|
| VISA | 16 | `4` |
| MASTERCARD | 16 | `51`–`55` |
| AMEX | 15 | `34` 或 `37` |

Luhn：**从右往左**，第 2、4、… 位加倍，加倍后 > 9 就减 9，全部数位求和，能被 10 整除即合法。

```python
def luhn_ok(num: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(num)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9: d -= 9
        total += d
    return total % 10 == 0
```

## 核心考点

`S02` 两种输入协议 · **`S05` 检查顺序（形状先于校验）** · `S08` 数值序排序 · `S09` 格式 ·
**`S14` 数位遍历 / 通配展开** · **`S15` 掩码组合 / 单编辑枚举** · `S19` P1 ⊂ P2 ⊂ P3/P4 复用

## 解题思路

### Part 1 / Part 2

```python
def network_of(num: str) -> str | None:
    if len(num) == 16 and num[0] == "4":                    return "VISA"
    if len(num) == 16 and "51" <= num[:2] <= "55":          return "MASTERCARD"
    if len(num) == 15 and num[:2] in ("34", "37"):          return "AMEX"
    return None

net = network_of(num)
print("UNKNOWN_NETWORK" if net is None else (net if luhn_ok(num) else "INVALID_CHECKSUM"))
```

**顺序是考点**：形状不匹配就是 `UNKNOWN_NETWORK`，**不管校验和过不过**。
13 位、17 位、16 位 `56…`、15 位 `4…` 全是 `UNKNOWN_NETWORK`。

### Part 3 — `*` 掩码

1–5 个 `*`，暴力枚举 `10^k ≤ 10^5` 完全可行：

```python
from itertools import product
counts = Counter()
holes = [i for i, c in enumerate(masked) if c == "*"]
for combo in product("0123456789", repeat=len(holes)):
    s = list(masked)
    for i, d in zip(holes, combo): s[i] = d
    num = "".join(s)
    net = network_of(num)
    if net and luhn_ok(num): counts[net] += 1
```

输出：每个计数非零的卡组一行 `NETWORK,count`，**按字母序**（AMEX < MASTERCARD < VISA）。

**更快的做法（可选）**：Luhn 是各位贡献之和模 10，每一位的贡献只和"它在右起第几位"有关。
先算已知位的和，再对每个洞做一次 mod-10 的 DP，`O(k·10)` 而不是 `10^k`。
前缀被掩盖时，把每个卡组的合法前缀分别当成约束试一遍。

### Part 4 — `?` 单处损坏

只有两类候选，规模都很小：

```python
cands = set()
n = len(obs)
for i in range(n):                       # ① 改一位
    for d in "0123456789":
        if d != obs[i]:
            cands.add(obs[:i] + d + obs[i+1:])
for i in range(n - 1):                   # ② 交换相邻两位
    if obs[i] != obs[i+1]:               # 相同的两位交换不算错误
        cands.add(obs[:i] + obs[i+1] + obs[i] + obs[i+2:])
res = sorted((c for c in cands if network_of(c) and luhn_ok(c)), key=int)   # 数值序
```

- **去重**：改一位和交换可能产生同一个候选 → 用 `set`。
- **观察到的号本身永远不是答案**（题面说"恰好一处错误"）。
- **数值升序**（`key=int`），不是字符串序。
- 原号可能属于**另一个**卡组。

## 坑

1. **形状检查先于 Luhn。**（Part 2 的头号坑）
2. `50…` / `56…` **不是** MASTERCARD；只有 `51`–`55`。
3. `2223003122003222`、`6011111111111117` 是 Luhn 合法的，但这里只有三个卡组 → `UNKNOWN_NETWORK`。
4. Part 3：掩码长度不匹配任何卡组 → **不输出任何行**；零计数的卡组**省略**。
5. Part 3：**前缀也可能被掩盖**（`**2424242424242` 是 15 位 → 只能是 AMEX，`34`/`37` 各试）。
6. Part 3：5 个 `*` = 10^5 次，不会超时；但要确认你的每次判定是 O(len) 而不是 O(len²)。
7. Part 4：**交换两个相同的数字不算错误**（结果和原号一样）。
8. Part 4：**去重** + **数值序**。
9. Part 4：一个本来就合法的卡号通常没有答案（改任何一位都会破坏 Luhn）。
10. 空行、前后空白、末尾换行。

## 变体

- Part 3 输出写成 `NETWORK: count` 的说法存在；本仓库用 `NETWORK,count`。
- 加 Discover（`6011`/`65`，16 位）作为第四个卡组 —— 在 `NETWORKS` 表加一行即可。
- phone screen 的"日志脱敏"变体：13–16 位的 token 除末 4 位外换成 `x`。

## Code Core 节点

**`algorithms.strings`**（Luhn 数位遍历、单编辑枚举） · **`algorithms.backtracking`**（掩码枚举） ·
`rules.thresholds`（检查顺序） · `output.ordering`（数值序 vs 字典序） · `input.normalization`

## 自测清单

- [ ] 四张 Stripe 测试卡 + 一张改末位的
- [ ] 13 位 / 17 位 / 16 位 `56…` / 15 位 `4…` → `UNKNOWN_NETWORK`
- [ ] Luhn 合法但卡组未知的号
- [ ] Part 3：1 个 `*` / 5 个 `*` / 掩码在前缀上 / 无解
- [ ] Part 3 输出的字母序与零计数省略
- [ ] Part 4：改位与交换产生同一候选（去重）
- [ ] Part 4：相邻相同数字的交换不算
- [ ] Part 4：数值升序（`4000…` vs `40000…` 不同长度不会同时出现，同长度时按 int 比）
