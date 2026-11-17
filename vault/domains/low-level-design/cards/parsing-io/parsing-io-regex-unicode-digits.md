---
id: parsing-io-regex-unicode-digits
node: parsing-io.regex
type: qa
step: 2
---
## Q
订单号只允许十进制数字，校验写成 `re.fullmatch(r"\d+", s)`。为什么 `"٣４"`（阿拉伯-印度数字加全角数字）也通过，后面还会出什么问题？

## A
**`\d` 匹配所有 Unicode 十进制数字，要用 `[0-9]`**

- **事实**：`str` 模式里的 `\d` 对应 Unicode 类别 Nd，阿拉伯-印度数字、全角数字、天城文数字都算；
- **后果**：`int("٣４")` 得到 34，`float("１_0")` 得到 10.0，所以校验通过的值照样能被转换，错误数据悄悄进了系统；
- **写法一**：`[0-9]` 明确只收 ASCII 数字；
- **写法二**：`re.ASCII` 标志让 `\d`、`\w`、`\s` 只认 ASCII；
- **同样的坑**：`\w` 会匹配中文、带重音的字母，用它校验标识符时同样要换。

```python
import re

print(re.fullmatch(r"\d+", "٣４"))             # 被接受
print(int("٣４"))                               # 34
print(re.fullmatch(r"[0-9]+", "٣４"))           # None
print(re.fullmatch(r"\d+", "٣４", re.ASCII))    # None
```

**知识点：**正则表达式（Regular Expressions）
