---
id: hl-j06-compile-quiz
node: java21.j06-instanceof-pattern
type: qa
step: 21
---
## Q
这四段哪些能编译？
(a) `if (o instanceof String s && s.length() > 2) { }`
(b) `if (o instanceof String s || s.length() > 2) { }`
(c) `if (!(o instanceof String s)) return;  System.out.println(s);`
(d) `if (!(o instanceof String s)) { System.out.println("no"); }  System.out.println(s);`

## A
- (a) **能**。
- (b) **不能**：`||` 右边在左边为假时才算，`s` 未绑定。
- (c) **能**：`if` 块 `return` 了，后面一定匹配。
- (d) **不能**：`if` 块只打印，能正常走完，后面不一定匹配。

答题思路：问"走到这一行时模式是否一定匹配"。
