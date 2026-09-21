# 卡片子代理指令 · `python` domain（skill `building-study-domains` 第 4 步）

> 你是 `sonnet` 子代理，**不得再派生代理**。你只拥有分配给你的顶层节点（见你的启动消息）在 `vault/domains/python/cards/<node>/` 下的卡片文件，不碰别的目录。
> 学习者：Chi，1.5 年后端（PayPal，Python/SQL/Snowflake），自建 66K 行 Python 量化平台；目标是对冲基金 SWE 面试里被追问两层仍答得出机制。所有卡片**中文**，术语英文（首次出现用全角括号，如 引用计数（reference counting））。

## 0. 先跑（resume rule）

```
cd /home/user/trellis
uv run trellis --domain python stats                 # 看你负责的节点哪些叶子已有卡片 → 跳过
ls vault/domains/python/cards/<node>/ 2>/dev/null
```
已有 ≥ 4 张卡的叶子直接跳过；用量上限中断后重启时也这样做。

## 1. 每个叶子的流程（每次一条命令，不写循环、不写 heredoc）

先看哪些语料覆盖了这个叶子：
```
uv run trellis --domain python digest python-docs --status
uv run trellis --domain python digest peps --status
uv run trellis --domain python digest cpython-internals --status
```
**A. 叶子有语料段落**（`--status` 里列为可 digest）：
```
uv run trellis --domain python digest <corpus> --leaf <leaf> -n 5 -o /tmp/claude-0/-home-user-trellis/2a620a6a-054d-572a-a687-5a54ebf3d695/scratchpad/cards/<leaf>.prompt.md
```
读这个 prompt（它内嵌了源文本与卡片 JSON 格式、语言规则），按它的格式把答案写到 `.../cards/<leaf>.json`，然后：
```
uv run trellis --domain python digest <corpus> --import /tmp/.../cards/<leaf>.json --leaf <leaf>
```
一个叶子被两个语料覆盖时，选源文本更机制化的那个（InternalDocs > 官方文档 > PEP）做 digest；另一个语料的内容可以作为你写"对比/失败场景"卡的依据。

**B. 叶子没有任何语料段落**：
```
uv run trellis --domain python grow --leaf python:<leaf> -n 5 -o /tmp/.../cards/<leaf>.prompt.md
uv run trellis --domain python grow --import /tmp/.../cards/<leaf>.json --leaf python:<leaf>
```
grow 出来的卡没有来源背书：**在你的最终回复里列出你最没把握的 3 条断言**（叶子 + 断言 + 你怀疑的点），编排者会去核对。

## 2. 卡片配比（每叶 4–6 张）

1. **机制**：它为什么这样工作（不是"是什么"）。
2. **数字或界限**：一个具体的量（5 ms 切换间隔、≤512 字节走 pymalloc、装载因子 2/3、`sys.getsizeof(1) == 28` 这类），要能从源文本或标准库文档核实；核实不了就不写数字。
3. **对比**：与最近的替代方案的差别（线程 vs 进程、`lru_cache` vs 手写 dict、`__slots__` vs `__dict__`）。
4. **失败或代价场景**：什么时候会出错、慢、泄漏、死锁；面试官追问的第二层。
5. （可选）**面试口播**：一张 "用 60 秒讲清 X" 的 QA，答案是可直接说出口的三句话。

## 3. 硬规则（validate 会抓）

- 每张卡**自包含**：不出现"如上文"、"该章节"、"文档里说"；问题单独读也能答（`not_self_contained` / `leans_on_source` 警告 = 退回）。
- 一题一答，答案 ≤ 120 字，先结论后机制；cloze 卡只挖一个空。
- 不编数字、不编版本号；不确定就写"量级"或不写。
- Python 版本口径：以 3.12/3.13 为准，历史差异注明版本（如"3.11 起…"）。
- 不写过程话；不改 skeleton、不改别人的节点。

## 4. 验收（编排者会重跑，你先自己跑）

```
uv run trellis --domain python validate      # 0 errors，且你的节点没有 not_self_contained / leans_on_source 警告
uv run trellis --domain python stats         # 你的每个叶子 ≥ 4 cards
```
最终回复：每个叶子的卡片数、用的语料（digest/grow）、validate 最后一行、最没把握的 3 条断言。
