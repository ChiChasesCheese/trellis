---
slug: job-board-platform
kind: low-level-design
---

## Q
**招聘信息平台（Job Board）**｜低层设计

设计一个招聘信息平台：雇主发布职位，求职者按关键词、地点、薪资、技能等条件搜索和筛选职位并投递申请；雇主查看收到的申请并推进状态（已查看、入围、拒绝、录用）；求职者可以撤回申请、查看自己的申请进度。要求给出类设计、搜索与筛选的可扩展方式、申请的状态与权限规则，以及核心代码。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 这题的看点是"查询条件会不断增加"和"状态迁移带权限"：搜索条件用规格模式（Specification）组合，使新增筛选项不改搜索主流程；申请是一个有合法迁移表的状态机，且同一求职者对同一职位只能有一个有效申请。

**需求。**
- 功能：
  1. 雇主发布、修改、关闭职位；职位可设过期时间。
  2. 求职者搜索：关键词、地点、是否远程、薪资区间、技能；支持排序与分页。
  3. 求职者投递申请（附简历引用），不可重复投递；可撤回。
  4. 雇主查看某职位的申请列表，推进申请状态；状态变化通知求职者，新申请通知雇主。
  5. 求职者查看自己的申请列表与状态。
- 非功能：
  - 权限：只有职位所属雇主能关闭职位和更改申请状态；求职者只能看到并撤回自己的申请。
  - 一致性：并发重复投递只产生一条申请；已关闭或已过期的职位不能再投递。
  - 扩展：新增筛选条件、新增通知渠道、新增状态，不重写核心流程；数据量增大后可把搜索换成专用搜索引擎。

**核心实体与接口。**
- 类与职责：
  - `Job`：职位，含雇主、标题、描述、地点、是否远程、薪资区间、技能集合、发布时间、过期时间、状态。
  - `Application`：申请，含求职者、职位、简历引用、状态、时间。
  - `Specification`（规格接口）与若干实现：`KeywordSpec`、`LocationSpec`、`SalarySpec`、`SkillSpec`、`OpenSpec`；支持用 `&` 与 `|` 组合。
  - `JobBoard`：门面与服务，负责发布、搜索、投递、状态变更，并持有倒排索引以缩小候选集。
  - `EventBus`（观察者）：发布 `ApplicationSubmitted`、`StatusChanged` 事件，通知渠道订阅。
- 接口：`post_job`、`close_job`、`search(query, spec, limit, cursor)`、`apply`、`withdraw`、`update_status`、`my_applications`、`applications_for(job)`。

