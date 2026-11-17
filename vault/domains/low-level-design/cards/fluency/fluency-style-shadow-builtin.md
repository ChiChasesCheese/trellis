---
id: fluency-style-shadow-builtin
node: fluency.style
type: qa
step: 4
---
## Q
交易列表接口的函数签名是 `def list_tx(rows, filter=None)`，函数体里还想用内置的 `filter(...)`。这会出什么问题？参数名、变量名撞上内置名字（`filter`、`id`、`type`、`list`）该怎么处理？

## A
**参数名别和内置同名，加后缀或换更具体的词**

- **遮蔽（shadowing）**：函数里 `filter` 指的是参数，内置的 `filter` 在这个作用域里看不见；本想调内置，调到的是参数（可能是 `None`、字典或字符串），报错信息是 `'NoneType' object is not callable`，和真正的原因离得很远；
- **不只是 `filter`**：`id`、`type`、`list`、`dict`、`input`、`sum`、`max`、`min`、`format` 都是常见的撞名；`list = [1]` 之后 `list(x)` 就挂了；
- **改法**：用更具体的名字（`status_filter`、`predicate`、`user_id`、`kind`），或按 PEP 8 加一个下划线后缀（`filter_`、`type_`）；
- **对外的参数名是接口的一部分**：公共函数参数改名会破坏按关键字调用的调用方，所以在第一版就起好名字；
- **让工具拦**：`ruff` 的 `A002`（参数遮蔽内置）和 `A001`（变量遮蔽内置）会报；在 CI 里开着，评审时不用靠人眼找。

```python
def list_tx(rows, filter=None):              # ruff A002：filter 遮住了内置
    return list(filter(lambda r: r["ok"], rows))

try: list_tx([{"ok": True}])
except TypeError as e: print(e)              # 'NoneType' object is not callable

def list_tx_ok(rows, *, status=None):        # 具体的名字，不撞内置
    return [r for r in rows if status is None or r["status"] == status]

print(list_tx_ok([{"status": "paid"}, {"status": "open"}], status="paid"))
```

**知识点：**命名与风格规范（Naming, Style & Linters）
