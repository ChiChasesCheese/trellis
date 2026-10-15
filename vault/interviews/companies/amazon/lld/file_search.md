# LLD：Unix `find` / 文件搜索（带过滤器）——教科书模式

> 题库里相邻的是 [lld:design-in-memory-file-system](../../../../domains/low-level-design/drills/problems/design-in-memory-file-system.md)（题解 [lld-solution:in-memory-file-system](../../../../domains/low-level-design/problems/in-memory-file-system/solution.py)）：它解决的是"文件系统本身"（mkdir/ls/mv/cp/glob 搜索，`File`/`Directory` 不共享基类）。
> **本题不同**：树已经存在，重点是 **"多条件、可组合、可扩展的搜索"**——这是 Amazon 的 OOD 轮最爱的形状（"加一个新条件时你要改几处代码？"）。
> 代码：`code/file_search.py`（`python3 -I code/file_search.py` 打印 `OK file_search`）。
> 参照规范：POSIX `find`（https://pubs.opengroup.org/onlinepubs/9699919799/utilities/find.html ，2026-10-15 抓取）。
> 官方对这轮的评分描述（`../catalog/raw/official.md` §4.3，逐字）："organize your methods and classes to ensure a clear separation of concerns … Make code extendable and avoid single functions that do everything … When you're satisfied you've met the original requirements, seek more requirements to show how your solution evolves when requirements change."

## 1. 这道题在问什么

面试官说："给你一棵文件系统树。实现 `find`：能按名字、扩展名、大小、修改时间、类型筛选文件；条件还要能用 AND / OR / NOT 组合。"

最小例子（树）：
```
/
├── a.txt        100 B   mtime=1000
├── b.py        2048 B   mtime=2000
├── docs/
│   ├── readme.md 5000 B
│   └── old.md      10 B
└── src/
    ├── main.py  3000 B
    └── util.py   500 B
```
查询："扩展名是 py **并且** 大小 ≥ 1 KB" → 手算：`b.py`(2048 ✓)、`main.py`(3000 ✓)、`util.py`(500 ✗) → `["/b.py", "/src/main.py"]`。
查询："(py 或 md) **并且不是** 名字以 test_ 开头" → 得到 `b.py, old.md, readme.md, main.py, util.py`。

**面试官真正想看到的**（官方措辞：separation of concerns / extendable / evolves when requirements change）：
1. 你把"遍历树"和"判断一个节点是否满足条件"**分开**。
2. 加第 7 种条件时，**不用改** `find` 本身，也不用改已有的条件。
3. 条件能自由组合，而且组合不需要为每种组合写一个类（`ExtAndSize`、`ExtOrName` …爆炸）。

## 2. 前置知识（每节四问：是什么 → 为什么需要 → 怎么工作 → Python 怎么写）

### 2.1 组合模式（Composite）与文件系统树
- **是什么**：树里"叶子"和"容器"用统一方式对待。文件是叶子，目录是容器。
- **为什么**：搜索要对树里每个节点做同样的判断，不想到处写 `if isinstance(...)`。
- **怎么工作**：本题里节点只有三种：`File`（有大小）、`Directory`（有 `children`）、`Symlink`（有 `target`）。
  题库那道题的结论是"File 和 Directory 不必共享基类"（题库 [lld:design-in-memory-file-system](../../../../domains/low-level-design/drills/problems/design-in-memory-file-system.md) 的评分点）；我们同样**不做共同基类**，而是都带一个 `type` 属性，过滤器按 `type` 判断即可。
- **注意**：节点**不存自己的完整路径**。路径是遍历时临时算出来的 `Entry(path, node, depth)`。原因：同一个目录可以经由符号链接从两个路径到达，存路径会错；这也与真实文件系统（名字存在父目录里）一致。

### 2.2 谓词与 Specification 模式
- **是什么**：一个"回答是/否"的小对象 `matches(x) -> bool`，可以用 AND / OR / NOT 组合成更大的谓词。
- **为什么**：没有它，你会写 `find(root, name=None, ext=None, min_size=None, max_size=None, after=None, …)` 一个参数越来越多的函数（见 §3）。
- **怎么工作**（树形结构，`Not(Or(Ext('py'), Ext('md')))`）：
```
         NotFilter
            │
         OrFilter
        /        \
  Extension(py)  Extension(md)         matches(entry): 先问子谓词再合并结果
```
- **Python**：给基类写 `__and__`、`__or__`、`__invert__`，就能写 `Extension("py") & Size(min_bytes=1024)`；这些返回**新对象**，原对象不变（不可变 → 可复用、线程安全）。
- **与 POSIX 的对应**：`find` 里 AND 是隐含的、`-o` 是 OR、`!` 是 NOT，并且规范要求"第二个表达式在第一个为假时不求值"（`-a` 短路），OR 同理——我们的 `AndFilter.matches` 用 Python 的 `and`，天然短路。
  **推论**：把便宜的条件（名字、类型）放在昂贵的条件（读文件内容）左边。

