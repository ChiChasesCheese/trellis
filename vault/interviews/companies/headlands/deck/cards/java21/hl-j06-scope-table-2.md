---
id: hl-j06-scope-table-2
node: java21.j06-instanceof-pattern
type: qa
step: 6
---
## Q
绑定变量 `s` 在这三种写法里哪里可用：(1) `if (!(o instanceof String s)) { return; } use(s);`；(2) `while (i < n && xs.get(i) instanceof Integer k) { ... }`；(3) 三元 `cond ? (o instanceof String s ? s : "") : ...`？

## A
- (1) **`if` 之后的整个剩余部分**：没匹配的路径已经 `return` 了，能走到后面的一定匹配了。
- (2) **循环体**：循环体只在条件为真时进入。
- (3) **三元运算符的对应分支**：同样按"一定为真"推。

判断法始终是同一个：走到那一行时，模式是否一定匹配。
