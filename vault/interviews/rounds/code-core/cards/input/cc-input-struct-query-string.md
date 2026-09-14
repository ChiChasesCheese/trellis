---
id: cc-input-struct-query-string
node: input.structured
type: qa
---
## Q
A request line is `API: amount=1000&merchant=121212&foo=bar`, values may contain spaces, and no URL-decoding is specified. Parse it.

## A
**Split off the prefix, then split on `&` and on the first `=` of each pair.**

```python
body = line.split(":", 1)[1].strip()
d = {}
for pair in body.split("&"):
    if "=" in pair:
        k, v = pair.split("=", 1)
        d[k.strip()] = v.strip()
```

`split("=", 1)` matters: a value may itself contain `=`. Do **not** reach for `urllib.parse.parse_qs` here — it percent-decodes, turns `+` into a space, and returns lists, none of which the statement asked for. Decode only when the statement says the input is URL-encoded.

## Q zh
一行请求是 `API: amount=1000&merchant=121212&foo=bar`，值里可能有空格，题面没有提到 URL 解码。解析它。

## A zh
**先切掉前缀，再按 `&` 切分，每对按第一个 `=` 切。**

```python
body = line.split(":", 1)[1].strip()
d = {}
for pair in body.split("&"):
    if "=" in pair:
        k, v = pair.split("=", 1)
        d[k.strip()] = v.strip()
```

`split("=", 1)` 很关键：值本身可能含 `=`。这里**不要**用 `urllib.parse.parse_qs` —— 它会做百分号解码、把 `+` 变成空格、并返回列表，这些题面一个都没要求。只有题面说明输入是 URL 编码时才解码。
