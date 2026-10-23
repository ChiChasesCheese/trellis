---
id: hl-c12-oral-answer
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 15
---
## Q
用英文口述（约 30 秒）：Why is C++ faster than Java?

## A
参考说法："It isn't compilation alone. C++ has no GC or VM in the way, data is laid out by value so arrays of structs are contiguous and cache-friendly, templates and inlining remove abstraction cost, and I control allocation. Java closes much of the steady-state gap with its JIT - devirtualization, escape analysis - but C++ wins on tail latency and predictability, which is what matters in trading."

四点：
- 无 GC / 无 VM
- 值布局连续、缓存友好
- 模板 + 内联
- 控制分配

结尾落到：稳态可接近，**尾延迟和布局**是差距。
