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

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求，定类和接口 |
| 8–15 分 | 讲规格模式和申请状态机，画整体设计 |
| 15–45 分 | 写核心实现：职位、申请、规格、`JobBoard` 的搜索、投递、改状态 |
| 45–50 分 | 跑例子：搜索、并发重复投递、权限和非法迁移 |
| 50–60 分 | 追问：「或」组合与新筛选项、通知、倒排索引、搜索引擎 |

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
  - `Job`：职位，含雇主、标题、薪资、发布时间、过期时间、状态。`Application`：申请，含求职者、职位、状态。
  - `Spec`（规格接口）与若干实现：`SalarySpec`、`OpenSpec`，后面再加 `KeywordSpec` 等。
  - `JobBoard`：门面与服务，负责发布、搜索、投递、状态变更。
  - `EventBus`（观察者）：发布 `ApplicationSubmitted`、`StatusChanged`，通知渠道订阅（逐步扩展 2）。
- 接口：`post_job`、`close_job`、`search(now, *specs)`、`apply`、`withdraw`、`update_status`、`my_applications`、`applications_for(job)`。
- 雇主和求职者不用继承：行为差异只是权限，用角色字段加权限检查更简单。

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
- 发布：`post_job` 写入职位。
- 搜索：把「开放且未过期」规格和用户选的规格一起逐个判断，按发布时间倒序，用 `(posted_at, job_id)` 作游标分页；数据量大时先用倒排索引缩小候选集（逐步扩展 3）。
- 投递：同一把锁内检查职位状态、唯一性、写入申请。
- 推进状态：校验操作者身份和迁移合法性，再更新。

**核心实现。** 97 行。用到的模式：规格模式（搜索条件可新增）、状态机（申请迁移表）、门面（`JobBoard`）。变化最多的是筛选项和通知渠道，两者都放在接口后面，加功能只增加类，不改 `search`、`apply` 的主体。

```python
from dataclasses import dataclass
from enum import Enum
from threading import Lock
import itertools


class JobStatus(Enum): OPEN = 1; CLOSED = 2


class AppStatus(Enum): SUBMITTED = 1; VIEWED = 2; SHORTLISTED = 3; REJECTED = 4; HIRED = 5; WITHDRAWN = 6


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
    salary_max: int
    posted_at: float
    expires_at: float
    status: JobStatus = JobStatus.OPEN


@dataclass
class Application:
    app_id: int
    job_id: int
    seeker_id: str
    status: AppStatus = AppStatus.SUBMITTED


class Spec:  # 规格：一个条件一个类，search 只认 ok(job)；新增筛选项只加类
    def ok(self, j: Job) -> bool: raise NotImplementedError

@dataclass
class SalarySpec(Spec):
    at_least: int
    def ok(self, j: Job) -> bool: return j.salary_max >= self.at_least

@dataclass
class OpenSpec(Spec):
    now: float  # 过期靠比较时间，不靠定时任务改状态
    def ok(self, j: Job) -> bool: return j.status is JobStatus.OPEN and j.expires_at > self.now


class JobBoard:
    def __init__(self) -> None:
        self.jobs: dict[int, Job] = {}
        self.apps: dict[int, Application] = {}
        self._applied: dict[tuple[str, int], int] = {}  # (求职者, 职位) -> 申请号，唯一性
        self._ids = itertools.count(1)
        self._lock = Lock()

    def post_job(self, employer_id: str, title: str, salary_max: int, now: float, ttl_days: int = 30) -> Job:
        j = Job(next(self._ids), employer_id, title, salary_max, now, now + ttl_days * 86400)
        self.jobs[j.job_id] = j
        return j

    def search(self, now: float, *specs: Spec, limit: int = 20) -> list[Job]:
        specs += (OpenSpec(now),)  # 全部条件都满足；"或" 见逐步扩展 1
        hits = [j for j in self.jobs.values() if all(s.ok(j) for s in specs)]
        hits.sort(key=lambda j: (-j.posted_at, j.job_id))  # job_id 打破并列，游标分页才稳定
        return hits[:limit]

    def apply(self, seeker_id: str, job_id: int, now: float) -> Application:
        with self._lock:  # 检查职位状态 + 唯一性 + 写入，必须在同一个临界区
            j = self.jobs[job_id]
            if j.status is not JobStatus.OPEN or j.expires_at <= now:
                raise ValueError("职位已关闭或过期")
            key = (seeker_id, job_id)
            if key in self._applied:  # 幂等：重复投递返回已有申请，而不是再建一条
                return self.apps[self._applied[key]]
            a = Application(next(self._ids), job_id, seeker_id)
            self.apps[a.app_id] = a
            self._applied[key] = a.app_id
            return a

    def update_status(self, actor_id: str, app_id: int, to: AppStatus) -> Application:
        with self._lock:
            a = self.apps[app_id]
            if to is AppStatus.WITHDRAWN:
                if actor_id != a.seeker_id:
                    raise PermissionError("只能撤回自己的申请")
            elif actor_id != self.jobs[a.job_id].employer_id:
                raise PermissionError("只有职位所属雇主可以推进状态")
            if to not in ALLOWED.get(a.status, set()):
                raise ValueError(f"{a.status.name} -> {to.name} 不允许")
            a.status = to
            return a
```

