---
id: patterns-chain-of-responsibility
node: patterns.behavioral
type: qa
step: 2
---
## Q
什么样的请求形状需要 Chain of Responsibility？它和 decorator 栈（同样是"链式包装器"的外观）有什么不同？

## A
适用场景：请求要沿着一串处理器传递，**每一个都可能处理、转换或拒绝，而且这串处理器的组成和顺序要能配置**——HTTP 中间件（鉴权 → 限流 → 校验）、审批升级（经理 → 总监 → VP）、日志级别过滤。

```python
from typing import Callable

Handler = Callable[[dict], dict | None]

def run_chain(handlers: list[Handler], request: dict) -> dict | None:
    for h in handlers:
        result = h(request)
        if result is None:
            return None
        request = result
    return request
```

Decorator 是给**一个**对象叠加行为；Chain of Responsibility 是让**多个**候选处理器依次获得处理请求的机会，其中任何一个都可能提前终止整个流程。
