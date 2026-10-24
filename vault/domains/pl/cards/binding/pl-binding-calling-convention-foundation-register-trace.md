---
id: pl-binding-calling-convention-foundation-register-trace
node: binding.calling-convention
type: qa
step: 2
---
## Q
从真实的机器码看，一次调用中参数、返回值、返回地址分别放在哪里？以 ARM64 上一个 Rust 函数及其调用者为例。

## A
被调用的函数 `add3`（返回 `a + b * c`，按 C 的 ABI 编译）在 Apple Silicon（ARM64）上只有两条指令：

```text
_add3:
    madd  x0, x2, x1, x0     ; x0 = x0 + x2 * x1  (a + c*b)
    ret                      ; jump to the address in x30
```

约定一目了然：三个参数在 `x0`、`x1`、`x2`（ARM64 用 `x0` 到 `x7` 传前 8 个整数参数），返回值写回 `x0`，`ret` 跳到寄存器 `x30`（链接寄存器 LR）里存的**返回地址**。

调用者 `caller(x)` 的关键部分：

```text
    stp  x20, x19, [sp, #-32]!   ; save x19, x20 on the stack
    stp  x29, x30, [sp, #16]     ; save frame pointer and return address
    mov  x19, x0                 ; keep x in x19
    mov  w1, #2 ; mov w2, #3     ; x0 already holds x
    bl   _add3                   ; x30 = next instruction, jump
    mov  x20, x0                 ; keep first result in x20
    mov  x0, x19 ; mov w1, #4 ; mov w2, #5
    bl   _add3
    add  x0, x0, x20             ; sum, result in x0
    ldp ... ; ret                ; restore, return to our own caller
```

要点：

1. `bl`（branch with link）一条指令完成「把返回地址写进 `x30` + 跳转」。
2. `caller` 自己也调用别的函数，会覆盖 `x30`，所以必须先把调用者留给它的 `x30` 存到栈上，最后恢复，这个栈上的存储区就是**栈帧**（stack frame）。
3. 参数 `x` 在第一次调用后还要用，但 `x0` 会被 `add3` 当作返回值覆盖，所以 `caller` 先把它搬到 `x19`，第二次调用前再搬回来。`x19` 里的值不会被 `add3` 破坏，因为 ABI 规定 `x19` 属于被调用者必须原样还原的寄存器。

x86-64（System V）的做法类似，参数用 `rdi`、`rsi`、`rdx`、`rcx`、`r8`、`r9`，返回值 `rax`，不同的是 `call` 指令把返回地址直接**压栈**。
