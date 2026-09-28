# CodeSignal ICF 心法：分级模拟题（Progressive Simulation）怎么做

适用范围：CodeSignal 的 Industry Coding Framework（ICF / ICA）题型。这类题都是"一个项目、4 个 level、90 分钟"：
In-Memory Database、Parcel Tracking、Bank System、Cloud Storage、File System 等等。
Airbnb、Coinbase、Ramp 等公司都用它。题目换皮，**骨架是同一个**，所以心法可以直接迁移。

## 1. 它考的不是算法，是"需求变更下的状态建模"（state modelling）

LeetCode 考的是：给定一个固定问题，找最优解。ICF 考的是：需求每 20 分钟变一次，你的代码能不能**不推倒重来**地跟上。
所以评分真正在意的只有两件事：

1. **正确性**：隐藏单元测试（hidden unit tests）全过才能解锁下一级。题面原话是
   "You are not required to provide the most efficient implementation"。
2. **速度**：90 分钟 4 级。大多数人死在 Level 3–4 的时间上，而不是写不出来。

推论：**不要优化复杂度，也不要提前设计。每一级只写让这一级测试通过的最少代码，到下一级再重构。**
时限要看清楚：页面上写的是 3 秒，但每个测试其实都带 `@timeout(0.4)`，也就是 0.4 秒。
即便如此，dict 加上每次 O(k log k) 的排序也绰绰有余；真正会超时的只有写出嵌套全表扫描这种代码。

## 2. 四级的固定骨架（背下来）

| Level | 典型需求 | 最少要写什么 |
|---|---|---|
| 1 | CRUD：set / get / delete | `dict[id, dict[field, value]]`，三个方法 |
| 2 | 查询：scan / 按前缀 / 排序 / top-k | 一个"过滤 + 排序 + 格式化"函数 |
| 3 | 时间：timestamp、TTL 过期、按时间查询 | value 换成 `(value, expires_at)`；读的时候判断是否还活着 |
| 4 | 历史：backup/restore、undo、merge、按历史时刻回放 | 快照（snapshot）和活状态隔离；TTL 换算成"剩余时间" |

**先把 4 行 level 概要读完，再写 Level 1。** 读概要是为了知道后面会往哪里加东西（这样就不会选错数据结构），而不是为了提前把后面的代码写好。

## 3. 六条心法

### 心法 1：每级只写这一级需要的，数据结构选对就行

Level 1 就是 `dict[parcel_id, dict[tag, value]]` 加三个方法，大约 10 行。**不要**提前包成 `Entry` 类，也**不要**提前写 `timestamp` 参数。

提前准备其实省不了多少时间：到 Level 3 时把 `value` 改成 `(value, expires_at)` 只涉及 3 个方法，大约 2 分钟。
而提前设计的代价是，Level 1 的时间花在测试根本不测的东西上，而且你猜的 L3 形状可能是错的，因为 L2–L4 的细节只有解锁之后才看得到。

数据结构选择这件事确实值得提前想：两层 dict（先按包裹再按 tag），因为 Level 2 要"列出一个包裹的所有 tag"。
这不是过度设计，这是选对容器。

### 心法 2：到 Level 3 才做的一次重构：旧方法委托给新方法

```python
def get_tag(self, p, t):         return self.get_tag_at(p, t, None)   # 旧方法只剩一行
def get_tag_at(self, p, t, ts):  ...                                  # 逻辑只写在这里
```

`None` 的意思是"忽略过期"。**这是 Level 3 解锁后才做的重构**，不是 Level 1 就写好的。
它的好处是：`get_tag` 和 `get_tag_at` 不会变成两份几乎一样、将来改一处忘一处的代码。

### 心法 3：时间区间一律左闭右开 `[start, end)`

`alive = ts < expires_at`，而不是 `<=`。几乎所有 ICF 的 TTL 题都写明了 `[timestamp, timestamp + ttl)`。
边界测试（在 `expires_at` 那一刻查询）一定会有。左闭右开还有一个好处：相邻区间首尾相接，不重叠也不留缝。

### 心法 4：快照要深拷贝，而且拷贝成"不可变的纯数据"

Level 4 最常见的两个 bug：

