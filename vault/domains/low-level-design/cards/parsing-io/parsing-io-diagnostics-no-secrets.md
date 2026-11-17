---
id: parsing-io-diagnostics-no-secrets
node: parsing-io.diagnostics
type: qa
step: 3
---
## Q
登录失败时打了一条日志 `logger.info("login %s", request)`，其中 `request` 是一个 dataclass，含用户名和密码。日志里为什么出现了密码？怎么既保留诊断价值又不泄露？

## A
**默认的 repr 会展开所有字段，敏感字段要排除**

- **隐蔽的来源**：`%s` 或 `%r` 一个对象，会调用它的 `__str__`、`__repr__`；dataclass 自动生成的 repr 包含全部字段；
- **`field(repr=False)`**：让密码、令牌、卡号不进 repr，对象一被记录就不会带出它们；
- **脱敏**：必须留痕时只留尾号，卡号保留末四位；令牌留前几位用于对账；
- **日志的去向**：日志会被收集、被许多人看、保存很久，比数据库的保护弱得多；
- **异常也一样**：`raise ... from e` 的链里带着原始参数，错误信息里不要拼入请求体。

```python
import logging, sys
from dataclasses import dataclass, field

@dataclass
class Login:
    user: str
    password: str = field(repr=False)             # 不进 repr

logging.basicConfig(stream=sys.stdout, format="%(levelname)s %(message)s", level=logging.INFO)
logging.info("login %s", Login("ann", "hunter2"))     # INFO login Login(user='ann')

def mask(card: str) -> str: return "*" * (len(card) - 4) + card[-4:]
print(mask("4242424242424242"))                       # ************4242
```

**知识点：**日志与诊断输出（Logging）
