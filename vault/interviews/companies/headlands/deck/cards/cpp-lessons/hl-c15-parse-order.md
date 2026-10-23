---
id: hl-c15-parse-order
node: cpp-lessons.c15-io-performance
type: qa
step: 6
---
## Q
任务：每行 `BUY AAPL 100 187.50`，解析成 `Order{bool buy; string sym; long qty; double px;}`，坏行返回空。写出 `parse_order`。

## A
```cpp
std::optional<Order> parse_order(std::string_view line) {
    auto f = split(line);
    if (f.size() != 4 || (f[0] != "BUY" && f[0] != "SELL")) return std::nullopt;
    auto q = parse_num<long>(f[2]);
    auto p = parse_num<double>(f[3]);
    if (!q || !p) return std::nullopt;
    return Order{f[0] == "BUY", std::string(f[1]), *q, *p};
}
```
- 先检查字段数和方向，再 `from_chars` 解析数量和价格，任何失败都返回 `nullopt`。
- 金额用整数分（`long`）而不是 `double`，避免舍入误差。
