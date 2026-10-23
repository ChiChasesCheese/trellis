---
id: hl-hc06-instr-hierarchy
node: problems.hc06-cpu-register-bitwise
type: qa
step: 12
---
## Q
指令集怎么用两层 sealed 加 record 建模？`apply` 为什么写成没有 `default` 的 switch 表达式？

## A
```java
public sealed interface Instr permits Update, Query {}
public sealed interface Update extends Instr
        permits And, Or, Xor, Not, Shl, Shr, Rol, Ror, SetBit, ClearBit, ToggleBit, Compress, Expand, Reverse, ByteSwap {}
public sealed interface Query extends Instr permits Popcount, TrailingZeros, LeadingZeros {}

public record And(int mask) implements Update {}
public record Not() implements Update {}
public record SetBit(int bit) implements Update {
    public SetBit { checkBit(bit); }   // 紧凑构造器：校验位号 0..31
}
public static int apply(int reg, Update u) {
    return switch (u) {
        case And(var m)    -> reg & m;
        case Not _         -> ~reg;
        case Shl(var n)    -> n >= 32 ? 0 : reg << n;
        case Shr(var n)    -> n >= 32 ? 0 : reg >>> n;
        case Rol(var n)    -> Integer.rotateLeft(reg, n);
        case SetBit(var b) -> reg | (1 << b);
        ...
    };
}
```
- 分 `Update` / `Query`：返回值含义不同（新寄存器值 vs 要输出的数），类型本身说明会不会改寄存器；
- 紧凑构造器在字段赋值之前校验，`SetBit(32)` 构造不出来；
- 没有 `default`：新增指令时所有 switch 编译报错，逼你补分支；
- `run`：`case Update u -> reg = apply(reg, u); case Query q -> out.add(query(reg, q));`，`List.copyOf(out)` 返回不可变列表；
- `case Not _` 的 `_` 是未命名模式（预览）。

语义要主动和面试官确认：`SHL/SHR n ≥ 32` 得 0；`ROL/ROR` 位数 mod 32；`SHR` 逻辑右移。

C++ 对应：`std::variant` + `std::visit(overloaded{...})`，漏一个类型编译失败；`Instr = variant<Update, Query>` 嵌套，要分发两次；记录校验用构造函数抛 `std::invalid_argument`。
