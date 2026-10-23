%% trellis:begin %%
# 静态分派：模板、CRTP 与虚函数的代价
*低延迟 C++*

虚函数调用要查虚表、难以内联、可能分支预测失败；用模板和 CRTP 在编译期确定调用目标。

**Requires:** [[domains/hft/map/machine.branch-prediction|分支预测与无分支（branchless）代码]]

## Drills
- [[cpp-hot-path-review|练习：评审一段 C++ 热路径，按对 p99.9 的伤害排序]]

## Cards (4)
1. [[hft-cpp-static-dispatch-virtual-cost]]
2. [[hft-cpp-static-dispatch-crtp]]
3. [[hft-cpp-static-dispatch-when-virtual]]
4. [[hft-cpp-static-dispatch-template-bloat]]
%% trellis:end %%

## Notes
