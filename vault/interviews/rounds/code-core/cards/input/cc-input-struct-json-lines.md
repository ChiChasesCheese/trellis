---
id: cc-input-struct-json-lines
node: input.structured
type: qa
---
## Q
The input mixes JSON record lines like `{"a": 1, "b": 2}` with plain command lines like `MIN a`, in any order. How do you read it?

## A
**Dispatch on the first character, and parse each JSON line on its own.**

```python
for line in lines:
    if line.startswith("{"):
        records.append(json.loads(line))
    else:
        queries.append(line.split())
```

`json.loads` per line, never `json.load` on the whole stream — the stream is not one document. Two details that bite: `{}` is a valid record and must not be treated as absent, and JSON numbers come back as `int` only if they were written without a decimal point (`1` is `int`, `1.0` is `float`), so a spec promising integer values is worth asserting rather than assuming.

## Q zh
输入里以任意顺序混着 `{"a": 1, "b": 2}` 这样的 JSON 记录行和 `MIN a` 这样的命令行。怎么读？

## A zh
**按首字符分派，每一行各自解析 JSON。**

```python
for line in lines:
    if line.startswith("{"):
        records.append(json.loads(line))
    else:
        queries.append(line.split())
```

逐行 `json.loads`，绝不对整个流用 `json.load` —— 这个流不是一个文档。两个会咬人的细节：`{}` 是合法记录，不能当成"不存在"；JSON 数字只有写成无小数点形式才解析为 `int`（`1` 是 `int`，`1.0` 是 `float`），所以题面承诺"整数值"时，值得断言而不是假设。
