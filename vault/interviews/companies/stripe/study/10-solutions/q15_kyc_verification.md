# q15 · KYC 商户核验（CSV 渐进式校验）

> `problems/q15_kyc_verification/` · 5 个 part
> **主题：一行数据跑一串规则，规则累积，理由码顺序固定。**

## 一句话题意

每行是一个商户的入驻资料（6 列 CSV）。Part n 应用规则 1..n，
**所有规则都要评估**（一行可以有多个理由码），输出 `VERIFIED:` / `NOT VERIFIED:`。

## 输入 / 输出

```
PART n [REASONS]        n ∈ 1..5，缺省 5
business_name,business_profile_name,full_statement_descriptor,short_statement_descriptor,url,product_description
```

- 用 `csv` 模块解析（**引号字段可含逗号**）。
- 第一格等于 `business_name`（大小写不敏感）的行是**表头，跳过**。
- 空行跳过；**缺尾列 = 空**；多余列忽略；**每个值先 trim**。最多 10^5 行。

输出：每行一条，输入序。`VERIFIED: <name>` / `NOT VERIFIED: <name>`。
带 `REASONS` 时：`NOT VERIFIED: Acme (EMPTY_FIELD, DESCRIPTOR_LENGTH)`。

## 五条规则（累积）

| Part | 规则 | 理由码 |
|---|---|---|
| 1 | 六个字段 trim 后都非空 | `EMPTY_FIELD` |
| 2 | `len(full_descriptor)` **5–31 闭区间**（trim 后按字符数） | `DESCRIPTOR_LENGTH` |
| 3 | full descriptor 不得等于黑名单（大小写不敏感、trim、**内部空白折叠**）：<br>`ONLINE STORE` `ECOMMERCE` `RETAIL` `SHOP` `GENERAL MERCHANDISE` | `DESCRIPTOR_BLACKLISTED` |
| 4a | short descriptor **2–10 字符**，且其**第一个词**（大小写不敏感）等于 full 的第一个词 | `SHORT_DESCRIPTOR` |
| 4b | full descriptor **包含** business_name **或** profile_name（大小写不敏感子串；空名字永不匹配） | `NAME_MISMATCH` |
| 5 | url 以 `http://` / `https://` 开头（scheme 大小写不敏感），host（到下一个 `/` `?` `#`）**含点**、**无空白**、**不以点开头或结尾** | `INVALID_URL` |

**理由码固定顺序**：`EMPTY_FIELD, DESCRIPTOR_LENGTH, DESCRIPTOR_BLACKLISTED, SHORT_DESCRIPTOR, NAME_MISMATCH, INVALID_URL`。

## 核心考点

`S02` CSV（引号内逗号） · **`S05` 闭区间阈值** · `S09` 精确输出 · **`S14` 归一化（大小写、空白）** ·
**`S18` 校验与错误路径** · `S19` 增量规则 · `S21` `csv` 模块 · `S24` 领域词汇

## 解题思路

**把每条规则写成一个独立的谓词，按固定顺序收集理由码**：

```python
CHECKS = [                      # (最低 part, 码, 谓词)
    (1, "EMPTY_FIELD",            lambda f: not all(f)),
    (2, "DESCRIPTOR_LENGTH",      lambda f: not (5 <= len(f[2]) <= 31)),
    (3, "DESCRIPTOR_BLACKLISTED", lambda f: collapse(f[2]).upper() in BLACKLIST),
    (4, "SHORT_DESCRIPTOR",       lambda f: not short_ok(f)),
    (4, "NAME_MISMATCH",          lambda f: not name_ok(f)),
    (5, "INVALID_URL",            lambda f: not url_ok(f[4])),
]
def check_row(fields, part=5):
    return [code for p, code, bad in CHECKS if p <= part and bad(fields)]
```

**理由码的顺序天然就是列表顺序** —— 不需要额外排序，也不会漏。
每条只出现**一次**（谓词返回布尔，不是列表）。

`collapse(s)` = `re.sub(r"\s+", " ", s.strip())`，用于黑名单比较（内部空白折叠）。

`url_ok`：

```python
def url_ok(u):
    low = u.lower()
    if not (low.startswith("http://") or low.startswith("https://")): return False
    rest = u.split("//", 1)[1]
    host = re.split(r"[/?#]", rest, 1)[0]
    return "." in host and not re.search(r"\s", host) and not host.startswith(".") and not host.endswith(".")
```

## 坑

1. **纯空白的字段算空**（`"  "`）；每个值**先 trim 再检查**。
2. 长度边界 **4 / 5 / 31 / 32** 逐个测；trim 之后按**字符**数（不是字节）。
3. 黑名单是**整串**比较且大小写不敏感、内部空白折叠：
   `SHOP ACME` **通过**，`shop` 失败，`General  Merchandise`（双空格）**失败**。
4. **引号 CSV**：`"Ed, Inc"`、`"Say ""hi"""`；表头行要跳过。
5. **少于 6 列** → 缺的当空 → `EMPTY_FIELD`。
6. **多条规则同时失败要全部打印**，按固定顺序，每条一次。
7. 空的 business_name 时输出是 `NOT VERIFIED: `（冒号后一个空格，然后什么都没有）。
8. Part n 只跑规则 1..n（Part 1 时 `online store` 是 VERIFIED 的）。
9. url 的反例：`acme.com`（无 scheme）、`ftp://acme.com`、`https://localhost`（无点）、
   `https://.com`（点开头）、`https://acme com`（有空格）。

## Code Core 节点

**`input.delimited`** · **`input.malformed`** · **`input.normalization`** ·
`rules.thresholds`（闭区间长度） · `output.formatting` · `correctness.edge-catalog`

## 自测清单

- [ ] 题面三个 worked example 逐字节
- [ ] 长度 4 / 5 / 31 / 32
- [ ] 黑名单：`SHOP ACME` / `shop` / `General  Merchandise`
- [ ] 引号内逗号、双引号转义、表头行
- [ ] 列数不足 / 超出
- [ ] 六条规则全部失败的那一行（理由码顺序）
- [ ] 空 business_name 的输出形状
- [ ] url 的五个反例
- [ ] Part 1 / Part 3 / Part 5 的不同结论
