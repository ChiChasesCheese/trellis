---
id: errors-chaining-add-note
node: errors.chaining
type: qa
step: 2
---
## Q
解析一批数据时，某一行的 `int()` 抛了 `ValueError`，但消息里没有行号。怎么把“第几行、原文是什么”补上去，又不改变异常的类型？

## A
**`add_note` 加上下文，然后原样 `raise`**

- **`e.add_note("row 2: 'x'")`**：给异常追加一条说明（Python 3.11 起），放在 `e.__notes__` 里，回溯会把它印在消息下面；
- **类型和栈都不变**：上层的 `except ValueError` 照常工作，不需要为了加一句话新建一个类；
- **必须裸 `raise`**：不要写 `raise ValueError(f"{e} ...")`，那会换成新对象，原来的栈位置丢了；
- **加的是“在做什么”**：哪一行、哪个用户、哪个文件，不是把原消息再说一遍；
- **仍要换类型的时候**：跨过公开接口，内部类型不该外泄，用 `raise ServiceError(...) from exc`，每层各管各的。

```python
def parse_rows(rows):
    for i, raw in enumerate(rows, 1):
        try: yield int(raw)
        except ValueError as e:
            e.add_note(f"row {i}: {raw!r}")           # 补上下文，类型不变
            raise                                     # 原样继续上抛

try: list(parse_rows(["1", "x"]))
except ValueError as e: print(e.__notes__)            # ["row 2: 'x'"]
```

**知识点：**保留原因（Wrapping & Chaining）
