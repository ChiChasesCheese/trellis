---
id: hl-c15-read-benchmark
node: cpp-lessons.c15-io-performance
type: qa
step: 10
---
## Q
读一百万行数字，`cin >>`、`scanf`、`fread + from_chars` 各多少毫秒？纯解析 `istringstream`、`stoi`、`strtol`、`from_chars` 呢？说明什么？

## A
读 100 万行文件（毫秒）：
- `cin >>`（同步）568.6；`cin >>`（关同步）541.9；`scanf` 36.6；**`fread + from_chars` 7.4**。

纯解析 100 万个字符串（毫秒）：
- `istringstream` 40.3；`stoi` 9.6；`strtol` 5.9；`from_chars` 4.9。

读法：
- `cin >> x` 在这个实现里很慢（和开关无关）；`scanf` 快一个数量级。
- `istringstream` 比 `strtol`/`from_chars` 慢约 8–10 倍；`stoi` 居中（异常和 `string` 开销）。
- 结论：大输入**读全部 → 手工解析**；输入不大用 `getline` + `from_chars`。
