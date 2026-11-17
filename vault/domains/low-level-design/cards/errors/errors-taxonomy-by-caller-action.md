---
id: errors-taxonomy-by-caller-action
node: errors.taxonomy
type: qa
step: 1
---
## Q
预约服务要设计自己的异常类。按“哪个模块抛的”分，还是按“调用方要做什么”分？异常到 HTTP 状态码的映射写在哪里？

## A
**按调用方的反应分类，状态码映射集中在一张表**

- **分类的依据是调用方的动作**：改输入重发（`InvalidInput`）、换个对象（`NotFound`）、重读再发（`Conflict`）、稍后再试（`Unavailable`）；按抛出的模块分，调用方还得去猜；
- **一个根，调用方一句 `except` 接住全部预期失败**：`ServiceError`；
- **领域异常不认识 HTTP**：状态码是路由层的事，放一张 `异常类 → 状态码` 的表，换成命令行或队列消费者时领域层不用动；
- **查表沿着继承链往上找**：`ThreadNotFound` 是 `NotFound` 的子类，不用单独登记也得到 404；
- **表里没有的，就是 500**：没预料到的异常一律当缺陷。

```python
class ServiceError(Exception): ...
class InvalidInput(ServiceError): ...
class NotFound(ServiceError): ...
class ThreadNotFound(NotFound): ...
class Conflict(ServiceError): ...

STATUS = {InvalidInput: 400, NotFound: 404, Conflict: 409}

def status_of(exc: Exception) -> int:
    for cls in type(exc).__mro__:                  # 沿继承链找最近的登记项
        if cls in STATUS: return STATUS[cls]
    return 500

print([status_of(e) for e in (InvalidInput(), ThreadNotFound(), Conflict(), KeyError())])   # [400, 404, 409, 500]
```

**知识点：**错误类型体系（Error Taxonomy）
