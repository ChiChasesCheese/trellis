---
id: fluency-functions-signature-markers
node: fluency.functions
type: qa
step: 1
---
## Q
`def f(a, b=1, /, c=2, *, d)` 里的 `/` 和 `*` 各把参数分成哪几类？什么时候该用仅位置（positional-only）、什么时候用仅关键字（keyword-only）？

## A
**`/` 之前只能按位置，`*` 之后只能按名字**

- **三个区域**：`/` 之前仅位置，`/` 与 `*` 之间位置或关键字都行，`*` 之后仅关键字；`*` 之后没有默认值的参数（`d`）是必填；
- **仅关键字适合“同类型、易写反、可选”的参数**：`pager(items, page, *, size=20)`，调用处写 `size=2`，不用去查定义，加新选项也不会让旧调用错位；
- **仅位置适合“名字不属于接口”的参数**：内置函数 `len(obj, /)` 就是这样；参数名以后改了，调用方不受影响，参数名也不会和 `**kwargs` 里的键冲突（`def g(name, /, **kw)` 可以收下一个叫 `name` 的关键字）；
- **公共函数的默认选择**：必填的 1 到 2 个按位置，其余可选项用 `*` 隔开；这样加参数是向后兼容的；
- **错误是明确的**：违反位置规则抛 `TypeError`，不会悄悄接收。

```python
def f(a, b=1, /, c=2, *, d):
    return a, b, c, d

print(f(1, d=4), f(1, 2, 3, d=4))            # (1, 1, 2, 4) (1, 2, 3, 4)
for call in ("f(1, 2, 3, 4)", "f(a=1, d=4)", "f(1)"):
    try: eval(call)
    except TypeError as e: print(e)          # 多传位置 / a 不能按名字 / 缺 d

def g(name, /, **kw): return name, kw
print(g("x", name="y"))                      # ('x', {'name': 'y'})
```

<details class="pt"><summary>延伸</summary>

布尔开关放到仅关键字位置，调用处就是 `export(report, include_totals=True)`，而不是看不出含义的 `export(report, True)`。

</details>

**知识点：**函数签名与参数（Function Signatures）
