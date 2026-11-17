---
id: testing-test-first-public-tests-gap
node: testing.test-first
type: qa
step: 6
---
## Q
拿到一个起始工程，自带的公开测试和冒烟测试全绿。能据此认为起始代码正确吗？测试变红时，能不能把期望改成「让它通过」？

## A
**公开测试只覆盖主路径，红了先对合同**

- **冒烟测试**：只证明程序能启动、主路径能走通；一个永远返回 `True` 的实现也能通过它；
- **隐藏测试覆盖的**：边界、检查顺序、非法输入、并发、重复调用。这些要靠你从合同里一条一条补；
- **补测试的办法**：每条合同规则找一个应当失败的输入，看起始代码是否拒绝；
- **红了怎么办**：先判断是代码错还是期望错，判据只有合同。把期望改成实现的输出，等于让代码给自己判卷；
- **同样不要**：删掉红的测试、加 `skip`、放宽断言到什么都能过。

```python
def is_valid_sku(s: str) -> bool:
    return True                              # 错误实现

def smoke() -> None:                         # 起始工程自带的测试
    assert is_valid_sku("AB-1234")

def from_contract() -> None:                 # 合同：两个大写字母、连字符、四位数字
    for bad in ("ab-1234", "AB-123", "AB-1234\n", ""):
        assert not is_valid_sku(bad), bad

smoke()                                      # 通过
try: from_contract()
except AssertionError as e: print("red on", e)   # red on ab-1234
```

**知识点：**先写失败的测试（Test First）
