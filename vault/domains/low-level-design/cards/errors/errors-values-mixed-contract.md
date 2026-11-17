---
id: errors-values-mixed-contract
node: errors.exceptions-vs-values
type: qa
step: 6
---
## Q
重置密码的 `reset(user, code)`：码不对返回 `False`，用户不存在却抛 `ValueError`。同一个函数混用两种风格，是不是前后不一致？

## A
**两种风格各管一类情况，并写进合同**

- **码不对是正常结果**：用户输错太常见，调用方马上要分支（提示重试），返回 `False` 比抛异常顺手；
- **用户不存在是调用方的错**：内部调用方拿着一个我们没发过的 id，是前提被破坏，抛 `ValueError`，让它在调试时暴露；
- **不一致的是没写进合同**：文档里要明确“哪些情形返回 `False`，哪些抛什么”，测试逐条钉住；
- **别为了统一而统一**：全抛则日常分支到处是 `try`；全返回 `False` 则把调用方的 bug 和用户输错混成一个值；
- **对外接口另说**：直接面对用户的入口，“用户不存在”和“码不对”要给同样的回答，否则泄露账号是否存在。

```python
class Resets:
    def __init__(self): self.codes = {"u1": "123"}

    def reset(self, user: str, code: str) -> bool:
        if user not in self.codes:
            raise ValueError("unknown user")     # 调用方的错：前提被破坏
        return self.codes[user] == code          # 码对不对：正常结果

r = Resets()
print(r.reset("u1", "123"), r.reset("u1", "999"))   # True False
try: r.reset("nobody", "1")
except ValueError as e: print(e)
```

**知识点：**异常与错误值（Exceptions vs Values）
