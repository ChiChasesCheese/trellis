# od02 · In-Memory File System：树形节点 + 分块存储，练的是"结构锁 vs 内容锁分开"

> [!tldr]
> - 这题考的是：LC 588 的功能扩展——`ls`/`mkdir`/`add_content_to_file`/`read_content_from_file` 打底，再叠加 `rm`/`rmdir`、大文件分块存储、按路径并发加锁
> - 三步套路：先建 `_Dir`/`_File` 两种节点的树 → Part 1/2 把基础 API 和"删除"错误分支写清楚 → Part 3 把文件内容从字符串拼接换成分块列表 → Part 4 把"改树结构"和"写文件内容"分成两把锁
> - 最值得带走的一个模式：**目录树的结构变更需要一把粗锁，但文件内容的追加不需要跟着这把粗锁走**——找到节点这一步锁树，写内容这一步只锁这个文件自己，无关路径的写操作互不阻塞

## 类设计先定契约
```python
class FileSystem:
    def ls(self, path: str) -> list[str]: ...              # 文件返回[文件名]；目录返回排序后子项名
    def mkdir(self, path: str) -> None: ...                 # 类似 mkdir -p；已是目录幂等，已是文件报错
    def add_content_to_file(self, file_path: str, content: str) -> None: ...  # 追加，父目录不存在则报错
    def read_content_from_file(self, file_path: str) -> str: ...
    def rm(self, path: str) -> None: ...                    # 删文件；对目录/根路径报错
    def rmdir(self, path: str) -> None: ...                 # 删空目录；对文件/非空目录/根路径报错
    def size(self, file_path: str) -> int: ...              # O(1)，全程维护累加计数器
```
**不变量（写代码前先想清楚）**：
1. `mkdir` 自动创建缺失的父目录；`add_content_to_file` **不会**——父目录不存在直接 `FileNotFoundError`。
   这是题目刻意设计的不对称点。
2. `rm` 只删文件，`rmdir` 只删空目录，两者的错误分支互不重叠（用错方法要报出对应的类型错误，而不是
   笼统的一个异常）。
3. 根目录 `/` 永远不能被 `rm`/`rmdir`。
4. 文件内容内部是分块列表，不是一个不断拼接的字符串；`size()` 是 O(1) 的累加计数器，不是每次现算。

## 1. 题目在说什么（人话版）
设计一个内存文件系统：`mkdir` 建目录、`ls` 列子项、`add_content_to_file`/`read_content_from_file`
写读文件内容。Snowflake 的版本在此基础上加了删除操作（`rm`/`rmdir`，各自有明确的错误分支）、大文件
分块存储（避免字符串反复拼接的 O(n²)）、以及并发下的按路径加锁。

三行小例子：
```
mkdir /a/b/c
add_content_to_file /a/b/c/d hello
add_content_to_file /a/b/c/d world   # 追加，不是覆盖
read_content_from_file /a/b/c/d      -> "helloworld"
```

## 2. 读题：把文字变成模型
- **实体**：目录节点（`_Dir`，有子项字典）、文件节点（`_File`，有分块列表和累加长度）。
- **输入长什么样**：`main()` 命令流 `MKDIR/ADD/LS/READ/RM/RMDIR/SIZE <path> [content...]`。
- **输出要什么**：成功大多无输出（`LS`/`READ`/`SIZE` 有返回值）；失败输出 `ERROR:<异常类名>`。
- **状态**：一棵 `_Dir`/`_File` 混合树；每个 `_File` 自己的分块列表和长度计数器；一把保护"树结构"的锁
  和每个文件自己的锁。
- **一句话建模**：这是一个 **树形节点 + 显式分离"结构变更"与"内容写入"两类操作的锁粒度设计**问题。