### 2.3 迭代器 / 生成器与"显式栈"遍历
- **是什么**：`yield` 一个一个地产出结果，调用方要多少取多少。
- **为什么**：(1) 树可能有几亿个节点，不能先把所有结果放进列表；(2) 调用方只想要第一个匹配（`next(...)`）就不该走完整棵树；(3) "拿到结果后做什么"（打印、求和、删除）变成消费者的事，不需要在 `find` 里加 `action` 参数。
- **为什么不用递归**：Python 默认递归深度约 1000；一条很深的目录链会 `RecursionError`。用 `stack = [...]` 手动深度优先。
- **怎么工作**：弹出一个条目 → 检查并 `yield` → 若是目录，把子节点**逆序**压栈（这样弹出时是升序，输出顺序稳定、可测试）。

### 2.4 符号链接、inode 与"环"
- **是什么**：符号链接是"一个存着另一条路径的文件"。`loop -> /` 会让遍历永远走下去：`/loop/loop/loop/...`
- **为什么需要处理**：不处理就是无限循环或栈爆。
- **怎么工作**：POSIX 的做法是默认**不跟随**符号链接（`-H`/`-L` 选项才跟随）。我们同样默认不跟随（链接只作为叶子条目出现）；跟随时，每个栈元素带上它的**祖先目录集合**（`frozenset(id(目录对象))`），目标目录已在祖先链上就不再展开。
- **为什么是"祖先链"而不是全局 visited 集合**：`/docs` 与 `/link_to_docs` 是**两条合法路径**指向同一个目录，用户期望两条路径下的文件都被报告；全局 visited 会漏掉第二条。环只发生在"自己的祖先"。
- **悬空链接**（目标不存在）当叶子，不报错。

### 2.5 glob 与正则
- `-name` 在 POSIX 里用 shell 模式（`*`、`?`、`[...]`），且只匹配**最后一段名字**。`fnmatch.fnmatchcase` 正好是它（区分大小写）。
- 正则功能更强但更慢、更难读；做成另一个过滤器 `NameRegex`，用 `re.fullmatch`（整名匹配，避免 `re.match` 只匹配开头的坑）。

## 3. 从最笨的解法开始

```python
def find(root, name=None, ext=None, min_size=None, max_size=None, after=None, before=None, owner=None, kind=None):
    for path, node in walk(root):                 # 递归
        if name and not fnmatch(node.name, name): continue
        if ext and not node.name.endswith("." + ext): continue
        if min_size is not None and node.size < min_size: continue
        ...
        yield path
```
**它具体在哪里错/慢**：
1. **只能 AND**。"py 或 md"、"不是 test_*" 没法表达 → 面试官一句"那 OR 呢"就卡住。
2. **每加一种条件改函数本身**：参数从 8 个变 9 个，测试要把所有组合重新跑；违反开闭原则。
3. **`min_size` 对目录没意义**，`ext` 对目录也没意义，这些语义混在一堆 `if` 里。
4. 递归遍历，深目录栈溢出；一次性 `list` 返回，大树吃内存。

## 4. 一步一步改进

