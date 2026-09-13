# int04 · Review Assignment via git diff + CSV Owners：封装 git 子进程，练的是"外部工具的错误怎么收敛成一个类型"

> [!tldr]
> - 这题考的是：调用 `git diff --name-status` 拿到两分支的变更文件，再用一份 CODEOWNERS 式 CSV 算出该找谁 review——不是算法题，是"怎么把一个外部命令行工具包装成可靠的库函数"
> - 三步套路：把所有 `subprocess.run` 收进一个函数，把 git 能出的各种错误统一成一个自定义异常 → 用一次命令拿到全部变更文件，不要对每个文件单独调用 git → CSV 规则匹配单独一层，"最具体规则优先"和"大小写不敏感"都在这一层解决
> - 最值得带走的一个模式：**调用方永远只应该看到一种异常类型**——`FileNotFoundError`（git 不存在）、非零退出码（分支不存在）、`OSError`（其他系统错误），全部在 `_run_git` 这一个函数里被捕获、归一化成 `RepoError`，业务代码不需要 `import subprocess` 之外的任何东西

## 1. 题目在说什么（人话版）
给定同一个 git 仓库的两个分支，算出它们之间改了哪些文件；再给一份 `path,owner` 的 CSV（支持精确路径和 `prefix/*` 通配），统计每个 owner 名下改了多少文件，找出该主要找谁 review。真实题面用 Java 的 JGit 库算 diff，本仓库为了能在 60 分钟内离线复现、且保持"仅用标准库"的约定，换成了 `git` 命令行 + `subprocess`——这个替换本身就是这题要考的能力：**面试官给的 API 文档说的是一种工具，你完全可以换成另一种语义等价的工具，只要把边界情况（rename 算几个文件、大小写、平局规则）想清楚**。

三行小例子：`feature` 相对 `main` 有一次 rename（`helpers.py -> helper_v2.py`）和三处普通改动，`changed_files` 返回 6 个路径（rename 贡献两个）；CSV 里 `src/payments/*` 命中 alice/bob，但 `src/payments/checkout.py` 有精确规则命中 dave——精确匹配赢过同前缀的通配，`checkout.py` 只算给 dave，不重复算给 alice/bob。

## 2. 读题：把文字变成模型（这里更接近"读 API 文档"而不是"抽数学模型"）
- **外部工具的契约**：`git diff --name-status base...head`（**三点** diff，与两分支的合并基准比较，语义上正好是"这个 PR 引入的变更"，不是简单两个 commit 的直接比较）；输出是 tab 分隔的状态码 + 路径，`A/M/D` 一行一个路径，`R100`/`C100` 一行两个路径（旧路径、新路径都算）。
- **CSV 的契约**：`path,owner`，`path` 可以是精确路径或 `prefix*` 通配；同一文件可能命中多条规则，取"最具体"（字符串最长）的那一档，该档所有 owner 都记一次。
- **输出要什么**：Part 1 是变更文件列表；Part 2 是单个 owner 名；Part 3 是 `--top k` 的 `owner: count` 列表，CLI 形式。
- **状态**：无跨调用状态，每次调用都是"跑一次 git、读一次 CSV、算一次"。
- **一句话建模**：这是一个 **外部命令的输出解析 + 规则表匹配 + 计数聚合** 问题，三层各自独立，唯一贯穿全题的纪律是"错误在最外层就要归一化"。

