---
id: cc-input-mal-unknown-vocabulary
node: input.malformed
type: qa
---
## Q
A field must be one of four card networks, and the input may spell it `VISA`, `visa` or `paypal`. Write the check.

## A
**Membership in an explicit set, after the one normalization the statement allows.**

```python
NETWORKS = {"visa", "mastercard", "amex", "discover"}
net = tok.strip().lower()
if net not in NETWORKS:
    return None            # corrupted, per the statement's policy
```

Three things this pins down: the vocabulary is closed (a fifth network is corrupt data, not an extension), the case policy is decided once (`lower()` here only because the statement says case-insensitive), and the *output* spelling is derived separately — usually upper-cased at render time, not stored. Never key state on the raw token: `Visa` and `visa` would become two networks.

## Q zh
某字段必须是四种卡组织之一，而输入里可能写成 `VISA`、`visa` 或 `paypal`。写出检查。

## A zh
**在题面允许的那一次归一化之后，做显式集合的成员判定。**

```python
NETWORKS = {"visa", "mastercard", "amex", "discover"}
net = tok.strip().lower()
if net not in NETWORKS:
    return None            # corrupted, per the statement's policy
```

它钉住了三件事：词汇表是封闭的（第五种卡组织是脏数据而不是扩展）；大小写策略只决定一次（这里用 `lower()` 仅因为题面说不区分大小写）；**输出**拼写是另行推导的 —— 通常在渲染时转大写，而不是存起来。绝不要用原始 token 作状态的 key：`Visa` 和 `visa` 会变成两种卡组织。
