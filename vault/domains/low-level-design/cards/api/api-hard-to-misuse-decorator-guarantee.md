---
id: api-hard-to-misuse-decorator-guarantee
node: api.hard-to-misuse
type: qa
step: 5
---
## Q
定时付款服务要求“任何公开操作开始前，先把到期的付款结算掉”。每个方法开头手写一行 `self._settle()`，以后有人新加一个方法忘了写，会发生什么？怎样让这条规则不依赖记忆？

## A
**把必须发生的步骤放进装饰器，不放进每个方法**

- **手写的约定会漏**：第 7 个方法忘了结算，读到的是过期的余额，测试多半覆盖不到；
- **装饰器包住公开入口**：`@settles` 标在方法上，新方法要么标、要么明显地没标，评审时一眼可见；
- **更彻底**：用一个只暴露公开方法的外观类，或者类装饰器统一包住所有以非下划线开头的方法；
- **`functools.wraps`**：保留原函数的名字和文档，否则调试信息里全是 `wrapper`；
- **同样的做法适用于**：加锁、记日志、计时、权限检查这类“每个入口都必须做”的事。

```python
import functools

def settles(method):
    @functools.wraps(method)
    def wrapper(self, *a, **kw):
        self._settle()                               # 每个公开入口先结算
        return method(self, *a, **kw)
    return wrapper
class Bank:
    def _settle(self): print("settle")
    @settles
    def balance(self): return 100

print(Bank().balance(), Bank.balance.__name__)       # settle / 100 balance
```

**知识点：**难以用错的接口（Hard to Misuse）