> [!note] 为什么把所有 git 调用收进一个 `_run_git`
> 候选是"每个需要跑 git 的地方各自 `subprocess.run` 一次，各自 `try/except`"，或者"一个 `_run_git(repo, args) -> str` 统一处理 `FileNotFoundError`（git 不存在）、非零退出码（分支不存在/不是仓库）、`OSError`，全部包成 `RepoError`"。选前者，`changed_files` 之外任何将来新加的 git 调用（比如 `git log`）都要重新写一遍错误处理；选后者，`RepoError` 是调用方唯一需要认识的异常类型，网络/CLI 工具类题目的通用做法都是这个模式（参考 int01 的 `_post_json`/`MapError`）。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **读文档，抄一张表**：把 `git diff --name-status` 的三种输出形态（`A/M/D` 一段、`R100/C100` 三段）、CSV 的两种 `path` 形态（精确/通配）、题面明确列出的 4 条边界情况（不在 CSV 里、匹配多个 owner、大小写、大仓库性能）抄下来——这就是这题的"需求文档"，比任何代码都先写。
2. **跑通最小调用**：在真实仓库里手动跑一次 `git diff --name-status main...feature`，确认输出格式和自己脑内的表一致，再回来写 `_run_git`。跳过这步直接写解析函数的人，容易在"tab 还是空格分隔""rename 到底几段"这些细节上凭猜测写错。
3. **Part 1 最小可用**：`_run_git` 统一执行 + 归一化异常；`changed_files` 逐行解析，`R/C` 贡献两个路径。用真实测试仓库自测。
4. **Part 2 叠加**：`load_owners`（读 CSV，跳过表头/空行）→ `_pattern_matches`（casefold 比较，`*` 前缀）→ `match_owners`（先筛出所有匹配，取最长 pattern 的那一档）→ `tally_owners`（未匹配归入 `UNOWNED` 桶）→ `assign`（取计数最大，并列取字典序最小）。
5. **Part 3 叠加**：`top_owners` 直接复用 `tally_owners`，排序 key 加一维；`main_cli` 用 `argparse` 包一层命令行，只做参数解析和打印，不碰任何 git/CSV 细节。
6. **收尾（健壮性 + 性能）**：确认三类 git 错误（git 不存在、不是仓库、分支不存在）都归一化成 `RepoError`；确认 `changed_files` 全程只发一次 git 请求、`tally_owners` 是一次遍历，没有对每个文件单独查一次 CSV 规则表之外的嵌套扫描。

## 4. 代码怎么组织
```
class RepoError(Exception)                              # 唯一对外暴露的错误类型
_run_git(repo, args) -> str                              # 唯一碰 subprocess 的地方，错误在这里收敛
changed_files(repo, base, head) -> list[str]              # 解析 --name-status 输出，Part 1
load_owners(csv_path) -> list[(pattern, owner)]           # 读 CSV，Part 2
_pattern_matches(pattern, path) -> bool                   # 精确/通配 + casefold
match_owners(path, owner_rows) -> list[str]                # 最具体规则优先，同档全记
tally_owners(changed, owner_rows) -> dict[owner, count]    # 未匹配 -> UNOWNED
assign(changed, owner_rows) -> str                         # 最大计数，字典序 tie-break
top_owners(changed, owner_rows, k) -> list[(owner,count)]  # Part 3，复用 tally_owners
main_cli(argv) -> int                                      # argparse 包装，只编排
main(stdin, stdout)                                        # PART n 驱动，供 io 测试
```
拆分原则：**"会不会碰子进程"是最高优先级的分割线**（同 int01 的"会不会碰网络"）。`_run_git` 之下是 git CLI 的输出格式细节；`changed_files` 只关心"两个 ref 之间改了哪些路径"，完全不知道 `subprocess`/`FileNotFoundError` 这些概念，因为已经被 `_run_git` 挡掉了。CSV 匹配这条线（`match_owners`/`tally_owners`/`assign`）纯粹是内存数据运算，单测完全不需要真实 git 仓库。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：子进程封装 -> diff 解析 -> CSV 最具体匹配 -> 计数。省略 argparse 与 CSV 表头跳过细节。
class RepoError(Exception):
    """git 不存在 / 不是仓库 / ref 无法解析，三种情况统一抛这个。"""

def _run_git(repo, args):
    try:
        result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, timeout=30)
    except FileNotFoundError as e:
        raise RepoError("git executable not found on PATH") from e
    if result.returncode != 0:
        raise RepoError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout

