---
id: testing-pytest-tools-parametrize
node: testing.pytest-tools
type: qa
step: 1
---
## Q
一个函数有八组边界输入要测。写八个 `test_` 函数，或者在一个测试里 `for` 循环断言八次，各有什么问题？`pytest.mark.parametrize` 怎么解决？

## A
**参数化：一张表，每行一个独立的用例**

- **`for` 循环的问题**：第一个断言失败，后面的就不跑了，看不出一共错了几行，也不知道是哪一行（除非自己拼消息）；
- **八个函数的问题**：重复的结构，加一个用例要复制一份；
- **`parametrize`**：每行是一个独立的测试，各自通过或失败，失败信息里带上这一行的参数；
- **`pytest.param(..., id="…")`**：给用例起可读的名字，看报告就知道是哪个边界；
- **表即规格**：期望值和输入并排，读者能一眼看出规则；新增边界只加一行。

```python
import pytest

def expired(days: int) -> bool: return days > 30

@pytest.mark.parametrize("days, want", [
    pytest.param(0, False, id="same-day"),
    pytest.param(30, False, id="day-30-inside"),
    pytest.param(31, True, id="day-31-expired"),
])
def test_expired(days, want):
    assert expired(days) is want

if __name__ == "__main__":
    pytest.main([__file__, "-q", "-p", "no:cacheprovider"])    # 3 passed
```

**知识点：**pytest 的常用工具（pytest Toolkit）
