---
id: api-specs-who-checks
node: api.specs
type: qa
step: 3
---
## Q
前置条件“key 必须存在”该由调用方保证，还是函数自己检查？什么时候把前置条件改写成后置条件？

## A
**公共入口负责检查，内部函数只写前置**

- **公共 API**：面向不可信的调用方，违反前置时抛明确的异常；规格没写错误行为，实现者“做什么都行”，抛得清楚才是最好的“做什么”；
- **内部辅助函数**：前置由上一层保证，用 `assert` 写下来就够；
- **改成后置**：把“key 必须存在”改成“不存在就返回默认值”，函数变成全函数（total），调用方不用先查再取；
- **取舍**：前置越多，调用方越容易写错；后置越宽，实现分支越多，也可能掩盖真正的 bug。

```python
def pop_item(d: dict, key, default=None):
    """Total: a missing key is not an error; returns default."""
    return d.pop(key, default)

def pop_item_strict(d: dict, key):
    """Requires: key in d, else KeyError."""
    return d.pop(key)

cart = {"shirt": 2}
print(pop_item(cart, "hat"), pop_item(cart, "shirt"))     # None 2
```

<details class="pt"><summary>延伸</summary>

购物车“删除一行”这类幂等操作适合全函数：重复删除、并发删除都得到同样的最终状态。创建、支付这类不可重复的操作，保留严格版本，让重复提交暴露出来。

</details>

**知识点：**规格与契约（Specifications）
