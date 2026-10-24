%% trellis:begin %%
# 未定义行为与优化器
*现代 C++：特性、取舍与最佳实践*

什么是 UB、编译器为什么能利用 UB 做优化（有符号溢出、空指针、越界、数据竞争）、实现定义与未指定行为的区别、怎样用 sanitizer 和 -fwrapv 等手段兜住。

**Requires:** [[domains/pl/map/memory.memory-safety|内存安全]]

**Unlocks:** [[domains/pl/map/cpp.safety|内存安全之争与 C++ 的回应]]

## Cards (9)
1. [[pl-cpp-undefined-behavior-principle]]
2. [[pl-cpp-undefined-behavior-found-four-kinds]]
3. [[pl-cpp-undefined-behavior-mechanism-optimizer]]
4. [[pl-cpp-undefined-behavior-found-sanitizers]]
5. [[pl-cpp-undefined-behavior-table]]
6. [[pl-cpp-undefined-behavior-unique-contract]]
7. [[pl-cpp-undefined-behavior-best-practice]]
8. [[pl-cpp-undefined-behavior-pitfall-deleted-check]]
9. [[pl-cpp-undefined-behavior-evolution-ub-shrinking]]
%% trellis:end %%

## Notes
