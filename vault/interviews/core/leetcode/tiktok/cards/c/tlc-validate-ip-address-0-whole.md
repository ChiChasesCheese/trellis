---
id: tlc-validate-ip-address-0-whole
node: c.validate-ip-address
type: qa
---
## Q
**LC 468 验证 IP 地址**｜Medium · LC TikTok 全时段热度 25/100 · CodeTop 国内累计 17 次 · 最近 2025-08-22（国内 CodeTop）

给定字符串 `queryIP`，如果是有效 IPv4 返回 `"IPv4"`，有效 IPv6 返回 `"IPv6"`，都不是返回 `"Neither"`。有效 IPv4 是 `x1.x2.x3.x4`，每段 `0 <= xi <= 255` 且不能有前导零（`192.168.01.1`、`192.168.1.00` 无效）。有效 IPv6 是 `x1:x2:x3:x4:x5:x6:x7:x8`，每段 `1 <= xi.length <= 4`，是十六进制字符串（数字、`a-f`、`A-F`），允许前导零（`2001:0db8:85a3::8A2E:037j:7334` 与 `02001:...` 无效）。`queryIP` 只含英文字母、数字、`.` 和 `:`。例：`"172.16.254.1"` → `"IPv4"`；`"2001:0db8:85a3:0:0:8A2E:0370:7334"` → `"IPv6"`；`"256.256.256.256"` → `"Neither"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按分隔符数量判断类型，切成段后逐段校验规则：IPv4 每段是不带前导零的 0 到 255，IPv6 每段是 1 到 4 位十六进制。

**识别。** 「格式校验」：把规则拆成「段数」加「每段合法性」，用分隔符的个数决定走哪条分支。核心是写全边界：空段、前导零、非法字符、段数不对。

**推导。** 用 `.` 的个数为 3 判断可能是 IPv4，`:` 的个数为 7 判断可能是 IPv6，其他直接 `Neither`。切开之后逐段检查：IPv4 段必须全是 ASCII 数字、长度 1 到 3、不以 `0` 开头（除非就是 `"0"`）、值不超过 255；IPv6 段长度 1 到 4、每个字符都在十六进制字符集中。

```python
from string import hexdigits


def valid_ip_address(queryIP: str) -> str:
    def is_ipv4_part(part: str) -> bool:
        return (
            part.isascii() and part.isdigit()    # 只允许 ASCII 数字（isdigit 对 "²" 之类也会为真）
            and len(part) <= 3
            and (part == "0" or part[0] != "0")  # 不允许前导零
            and int(part) <= 255
        )

    def is_ipv6_part(part: str) -> bool:
        return 1 <= len(part) <= 4 and all(ch in hexdigits for ch in part)   # 允许前导零

    if queryIP.count(".") == 3:
        parts = queryIP.split(".")
        if all(map(is_ipv4_part, parts)):
            return "IPv4"
    elif queryIP.count(":") == 7:
        parts = queryIP.split(":")
        if all(map(is_ipv6_part, parts)):
            return "IPv6"
    return "Neither"
```

运行：`"172.16.254.1"` → `"IPv4"`，`"2001:0db8:85a3:0:0:8A2E:0370:7334"` → `"IPv6"`，`"256.256.256.256"` → `"Neither"`；`"192.168.01.1"` → `"Neither"`，`"1.1.1.1."` → `"Neither"`，`"2001:0db8:85a3::8A2E:037j:7334"` → `"Neither"`，`"::1"` → `"Neither"`（段数不足）。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（切出的段）。

**拓展优化。**
- 正则一行搞定，用 `re.ASCII` 避免 `\d` 匹配非 ASCII 数字：

```python
import re

V4_PART = r"(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
V4 = re.compile(rf"{V4_PART}(?:\.{V4_PART}){{3}}")
V6 = re.compile(r"[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){7}")


def valid_ip_address_re(queryIP: str) -> str:
    if V4.fullmatch(queryIP):
        return "IPv4"
    return "IPv6" if V6.fullmatch(queryIP) else "Neither"
```

- 真实世界的 IPv6 还允许 `::` 压缩和嵌入 IPv4，应使用标准库 `ipaddress.ip_address`；它的规则和这里的定义不同，面试里要说明。

**易错点。**
- 只判断 `int(part) <= 255` 而不管前导零：`"01"` 和 `"1"` 的整数值相同，`192.168.01.1` 会被当成有效。
- `"1.1.1.1."` 末尾多一个 `.`：切出空串，`isdigit` 为假，必须保证空段不通过。
- IPv6 段用 `int(part, 16)` 校验：`"+1"`、`" 1"`、`"1_0"` 之类也能被 `int` 接受，用字符集判断才可靠。

**追问。**
- 支持 `::` 压缩的 IPv6：段数少于 8 且恰好有一个 `::`，补零后再校验。
- 判断 IP 是否属于某个 CIDR 网段：转成整数后比较前缀位，标准库 `ipaddress.ip_network(...).__contains__`。

**同模式。** LC 93 复原 IP 地址、LC 65 有效数字、LC 8 字符串转换整数、LC 929 独特的电子邮件地址、LC 1108 IP 地址无效化。
