---
id: hl-j05-sugar-bytecode
node: java21.j05-switch-expressions
type: qa
step: 14
---
## Q
箭头 `->` 和 `yield` 在 JVM 层有新指令吗？`sign(Side s)` 的箭头 `switch` 编译成什么？

## A
**没有新 JVM 指令**，只是语法糖，编译出来还是 `tableswitch` / `lookupswitch` + `goto`。

`sign` 的字节码要点：
```
tableswitch { 0: 42   1: 46   2: 46   default: 32 }   // BUY -> 42；SELL、SHORT 都 -> 46
32: new MatchException ... athrow                       // default：不应走到
42: iconst_1;  goto 47
46: iconst_m1
47: ireturn
```
- 每个分支后的 `goto` 是编译器加的"跳到 `switch` 末尾"，就是 `break`，由编译器写，你不会忘；
- 多标签 `SELL, SHORT` 是**两个下标指向同一地址**，不是 fall-through。