- **浅拷贝（shallow copy）**：`snapshot = dict(self.data)` 只复制外层，内层的 tag 字典还是共享的，之后的写入会"漏进"快照。
- **恢复时引用别名（aliasing on restore）**：`self.data = snapshot` 让活状态直接指向快照对象，之后的修改会污染快照，第二次 restore 就错了。

解法：checkpoint 时构造新的纯数据（tuple），restore 时再重新构造一份新的活对象。**两个方向都要拷贝。**
`copy.deepcopy` 也能用，但显式构造更清楚，还能顺便完成 TTL 换算（见心法 5）。

### 心法 5：存"剩余量"，不存"绝对量"（relative, not absolute）

restore 的题面几乎都会说"expiration times should be recalculated according to the timestamp of this operation"。
意思是：checkpoint 时剩多少寿命，restore 之后还剩多少寿命。所以快照里存的是 `remaining = expires_at - checkpoint_ts`，
restore 时再换算成 `new_expires_at = restore_ts + remaining`。
另外，**checkpoint 时已经过期的条目根本不存**，否则 restore 会让它"复活"。

### 心法 6：返回值的类型要精确

- 要 `bool` 就返回 `True/False`，不要返回 `1`、`None` 或 dict。有的测试用 `assertIs(x, True)`。
- 要 `str | None` 就不要用 `if value:` 判断存在性。空字符串 `""` 是合法值，应该用 `is None` 判断。
- 列表格式 `"field(value)"` 逐字照抄，排序规则写明：Python 默认的字符串排序是按码点（code point），所以大写排在小写前面。

## 4. 90 分钟怎么分配

| 阶段 | 时间 | 动作 |
|---|---|---|
| 读题 | 5 min | **把 4 个 level 的概要全读完。** 它们就写在 Requirements 里，照片里那段就是。根据 L3/L4 决定 L1 的数据模型。 |
| L1 | 5–10 min | 两层 dict + 3 个方法，约 10 行。跑测试，提交。 |
| L2 | 10 min | 一个 `_list(prefix, ts)` 通用函数。 |
| L3 | 25 min | value 改成 `(value, expires_at)`；旧方法委托给 `_at` 版本（心法 2）。 |
| L4 | 30 min | 快照隔离 + TTL 换算 + `bisect` 找"≤ t 的最近一个"。 |
| 缓冲 | 10 min | 看失败的测试名，逐个用 `run_single_test.sh` 定位。 |

实战技巧：

- **题面最上面那 4 行 level 概要是免费的剧透。** 大多数人直接跳到 Level 1 开写，这就浪费了它。
- 每过一级都会解锁新的测试文件。先读新测试的**名字**：它们就是这一级的边界清单。
- 某一级卡住超过 10 分钟，先让大部分测试通过再提交。分数通常按通过的测试数算，部分分也是分。
- 不要写 print 调试然后忘了删。用 `run_single_test.sh "<name>"` 只跑一个测试。

## 5. 识别信号：什么样的题该用这套

- 题目要求实现一个类（`XxxSystemImpl(XxxSystem)`），有一个锁定的 ABC 接口
- 分成 Level 1–4，写着 "Subsequent levels are opened when the current level is correctly solved"
- 出现 timestamp / TTL / backup / restore / history / undo 这类词

看到这些信号，第一反应应该是：**先读完 4 行概要选对容器；每级只写最少代码；区间左闭右开；快照两头都拷贝；存剩余量。**

## 6. 同族题（骨架一样，换皮而已）

只有 In-Memory Database 这一行查过来源（见 `catalog/raw/in_memory_db_isomorph.md`）。
Bank System 和 Cloud Storage 两行是按网上流传版本凭记忆写的，**本 repo 没有核实过**，做之前先查原题。

| 题 | L3 的"时间"是什么 | L4 的"历史"是什么 |
|---|---|---|
| In-Memory Database | field 的 TTL | backup / restore |
| Parcel Tracking（本题 q01） | tag 的 TTL | checkpoint / restore |
| Bank System | 定时付款（scheduled payment） | 合并账户（merge accounts）、查询历史余额 |
| Cloud Storage / File System | 用户容量配额 | 备份和恢复用户文件 |

练习路径：先把 q01 写熟，再把同一套骨架套到 Bank System 上，确认你能在 60 分钟内写完。