> [!note] 为什么选这个数据结构
> `_Dir`/`_File` 是同一个"节点"抽象的两个变体，用 `isinstance` 区分,这样 `ls`/`mkdir` 等方法可以统一
> 从根开始按路径分量走到目标节点，遇到类型不对（比如中途碰到一个文件却还要继续往下走）就抛
> `NotADirectoryError`。文件内容用分块列表而不是字符串,是因为字符串拼接 `s += chunk` 是 O(len(s))
> 的，n 次追加会退化成 O(n²)；列表 `append` 是均摊 O(1)，`size` 额外维护一个累加计数器就不需要每次
> 都 `len("".join(chunks))`。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：先写 `_Dir`/`_File` 两个节点类的字段，再把 7 个方法的签名和各自的错误分支列成表格
   （哪种非法输入对应哪个异常类型），这张表比代码本身更容易在面试里讲清楚。
2. **Part 1 最小可用**：`_get_node(components)` 从根按路径分量走到目标节点（中途类型不对就报错）；
   `ls`/`mkdir`/`add_content_to_file`/`read_content_from_file` 依次实现，注意 `add_content_to_file`
   不自动建父目录。
3. **Part 2 叠加**：`rm`/`rmdir` 复用 `_get_node` 找到父节点，检查目标类型和是否为空，对应抛四种不同
   的异常；根路径特判 `PermissionError`。
4. **Part 3 叠加**：`_File` 内部把内容存成 `chunks: list[str]`，`add_content_to_file` 只 `append`，
   `read_content_from_file` 才 `"".join`；额外维护 `total_len` 累加器支持 O(1) `size()`。
5. **Part 4 叠加**：给 `FileSystem` 加一把 `_tree_lock`（保护树结构：查找、mkdir、rm、rmdir、插入新
   文件节点），给每个 `_File` 加一把自己的 `lock`（保护它的 chunks 列表）。`add_content_to_file` 先
   在树锁下拿到/创建文件节点，**放开树锁**，再在文件自己的锁下追加内容——这样不同文件的写入不会互相
   等待。

## 4. 代码怎么组织
```
_Dir / _File                          # 两种节点，__slots__ 减少内存开销
_split(path) -> list[str]             # 路径切分成分量列表
FileSystem._get_node(components)       # 树锁内：从根走到目标节点，中途类型不对就报错
ls/mkdir/add_content_to_file/read_content_from_file/rm/rmdir/size(...)
main(stdin, stdout)                    # 解析命令流，按 verb 分派，异常转成 ERROR:<类名>
```
每个公开方法都先算出 `components`，再决定锁的范围：纯读/纯结构变更操作全程持有 `_tree_lock`；
`add_content_to_file`/`read_content_from_file`/`size` 只在"定位/创建节点"这一步短暂持锁，随后切换到
该文件自己的锁去做真正的内容读写。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
class _Dir:
    def __init__(self):
        self.children = {}                     # name -> _Dir | _File

class _File:
    def __init__(self):
        self.chunks = []                       # 分块列表，避免 O(n^2) 拼接
        self.total_len = 0
        self.lock = threading.Lock()           # 只保护这个文件自己

class FileSystem:
    def __init__(self):
        self._root = _Dir()
        self._tree_lock = threading.Lock()     # 保护树结构（查找/建/删节点）

    def _get_node(self, components):           # 假设已持有 _tree_lock
        node = self._root
        for name in components:
            if not isinstance(node, _Dir):
                raise NotADirectoryError()
            if name not in node.children:
                raise FileNotFoundError()
            node = node.children[name]
        return node

    def add_content_to_file(self, file_path, content):
        *parent_parts, name = _split(file_path)
        with self._tree_lock:                   # 短暂持有：定位/创建文件节点
            parent = self._get_node(parent_parts)
            existing = parent.children.get(name)
            if existing is None:
                file_node = _File()
                parent.children[name] = file_node
            elif isinstance(existing, _Dir):
                raise IsADirectoryError()
            else:
                file_node = existing
        with file_node.lock:                    # 放开树锁后才写内容，不阻塞别的文件
            file_node.chunks.append(content)
            file_node.total_len += len(content)

    def rmdir(self, path):
        *parent_parts, name = _split(path)
        with self._tree_lock:
            parent = self._get_node(parent_parts)
            target = parent.children[name]
            if isinstance(target, _File):
                raise NotADirectoryError()
            if target.children:                  # 非空目录不能删
                raise OSError()
            del parent.children[name]