def changed_files(repo, base, head):
    out = _run_git(repo, ["diff", "--name-status", f"{base}...{head}"])   # 三点 diff：只看这条分支自己的变更
    paths = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if parts[0][:1] in ("R", "C"):          # rename/copy 贡献旧、新两个路径
            paths.append(parts[1]); paths.append(parts[2])
        else:                                    # A/M/D 贡献一个路径
            paths.append(parts[1])
    return paths

def match_owners(path, owner_rows):              # 最具体（最长 pattern）优先，同档全记
    hits = [(pat, owner) for pat, owner in owner_rows if _pattern_matches(pat, path)]
    if not hits:
        return []
    max_len = max(len(pat) for pat, _ in hits)
    return [owner for pat, owner in hits if len(pat) == max_len]

def tally_owners(changed, owner_rows):            # 一次遍历，未匹配归入 UNOWNED
    counts = {}
    for path in changed:
        for owner in match_owners(path, owner_rows) or ["UNOWNED"]:
            counts[owner] = counts.get(owner, 0) + 1
    return counts
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认几个边界——三点 diff 还是两点 diff？rename 算一个文件还是两个？平局怎么处理？这些题面里明确列出'需要处理'但没给具体规则，我会自己定死并且说清楚。」
- 写 `_run_git` 时：「我把所有子进程调用收进一个函数，`FileNotFoundError`（git 没装）、非零退出码（分支不存在）都在这里统一包成 `RepoError`，往上层业务代码永远只用认识这一种异常。」
- 写 `changed_files` 时：「我用三点 diff 是因为这更贴近'这个 PR 到底改了什么'的语义——两点 diff 会把 base 分支同期的新提交也算进来，产生噪音。」
- 写 CSV 匹配时：「大小写我用 `casefold` 不用 `lower`，因为要处理一些语言里大小写折叠不是简单映射的情况；'最具体规则优先'我用字符串长度做代理，精确路径几乎总比同前缀的通配长。」
- 交付时：「三个 Part 都过了；性能上 `changed_files` 全程只发一次 git 请求，`tally_owners` 是一次遍历，10^4 变更文件规模下测过在预算内。」

## 7. 常见跑偏（方法层面，3 条）
- **每个需要跑 git 的地方各写一次 `subprocess.run` + 裸 `try/except`**：短期能跑，但异常类型（`FileNotFoundError`/`CalledProcessError`/自己判断返回码）散落在业务代码各处，调用方要 `import subprocess` 才能正确 catch——所有子进程调用应该收进一个函数，对外只抛一种类型的异常。
- **对每个变更文件单独调用一次 git 或单独扫一遍 CSV**：`changed_files` 只应该发一次 `git diff` 请求；如果发现自己在写"对每个文件再跑一次 git show"这种代码，说明信息其实已经在第一次输出里了，只是解析没做完整。
- **把"题面没规定"的边界情况留到写测试时才现场决定**：平局规则、大小写敏感与否、"匹配多个 owner"怎么计数，这些题面明确写"需要处理"但没给规则的地方，应该在读题阶段就显式定死并记录下来（本题的 Clarifications 一节就是这么做的），而不是写代码时随手一个 `if` 就定了，事后自己都说不清楚为什么这么选。

## 8. 同族题 / 延伸
- int01（BikeMap）是同一方法论的网络版：把所有 `urllib` 调用收进 `_post_json`，网络错误在那里收敛成 `MapError`；int04 把同一个模式用在子进程上，`_run_git` 对应 `_post_json`，`RepoError` 对应 `MapError`——"外部工具封装 + 错误归一化"这条纪律不区分是网络调用还是子进程调用。
- int03（multi_json_etl）是同一方法论在"多个数据源汇入一个 ETL 管线"上的版本，可以对照看"错误归一化"在纯数据处理场景下长什么样。
- 延伸思考：如果要支持"忽略某些文件类型不计入 review 统计"（如 `*.md`），只需要在 `changed_files` 后面加一个过滤步骤，`tally_owners`/`assign` 不用改；如果 CODEOWNERS 规则要支持 glob（`**/*.py`）而不仅仅是前缀通配，只需要换 `_pattern_matches` 的实现。
- 练习命令：`python3 loop/mock.py start int04 -m 60`
