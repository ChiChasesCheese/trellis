---
id: hl-j13-quiz-legal
node: java21.j13-unnamed-variables
type: qa
step: 16
---
## Q
JDK 21（开预览）下哪些合法？(a) `int _ = 5;` (b) `System.out.println(_);` (c) `void f(int _) {}` (d) `list.forEach(_ -> n[0]++);`

## A
- (a) **合法**：有初始化的局部变量。
- (b) **非法**：`_` 不能读。
- (c) **非法**：方法参数不在允许位置。
- (d) **合法**：lambda 参数。

允许位置只有：catch 参数、增强 for 变量、有初始化的局部变量、try-with-resources 资源、lambda 参数、传统 for 的初始化，以及模式里的 `_`。
