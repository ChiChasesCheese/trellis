---
id: craft-predicate-algebra-three-valued-5-across-problems-and-scales
node: craft.patterns.predicate-algebra-three-valued
type: qa
step: 5
---
## Q
**谓词代数与三值逻辑 · find、条件解析器、迷你数据库、折扣资格里的同一套组合子**｜模式

Linux `find` 的过滤器、查询条件解析器、迷你 SQL 的 `WHERE`、折扣的适用范围（Scope），都是"一个条件加几种组合"。它们共享什么？不同在哪里？放大到分布式系统，这类条件出现在哪儿？

## A
**要点。** 同一套代数：原子谓词 + `And`/`Or`/`Not` + 一个恒真元素（不限制）。差别只在返回类型：`find` 的谓词是两值，条件解析器和 SQL 的是三值（因为数据可能是 NULL）。折扣的 `Scope` 把"不限制"写成 `None`，就是 `And` 的单位元：`None` 的维度不过滤，所有给出的维度必须同时满足。

```python
# amz-linux-find：两值谓词，基类提供 & | ~
def __and__(self, other): return AndFilter(self, other)
# query-condition-parser：三值，And 里"一个确定为假就是假"
if a is False or b is False: return False
# amz-discount-engine：Scope 里 None 表示不限制，全场折扣就是默认的 Scope()
return ((self.skus is None or line.sku in self.skus)
        and (self.categories is None or line.category in self.categories))
```

**见于。** amz-linux-find、query-condition-parser、amz-in-memory-db、amz-discount-engine。

**不变的。** 谓词是不可变的值；组合子本身也是谓词；恒真元素让"没有条件"成为一个合法的条件；返回值只有 `True` 才放行。**变化的。** 两值还是三值；谓词是否带 `refs` 之类的元信息；组合时的短路顺序。

**信号。** 需求里出现"满足任意组合的条件""过滤规则""适用范围""可配置的筛选"；或者你正写第二个几乎相同的 `if a and b and not c`，且知道还会出现第三个。数据里有"可能缺失"的字段，且业务要求缺失时不能当作假，就该用三值。

**尺度对照。** 低层设计：frozen 的谓词树，`matches` 加 `refs`。分布式：搜索引擎的 bool 查询（must / should / must_not）、云厂商权限策略里的条件、Kubernetes 的标签选择器、特性开关的目标规则；SQL 优化器会遍历谓词树做下推和选择索引。变化：条件要序列化传输（所以谓词必须是数据而不是闭包），并且要有版本和兼容性：新的谓词类型被旧的消费者遇到时，应该"显式失败"而不是静默当成真或假。
