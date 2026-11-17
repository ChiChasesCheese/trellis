---
id: fluency-style-lint-real-bugs
node: fluency.style
type: qa
step: 3
---
## Q
下面这个函数在 `ruff` 里被标出 `F401`、`A002`、`E722`、`E711`、`B006`。其中哪几条指向的是真正的 bug，什么时候可以破例关掉一条规则？

## A
**多数规则指向真 bug，破例要写理由**

- **`B006` 可变默认参数**：`bucket=[]` 所有调用共享一个列表，是运行期 bug；
- **`E722` 裸 `except:`**：连 `SystemExit`、`KeyboardInterrupt` 也一并吞掉，程序没法被正常终止；写 `except Exception:`，更好的是只捕获预期的异常；
- **`A002` 遮蔽内置**：参数名盖住 `filter` 一类的内置，函数体里再调内置就出错；
- **`E711` 用 `==` 比较 `None`**：`==` 可以被自定义类重写，`x == None` 可能为真；判断 `None` 一律用 `is None`；
- **`F401` 未使用的导入**：多半只是脏代码，但漏掉的名字常常说明有一段逻辑没写完；
- **破例的做法**：行内写 `# noqa: A002  理由`，说明为什么；不要整文件关闭；为兼容旧接口保留 `filter` 参数名就是正当理由；
- **格式类规则**（行宽、引号）不用破例，改规则或交给格式化器。

```python
import os                                     # F401：没用到

def pick(rows, filter=None, bucket=[]):      # A002 + B006
    try:
        return [r for r in rows if r == None]    # E711
    except:                                  # E722
        return bucket

def bad():
    try: raise SystemExit(1)
    except: return "swallowed"               # 连退出信号也吞了
print(bad())                                 # swallowed

class Always:
    def __eq__(self, o): return True
print(Always() == None, Always() is None)    # True False
```

**知识点：**命名与风格规范（Naming, Style & Linters）