| 步 | 发现的问题 | 想法 | 为什么有效 | 代码变化 | 新代价 |
|---|---|---|---|---|---|
| 1 | 只能 AND | 把每个条件变成一个对象 `Filter.matches(entry)`；`find(root, filters: list)` 全部满足才输出 | 条件成了数据，可存储可传递 | `find` 里 `all(f.matches(e) for f in filters)` | 仍然没有 OR / NOT |
| 2 | 没有 OR / NOT | 加 `AndFilter / OrFilter / NotFilter`（本身也是 Filter） | 组合器和叶子条件同一接口 → 任意嵌套（Composite） | 3 个小类 | 写法啰嗦：`AndFilter(Extension("py"), Size(...))` |
| 3 | 写法啰嗦 | 重载 `& \| ~` | 读起来像逻辑表达式；返回新对象不改旧的 | 基类 3 个 dunder 方法 | 无 |
| 4 | 递归 + 返回列表 | 显式栈 + `yield` | 惰性、不爆栈、可只取第一个 | `find` 变成生成器 | 要自己维护栈元素 |
| 5 | 排序不稳定 | 同目录按名字排序、逆序压栈 | 输出确定，可 assert | 一行 `sorted(..., reverse=True)` | 每个目录排序 O(k log k) |
| 6 | 符号链接环 | 栈元素带祖先目录集合 | 只在"自己的祖先"处止步 | 栈元素多一个 `frozenset` | 每个栈元素多占一个集合（共享不可变，省内存）|
| 7 | 不想进入某些目录 | `prune(entry)` 回调 | 整棵子树不展开 → 少读目录 | 一个可选参数 | 语义要说清（目录本身仍被过滤器检查）|
| 8 | 不知道是否真的惰性/剪枝 | `FindStats` 计数 | 测试可以断言"走过的节点数更少" | 一个小数据类 | 无 |

## 5. 逐段讲参考解（`code/file_search.py`）

**5.1 节点与 Entry**
```python
@dataclass
class Directory:
    name: str; ...; children: dict[str, "Node"] = field(default_factory=dict)
    def add(self, node): ...   # 同目录重名 → ValueError
```
`children` 用 `dict[name -> node]`：按名字 O(1) 查找（路径解析、`add` 防重名）；遍历时再 `sorted`。为什么不用 list：重名检查要 O(n)。
`type = NodeType.DIR` 写在类里（不是 dataclass 字段，没有类型注解），所以不进 `__init__`，是每个类的常量。

**5.2 过滤器基类**
```python
class Filter(ABC):
    @abstractmethod
    def matches(self, entry: Entry) -> bool: ...
    def __and__(self, o): return AndFilter(self, o)
    ...
```
- 为什么 `matches` 收 **Entry** 而不是 Node：`MaxDepth` 要深度，将来的 `PathPrefix` 要路径。给过滤器**够用的上下文**，又不暴露整个遍历器。
- `@dataclass(frozen=True)`：给叶子条件自动生成 `__init__/__eq__/__hash__`，且**不可变**。

**5.3 Size 与 Modified 的"闭区间 + None"**
`Size(min_bytes=1024)` / `Size(max_bytes=…)` / 两者都给 → 区间。`None` 表示该端不限。一个类覆盖 `>`、`<`、`=`、范围。
对目录/链接恒不匹配 `Size`：因为目录的 `size` 在真实系统里没有"文件大小"的含义（POSIX `-size` 说的是文件大小）。

**5.4 `FileSearcher.find` 主循环**（看代码里的中文注释，逐行对应上面表格的步骤 4–7）
- `if entry.path != "/" and flt.matches(entry): yield entry`：根目录自己不输出。
- 符号链接且跟随：把 `node` 换成目标目录再往下走；悬空/指向文件 → `continue`。
- `id(node) in ancestors` → 环，不展开。
- `prune(entry)` 为真 → 不展开（但目录条目本身刚刚已经被检查/输出过）。
- 与 POSIX `-prune` 的区别：POSIX 的 `-prune` 是一个**永远为真、带副作用的条件**，要用 `-o -print` 的惯用法拼出来（容易写错）；我们把它拆成独立参数，语义更直白。

**5.5 查询小语言**（追问：用字符串表达条件）
递归下降解析器，**每个产生式一个函数**：`expr`(or) → `term`(and) → `factor`(not/括号/原子)。优先级 not > and > or 与 Python 的 `~ > & > |` 一致，所以解析结果能直接用运算符组合。语法错误抛 `ValueError`。

## 6. SOLID 与设计选择（面试里要说出口）

| 原则 | 本题里的体现 | 一句话 |
|---|---|---|
| S 单一职责 | `FileSearcher` 只管遍历；`Filter` 只管判断；输出由调用方消费 | "遍历、判断、动作三件事分开" |
| O 开闭 | 新增条件 = 新增 `Filter` 子类（测试 §10 就在测试里临时定义了 `NameLongerThan`） | "加条件不改 find" |
| L 里氏替换 | 任何 `Filter` 子类（含组合器）可互换使用 | 组合器与叶子同一接口 |
| I 接口隔离 | `Filter` 只有一个方法 | 不逼实现者实现用不到的东西 |
| D 依赖倒置 | `FileSearcher` 依赖抽象 `Filter`，不依赖具体条件 | 搜索器对条件种类无知 |
| 模式 | Composite（树与组合器）、Specification（谓词）、Iterator（生成器）| 不要为模式而模式：没写 Visitor/Command，因为生成器已够用 |

