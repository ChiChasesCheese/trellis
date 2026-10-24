%% trellis:begin %%
# RAII、零/三/五法则与智能指针
*现代 C++：特性、取舍与最佳实践*

析构函数保证释放、rule of zero / three / five、unique_ptr、shared_ptr 的引用计数与控制块、weak_ptr 打破循环；在接口签名里表达所有权。

**Requires:** [[domains/pl/map/memory.manual-raii|手动管理与 RAII]], [[domains/pl/map/cpp.value-categories|值类别、移动语义与拷贝省略]]

**Unlocks:** [[domains/pl/map/cpp.errors|错误处理：异常、错误码与 std::expected]], [[domains/pl/map/cpp.concurrency|并发：线程、原子与内存序、协程]], [[domains/pl/map/cpp.modern-practice|现代 C++ 写法清单]]

## Cards (11)
1. [[pl-cpp-raii-ownership-principle]]
2. [[pl-cpp-raii-ownership-found-destructor-unwinding]]
3. [[pl-cpp-raii-ownership-found-rule-of-zero-five]]
4. [[pl-cpp-raii-ownership-found-unique-ptr]]
5. [[pl-cpp-raii-ownership-found-shared-ptr]]
6. [[pl-cpp-raii-ownership-found-weak-ptr-cycles]]
7. [[pl-cpp-raii-ownership-mechanism-shared-cost]]
8. [[pl-cpp-raii-ownership-table]]
9. [[pl-cpp-raii-ownership-unique-signature-ownership]]
10. [[pl-cpp-raii-ownership-best-practice]]
11. [[pl-cpp-raii-ownership-pitfall-double-owner]]
%% trellis:end %%

## Notes
