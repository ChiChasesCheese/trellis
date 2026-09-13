# q14 · 数据集 Join（把旧处理商的导出合并进 Stripe 客户数据）

> `problems/q14_join_dataset/` · 3 个 part
> **主题：没有算法，只有 CSV 纪律、确定性排序和精确输出。**

## 一句话题意

给两份 CSV（客户表、处理商表）和一个 join 字段名，做内连接 / 左连接 / 一对多，
输出「客户表全部列 + 处理商表全部列」的 CSV。

## API 与输入协议

```python
join_dataset(field_name, customer_csv, processor_csv, skip_unmatched=True) -> str
```

stdin 协议：

```
JOIN <field_name> <true|false>        第三个 token 是 skip_unmatched
<客户 CSV，含表头>
---
<处理商 CSV，含表头>
```

表头名和单元格值都 `strip()`；CSV 内的空行忽略；行短于表头则补空串，长于表头则截断；
匹配是 **strip 之后精确、大小写敏感**。

**输出列顺序 = 客户表全部列 + 处理商表全部列**（join 列因此出现两次，每边一次）。

## 核心考点

`S02` CSV 解析（引号内的逗号） · `S03` 按 id 建索引 · `S04` 分组 · **`S08` 完整 tie-break** ·
`S09` 精确格式（CSV 引用规则） · `S18` 错误路径 · `S19` 增量

## 解题思路

```python
import csv, io
def rows_of(text):
    r = list(csv.reader(io.StringIO(text)))
    r = [row for row in r if any(c.strip() for c in row)]      # 去空行
    header = [c.strip() for c in r[0]]
    body = []
    for row in r[1:]:
        row = [c.strip() for c in row]
        row = (row + [""] * len(header))[:len(header)]          # 补齐 / 截断
        body.append(row)
    return header, body
```

**索引 + 连接**：

```python
idx = defaultdict(list)
for j, prow in enumerate(prows):
    idx[prow[pkey]].append((porder(j), j, prow))               # 处理商侧按 (order, 位置) 排
for k in idx: idx[k].sort()

out = []
for i, crow in enumerate(crows):
    matches = idx.get(crow[ckey], [])
    if matches:
        for _, _, prow in matches:  out.append((corder(i), i, crow + prow))
    elif not skip_unmatched:
        out.append((corder(i), i, crow + [""] * len(pheader)))  # 左连接补空
out.sort(key=lambda t: (t[0], t[1]))                            # 稳定 → 处理商侧顺序保住
```

**排序键（四级）**：客户表的 `order` 列（**数值**升序）→ 客户行的输入位置 →
处理商表的 `order` 列（数值）→ 处理商行的输入位置。
**没有 `order` 列、或值不是整数时，用输入位置代替** —— 所以输出永远确定。

**错误路径**：`field_name` 不是**两边**的列 → 抛 `ValueError("missing join column '<field_name>'")`；
`main()` 把它打到 stderr、退出码 1、**stdout 什么都不输出**。空文件（连表头都没有）同样报错。

**输出**：用 `csv.writer` 写，让它处理引用（含 `,` 或 `"` 的值自动加引号）。

## 坑

1. **只有表头的客户文件** → 只有表头的输出（**仍然是两边表头拼起来**）。
2. **引号字段里的逗号和引号必须原样往返**（用 `csv` 模块，别手写 `split(",")`）。
3. 表头名和单元格的**前后空白**要 strip，否则匹配不上。
4. **`order` 按数值排**（`10` 在 `2` 之后），不是字符串排。
5. 平手 → 输入位置（两边各一层）。
6. 左连接的未匹配行补**恰好 `len(处理商表头)` 个**空单元格。
7. 一对多：客户字段在每一行**重复**；客户侧的重复 key 各自独立连接。
8. join 列在输出里**出现两次**（这是题面要求的，不是 bug）。

## Code Core 节点

**`input.delimited`**（CSV / 引号） · **`output.ordering`**（四级 tie-break） ·
`model.index` · `output.formatting` · `input.malformed` · `correctness.determinism`

## 自测清单

- [ ] 只有表头的两边
- [ ] 含逗号 / 含引号的字段往返
- [ ] 表头和值带空白
- [ ] `order` 的数值序（2 / 10）
- [ ] 客户侧平手 / 处理商侧平手
- [ ] 左连接补空的列数
- [ ] 一对多
- [ ] join 列不存在 → stderr + 退出码 1 + stdout 空
