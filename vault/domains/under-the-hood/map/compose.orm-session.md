%% trellis:begin %%
# ORM 的 Session：身份映射 + 工作单元
*数据结构组合：开源框架里的类设计*

SQLAlchemy / Hibernate 的会话：一张“(类, 主键) → 对象”的身份映射保证同一行只有一个对象；SQLAlchemy 用 new、dirty、deleted 三个集合记下改动（Hibernate 用动作队列），flush 时按依赖顺序一次性写回数据库。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-orm-session-1-spec]]
2. [[uth-compose-orm-session-2-three-sets]]
3. [[uth-compose-orm-session-3-core-code]]
4. [[uth-compose-orm-session-4-real-session]]
5. [[uth-compose-orm-session-5-interview]]
%% trellis:end %%

## Notes