## 7. 追问预演（每个：问题 → 思考 → 答案要点）

**Q1. 加一个"文件内容包含某字符串"的条件。**
思考：这是新的**昂贵**条件，需要读文件；`File` 没有内容字段。
答案：新增 `ContentContains(text, reader)` 子类；`reader: Callable[[Entry], Iterable[bytes]]` 由外部注入（依赖倒置，测试里用内存桩）。放在 AND 的**右边**，利用短路，先用名字/大小过滤掉大多数文件。不改 `FileSearcher`。

**Q2. 结果要按大小降序取前 N 个。**
答案：消费者的事。`heapq.nlargest(n, finder.find(root, flt), key=lambda e: e.node.size)`：O(M log N) 时间、O(N) 内存（M = 匹配数）。不要先 `list` 再 `sort`（O(M) 内存）。

**Q3. 要"对每个匹配执行动作"（删除、打印、统计总大小）。**
答案：`for e in finder.find(...): action(e)` 或 `sum(e.node.size for e in …)`。生成器就是 Iterator 模式；不需要 Visitor。若需要**可撤销/可记录**的动作（先 dry-run 再执行）再引入 Command：先收集成列表审查，再逐个执行。

**Q4. 树有几亿个文件，每次搜索都遍历太慢。**
答案：建**倒排索引**：`ext -> {path}`、`name -> {path}`、按 size 分桶。代价：(1) 内存；(2) **失效**——文件变更要更新索引（监听文件系统事件 inotify / 或周期性重建，接受陈旧）。通配符和范围查询对精确匹配索引不友好（题库在 [lld:design-in-memory-file-system](../../../../domains/low-level-design/drills/problems/design-in-memory-file-system.md) 第 3 关讨论过：通配符模式没有精确匹配划算）。折中：索引用于**粗过滤**，再用 `Filter` 做**精确复核**，保证正确性。

**Q5. 并发：搜索进行中有人创建/删除文件。**
答案：几种语义：(1) 弱一致——遍历时看到什么算什么（Unix `find` 就是这样），实现上遍历前对 `children` 做**快照** `list(node.children)`；(2) 读写锁/全局锁——简单但阻塞写；(3) 不可变树 + 写时复制（持久化数据结构），搜索读旧版本，天然一致。面试里先选(1)并说清语义，再谈(3)。我们的代码对 `children` 迭代用的是 `sorted(node.children)` 先得到列表，已经是一次性快照键列表。

**Q6. 并行加速。**
答案：把顶层子目录作为任务交给线程/进程池，各自生成结果再合并；注意 (a) 输出顺序不再稳定（要排序则需要归并）；(b) I/O 密集用线程，CPU 密集（正则、解压）用进程；(c) 每个任务带自己的祖先链，不共享可变状态；(d) 总并发数要限制，避免打爆磁盘或 S3（若底层是对象存储，LIST 有速率限制）。

**Q7. 大小写不敏感 / Windows 路径 / Unicode 规范化。**
答案：`NameGlob(pattern, case_sensitive=True)` 用 `fnmatch.fnmatch`（平台相关）或 `.lower()` 比较；路径分隔符统一在 `Entry` 构造处处理；Unicode NFC/NFD 差异（macOS）在比较前统一规范化。

**Q8. 权限不足的目录。**
答案：真实实现里 `children` 访问可能抛 `PermissionError`；`find` 应该**跳过并记录**，不要整个搜索失败（Unix `find` 打印 "Permission denied" 后继续）。在 `FileSearcher` 加 `on_error` 回调（默认收集）。

**Q9. 分页（"每次给我 100 个"）。**
答案：因为输出顺序是确定的（字典序前序），**游标 = 上一页最后一个路径**；下一页从该路径之后继续遍历（需要能 seek：沿路径逐层 `sorted` 后跳过小于游标的兄弟）。不要用 offset（每页都重走）。

**Q10. 把它做成服务（给很多用户用）。**
答案：此时是系统设计题：索引服务 + 元数据存储 + 增量更新 + 权限过滤（只返回用户有权看到的）。可以引向 `../sd/` 里的题。

**Q11. 条件太多时，怎么保证顺序性能？**
答案：成本模型：给 `Filter` 加 `cost` 属性，组合器按 cost 升序重排 AND 的子条件（OR 同理按"命中率高/成本低"重排）。前提：条件之间**无副作用**且**可交换**。

