%% trellis:begin %%
# 对象布局与机械同理心（mechanical sympathy）
*低延迟 Java*

对象头、引用即指针、对象数组是指针数组；primitive 数组与"数组的结构"（structure of arrays）对缓存友好；JOL 查看布局。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/machine.cache-lines|缓存行、局部性与预取]]

**Unlocks:** [[domains/hft/map/java.modern|现代 Java 特性与低延迟]]

## Readings
- [[mechanical-sympathy-false-sharing|False Sharing]]
- [[shipilev-jvm-anatomy|JVM Anatomy Quarks]]

## Cards (5)
1. [[hft-java-object-layout-header]]
2. [[hft-java-object-layout-pointer-array]]
3. [[hft-java-object-layout-soa]]
4. [[hft-java-object-layout-jol]]
5. [[hft-java-object-layout-pointer-chase]]
%% trellis:end %%

## Notes
