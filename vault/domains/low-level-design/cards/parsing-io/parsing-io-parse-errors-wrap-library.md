---
id: parsing-io-parse-errors-wrap-library
node: parsing-io.parse-errors
type: qa
step: 3
---
## Q
解析器要求输入是 ASCII，数字最长十九位。直接写 `raw.decode("ascii")` 和 `int(digits)`，遇到坏字节或超长数字时，抛出的错误为什么不能直接交给调用方？

## A
**库的异常要在边界翻译成自己的错误码**

- **`UnicodeDecodeError` 是 `ValueError` 的子类**：调用方写 `except ValueError` 会误以为它是自己定义的语法错，也可能漏掉它；
- **`int()` 有自己的上限**：3.11 起，十进制字符串超过 4300 位会抛另一个 `ValueError`（信息是库的原文），和你的 `invalid_json` 不是一回事；
- **翻译**：`raise InvalidJson("invalid_json") from None`；`from None` 让 traceback 不再显示库的细节，错误码里也不会漏出「在第几个字节解码失败」；
- **先判长度再转换**：超过十九位的数字一定溢出 64 位，用 `len` 判，不交给 `int()`；
- **范围另说**：十九位以内也可能超 64 位，转换后再比较范围。

```python
class InvalidJson(ValueError): pass

def decode(raw: bytes) -> str:
    try: return raw.decode("ascii")
    except UnicodeDecodeError: raise InvalidJson("invalid_json") from None

def to_int(digits: str) -> int:
    if len(digits) > 19: raise InvalidJson("invalid_json")     # 不让 int() 去碰超长串
    return int(digits)

print(issubclass(UnicodeDecodeError, ValueError))              # True
for f, x in ((decode, b"\xff"), (to_int, "9" * 5000)):
    try: f(x)
    except InvalidJson as e: print(f.__name__, e)
```

**知识点：**解析错误（Parse Errors）