**运行。**

```python
b = JobBoard(); now = 1000.0
j1 = b.post_job("acme", "Python Engineer", 180, now)
j2 = b.post_job("acme", "Go Engineer", 150, now + 1)
j3 = b.post_job("beta", "Python Intern", 60, now + 2)
```

- **搜索结果最新在前：** `b.search(now + 3, SalarySpec(100))` → Go Engineer、Python Engineer（最新的在前）。
- **30 天后全部过期：** `b.search(now + 31 * 86400)` → `[]`，30 天后全部过期，不需要定时任务。
- 8 个线程同时用 `"ann"` 投 `j1` → 8 次返回同一条申请，`len(b.apps) == 1`。
- 雇主 `acme` 把它改成 `VIEWED` 成功；`beta` 改 `SHORTLISTED` → `PermissionError`；`acme` 直接改 `HIRED` → `ValueError`（`VIEWED -> HIRED 不允许`）；`ann` 撤回成功，再改任何状态都是 `ValueError`。

**复杂度。** 搜索 `O(n · k)`，`n` 是职位数，`k` 是条件数；投递和改状态 `O(1)`。

**逐步扩展。**
1. 【追问再讲】「或」和新筛选项：给 `Spec` 加 `&`、`|`，条件组合成树；新增筛选项只加一个类，`search` 不改。

```python
class Spec:
    def ok(self, j: Job) -> bool: raise NotImplementedError
    def __and__(self, o): return Combined(lambda j: self.ok(j) and o.ok(j))
    def __or__(self, o): return Combined(lambda j: self.ok(j) or o.ok(j))


class Combined(Spec):
    def __init__(self, f) -> None: self.ok = f


@dataclass
class KeywordSpec(Spec):
    word: str
    def ok(self, j: Job) -> bool: return self.word.lower() in j.title.lower()
```

`b.search(now + 3, KeywordSpec("go") | SalarySpec(170))` → Go Engineer、Python Engineer；`KeywordSpec("python") & SalarySpec(100)` → 只有 Python Engineer。

2. 【追问再讲】通知：邮件、站内信、推送各自订阅事件，发布放在锁外，慢订阅者不会阻塞投递。

```python
class EventBus:
    def __init__(self) -> None:
        self._subs: list = []

    def subscribe(self, fn) -> None:
        self._subs.append(fn)

    def publish(self, name: str, payload: dict) -> None:
        for fn in self._subs:  # 各渠道自己订阅，主流程不关心
            fn(name, payload)

# JobBoard.__init__(self, bus) 保存 self.bus；apply 里新建申请之后，跳出 with 块再发布：
#     self.bus.publish("ApplicationSubmitted", {"employer": j.employer_id, "app": a.app_id})
#     return a
```

