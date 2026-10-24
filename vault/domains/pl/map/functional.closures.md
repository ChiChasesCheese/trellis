%% trellis:begin %%
# 闭包与捕获语义
*函数式特性*

捕获的是值还是变量：Java 要求 effectively final、Go 按引用捕获（1.22 修复循环变量）、Rust Fn/FnMut/FnOnce 与 move、Python 晚绑定陷阱。

**Requires:** [[domains/pl/map/binding.names-scope|名字与作用域]], [[domains/pl/map/functional.first-class-functions|一等函数与 lambda]], [[domains/pl/map/memory.value-reference-semantics|值语义与引用语义]]

## Drills
- [[functional-capture-and-reuse|练习：循环里创建的闭包捕获了什么，迭代器能不能用第二遍]]

## Cards (11)
1. [[pl-functional-closures-principle]]
2. [[pl-functional-closures-foundation-java-effectively-final]]
3. [[pl-functional-closures-foundation-go-shared-variable]]
4. [[pl-functional-closures-foundation-rust-fn-traits]]
5. [[pl-functional-closures-foundation-python-cells]]
6. [[pl-functional-closures-mechanism]]
7. [[pl-functional-closures-table]]
8. [[pl-functional-closures-unique-rust-fn-hierarchy]]
9. [[pl-functional-closures-best-practice]]
10. [[pl-functional-closures-pitfall-late-binding-loop]]
11. [[pl-functional-closures-history-go-loopvar]]
%% trellis:end %%

## Notes
