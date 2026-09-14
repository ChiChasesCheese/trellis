# miniyaml 代码导读

面向"没读过缩进敏感解析器源码"的人。目的是让你看懂这份代码在干什么、模块之间怎么调，**不是**帮你定位这
道题的 bug——找 bug 的过程本身就是这轮练习的价值所在，所以下文不会提这份代码哪里有问题。

## 数据流

```
YAML 子集文本
  │
  ▼
lexer.tokenize()
  │  按行处理：跳过空行/注释行；每一行算出"前导空格数"（indent），
  │  再判断这一行是普通的 "key: value"（map_entry）还是 "- ..." 列表项（list_item）
  ▼
一串 Line 记录（indent / kind / key / value / list_item_kind）
  │
  ▼
parser.Parser.parse() / parse_text()
  │  从头到尾扫描 Line 记录，按缩进深度递归下降：
  │    同一缩进的一串连续行 = 一个"块"（block）
  │    某一行的 value 缺失（裸 "key:"）或某个列表项本身是映射 → 块的内容在它下面缩进更深的行里
  ▼
嵌套的 Python 结构（dict / list / 标量：int / float / bool / None / str）
  │
  ▼
csvio.to_csv_text() / from_csv_text()
  │  只认"顶层是一个 dict 组成的 list"这种形状（例如 [{"name": "Alice", ...}, ...]）；
  │  把所有记录出现过的 key 并起来当表头，逐行写成 CSV；反向时把每个单元格文本转回标量类型
  ▼
CSV 文本 ⇄ Python 记录列表
```

## 逐模块

### `lexer.py` —— 把文本行变成结构化的 Line
`tokenize(text)` 逐行处理，跳过空行和 `#` 开头的注释行，对每一行算出两件事：
- `indent`：这一行前面有几个空格（`len(line) - len(line.lstrip(" "))`）。
- 这一行属于哪一种：
  - 不是以 `"- "` 开头的普通行 → `map_entry`，用 `_split_key_value()` 按第一个 `:` 拆成
    `key`/`value`（`"key:"` 没有值的情况 `value` 是 `None`）。
  - 以 `"- "` 开头的列表项行 → `list_item`。这里又分两种写法：`"- 42"` 这种"整个item就是一个标量"
    （`list_item_kind = scalar`），和 `"- host: a.example.com"` 这种"这个item是一条映射，第一个key
    写在dash后面"（`list_item_kind = mapping_inline`）——靠这一行里有没有冒号来区分。

### `scalars.py` —— 字符串到底代表什么类型
`coerce_scalar(raw)` 把一段原始文本按顺序尝试：带引号的字符串（原样去掉引号，不再进一步转换）→
`true`/`false` → `null`/`~` → 整数 → 浮点数 → 都不是就原样当字符串返回。`scalar_to_text()` 是写 CSV
单元格时用的反向映射（只关心类型对不对，不保证还原成当初写 YAML 时那个具体字符串）。

### `parser.py` —— 核心：按缩进递归下降
`Parser` 是一个带状态的小对象：`self.lines`（`tokenize()` 的结果）和 `self.pos`（当前读到第几行的
游标）。之所以不用"传下标的一堆函数"而是用一个对象存游标，是因为 `_parse_map_block` 和
`_parse_list_block` 会互相递归调用，需要共享同一个不断前进的游标。

- `_parse_block(indent)`：看 `self.pos` 指的这一行是 `map_entry` 还是 `list_item`，分派给
  `_parse_map_block` 或 `_parse_list_block`。
- `_parse_map_block(indent)`：只要接下来的行缩进等于 `indent` 且是 `map_entry`，就一直往
  一个 dict 里塞键值对；遇到"key:"没有内联值的情况，就去看下一行缩进是不是比当前更深——是的话
  递归调用 `_parse_block()` 解析出嵌套内容当作这个 key 的 value。
- `_parse_list_block(indent)`：只要接下来的行缩进等于 `indent` 且是 `list_item`，就往一个 list 里塞
  东西；纯标量的 item 直接 append；`mapping_inline` 的 item 先建一个只有第一个 key 的 dict，再调用
  `_parse_map_block()` 去读这个 item 剩下的键值对（写在 dash 那一行下面、缩进对齐到第一个 key 开始
  的那一列的那些行）。

### `csvio.py` —— 记录列表 ⇄ CSV 文本
`collect_fieldnames(records)` 把所有记录出现过的 key 按"第一次见到的顺序"并成一份表头列表（不是按
字母排序）。`to_csv_text()` 用 `csv.DictWriter` 按这份表头写，缺某一列的记录留空单元格。
`from_csv_text()` 用 `csv.DictReader` 读回来，每个单元格都过一遍 `coerce_scalar()` 恢复类型。这个
模块完全不知道 YAML 的存在——它拿到的已经是 `parser.py` 处理完的纯 Python 数据。

## 读这份代码时容易误解的地方（语言机制，不是这道题的 bug）

- **`Parser` 是一个实例，`self.pos`/`self.lines` 是实例的字段，不是每次 `parse()` 调用临时创建的局部
  变量。** Python 的实例字段在多次方法调用之间是"持久"的——除非某个方法自己把它们重新赋值，否则上一次
  调用留下的值原样留到下一次调用开始时还在。这和很多"每次调用都是全新一份"的直觉不一样，尤其是当你
  习惯了纯函数式的写法时。
- **递归函数之间共享的是同一个 `self`，不是各自拷贝一份状态。** `_parse_map_block` 递归调用
  `_parse_block`，`_parse_block` 又可能调回 `_parse_list_block`——这些调用全都读写同一个
  `self.pos`，所以任何一层往前挪动了游标，外层继续执行时看到的就是挪动之后的值，不需要显式"回传"。
  这既是这套递归下降解析器能工作的原因，也是"某处忘了正确维护 `self.pos`"这类 bug 特别容易发生、又
  特别不容易一眼看出来的原因。
- **`dict` 按插入顺序遍历（Python 3.7+ 的语言保证），不是按 key 排序。** `collect_fieldnames()` 依赖
  这一点：用 `dict` 当"去重但保留顺序"的集合（`seen.setdefault(key, None)`），最后 `list(seen)` 拿到
  的就是插入顺序，而不是字母顺序。如果你以为 Python 的 dict/set 会自动排序，这里的行为会让你意外。
  同理，csv 表头的顺序是"第一次见到的顺序"，不是"字母顺序"——这是设计选择，不是遗漏了排序步骤。
- **字符串切片 `raw[1:-1]`（`scalars.py` 里去引号用的写法）在字符串长度小于 2 时不会报错，只会返回一
  个可能没意义的结果。** `coerce_scalar()` 先检查了 `len(raw) >= 2` 才做这个切片，这个检查是必要的，
  不是可有可无的防御性代码。

---
真实面试里没有这份指南。第二遍练这道题时，跳过这一节直接看代码。
