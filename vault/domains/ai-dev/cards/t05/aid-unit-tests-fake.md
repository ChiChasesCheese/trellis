---
id: aid-unit-tests-fake
node: t05.unit-tests
type: qa
step: 2
tags: [考点]
---
## Q
**伪测试 · 只断言实现**｜考点 · 必会

下面这个测试是 agent 写的，覆盖了 `apply_discount`。问题在哪？

```python
def test_apply_discount(mocker):
    spy = mocker.patch("shop.pricing.calc_rate", return_value=0.9)
    assert apply_discount(100, "VIP") == 90
    spy.assert_called_once_with("VIP")
```

## A
| 问题 | 为什么是问题 |
|---|---|
| mock 了 `calc_rate`，返回值是测试自己定的 | `apply_discount` 的核心逻辑（取费率）被替换了；`calc_rate` 错了测试也绿 |
| `assert_called_once_with` | 断言内部调用方式；重构成别的写法测试就红，但行为没变 |
| 只有一个例子 | 没有 0、负价格、未知等级 |

**改法：** 不 mock 内部函数，用真实的费率表；断言返回值；加边界：

```python
@pytest.mark.parametrize("price,tier,expected",
    [(100, "VIP", 90), (0, "VIP", 0), (100, "UNKNOWN", 100)])
def test_apply_discount(price, tier, expected):
    assert apply_discount(price, tier) == expected
```

**检验：** 把 `apply_discount` 里的 `*rate` 改成 `+rate`，新测试应当红。

**出处：** 示例为教学构造；方法依据 Claude Code docs《Best practices》（Give Claude a check to run）
