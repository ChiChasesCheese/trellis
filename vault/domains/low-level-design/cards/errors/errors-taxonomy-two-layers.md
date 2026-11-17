---
id: errors-taxonomy-two-layers
node: errors.taxonomy
type: qa
step: 3
---
## Q
退货政策服务一行一个请求：格式不对（`abc`）和格式对但政策不允许（超过上限）都是“错误”。要不要分成两个类？谁先检查？

## A
**语法错与策略错是两层，各一个类，语法先于策略**

- **语法错（输入不是合法请求）**：说明上游出了问题，如格式、编码、位数溢出；
- **策略拒绝（合法请求，被规则否决）**：业务正常，这是系统在起作用；
- **分开计数、分开告警**：语法错上升要找上游，拒绝率上升要看规则或活动；混成一个数，两件事都看不清；
- **语法先检查**：连请求是什么都没读懂，谈不上按政策判断；
- **两个类都继承 `ValueError`**：旧代码的 `except ValueError` 仍然有效；代价是别处过宽的 `except ValueError` 会把两层再混起来。

```python
class RequestError(ValueError): ...
class SyntaxProblem(RequestError): ...        # 请求读不懂
class PolicyRejection(RequestError): ...      # 读懂了，规则不允许

def handle(line: str) -> int:
    try: n = int(line)
    except ValueError as e: raise SyntaxProblem(line) from e
    if n > 5: raise PolicyRejection(n)
    return n

for line in ("3", "abc", "9"):
    try: print("ok", handle(line))
    except SyntaxProblem: print("invalid")
    except PolicyRejection: print("rejected")   # ok 3 / invalid / rejected
```

**知识点：**错误类型体系（Error Taxonomy）
