---
id: craft-descriptors-where-they-earn-5-scales-declare-in-schema
node: craft.idioms.descriptors-where-they-earn
type: qa
step: 5
---
## Q
**描述符 · 从字段描述符到 schema 里的约束声明**｜写法

库存服务里「数量必须为正整数」这类规则，如果每个接口处理函数各自手写检查，迟早不一致。系统级的做法是把约束声明在 schema（JSON Schema、protobuf 的校验注解）里，由统一的校验器执行。它和字段描述符是同一个想法吗？

## A
**要点。** 是同一个想法在不同层级：约束作为数据声明在字段旁边，执行代码只写一次。进程内，描述符或共享校验函数把规则挂在字段上；系统级，schema 把规则写成数据，所有入口（HTTP、消息队列、批量导入）共用同一个校验器，网关、服务端、客户端生成的代码还可以共用同一份 schema。

```python
from typing import Any

# schema 是数据：约束声明一处，所有入口共用同一个校验器
SCHEMA: dict[str, dict[str, Any]] = {
    "qty":   {"type": int, "minimum": 1},
    "cents": {"type": int, "minimum": 0},
    "sku":   {"type": str, "min_length": 1},
}

def validate(doc: dict[str, Any]) -> list[str]:
    errors = []
    for field, rule in SCHEMA.items():
        if field not in doc:
            errors.append(f"{field}: required")
            continue
        v = doc[field]
        if type(v) is not rule["type"]:
            errors.append(f"{field}: expected {rule['type'].__name__}")
        elif "minimum" in rule and v < rule["minimum"]:
            errors.append(f"{field}: must be >= {rule['minimum']}")
        elif "min_length" in rule and len(v) < rule["min_length"]:
            errors.append(f"{field}: too short")
    return errors

print(validate({"qty": 2, "cents": 500, "sku": "a-1"}))
print(validate({"qty": 0, "cents": "5", "sku": ""}))
print(validate({"qty": 1}))
```

实际输出：

```
[]
['qty: must be >= 1', 'cents: expected int', 'sku: too short']
['cents: required', 'sku: required']
```

**变化。** 数据作为 schema 带来三点：一次返回所有错误（而不是遇到第一个就抛）；约束可以被文档、测试、其他语言的客户端读取；改规则不改代码。代价是 schema 能表达的有限，跨字段规则（结束时间晚于开始时间）和需要查库的规则（账户是否存在）还是要写代码，所以 schema 校验管形状，业务校验管含义。

**信号。** 同一个约束在多个入口手写，或需要给调用方返回完整的错误列表：声明在 schema 里。规则只在一个类里：不要为它设计框架。
