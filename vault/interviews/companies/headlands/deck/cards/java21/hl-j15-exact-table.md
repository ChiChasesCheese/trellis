---
id: hl-j15-exact-table
node: java21.j15-math-string-utils
type: qa
step: 3
---
## Q
`Math.xxxExact` 家族有哪些方法？各自的版本、溢出时抛什么？

## A
溢出就抛 `ArithmeticException`：
- `addExact` / `subtractExact` / `multiplyExact`：加/减/乘，`int` 与 `long` 重载（还有 `multiplyExact(long, int)`），Java 8；
- `incrementExact` / `decrementExact` / `negateExact`：+1 / −1 / 取负，Java 8；
- `toIntExact(long)`：`long` 转 `int`，放不下就抛，Java 8；
- `absExact`：绝对值，`MIN_VALUE` 的绝对值放不下会抛，Java 15；
- `divideExact`、`floorDivExact`、`ceilDivExact`：仅 `MIN_VALUE / -1` 会溢出，Java 18。

典型消息：`long overflow`、`integer overflow`。
