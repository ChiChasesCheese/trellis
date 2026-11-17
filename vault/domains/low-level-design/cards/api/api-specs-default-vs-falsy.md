---
id: api-specs-default-vs-falsy
node: api.specs
type: qa
step: 7
---
## Q
配置项“没设置时用默认值”。写成 `env.get("URL") or DEFAULT` 和 `env.get("URL", DEFAULT)`，在规格上差在哪？

## A
**“没设”和“设成空”是两个不同的输入**

- **`or` 看真假**：空串、`0`、空列表都被当成“没设”，调用方明确设成空串的意图被盖掉；
- **`get(key, default)` 看键在不在**：设成空串就原样保留；
- **规格要写清**：缺省指“键不存在”，还是“值为假”；两种都合理，但不能让实现随手挑；
- **同类坑**：`items or []` 会把调用方传入的空列表换成新列表，他以为共享的那个对象不再是同一个；
- 合同说“设了就原样保留”，实现就不要顺手 `strip()` 或补末尾斜杠。

```python
DEFAULT = "http://internal.auth.local"

def base_url_or(env: dict) -> str:
    return env.get("AUTH_URL") or DEFAULT          # 设成 "" 被吞掉

def base_url(env: dict) -> str:
    return env.get("AUTH_URL", DEFAULT)            # 设了就原样

print(repr(base_url_or({"AUTH_URL": ""})), repr(base_url({"AUTH_URL": ""})))
```

**知识点：**规格与契约（Specifications）
