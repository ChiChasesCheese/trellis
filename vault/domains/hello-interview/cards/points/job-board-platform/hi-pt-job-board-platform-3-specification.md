---
id: hi-pt-job-board-platform-3-specification
node: qb.lld.job-board-platform.points
type: qa
step: 3
---
## Q
**招聘信息平台 · 规格模式**｜必会 · 出自：招聘信息平台 › 深入 1

招聘平台的搜索条件（地点、薪资、技能、是否远程）会不断增加。为什么用规格模式而不是长参数列表？

## A
**反面。** search(keyword, city, salary, skills, ...) 每加一个条件就改签名和实现，且并且、或者的组合写死。
**规格模式。** 每个条件一个对象，search 只依赖 ok(job)，所有条件都满足才算命中：
```python
class SalarySpec(Spec):
    def ok(self, j): return j.salary_max >= self.at_least
jobs = board.search(now, SalarySpec(100), KeywordSpec("go"))
```
**演进。** 加 & 与 | 就能组合成树；规格也可翻译成数据库查询或搜索引擎过滤器，接口不变。
