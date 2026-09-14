---
id: s11-idempotency-dedup
node: stripe.streams
type: qa
---

## Q
题面出现 "a repeated X is ignored"、"duplicate ids"、"a second DISPUTE is a no-op" 这类描述，对应真实世界的哪个概念？去重要在处理之前还是之后判断？"忽略"、"覆盖"、"报错"这三种重复语义怎么区分，id 被释放后再出现算什么？

## A
**为什么考**：对应真实世界的 idempotency key 和 webhook event id。

**怎么识别**：题面出现 "a repeated X is ignored"、"duplicate ids"、"already exists"、
"a second DISPUTE is a no-op"、"double free"。

**标准做法**：用一个 `set` 或 `dict` 记住已见过的 id，**在处理之前**查：

```python
if charge_id in charges:      # 已存在 → 整条忽略，不是覆盖
    continue
charges[charge_id] = Charge(...)
```

**三种不同语义，别混**：
- **忽略**（ignore）：第二次完全不处理，第一次的效果保留。
- **覆盖**（last wins）：第二次替换第一次。题面写 "last one wins if repeated" 时用它。
- **报错**：输出一行错误。

**一个真实的细节**：id 被撤销/释放之后**再次出现**，算新记录还是重复？
不同题不同答案 —— `q01` 的澄清说"被 dispute 过的 charge id 再出现算新的一笔"。
规格没说时，写注释声明假设。