订阅一个收集函数，投递一次 → 收到 `("ApplicationSubmitted", {"employer": "acme", "app": 2})`。`update_status` 同理发布 `StatusChanged`。

3. 【追问再讲】倒排索引：关键词先查「词 → 职位集合」求交集，再套规格。

```python
def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9+#]+", text.lower()))

# post_job 里：for t in tokens(title): self._index.setdefault(t, set()).add(job_id)
# search 里：ids = set.intersection(*(self._index.get(w, set()) for w in tokens(query)))，候选只取 ids
```

`query="python engineer"` → 只有 Python Engineer；`query="python"` 加 `SalarySpec(100)` → Python Engineer。

**深入。**
1. 【必讲】搜索条件为什么用规格模式。
   - 把所有条件写成 `search(keyword, city, salary, skills, ...)` 的长参数列表：每加一个筛选项就要改签名和实现，「并且」「或者」的组合也写死。
   - 规格模式：每个条件一个对象，`&` 与 `|` 组合成树，`search` 只依赖 `ok(job)`；新增筛选项（公司规模、学历）只增加一个类。
   - 数据量大时，规格也可以翻译成数据库查询或搜索引擎的过滤器，接口不变。
2. 【必讲】申请的状态与权限。
   - 迁移表集中定义，非法迁移（比如已拒绝再入围）直接拒绝，终态没有出边。
   - 权限放在服务方法内，而不是靠调用方自觉：撤回只能由申请人，推进只能由职位所属雇主。
3. 【必讲】投递的原子性。
   - 「检查职位开放 + 检查是否已投 + 写入」是一个复合动作，必须原子。内存版一把锁；数据库版在事务里插入，依赖唯一约束 `(job_id, seeker_id)`，冲突时返回已有记录。
   - 职位关闭与投递的竞争用 `SELECT ... FOR UPDATE` 或乐观版本号。
   - 事件发布放在锁外，避免订阅者阻塞核心流程。
4. 【追问再讲】过期不依赖定时任务：用 `expires_at` 和当前时间比较（`OpenSpec`），即使清理任务延迟，搜索与投递也不会返回过期职位；定时任务只负责归档。关闭职位后，已有申请保持原状态由雇主继续处理，或批量标记为拒绝并通知。时间通过参数注入，便于测试。
5. 【追问再讲】通知解耦：观察者模式，新增渠道只加订阅者，不改 `apply` 和 `update_status`。生产里订阅者通过消息队列异步消费，对重复事件幂等，通知失败不能影响投递结果。
6. 【加分】演进到搜索引擎：内存倒排索引适合几千到几万个职位。上到百万级换成 Elasticsearch 一类：职位写入数据库后异步同步到索引，搜索走索引，详情走数据库；筛选项用过滤器（不计分），关键词用相关性评分；热门筛选结果可缓存。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 搜索排序：初版按时间倒序；进一步按相关性（关键词命中、技能匹配度）加时间衰减；个性化推荐是另一个子系统。
- 防刷：投递限流、每人每天投递上限、验证码；职位发布需要审核或信用额度。
- 简历怎么存：对象存储，申请里只存引用与版本，投递时锁定当时的简历版本。
- 怎么测试：时间通过参数注入；对 `apply` 做并发测试，多个线程重复投递同一职位，断言只有一条申请。
- 申请量巨大的雇主视图：申请列表分页，按状态索引；统计用只读视图或预聚合。

**级别期望。**
- 中级：职位、申请几个类，基本的发布、搜索、投递流程；核心实现能跑通搜索和投递。
- 高级：规格模式组合搜索条件、申请状态机与权限、重复投递的唯一性与并发、观察者式通知、游标分页。
- 资深（staff）：内存索引到搜索引擎的演进、数据库约束与事务边界、过期的无定时依赖设计、通知的异步与幂等、可测试性，以及哪些变化点值得抽象。

**先修概念。** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-concurrency-intro|并发入门]]

**同类题。** [[solution-linkedin]]、[[solution-online-shopping]]、[[solution-notification-service]]、[[solution-task-management]]
