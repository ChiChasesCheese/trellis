%% trellis:begin %%
# Spring 单例 Bean 的三级缓存：为什么是三层
*数据结构组合：开源框架里的类设计*

单例 Bean 互相依赖时怎样不死循环：成品表、半成品表、工厂表三张 Map 加一个“正在创建”集合；为什么两层不够（AOP 代理要延迟到真的被引用时才生成）；Spring Boot 2.6 起默认禁止循环依赖。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-spring-three-level-cache-1-spec]]
2. [[uth-compose-spring-three-level-cache-2-parts]]
3. [[uth-compose-spring-three-level-cache-3-invariant-code]]
4. [[uth-compose-spring-three-level-cache-4-why-three]]
5. [[uth-compose-spring-three-level-cache-5-real-world]]
%% trellis:end %%

## Notes
