---
id: errors-bug-vs-failure-two-kinds
node: errors.bug-vs-failure
type: qa
step: 1
---
## Q
同样是“抛了异常”，缺陷（bug）和预期失败（failure）有什么本质区别？为什么两者必须用不同的方式处理？

## A
**失败是设计内的，缺陷是设计外的**

- **预期失败**：来自外部世界，正常运行就会遇到：输入不合法、文件不存在、网络超时、依赖宕机。它们有合同：约定好的异常类型、状态码、错误码；
- **缺陷**：程序违反了自己的假设，比如调用顺序错、不变量被破坏、`None` 当列表用。正常运行不该出现；
- **处理方式相反**：失败要接住，翻译成合同里的响应；缺陷不接，让它往上冒到顶层，记录完整的栈，返回 500；
- **判别问题**：“调用方换一种做法，这个错能避免吗？”能，就是失败；只有改我们的代码才能避免，就是缺陷；
- **把缺陷当失败处理**：错误被安静地收下，数据已经坏了，还没人知道。

```python
class InvalidInput(Exception): ...

def handle(fn):
    try:
        return 200, fn()
    except InvalidInput as e:
        return 400, str(e)               # 预期失败：有合同，接住
    # 其他异常是缺陷：不接，冒到顶层记日志

def bad_input(): raise InvalidInput("qty")
def buggy(): return {}["k"]

print(handle(lambda: 1), handle(bad_input))     # (200, 1) (400, 'qty')
try: handle(buggy)
except KeyError: print("缺陷冒出来了")
```

**知识点：**缺陷与预期失败（Bugs vs Failures）