```

## 6. 并发追问怎么答
- **为什么不用一把全局锁**：全局锁会让互不相关路径的操作互相阻塞——在元数据服务这种高并发场景下，
  给 `/a/x` 写内容不该等 `/b/y` 的 `mkdir` 完成。per-path/per-node 锁让无关操作并行。
- **哪些操作用粗粒度的"树结构锁"，哪些用细粒度的"文件锁"**：改变树形状的操作（`mkdir`/`rm`/`rmdir`、
  以及"插入一个新文件节点"这个动作）必须在树锁下做，因为它们会修改共享的 `children` 字典；已存在
  文件的内容追加只需要这个文件自己的锁，不需要占着树锁。
- **`mkdir` 的 check-then-create 竞态怎么防**：两个线程同时对同一条尚不存在的路径 `mkdir`，"检查
  是否存在"和"创建节点"必须在同一把树锁的临界区内完成，不能先查后建（否则两个线程都判断"不存在"，
  各自创建出两份重复节点，后创建的会覆盖前一份，数据丢失）。
- **测试怎么证明**：并发场景下多个线程对同一文件反复 `add_content_to_file`，验证最终内容包含所有
  线程写入的全部 chunk、且每个线程自己写入的 chunk 顺序不变；再用一个"多路径并发明显快于强制串行"的
  计时对照测试证明锁粒度确实做到了细粒度隔离（不做过严的绝对时间断言，只验证有明显差距）。

## 7. 常见跑偏（方法层面，3 条）
- **文件内容用字符串拼接 `content += new_chunk`**：单次操作看起来没问题，但 n 次追加会退化成
  O(n²)，题目专门有一条 perf 测试（1e4 次追加）来抓这个坑，必须用分块列表 + 累加计数器。
- **`add_content_to_file` 也像 `mkdir` 一样自动创建父目录**：题目故意设计成不对称——`mkdir` 是
  `mkdir -p` 语义，`add_content_to_file` 的父目录不存在必须报错，写代码前要把这条列进契约表格，不能
  凭直觉"顺手"让它们行为一致。
- **把树结构锁的范围拉得太大，覆盖到文件内容读写**：如果整个 `add_content_to_file` 都持有 `_tree_lock`
  直到写完内容，等于又退化成了一把全局锁，Part 4 的并发追问会直接问出这个问题。

## 自测清单
- `ls("/")` 初始状态返回 `[]`；`ls` 一个文件路径返回长度为 1 的列表。
- `mkdir` 已存在目录幂等；已存在文件路径报 `FileExistsError`。
- `add_content_to_file` 父目录不存在报 `FileNotFoundError`；空内容合法。
- `rm` 对目录报 `IsADirectoryError`；`rmdir` 对文件报 `NotADirectoryError`；`rmdir` 非空目录报
  `OSError`；对根路径两者都报 `PermissionError`。
- 1e4 次追加（每次 100 字符）在 2s 内完成，验证不是 O(n²) 拼接。
- 多线程对同一文件并发追加不丢更新；多路径并发不退化成整体串行。

## 相关题与 skills id
- skills: **S09**（类设计先定契约，尤其是"对称 vs 不对称"的错误策略）· **S10**（并发正确性：
  per-path 锁粒度）· **S11**（持久化追问：WAL + 快照）· S12（分块存储与缓存分页思路相通）。
- 同族：`od08_lru_ttl_cache` 同样是"树/表结构 + 独立的按 key 加锁"模式。
- 练习命令：`python3 loop/mock.py start od02`
