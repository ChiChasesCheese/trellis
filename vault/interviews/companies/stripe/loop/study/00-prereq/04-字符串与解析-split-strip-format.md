# 04 · 字符串与解析：把一行文本变成一条记录

> 每道 Stripe 题的前 10 分钟都是解析。输入长这样：`CHARGE,ch_1,acct_9,1250,US` 或 `acct_1|Alpha Inc.` 或 `en-US, fr-CA;q=0.8`。你要把它拆成字段、转类型、去噪音。

## 1. 常用操作

```python
s = "  CHARGE, ch_1 ,1250 \n"
s.strip()              # 去两端空白（含换行）→ "CHARGE, ch_1 ,1250"
s.lstrip(); s.rstrip()
s.split(",")           # 按逗号拆 → ["  CHARGE", " ch_1 ", "1250 \n"]
s.split()              # 不带参数：按任意空白拆，且自动去空 → ["CHARGE,", "ch_1", ",1250"]
s.split(",", 1)        # 只拆一次（第一段是命令，后面是参数）
"a-b-c".rsplit("-", 1) # 从右边拆一次 → ["a-b", "c"]
",".join(["a", "b"])   # 拼 → "a,b"
s.lower(); s.upper()
s.startswith("CH"); s.endswith("\n")
s.replace(" ", "")
s.find("ch")           # 下标，找不到 -1
"ch_1"[3:]             # 切片 → "1"
s.isdigit()            # 全是数字？（"12"→True，"-1"→False，"1.5"→False）
len(s)
f"{name}:{amount}"     # f-string
```

**每个字段都 `strip()`**：`[f.strip() for f in line.split(",")]`。题目说"字段两侧可能有空格"就是在提示这个。

## 2. 标准解析模板

```python
def parse_line(line: str) -> dict | None:
    line = line.strip()
    if not line:                         # 空行
        return None
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:                  # 字段数不对 → 按题意：跳过 / 报错
        return None
    kind, cid, acct, amount, country = parts
    return {"kind": kind, "id": cid, "acct": acct, "amount": int(amount), "country": country}
```

要点：
1. 先 strip 整行，再 split，再 strip 每段。
2. **解包**：`a, b, c = parts`——段数不对会 `ValueError`，所以先检查 `len`。
3. 类型转换集中在这一处：`int(amount)`。后面的代码就都能放心当数字用。
4. 返回 `None` 表示"这行不算"，调用方 `if rec is None: continue`。

## 3. 多种记录混在一起：按第一个字段分发

```
CHARGE,ch_1,acct_9,1250
DISPUTE,ch_1
REFUND,ch_1,500
```

```python
for line in lines:
    parts = [p.strip() for p in line.strip().split(",")]
    if not parts or not parts[0]:
        continue
    kind = parts[0]
    if kind == "CHARGE":
        _, cid, acct, amount = parts
        ...
    elif kind == "DISPUTE":
        _, cid = parts
        ...
    else:
        ...   # 未知命令：按题意忽略或报错
```

`_` 是"这个值我不要"的惯用名。

## 4. 键值对 / 查询串 / 带参数的字段

```python
# "en-US;q=0.8" → tag="en-US", q=0.8
tag, *params = [p.strip() for p in "en-US;q=0.8".split(";")]
q = 1.0
for p in params:
    if p.startswith("q="):
        q = float(p[2:])

# "a=1&b=2" → {"a": "1", "b": "2"}
kv = dict(pair.split("=", 1) for pair in "a=1&b=2".split("&"))
```

`*params` 是"剩下的都装进列表"。

## 5. 数字与金额

```python
int("1250")            # 1250
int("-5")              # -5
int(" 12 ")            # 12（int 会自己去空白）
int("12.0")            # ValueError！
float("12.50")         # 12.5 —— 但金额别用 float

# 金额字符串 "12.50" → 1250 分（不经过 float）
def to_cents(s: str) -> int:
    s = s.strip()
    neg = s.startswith("-")
    s = s.lstrip("-")
    whole, _, frac = s.partition(".")     # "12.50" → "12", ".", "50"
    frac = (frac + "00")[:2]              # "5" → "50"；"" → "00"
    cents = int(whole) * 100 + int(frac)
    return -cents if neg else cents

# 1250 分 → "12.50"
def fmt_cents(c: int) -> str:
    sign = "-" if c < 0 else ""
    c = abs(c)
    return f"{sign}{c // 100}.{c % 100:02d}"
```

`{c % 100:02d}`：整数、至少两位、不够补 0。`partition` 比 `split(".")` 安全（没有点也不报错）。

## 6. 大小写、空白、Unicode 噪音（normalization）

```python
name = "  Alpha   Inc. "
norm = " ".join(name.split()).lower()      # 压缩内部空白 + 小写 → "alpha inc."
norm = norm.rstrip(".")                    # 去尾部标点
```

原则：**在边界上做一次归一化，后面全部用归一化的值比较；但输出用原始拼写**（题目常说"按 supported 列表里的拼写输出"）。所以要同时保存 `raw` 和 `norm`：`{norm: raw}`。

## 7. 正则（只在 split 不够用时）

```python
import re
m = re.match(r"^(\w+)\s*=\s*(\d+)$", "amount = 42")
if m:
    key, val = m.group(1), int(m.group(2))
re.findall(r"\d+", "a1b22c333")       # ['1', '22', '333']
re.split(r"[,\s]+", "a, b  c")        # ['a', 'b', 'c']
```

`\d` 数字、`\w` 字母数字下划线、`\s` 空白、`+` 一个或多个、`*` 零个或多个、`^` 开头、`$` 结尾。面试里 80% 的题 `split` 就够，正则写错反而慢。

## 8. 输出格式化

```python
f"{x}"            # 原样
f"{x:.2f}"        # 两位小数（只对 float；金额用 fmt_cents）
f"{x:>10}"        # 右对齐宽 10
f"{x:<10}"        # 左对齐
f"{x:08d}"        # 整数补 0 到 8 位
f"{x:,}"          # 千分位 1,234,567
f"{s!r}"          # repr，调试时看清引号和空白
"\n".join(lines)  # 多行输出
```

**输出要"字节级精确"**：多一个空格、少一个换行都挂。最后一定拿题目样例逐字符对比。

## 9. 练习

`exercises/ex04_parsing.py`：
1. `parse_record(line)`：`"CHARGE, ch_1 ,acct_9, 12.50 "` → `{"kind":"CHARGE","id":"ch_1","acct":"acct_9","cents":1250}`；空行 / 字段数≠4 返回 `None`。
2. `to_cents("12.5")==1250`, `to_cents("-0.05")==-5`, `to_cents("7")==700`。
3. `fmt_cents(1250)=="12.50"`, `fmt_cents(-5)=="-0.05"`, `fmt_cents(0)=="0.00"`。
4. `parse_header("en-US, fr;q=0.8 , *;q=0.1")` → `[("en-US",1.0),("fr",0.8),("*",0.1)]`（tag 去空白，q 缺省 1.0，坏 q 当 1.0）。
5. `normalize_name("  Alpha   INC. ")=="alpha inc"`（压缩空白、小写、去尾部句点）。

`python -m pytest test_ex04.py -q`

## 10. 自查

- [ ] strip 整行 → split → strip 每段 → 检查段数 → 解包 → 转类型，顺序固定
- [ ] 金额字符串直接算分，不经过 float
- [ ] 归一化只做一次，输出用原始拼写
- [ ] 输出最后逐字符比对样例
