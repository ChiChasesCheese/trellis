---
id: cc-input-lp-optional-trailing-field
node: input.line-protocols
type: qa
---
## Q
`CONNECT <id> <user>` gains an optional third field in Part 3, and `INIT <merchant> <balance>` gains an optional fourth in Part 5. How do you parse them, and what is the trap?

## A
**Unpack with a default, but check the arity *per part*, not as a minimum.**

```python
parts = line.split()
obj = parts[3] if len(parts) > 3 else None
```

The trap: an extra argument that only a later part gives meaning to must be **invalid** in the earlier part. If Part 1's `INIT` silently accepts a third token, a hidden test that feeds a malformed `INIT` expecting it to be ignored will instead see a merchant created. Accepting a superset of the grammar is not leniency — it is a wrong answer on the ignore-path tests.

## Q zh
`CONNECT <id> <user>` 在 Part 3 多出一个可选的第三字段，`INIT <merchant> <balance>` 在 Part 5 多出一个可选的第四字段。怎么解析，坑在哪？

## A zh
**用默认值解包，但参数个数要按部分（per part）检查，而不是只检查下限。**

```python
parts = line.split()
obj = parts[3] if len(parts) > 3 else None
```

坑在于：只有后面部分才赋予意义的额外参数，在前面的部分必须是**非法的**。如果 Part 1 的 `INIT` 默默接受第三个 token，那么一个喂进畸形 `INIT`、期望它被忽略的隐藏测试，就会看到一个商户被创建出来。接受语法的超集不是宽容 —— 那是"忽略路径"测试上的错误答案。
