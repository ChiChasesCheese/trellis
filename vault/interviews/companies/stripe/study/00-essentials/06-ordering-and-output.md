# 06 · 排序、tie-break、字节级输出

> 这一章的所有内容都属于"算对了还是会挂"的范畴。53 道题里 `fmt` 标记的测试有 60 个，
> 全部集中在这一章。

---

## 1. 排序键写成一个元组

```python
rows.sort(key=lambda r: (-r.score, r.name, r.id))
```

读法：score 降序 → name 升序 → id 升序。**元组比较是逐位短路的**，
第一位分出胜负就不看后面。

**混合方向的三种写法**：

| 情况 | 写法 |
|---|---|
| 数值降序 | 取负：`-r.score` |
| 字符串降序 | 不能取负 → 多趟稳定排序，或 `cmp_to_key` |
| 布尔降序（True 在前） | `not r.flag`（False < True） |
| `None` 排在最后 | `(r.x is None, r.x)` |

**多趟稳定排序**（从最次要的键开始，每趟一个键）：

```python
rows.sort(key=lambda r: r.id)                      # 第三键
rows.sort(key=lambda r: r.name, reverse=True)      # 第二键，降序
rows.sort(key=lambda r: r.score, reverse=True)     # 第一键，降序
```

Python 的 `sort` **保证稳定**，所以后一趟不会打乱前一趟已经排好的相对顺序。

**`cmp_to_key`**（元组表达不了的顺序，例如"按自定义优先级表"）：

```python
from functools import cmp_to_key
PRIORITY = {"HIGH": 0, "MED": 1, "LOW": 2}
def cmp(a, b):
    if PRIORITY[a.level] != PRIORITY[b.level]:
        return PRIORITY[a.level] - PRIORITY[b.level]
    return -1 if a.name < b.name else (1 if a.name > b.name else 0)
rows.sort(key=cmp_to_key(cmp))
```

`cmp_to_key` 比元组键慢（每次比较一次 Python 函数调用），10^5 条以内没问题，10^6 条要小心。

---

## 2. 字典序 vs 数值序

```python
sorted(["acct_10", "acct_2", "acct_1"])
# → ['acct_1', 'acct_10', 'acct_2']        ← 这是对的！
```

题面写 **"lexicographically sorted" / "plain string order"** 就是要这个结果。
不要"贴心地"改成数值排序 —— 隐藏测试就是拿 `acct_2` / `acct_10` 来抓这个的。

要数值排序时，题面会说 "sorted by the numeric part" 或者给一个样例透露。
此时：`sorted(ids, key=lambda s: int(s.rsplit("_", 1)[1]))`。

**大小写**：`"Z" < "a"`（大写字母的码点更小）。要不区分大小写就
`key=str.casefold`，但那样 `"a"` 和 `"A"` 平手 —— 需要再加一个 tie-break。

---

## 3. 没说 tie-break 怎么办

**必须自己定一个，并且写注释。** 不确定的输出顺序 = 随机挂测试。

优先级：
1. 题面里出现过的任何唯一标识（id、name）升序。
2. 输入中的出现顺序（"first seen wins"）—— 用 `enumerate` 记录序号当 tie-break 键。
3. 实在没有 → 输出的字符串本身升序。

```python
# 假设：题面未指定同分时的顺序，按 account id 升序（确定性）。
rows.sort(key=lambda r: (-r.score, r.account))
```

**"保持输入顺序"的实现**：Python 的 dict 保证插入序，`sort` 保证稳定，
所以"按分数降序，同分按出现顺序"只需要 `rows.sort(key=lambda r: -r.score)`，
前提是 `rows` 本来就是按出现顺序建的。

---

## 4. 字节级格式

**唯一真相是题面的样例。复制粘贴，不要手敲。**

| 需求 | 写法 | 注意 |
|---|---|---|
| 两位小数 | `f"{x:.2f}"` | 对 float 有舍入风险；金额用 `04` 章的整数写法 |
| 补零 | `f"{n:016d}"` | 卡号、时间 |
| 时间 | `f"{h:02d}:{m:02d}"` | 24:00 是合法输出时要特判 |
| 千分位 | `f"{n:,}"` | 只有题面要求才加 |
| 左/右对齐 | `f"{s:<10}"` / `f"{s:>10}"` | 会产生**尾随空格** |
| 连接 | `",".join(parts)` | 注意 `,` 还是 `, ` |
| 百分比 | `f"{x:.1f}%"` | 先确认是 0–1 还是 0–100 |

**格式化只写在一个地方。** 把它做成函数：

```python
def render(rows) -> list[str]:
    return [f"{r.acct},{r.mcc},{fmt_cents(r.amount)}" for r in rows]
```

改分隔符时只改这一行；散落在 8 个 `print` 里就一定漏。

---

## 5. 空结果与哨兵

**这是三个不同的测试，题面一定说了其中一种：**

```python
if not flagged:
    return ["NONE"]      # ① 输出字面量 NONE
    return [""]          # ② 输出一个空行
    return []            # ③ 什么都不输出
```

读题时专门找这句话。找不到就看样例里有没有空结果的例子。都没有 → 写注释声明假设，
并把三种做成一个常量方便切换。

**错误行也是输出契约的一部分**：`REJECTED:acct_1`、`ERROR: unknown currency`、
`INVALID` —— 冒号后有没有空格、大小写，都要和样例一字不差。

---

## 6. 末尾换行

```python
print("\n".join(lines))                 # 末尾有一个 \n
sys.stdout.write("\n".join(lines))      # 末尾没有 \n
sys.stdout.write("\n".join(lines) + "\n")
```

**空输出时的区别**：`print("")` 会输出一个空行；`sys.stdout.write("")` 什么都不输出。
如果正确答案是"什么都不输出"，用 `print` 就多了一个空行 → 挂。

安全写法：

```python
out = render(result)
if out:
    stdout.write("\n".join(out) + "\n")
```

---

## 7. 常见格式陷阱清单

- [ ] 分隔符：`,` 还是 `, `？（看样例）
- [ ] 小数位数固定吗？`0` / `0.0` / `0.00` 是三个不同的字符串
- [ ] 负零：`-0.00` 应该输出成 `0.00` 吗？
- [ ] 大整数有没有变成科学计数法？（float 会，int 不会 —— 又一个不用 float 的理由）
- [ ] 布尔怎么输出？`True` / `true` / `1` / `YES`
- [ ] 列表怎么连接？空列表连接出来是空串，符合预期吗？
- [ ] 有没有尾随空格？（对齐格式化会产生）
- [ ] 末尾换行符对吗？
- [ ] Windows 换行 `\r\n` 有没有混进来？（`splitlines()` 会处理输入侧）

---

## 8. 逐字节对照的自查

```python
expected = """acct_a,5411,count,2
acct_b,5812,ratio,0.5
acct_c,5411,count,2"""
actual = "\n".join(part1(lines))
assert actual == expected, f"\n got: {actual!r}\nwant: {expected!r}"
```

用 `repr` 是关键：尾随空格、`\r`、全角空格、不间断空格，肉眼一律看不出来。

差异定位到具体行：

```python
for i, (a, b) in enumerate(zip(actual.split("\n"), expected.split("\n"))):
    if a != b:
        print(f"line {i}: {a!r} != {b!r}", file=sys.stderr)
```