```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
from typing import Callable, Protocol
import itertools, re


class JobStatus(Enum):
    OPEN = 1; CLOSED = 2


class AppStatus(Enum):
    SUBMITTED = 1; VIEWED = 2; SHORTLISTED = 3; REJECTED = 4; HIRED = 5; WITHDRAWN = 6


# 申请的合法迁移：雇主推进 + 求职者撤回。终态没有出边
ALLOWED = {
    AppStatus.SUBMITTED: {AppStatus.VIEWED, AppStatus.REJECTED, AppStatus.WITHDRAWN},
    AppStatus.VIEWED: {AppStatus.SHORTLISTED, AppStatus.REJECTED, AppStatus.WITHDRAWN},
    AppStatus.SHORTLISTED: {AppStatus.HIRED, AppStatus.REJECTED, AppStatus.WITHDRAWN},
}


@dataclass
class Job:
    job_id: int
    employer_id: str
    title: str
    description: str
    location: str
    remote: bool
    salary_min: int
    salary_max: int
    skills: frozenset[str]
    posted_at: float
    expires_at: float
    status: JobStatus = JobStatus.OPEN


@dataclass
class Application:
    app_id: int
    job_id: int
    seeker_id: str
    resume_ref: str
    status: AppStatus = AppStatus.SUBMITTED


class Spec(Protocol):
    def ok(self, j: Job) -> bool: ...


class _Combinable:
    def __and__(self, o): return _And(self, o)
    def __or__(self, o): return _Or(self, o)


@dataclass
class _And(_Combinable):
    a: Spec; b: Spec
    def ok(self, j: Job) -> bool: return self.a.ok(j) and self.b.ok(j)


@dataclass
class _Or(_Combinable):
    a: Spec; b: Spec
    def ok(self, j: Job) -> bool: return self.a.ok(j) or self.b.ok(j)


@dataclass
class LocationSpec(_Combinable):
    city: str
    allow_remote: bool = True
    def ok(self, j: Job) -> bool:
        return j.location.lower() == self.city.lower() or (self.allow_remote and j.remote)


@dataclass
class SalarySpec(_Combinable):
    at_least: int
    def ok(self, j: Job) -> bool: return j.salary_max >= self.at_least


@dataclass
class SkillSpec(_Combinable):
    required: frozenset[str]            # 职位要求的技能里至少命中一个
    def ok(self, j: Job) -> bool: return bool(self.required & j.skills)


@dataclass
class OpenSpec(_Combinable):
    now: float
    def ok(self, j: Job) -> bool: return j.status is JobStatus.OPEN and j.expires_at > self.now


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9+#]+", text.lower()))


class EventBus:
    def __init__(self) -> None:
        self._subs: list[Callable[[str, dict], None]] = []

    def subscribe(self, fn: Callable[[str, dict], None]) -> None:
        self._subs.append(fn)

    def publish(self, name: str, payload: dict) -> None:
        for fn in self._subs:           # 通知渠道（邮件、站内信、推送）各自订阅，主流程不关心
            fn(name, payload)


class JobBoard:
    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
        self.jobs: dict[int, Job] = {}
        self.apps: dict[int, Application] = {}
        self._applied: dict[tuple[str, int], int] = {}     # (求职者, 职位) -> 申请号，唯一性
        self._index: dict[str, set[int]] = {}              # 倒排索引：词 -> 职位集合
        self._ids = itertools.count(1)
        self._lock = Lock()

    def post_job(self, employer_id: str, title: str, description: str, location: str, remote: bool,
                 salary: tuple[int, int], skills: set[str], now: float, ttl_days: int = 30) -> Job:
        with self._lock:
            j = Job(next(self._ids), employer_id, title, description, location, remote,
                    salary[0], salary[1], frozenset(s.lower() for s in skills), now, now + ttl_days * 86400)
            self.jobs[j.job_id] = j
            for t in tokens(title + " " + description) | set(j.skills):
                self._index.setdefault(t, set()).add(j.job_id)
            return j

    def search(self, query: str, spec: Spec | None, now: float, limit: int = 20) -> list[Job]:
        words = tokens(query)
        if words:                       # 先用倒排索引求交集缩小候选，再逐个套规格
            ids = set.intersection(*(self._index.get(w, set()) for w in words))
            cands = [self.jobs[i] for i in ids]
        else:
            cands = list(self.jobs.values())
        base = OpenSpec(now)
        spec = base if spec is None else base & spec
        hits = [j for j in cands if spec.ok(j)]
        hits.sort(key=lambda j: (-j.posted_at, j.job_id))  # 新的在前；job_id 打破并列，游标分页才稳定
        return hits[:limit]

    def apply(self, seeker_id: str, job_id: int, resume_ref: str, now: float) -> Application:
        with self._lock:                # 检查职位状态 + 唯一性 + 写入，必须在同一个临界区
            j = self.jobs[job_id]
            if j.status is not JobStatus.OPEN or j.expires_at <= now:
                raise ValueError("职位已关闭或过期")
            key = (seeker_id, job_id)
            if key in self._applied:    # 幂等：重复投递返回已有申请，而不是再建一条
                return self.apps[self._applied[key]]
            a = Application(next(self._ids), job_id, seeker_id, resume_ref)
            self.apps[a.app_id] = a
            self._applied[key] = a.app_id
        self.bus.publish("ApplicationSubmitted", {"employer": j.employer_id, "app": a.app_id})
        return a

    def update_status(self, actor_id: str, app_id: int, to: AppStatus) -> Application:
        with self._lock:
            a = self.apps[app_id]
            j = self.jobs[a.job_id]
            if to is AppStatus.WITHDRAWN:
                if actor_id != a.seeker_id:
                    raise PermissionError("只能撤回自己的申请")
            elif actor_id != j.employer_id:
                raise PermissionError("只有职位所属雇主可以推进状态")
            if to not in ALLOWED.get(a.status, set()):
                raise ValueError(f"{a.status.name} -> {to.name} 不允许")
            a.status = to
        self.bus.publish("StatusChanged", {"seeker": a.seeker_id, "app": a.app_id, "to": to.name})
        return a
```

用到的模式：规格模式（搜索条件可组合、可新增）、观察者模式（事件总线解耦通知）、状态机（申请迁移表）、门面（`JobBoard`）。原因：这个领域变化最多的是筛选项和通知渠道，两者都放在接口后面，加功能只增加类，不改 `search`、`apply` 的主体。

