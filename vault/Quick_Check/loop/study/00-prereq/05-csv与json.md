# 05 · CSV 与 JSON：两种最常见的输入/输出格式

> 电面 / integration 轮 / bug squash 里，数据要么是 CSV 文件，要么是 JSON（API 的请求和响应）。这两种都有标准库，**不要手写解析器**——除非题目明确说"不能用库"。

## 1. CSV

### 1.1 为什么不能 `line.split(",")`

```
name,city,amount
"Alpha, Inc.",SF,100
```
第二行按逗号拆会得到 4 段。带引号的字段里可以有逗号、换行——只有 `csv` 模块处理得对。

### 1.2 读

```python
import csv
import io

text = 'name,city,amount\n"Alpha, Inc.",SF,100\nBeta,NY,50\n'

# 方式一：reader —— 每行是 list
rows = list(csv.reader(io.StringIO(text)))
# [['name','city','amount'], ['Alpha, Inc.','SF','100'], ['Beta','NY','50']]
header, body = rows[0], rows[1:]

# 方式二：DictReader —— 每行是 dict（第一行自动当表头）
for r in csv.DictReader(io.StringIO(text)):
    print(r["name"], int(r["amount"]))
```

- `io.StringIO(text)`：把字符串包成"文件"，csv 只认文件对象。真文件用 `open(path, newline="")`（`newline=""` 是 csv 文档要求的固定写法）。
- 从 stdin 读：`csv.reader(sys.stdin)`。
- **所有值都是字符串**，数字要自己 `int()`。
- 分隔符不是逗号：`csv.reader(f, delimiter="|")` 或 `"\t"`。
- 空行：`csv.reader` 会产出 `[]`，要 `if not row: continue`。
- 列数不齐：自己检查 `len(row)`；`DictReader` 少列给 `None`，多列塞到 key `None`。

### 1.3 写

```python
buf = io.StringIO()
w = csv.writer(buf)
w.writerow(["name", "total"])
w.writerow(["Alpha, Inc.", 100])       # 自动加引号
print(buf.getvalue())                  # 注意：行尾是 \r\n（csv 默认）

# 要 \n 结尾：
w = csv.writer(buf, lineterminator="\n")

# DictWriter
w = csv.DictWriter(buf, fieldnames=["name", "total"], lineterminator="\n")
w.writeheader()
w.writerow({"name": "Beta", "total": 50})
```

**面试坑**：题目要求输出逐字节一致时，`csv.writer` 默认的 `\r\n` 会挂。要么设 `lineterminator="\n"`，要么自己 `",".join(...)`（前提是字段里没有逗号）。

### 1.4 CSV 题的标准骨架

```python
def load(path_or_file) -> list[dict]:
    out = []
    for r in csv.DictReader(path_or_file):
        r = {k.strip(): (v or "").strip() for k, v in r.items() if k is not None}
        if not r.get("id"):
            continue                     # 或者记录一条错误
        r["amount"] = int(r["amount"])
        out.append(r)
    return out
```

## 2. JSON

### 2.1 JSON ↔ Python 对照

| JSON | Python |
|---|---|
| `{"a": 1}` object | `dict` |
| `[1, 2]` array | `list` |
| `"s"` string | `str` |
| `1` / `1.5` number | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### 2.2 读写

```python
import json

text = '{"id": "ch_1", "amount": 1250, "refunded": false, "metadata": {"order": "o_9"}, "tags": ["a","b"]}'
obj = json.loads(text)             # 字符串 → Python 对象（loads = load string）
obj["amount"]                      # 1250
obj["metadata"]["order"]           # "o_9"
obj["tags"][0]                     # "a"
obj.get("missing")                 # None，不报错

json.dumps(obj)                    # Python 对象 → 字符串（一行）
json.dumps(obj, indent=2)          # 美化
json.dumps(obj, sort_keys=True)    # key 排序，输出才确定
json.dumps({"n": 1}, separators=(",", ":"))   # 最紧凑

with open("x.json") as f:          # 文件
    obj = json.load(f)             # load 没有 s = 从文件
with open("out.json", "w") as f:
    json.dump(obj, f, indent=2)
```

- 中文/非 ASCII：`json.dumps(obj, ensure_ascii=False)`，否则会变成 `\uXXXX`。
- `json.dumps` 不认 `Decimal`、`datetime`、`set`、dataclass：先转成 str / list / `dataclasses.asdict(x)`。
- 坏 JSON：`json.JSONDecodeError`（是 `ValueError` 的子类）。

### 2.3 安全地深挖嵌套

```python
# 想要 obj["charges"]["data"][0]["amount"]，但任何一层都可能缺
def dig(obj, *path, default=None):
    cur = obj
    for p in path:
        if isinstance(cur, dict):
            cur = cur.get(p)
        elif isinstance(cur, list) and isinstance(p, int) and 0 <= p < len(cur):
            cur = cur[p]
        else:
            return default
        if cur is None:
            return default
    return cur

dig(obj, "charges", "data", 0, "amount", default=0)
```

### 2.4 JSON Lines（每行一个 JSON）

日志、事件流常用：
```python
events = [json.loads(line) for line in text.splitlines() if line.strip()]
```

### 2.5 Stripe 风格的 JSON 长什么样（integration 轮会见到）

```json
{
  "id": "pi_3Abc",
  "object": "payment_intent",
  "amount": 1250,
  "currency": "usd",
  "status": "requires_payment_method",
  "metadata": {"order_id": "o_1"},
  "created": 1700000000
}
```
列表响应：
```json
{"object": "list", "data": [ {...}, {...} ], "has_more": true, "url": "/v1/charges"}
```
错误响应：
```json
{"error": {"type": "invalid_request_error", "code": "resource_missing", "message": "No such charge", "param": "id"}}
```
写客户端时先 `if "error" in body:`，再拿 `body["data"]` 循环，`has_more` 为真就带 `starting_after=最后一个 id` 再请求（分页，见第 06 章）。

## 3. 练习

`exercises/ex05_csv_json.py`：
1. `read_csv_text(text) -> list[dict]`：用 `csv.DictReader`；去掉 key/value 两侧空白；`amount` 转 int；跳过没有 `id` 的行。
2. `write_csv_rows(rows, fieldnames) -> str`：用 `DictWriter`，`\n` 结尾，带表头。
3. `parse_events_jsonl(text) -> list[dict]`：跳过空行，坏行跳过（不抛异常）。
4. `dig(obj, *path, default=None)`。
5. `summarize_list_response(body) -> tuple[int, str | None]`：Stripe 风格列表响应 → `(data 里 amount 总和, 最后一个 id 或 None)`；`body` 里有 `error` 时返回 `(0, None)`。

`python -m pytest test_ex05.py -q`

## 4. 自查

- [ ] CSV 永远用 `csv` 模块，写的时候记得 `lineterminator="\n"`
- [ ] `loads`/`dumps` 是字符串，`load`/`dump` 是文件
- [ ] JSON 里的 `null` 是 `None`，用 `.get()` 防 KeyError
- [ ] 输出 JSON 要确定性就 `sort_keys=True`
