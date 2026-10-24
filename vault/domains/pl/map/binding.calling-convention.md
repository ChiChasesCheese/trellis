%% trellis:begin %%
# 函数调用在机器层面：栈帧与调用约定
*名字、绑定与求值*

调用时发生了什么：返回地址、栈帧、寄存器传参、调用者与被调者保存寄存器；Go 1.17 改用寄存器 ABI、栈增长、内联为什么能消掉这些开销。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/binding.parameter-passing|参数传递：传值、传引用与传共享]]

## Cards (10)
1. [[pl-binding-calling-convention-principle]]
2. [[pl-binding-calling-convention-foundation-register-trace]]
3. [[pl-binding-calling-convention-foundation-saved-registers]]
4. [[pl-binding-calling-convention-foundation-go-stack-abi]]
5. [[pl-binding-calling-convention-foundation-vm-frames]]
6. [[pl-binding-calling-convention-mechanism-inlining]]
7. [[pl-binding-calling-convention-table]]
8. [[pl-binding-calling-convention-philosophy-no-tail-calls]]
9. [[pl-binding-calling-convention-best-practice]]
10. [[pl-binding-calling-convention-pitfall-recursion-depth]]
%% trellis:end %%

## Notes
