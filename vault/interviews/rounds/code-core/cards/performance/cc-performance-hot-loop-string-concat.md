---
id: cc-performance-hot-loop-string-concat
node: performance.hot-loop
type: cloze
---
Building output with `out += line + "\n"` inside a loop is {{c1::O(n²)}}, because every `+=` copies the whole accumulated string; append to a list and call {{c2::"\n".join(parts)}} once at the end for {{c1::O(n)}}. The identical rule kills `acc = acc + [x]` inside a loop — use `acc.append(x)`.

## zh
在循环里用 `out += line + "\n"` 拼输出是 {{c1::O(n²)}}，因为每次 `+=` 都要复制整个已累积的字符串；改成 append 到 list、最后调一次 {{c2::"\n".join(parts)}}，就是 {{c1::O(n)}}。同一条规则也毙掉循环里的 `acc = acc + [x]` —— 用 `acc.append(x)`。
