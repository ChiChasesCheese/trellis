---
id: pl-cpp-undefined-behavior-pitfall-deleted-check
node: cpp.undefined-behavior
type: qa
step: 8
---
## Q
为什么 `if (x + 1 < x)` 这样的溢出检查在优化构建里会失效？线上遇到这类"安全检查被优化掉"的问题怎样排查和修复？

## A
**场景**：写一个想检测溢出的函数：

```cpp
bool will_overflow(int x)    { return x + 1 < x; }
bool will_overflow_ok(int x) { return x == INT_MAX; }
```

**`-O2` 汇编（本机真实输出）**：

```
will_overflow:      mov w0, #0 ; ret
will_overflow_ok:   mov w8, #2147483647 ; cmp w0, w8 ; cset w0, eq ; ret
```

`will_overflow` 被编译成永远返回 `0`（`false`）：编译器推理"有符号溢出不会发生，所以 `x + 1 < x` 恒为假"。检查代码在源码里存在，在二进制里不存在。

**危害**：这类检查常见于边界校验、长度计算、分配大小检查。检查被删除后，攻击者构造溢出值，后续的分配或拷贝就越界，这是经典的安全漏洞来源。症状：调试构建通过所有测试，发布构建出现安全问题。

**排查**：
1. **UBSan**：`-fsanitize=signed-integer-overflow` 在测试里直接报告出现溢出的位置。
2. **看汇编**：怀疑某个检查，用 `-S` 或编译器资源管理器（Compiler Explorer）对比 `-O0` 与 `-O2`。
3. **编译器警告**：`-Wstrict-overflow`、clang-tidy 的相关检查。

**修复（三种）**：
1. **事前检查**：`if (x == INT_MAX)`、`if (a > INT_MAX - b)`，不依赖溢出本身。
2. **用扩宽类型计算再检查范围**：`int64_t` 做加法，再比较。
3. **用编译器内建**：`__builtin_add_overflow(a, b, &r)`，返回是否溢出，且有明确定义。

**还有一个同类陷阱**：先解引用、后判空，判空会被删：`int v = *p; if (p == nullptr) return -1;` 在 `-O2` 下只剩 `ldr w0, [x0]; ret`。

**要记住的一点**：写检查时问自己，"这个检查本身依赖 UB 吗"；如果依赖，编译器有权删掉它。
