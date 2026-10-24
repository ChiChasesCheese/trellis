---
id: pl-data-serialization-intro-python
node: data.serialization
type: qa
step: 6
---
## Q
Python 的 `json` 和 `pickle` 各是什么？它们对类型、键和对象重建的处理有什么本质区别？

## A
**`json`**：标准库模块，只处理 JSON 能表达的类型：`dict`、`list`、`str`、数字、`bool`、`None`。它不理解你的自定义类，遇到不认识的类型直接拒绝：

```python
json.dumps({1, 2})   # TypeError: Object of type set is not JSON serializable
json.dumps({1: "a"})  # '{"1": "a"}'   int key becomes a string
json.loads('{"1": 1}') # {'1': 1}       and stays a string on the way back
```

要序列化自定义对象，你得自己转成字典（或写 `default=` 函数）。`json.dumps(float("nan"))` 会输出 `NaN`，这不是合法的 JSON，其他语言的解析器可能拒绝；`allow_nan=False` 可以让它报错。一次本机测量，解码小对象约 415 ns，编码约 570 ns（用 C 加速的 `_json`）。

**`pickle`**：Python 专用的二进制序列化，能序列化几乎任何对象（自定义类、函数引用、循环引用、闭包除外）。它的做法是：一个对象可以通过 `__reduce__` 方法告诉 pickle「怎样重建我」，返回一个（可调用对象，参数）。`pickle.loads` 读到它，就**调用那个可调用对象**。

**心智模型**：`pickle` 数据不是数据，而是一段小程序，由 `loads` 执行。

```python
class Evil:
    def __reduce__(self): return (print, ("code ran during pickle.loads",))
pickle.loads(pickle.dumps(Evil()))   # prints: code ran during pickle.loads
```

真实输出：`code ran during pickle.loads`。这里调用的是无害的 `print`，换成 `os.system` 就是远程代码执行。

**要记住的一点**：`json` 安全但窄；`pickle` 强大但等于执行代码。官方文档的警告是「永远不要 unpickle 不可信的数据」。
