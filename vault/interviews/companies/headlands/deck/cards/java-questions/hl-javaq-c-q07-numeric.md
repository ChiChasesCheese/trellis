---
id: hl-javaq-c-q07-numeric
node: java-questions.c-languages
type: qa
step: 3
---
## Q
Java 与 Python 在整数、除法与取模、参数传递上有哪些容易答错的差异？

## A
- **整数**：Java 的 `int` 32 位、`long` 64 位，溢出回绕（`Integer.MAX_VALUE + 1 = -2147483648`），大数用 `BigInteger`；Python 是任意精度整数。
- **除法 / 取模**：Java 向零截断，`-7 / 2 = -3`，`-7 % 2 = -1`，要非负余数用 `Math.floorMod(-7, 2) = 1`；Python 向下取整，`-7 // 2 = -4`，`-7 % 2 = 1`。
- **参数传递**：两者相同——**引用的值传递**（Python 称 call by sharing）：对象引用被复制，可以改对象内容，但不能让调用者的变量指向别处。
