---
id: parsing-io-diagnostics-library-logging
node: parsing-io.diagnostics
type: qa
step: 2
---
## Q
写一个会被别人引用的库，里面怎么打日志？为什么用 `logger.debug("v=%s", x)` 而不是 f-string，库里又为什么不能调 `logging.basicConfig()`？

## A
**库只发日志，不配置日志；参数交给 logger 延迟格式化**

- **`getLogger(__name__)`**：每个模块一个以包路径命名的 logger，使用者能按包名单独调级别；
- **库里加 `NullHandler`**：保证没人配置日志时不会输出警告；输出到哪里、什么格式，是应用的事；`basicConfig` 在库里调用会抢走应用的配置；
- **`%s` 参数而不是 f-string**：级别不够时 logger 不会去格式化；f-string 在调用前就已经格式化，哪怕这条日志根本不输出；
- **结构化字段**：`extra={"order_id": 7}` 把字段挂在记录上，格式器和 JSON 输出能取到，比拼进消息文本更好检索；
- **级别含义**：DEBUG 排查细节、INFO 正常里程碑、WARNING 可恢复的异常、ERROR 这次操作失败了。

```python
import logging

log = logging.getLogger("shop.pricing")
log.addHandler(logging.NullHandler())              # 库：只加这个
log.setLevel(logging.WARNING)

class Costly:
    calls = 0
    def __str__(self): Costly.calls += 1; return "x"

log.debug("value=%s", Costly())                    # 级别不够：不会调用 __str__
print(Costly.calls)                                # 0
log.debug(f"value={Costly()}")                     # f-string：先格式化再交给 logger
print(Costly.calls)                                # 1
```

**知识点：**日志与诊断输出（Logging）
