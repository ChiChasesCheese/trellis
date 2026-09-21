---
id: orm-descriptor-indirection
node: classes.properties-descriptors
type: qa
source: python-docs
---
## Q
在一个用描述符实现的简化 ORM（object-relational mapping，对象关系映射）里，类属性访问（如 `movie.director`）实际发生了什么，数据真的存在实例里吗？

## A
不存在实例里。实例（如 `Movie` 的对象）只持有一个主键（如 `self.key`），真正的数据留在外部数据库表中。类属性（如 `director`）是一个数据描述符实例：`__get__()` 被触发时才拼出一条 SQL 查询，用实例持有的主键去数据库里查这一列的值；赋值触发 `__set__()` 时则拼出一条 `UPDATE` 语句写回数据库。也就是说描述符把「看起来像普通字段访问」的语法，转译成了「按需查询/更新外部存储」的动作，实例本身完全不缓存这份数据。
