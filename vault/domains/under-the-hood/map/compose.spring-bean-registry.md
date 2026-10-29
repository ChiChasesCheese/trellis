%% trellis:begin %%
# Spring 的 Bean 注册表：Map + 列表与双向依赖表
*数据结构组合：开源框架里的类设计*

按名字查定义要快、遍历要保持注册顺序：一张 Map 加一个名字列表；谁依赖谁存成两张方向相反的 Map；关闭容器时按创建顺序倒着销毁，销毁每个 Bean 之前先销毁依赖它的 Bean。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-spring-bean-registry-1-spec]]
2. [[uth-compose-spring-bean-registry-2-parts]]
3. [[uth-compose-spring-bean-registry-3-invariant-code]]
4. [[uth-compose-spring-bean-registry-4-real-world]]
5. [[uth-compose-spring-bean-registry-5-interview]]
%% trellis:end %%

## Notes
