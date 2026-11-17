---
id: parsing-io-recursive-descent-object
node: parsing-io.recursive-descent
type: qa
step: 4
---
## Q
用递归下降解析 JSON 对象 `{"a": 1, "b": 2}` 时，引号、冒号、逗号缺一不可，且不允许尾逗号，对象之后只能结束。函数怎么写，才不会漏掉这些情形？

## A
**每个符号都要「取到并核对」，缺了就拒绝**

- **文法**：`object = "{" [member ("," member)*] "}"`，`member = 键 ":" 值`；
- **逗号放在条目之间**：第二项起先核对 `,`，再读键；尾逗号之后下一个不是键而是 `}`，在读键时被拒绝，不需要为它另写一条规则；
- **哨兵**：token 列表末尾追加几个 `"<EOF>"`，读到末尾时是个明确的、会被拒绝的 token，而不是 `IndexError`；
- **截断**：`{"a":` 之后值的位置是哨兵，被拒绝；缺冒号、缺逗号同理；
- **整体结束**：对象的 `}` 之后必须是哨兵，多出来的内容就是语法错；
- **值在这里简化**：示例把值当作单个 token 原样收下，不递归；真正的解析器在值的位置调用 `parse_value`，对象和数组就此互相递归。

```python
def parse_object(t):                          # t 末尾带三个 "<EOF>" 哨兵
    if t[0] != "{": raise ValueError("invalid_json")
    i, out = 1, {}
    while t[i] != "}":
        if out:
            if t[i] != ",": raise ValueError("invalid_json")
            i += 1
        key, colon, val = t[i:i + 3]
        if key[0] != '"' or colon != ":" or val in (",", ":", "}", "<EOF>"): raise ValueError("invalid_json")
        out[key] = val; i += 3
    if t[i + 1] != "<EOF>": raise ValueError("invalid_json")
    return out
for s in ('{ "a" : 1 , "b" : "x" }', '{ "a" : 1 , }', '{ "a" : 1 } 2', '{ "a" : ', '{ "a" 1 }'):
    try: print(parse_object(s.split() + ["<EOF>"] * 3))
    except ValueError: print(s, "invalid_json")
```

**知识点：**递归下降解析（Recursive Descent）
