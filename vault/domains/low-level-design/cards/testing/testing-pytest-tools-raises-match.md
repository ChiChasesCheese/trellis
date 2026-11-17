---
id: testing-pytest-tools-raises-match
node: testing.pytest-tools
type: qa
step: 3
---
## Q
测试「超长数字应当报 `invalid_json`」写成 `with pytest.raises(ValueError):`，实现里漏了长度检查，测试仍然是绿的。为什么？怎么写才抓得住？

## A
**`raises` 要带 `match`，且用锚定的正则**

- **`ValueError` 太宽**：漏了长度检查时，`int()` 对 5000 位的数字自己抛 `ValueError`（3.11 的位数上限），测试因为错误的原因通过了；
- **`match` 是 `re.search`**：`match="invalid_json"` 也会匹配 `invalid_json_extra`；写 `match=r"^invalid_json$"`；
- **专用的错误类更好**：`pytest.raises(InvalidJson)`，库抛的 `ValueError` 就不会混进来；
- **检查异常对象**：`with pytest.raises(...) as info:` 之后看 `info.value.args`、自定义属性；
- **反面也要测**：合法输入不抛异常，直接调用就行，不用包 `raises`，抛了测试自然失败；
- **失败时的样子**：下面的第二个测试红了，输出里同时列出期望的错误消息和实际抛出的库错误消息，一眼就知道是错在哪个环节。

```python
import pytest

def parse_int(s: str) -> int:
    return int(s)                    # 缺陷：漏了 len(s) > 19 的检查

def test_too_long_wide():            # 太宽的写法：错误的原因也通过
    with pytest.raises(ValueError):
        parse_int("9" * 5000)

def test_too_long_exact():
    with pytest.raises(ValueError, match=r"^invalid_json$"):
        parse_int("9" * 5000)

if __name__ == "__main__":
    pytest.main([__file__, "-q", "-p", "no:cacheprovider"])    # 1 failed, 1 passed
```

**知识点：**pytest 的常用工具（pytest Toolkit）