**Q12. 为什么不用继承做"FileFilter / DirectoryFilter"？**
答案：条件的种类和组合方式是两个独立变化的维度；继承把它们绑死。组合（对象持有对象）让两者各自扩展：这就是"优先使用组合而非继承"。

## 8. 常见误区（很多人这样写 → 为什么错 → 正确写法）

1. **把路径存进节点**：同一目录经符号链接有多条路径；移动目录时要递归更新所有子节点。→ 路径在遍历时算。
2. **用全局 `visited` 防环**：漏报合法的第二条路径。→ 祖先链。
3. **`AndFilter` 里先 `left.matches` 再 `right.matches` 都算好再 `and`**：失去短路，昂贵条件白算。→ 直接 `left.matches(e) and right.matches(e)`。
4. **`Size` 对目录也比较 `size`**：目录大小在不同系统意义不同，结果混乱。→ 明确只对文件生效。
5. **递归实现 + 返回列表**：深树栈溢出、全量内存。→ 显式栈 + 生成器。
6. **用 `re.match` 做名字匹配**：只匹配开头，`test_` 会误中 `test_x_backup`。→ `re.fullmatch` 或 `fnmatch`。
7. **扩展名用 `name.split(".")[-1]`**：`.bashrc`、`Makefile` 会被误判。→ 先判断是否有"非开头的点"。
8. **每种条件组合一个类**（`ExtAndSize` …）：类爆炸。→ 组合器。
9. **`prune` 放进过滤器里**：过滤器只回答"要不要输出"，不应控制遍历。→ 独立参数。

## 9. 自测题

1. 为什么节点不存路径？
<details><summary>答案</summary>同一目录可经符号链接从多条路径到达；移动目录会使所有子孙路径失效。路径是遍历的函数，不是节点的属性。</details>

2. `~Extension("py") & Size(min_bytes=5000)` 与 `~(Extension("py") & Size(min_bytes=5000))` 结果有何不同？举例。
<details><summary>答案</summary>第一个：非 py 且 ≥5000 字节（如 `readme.md` 5000）；第二个：不满足"py 且 ≥5000"的所有东西，包括小文件、目录、链接。运算符优先级 `~` 高于 `&`。</details>

3. 为什么遍历要把子节点逆序压栈？
<details><summary>答案</summary>栈后进先出；逆序压栈后弹出顺序是升序，保证输出稳定为字典序前序。</details>

4. 写出让搜索只展开前两层、但仍然检查所有已展开条目的调用。
<details><summary>答案</summary>`FileSearcher(max_depth=2)`：深度 ≥2 的目录不再展开。注意 `MaxDepth` 过滤器只是不输出、仍会遍历更深层，不省时间。</details>

5. 现在要支持"修改时间在最近 7 天"，怎么避免代码里读系统时钟？
<details><summary>答案</summary>`Modified(after=now - 7*86400)`，其中 `now` 由调用方传入（或构造 `RecentlyModified(days, clock)` 并注入时钟）。过滤器本身不读时钟，才能确定性测试。</details>

6. （senior）如果底层不是内存树，而是 S3 前缀（每个 `LIST` 一次最多 1000 个键、有请求速率限制），你的设计哪里要变？
<details><summary>答案</summary>节点变成"懒加载"：`children` 不是 dict 而是按需分页拉取的迭代器；遍历器要处理分页 token、限速与重试（带抖动）；"目录"是前缀+分隔符的约定；`Size/Modified` 来自 LIST 返回的元数据（无需 GET）；内容类条件要额外 GET（昂贵 → 放在 AND 右边）；并行按前缀分片。`FileSearcher` 与 `Filter` 的接口不变——这正是依赖倒置的收益。</details>

## 10. 延伸阅读
- POSIX `find`：条件的短路求值、`-prune`、`-H/-L` 对符号链接的语义（本文已抓取核对）。
- 题库：[lld:design-in-memory-file-system](../../../../domains/low-level-design/drills/problems/design-in-memory-file-system.md)（树的建模与 glob 搜索的取舍）、[lld:design-amazon-locker](../../../../domains/low-level-design/drills/problems/design-amazon-locker.md)、[lld:design-parking-lot](../../../../domains/low-level-design/drills/problems/design-parking-lot.md)。
- 模式参考（凭记忆，未抓取）：Evans & Fowler《Specifications》(2002) 为 Specification 模式的出处 `【凭记忆，面试前核对】`。
