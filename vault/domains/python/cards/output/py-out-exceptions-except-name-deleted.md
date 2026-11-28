---
id: py-out-exceptions-except-name-deleted
node: output.exceptions
type: qa
step: 3
---
## Q
**except as 的变量去哪了**｜读代码说输出

```python
e = "keep"
try:
    1 / 0
except ZeroDivisionError as e:
    print(e)
try:
    print(e)
except NameError as err:
    print(err)
```

输出什么？

## A
**输出。**
```
division by zero
name 'e' is not defined
```

**为什么。**
- `except ... as e` 把异常绑定到 `e`，`except` 块结束时解释器自动执行 `del e`。
- 这个 `del` 不管原来有没有 `e`：外面那个 `"keep"` 已经被覆盖再被删掉，所以第二次 `print(e)` 是 NameError。
- 想在块外使用异常，必须先赋给另一个名字。

**语言为什么这样设计。**
- 异常对象的 `__traceback__` 引用着栈帧，栈帧又引用着局部变量，包括这个 `e` 自己：形成引用环，对象要等垃圾回收才释放。结束时删掉名字就打破了环，让内存及时回收（Python 3 的规定）。
- Java 的 catch 参数天然只在块内可见；Python 的作用域是函数级，所以只能靠 `del` 模拟。

**怎么写才对。**
```python
except ZeroDivisionError as e:
    saved = e          # 需要块外使用时，另存一个名字
```

**面试里一句话。**
Python deletes the `except ... as e` name at the end of the block to break the exception-traceback reference cycle, so copy it if you need it later.
