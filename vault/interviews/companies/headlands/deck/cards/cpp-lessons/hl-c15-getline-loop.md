---
id: hl-c15-getline-loop
node: cpp-lessons.c15-io-performance
type: qa
step: 7
---
## Q
写出读未知行数输入、跳过空行和 `#` 注释、汇总每个代码净持仓与成交额、坏行写到 stderr 的主循环。

## A
```cpp
std::map<std::string, long> net;
std::map<std::string, double> notional;
std::string line;
int bad = 0;
while (std::getline(std::cin, line)) {
    if (line.empty() || line[0] == '#') continue;
    if (auto o = parse_order(line)) {
        net[o->sym] += o->buy ? o->qty : -o->qty;
        notional[o->sym] += static_cast<double>(o->qty) * o->px;
    } else {
        ++bad;
        std::cerr << "skipped: " << line << "\n";
    }
}
```
- `getline` 读到换行（不含），EOF 返回假，循环条件直接用它。
- 读未知行数的输入：`while (getline(...))` / `while (cin >> x)`。