**整体设计。**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="170" y1="36" x2="170" y2="53"/>
<line x1="170" y1="86" x2="170" y2="103"/>
<line x1="170" y1="136" x2="170" y2="153"/>
<line x1="170" y1="186" x2="170" y2="203"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="12" y="8" width="316" height="28" rx="3"/>
<rect x="12" y="58" width="316" height="28" rx="3"/>
<rect x="12" y="108" width="316" height="28" rx="3"/>
<rect x="12" y="158" width="316" height="28" rx="3"/>
<rect x="12" y="208" width="316" height="28" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="170,58 167,52 173,52"/>
<polygon points="170,108 167,102 173,102"/>
<polygon points="170,158 167,152 173,152"/>
<polygon points="170,208 167,202 173,202"/>
</g>
<g fill="currentColor">
<text x="170" y="26" font-size="12">雇主 post_job -> 职位 + 倒排索引</text>
<text x="170" y="76" font-size="12">搜索: 索引求交集 -> 规格组合过滤</text>
<text x="170" y="126" font-size="12">apply: 锁内 校验 + 唯一性 + 写入</text>
<text x="170" y="176" font-size="12">事件总线 -> 通知渠道</text>
<text x="170" y="226" font-size="12">update_status: 权限 + 迁移表</text>
</g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="252" font-size="11">规格可用 and or 组合, 新增筛选只加类</text></g>
</g></svg>
```
- 发布：`post_job` 写入职位并更新倒排索引。
- 搜索：关键词先走倒排索引求交集，得到候选集；再与"开放且未过期"规格以及用户选择的规格组合逐个判断；按发布时间倒序，用 `(posted_at, job_id)` 作游标分页。
- 投递：同一把锁内检查职位状态、唯一性、写入申请，然后发布事件；通知订阅者（雇主）异步处理。
- 推进状态：校验操作者身份、迁移合法性，更新并发布事件通知求职者。

**深入。**
1. 搜索条件为什么用规格模式。
   - 把所有条件写成 `search(keyword, city, salary, skills, ...)` 的长参数列表：每加一个筛选项就要改签名和实现，条件之间的组合（并且、或者）也写死。
   - 规格模式：每个条件是一个对象，`&` 与 `|` 组合成树，`search` 只依赖 `ok(job)`；新增筛选项（公司规模、学历）只增加一个类。
   - 数据量大时，规格也可以翻译成查询语句或搜索引擎的过滤器，接口不变，实现换掉。
2. 内存索引与专用搜索引擎。
   - 内存倒排索引适合几千到几万个职位，说明思路即可。
   - 数据量上到百万级，换成 Elasticsearch 一类：职位写入数据库后异步同步到索引，搜索走索引，详情走数据库；筛选项用过滤器（不计分）、关键词用相关性评分；热门筛选结果可以缓存。
3. 申请的状态与权限。
   - 迁移表集中定义，非法迁移（比如已拒绝再入围）直接拒绝；终态没有出边。
   - 权限放在服务方法内，而不是调用方自觉：撤回只能由申请人，推进只能由职位所属雇主。
   - 唯一性：内存版用 `(求职者, 职位)` 键；数据库版用唯一约束 `(job_id, seeker_id)`，并发插入冲突时返回已有记录。
4. 并发。
   - 投递时"检查职位开放 + 检查是否已投 + 写入"是一个复合动作，必须原子。内存版一把锁；数据库版在事务里插入并依赖唯一约束，职位关闭与投递的竞争用 `SELECT ... FOR UPDATE` 或乐观版本号。
   - 事件发布放在锁外，避免订阅者阻塞核心流程。
5. 过期与关闭。
   - 过期用 `expires_at` 与当前时间比较，不依赖定时任务改状态，这样即使清理任务延迟，搜索与投递也不会返回过期职位；定时任务只负责归档。
   - 关闭职位后，已有申请保持原状态，由雇主继续处理，或批量标记为拒绝并通知。
6. 通知。
   - 事件总线让邮件、站内信、推送各自订阅；失败不能影响投递结果，生产系统里订阅者通过消息队列异步消费，并对重复事件幂等。

**取舍与追问。**
- 追问"为什么不用继承建模雇主与求职者"：二者行为差异小，主要是权限不同；用角色字段加权限检查更简单，类层次不必要。
- 追问"搜索排序怎么做"：初版按时间倒序；进一步按相关性（关键词命中、技能匹配度）加时间衰减；个性化推荐是另一个子系统。
- 追问"防刷"：投递限流、每人每天投递上限、验证码；职位发布需要审核或信用额度。
- 追问"申请量巨大的雇主视图"：申请列表分页，按状态索引；雇主面板的统计用只读视图或预聚合。
- 追问"如何测试"：时间通过参数注入；对 `apply` 做并发测试，让多个线程重复投递同一职位，断言只有一条申请。
- 追问"简历怎么存"：对象存储，申请里只存引用与版本，投递时锁定当时的简历版本。

**级别期望。**
- 中级：雇主、职位、求职者、申请几个类，基本的发布、搜索、投递流程。
- 高级：规格模式组合搜索条件、申请状态机与权限、重复投递的唯一性与并发、观察者式通知、游标分页。
- 资深（staff）：内存索引到搜索引擎的演进、数据库约束与事务边界、过期的无定时依赖设计、通知的异步与幂等、可测试性，以及哪些变化点值得抽象。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-concurrency-intro|并发入门]]

**同类题。** [[solution-linkedin]]、[[solution-online-shopping]]、[[solution-notification-service]]、[[solution-task-management]]
