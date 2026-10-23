---
id: hl-j15-compress-expand
node: java21.j15-math-string-utils
type: qa
step: 12
---
## Q
`Integer.compress(v, mask)` 与 `Integer.expand(v, mask)`（Java 19）各做什么？写出 `compress(0b1011_0110, 0b1111_0000)` 的结果。

## A
给一个**掩码** `mask`：
- `compress(v, mask)`：把 `v` 中 `mask` 为 1 的那些位**抽出来，靠右紧挨着排好**（分散 → 紧凑）；
- `expand(v, mask)`：反过来，把 `v` 的低位依次**撒到 `mask` 为 1 的位置**（紧凑 → 分散）。

```
v    = 1011 0110
mask = 1111 0000
compress(v, mask)    = 1011        (取出高 4 位，靠右)
expand(0b1011, mask) = 1011 0000   (撒回高 4 位)
```
同一 mask 下互逆（对 `mask` 之内的位）。这是**位域打包**的原语；`Long` 有同名方法。支持 BMI2 的 x86 上 JIT 可能编译成单条 `PEXT`/`PDEP` 指令。
