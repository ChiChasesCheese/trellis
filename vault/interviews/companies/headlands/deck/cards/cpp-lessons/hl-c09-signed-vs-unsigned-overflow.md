---
id: hl-c09-signed-vs-unsigned-overflow
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 4
---
## Q
面试问：有符号溢出和无符号溢出有什么区别？`unsigned x = 0; x--;` 是 UB 吗？
Interview question: What is the difference between signed and unsigned overflow?

## A
- **有符号溢出是 UB**；**无符号**按模 2^n **回绕，有定义**。
- `unsigned x = 0; x--;` **不是** UB，结果是 `UINT_MAX`（4294967295）。
- 因为有符号溢出是 UB，编译器假设它不会发生，会据此删掉检查（如 `x + 1 < x`）。
- UBSan 报：`signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'`。
- 注意 `size()` 是无符号，倒序循环写 `for (size_t i = n; i-- > 0;)`。
