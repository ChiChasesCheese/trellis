---
slug: validate-ip-address
---
## Q
**LC 468 验证IP地址**｜Medium

判断 `queryIP` 是 `"IPv4"`、`"IPv6"` 还是 `"Neither"`。IPv4 是 4 段点分，每段 `0` 到 `255` 且无前导零；IPv6 是 8 段冒号分隔，每段 1 到 4 位十六进制，允许前导零。例：`"256.256.256.256"` → `"Neither"`。

## A
**一句话。** 按分隔符数量判断类型，切段后逐段校验：IPv4 每段是不带前导零的 0 到 255，IPv6 每段是 1 到 4 位十六进制。

```python
def valid_ip_address(queryIP):
    def v4(part):
        return (part.isascii() and part.isdigit()  # 仅 ASCII
                and len(part) <= 3
                and (part == "0" or part[0] != "0")  # 无前导零
                and int(part) <= 255)

    def v6(part):
        return (1 <= len(part) <= 4
                and all(ch in hexdigits for ch in part))

    if queryIP.count(".") == 3:
        if all(map(v4, queryIP.split("."))):
            return "IPv4"
    elif queryIP.count(":") == 7:
        if all(map(v6, queryIP.split(":"))):
            return "IPv6"
    return "Neither"
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只判断 `int(part) <= 255` 不管前导零：`192.168.01.1` 被当成有效。
- 末尾多一个分隔符：`"1.1.1.1."` 切出空段，必须保证空段不通过。
- IPv6 段用 `int(part, 16)` 校验：`"+1"`、`"1_0"` 也能被接受，用字符集判断才可靠。

**追问。**
- 支持 `::` 压缩的 IPv6？：段数少于 8 且恰好一个 `::`，补零后再校验。
- 判断 IP 是否属于某个 CIDR 网段？：转成整数比较前缀位，或用标准库 `ipaddress`。

**同模式。** LC 93 复原 IP 地址、LC 65 有效数字、LC 8 字符串转换整数
