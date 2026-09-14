# bs02 · minihttp：一个"值不对但没崩"和一个"崩了但栈顶就是答案"，练"先信 docstring 还是先怀疑测试"

> [!tldr]
> - 这轮考的不是"你会不会写 HTTP 客户端"，是能不能在一个 330 行的陌生仓库里，从两条不同风格的
>   失败断言，分别走到"少了一行"的根因
> - 三步套路：跑测试看红几个 → 分辨这条失败是"值不对没异常"还是"异常栈顶直接指哪一行" → 前者靠
>   对比相邻的通过测试缩小范围，后者直接读栈顶那一行 + 它上面的 docstring
> - 最值得带走的一个信号：**docstring 写了契约、代码没做到 → 先信 docstring，不要怀疑测试写错了**

## 1. 题目在说什么
`minihttp` 是一个仿 [`requests`](https://requests.readthedocs.io/) 公开接口的小型 HTTP 客户端：
`Session` 建一个 `Request`，`.prepare()` 把它变成一个"上线可发"的 `PreparedRequest`（算好
`Content-Length`、合并好 headers），交给 `HTTPAdapter` 真正发出去，命中 `status_forcelist` 就
按指数退避重试，最后包成一个 `Response`。README 里的两条 issue 长这样：

```
Bug report 1 — 大文件上传发出去是空的（或被截断）
> Content-Length 算出来是对的（11），但 prepared.body.read() 读回来是 b""——只对
> io.BytesIO 这类"能 seek 但没有 __len__/.len/可用 .fileno()"的 body 复现，
> 普通 bytes / dict / json= 都不受影响。

Bug report 2 — response.iter_content()（不传参数）直接崩，而不是返回整个 body
> TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
> 传显式 chunk_size（比如 iter_content(4)）完全正常，只有不传参数这一种调用方式崩。
```

这就是真实 bug 报告的样子：有 repro、有 expected/actual，但不会告诉你哪一行错了。

## 2. 读库：3 分钟摸清结构
1. **README 的 Layout**：`length.py`（探测 body 长度）→ `multipart.py`（切块 + 组装表单体）→
   `retry.py`（重试策略，纯计算）→ `models.py`（`Request`/`PreparedRequest`/`Response`）→
   `adapters.py`（唯一碰 socket 的地方）→ `sessions.py`（重试循环）。单向数据流：body 相关的
   bug 去 `length.py`/`multipart.py`/`models.py`，网络相关的去 `adapters.py`/`sessions.py`。
2. **入口**：`Session().get/post(...)` 或直接 `Request(...).prepare()`——两个 bug report 的
   repro 分别对应这两种入口，不用读实现也能照着敲。
3. **跑测试**：`python -m pytest tests`，25 个测试，2 红。

## 3. 下手顺序（面试里就按这个来）
1. **跑失败测试，先不读代码**：记下两个失败测试名——
   `test_prepare_body_streams_full_bytesio_content_matching_content_length` 和
   `test_iter_content_default_returns_whole_body_as_one_chunk`。
2. **分辨这条失败是"值不对"还是"崩了"**：第一个失败是 `assert 0 == 11`——没有异常，说明这是一个
   **安静吃掉数据**的 bug，不是崩溃类；第二个失败是 `TypeError`，有完整 traceback，栈顶直接指向
   `iter_slices` 内部的一行。这两种失败要用不同的读法。
3. **对"值不对"类：找紧邻的通过测试，缩小范围**：`test_super_len_of_fresh_bytesio_matches_its_size`
   紧挨着失败测试、而且是通过的——这条测试已经排除了"长度算错"这个可能性。既然 `Content-Length`
   对、body 却是空的，问题一定出在"body 对象在真正被读取之前，中间发生了什么"，而不是"怎么算
   长度"。
4. **对"崩了"类：栈顶就是答案，往上找 docstring**：`TypeError` 的 traceback 已经把出错的那一行
   指给你了，不需要形成复杂假设。往上看这个函数的 docstring/注释，通常会写"这个参数默认值应该
   干什么"——如果代码没做到 docstring 承诺的事，那就是根因，不是测试写错了断言。
5. **假设，然后验证**：对"值不对"类的假设要通过打印/断点验证（比如在真正 `.read()` 之前打印流的
   当前位置），不要靠脑内模拟；对"崩了"类，验证往往只需要对照调用方是不是真的把默认值原样传了
   下去。
6. **最小修复 + 回归**：改动应该正好覆盖失败断言要求的东西——这题两个 bug 加起来只有 3 行改动。
   重跑全部 25 个，不是只跑你改的那个。

## 4. 调试工具怎么用
这题的两类失败正好对应两种排查手法：pdb 命令表见 `loop/rounds/04_bug_squash/DEBUG_101.md`，这里
只说这道题具体怎么用——

- 对"值不对没异常"的 bug：在 `adapters.py` 里真正调用 `.read()` 的那一行前面插一句
  `print(body.tell(), file=sys.stderr)`（或者 `breakpoint()` 之后 `p body.tell()`），看流的
  当前位置是不是已经在末尾。这比读代码猜"到底谁动过这个流"快得多。
- 对"崩了有 traceback"的 bug：`pytest tests -k iter_content --pdb --tb=short` 直接停在异常处，
  `p slice_length` 一眼看到它是 `None`——不需要单步跟，栈顶信息本身已经足够。
- 改完用 `pytest tests --lf` 只重跑上次失败的两个，确认变绿了再跑全量。

## 5. 本题两个 bug 的排查实录

**Bug 1 — `super_len()` 量完长度不把流的位置放回去（跨调用残留状态）**
- 现象：`test_prepare_body_streams_full_bytesio_content_matching_content_length` 报
  `assert 0 == 11`——没有异常。
- 定位路径：紧邻的 `test_super_len_of_fresh_bytesio_matches_its_size` 是绿的，说明"长度计算逻辑
  本身没问题"。读 `models.py` 的 `prepare_body()`：对于非 `dict`/`json`/`files` 的 body（比如
  `io.BytesIO`），它把原始流对象原样存进 `self.body`，不立刻读取（为了支持流式发送）。真正的
  `.read()` 发生在 `adapters.py` 的 `HTTPAdapter.send()` 里。假设：`super_len()` 为了测长度，
  必须先 `seek` 到末尾，如果没有把位置 seek 回去，等 `adapter` 真正 `.read()` 的时候，流已经在
  EOF，读出来自然是空的。验证：在 `.read()` 前面打印 `body.tell()`，确认位置确实停在末尾。
- 根因分类：**跨调用残留状态**——`super_len()` 这次"测量"的副作用（改变了流的位置），残留到了
  下一次真正读取的时候，而这两次操作之间没有人把状态复位。
- 修复：一行，测完长度之后 `o.seek(current_position)` 把位置放回去。

**Bug 2 — `iter_slices` 没做自己 docstring 承诺的默认值处理（逻辑错误）**
- 现象：`test_iter_content_default_returns_whole_body_as_one_chunk` 报
  `TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'`，栈顶直接指向
  `multipart.py` 里 `data[pos : pos + slice_length]` 这一行。
- 定位路径：不需要形成复杂假设——`pos + slice_length` 在 `slice_length=None` 时必然
  `TypeError`，这一点从栈顶就能看出来。往上看这个函数的 docstring："`slice_length=None` 的约定
  是整段当一块"——代码完全没有实现这句话，只是直接假设 `slice_length` 一定是个数字。
- 验证：读调用方 `Response.iter_content(chunk_size=None)`，确认它确实把 `None` 原样传了下去，
  跟 repro 描述的"只有不传参数才崩"完全对得上。
- 根因分类：**逻辑错误**（缺一个应有的边界检查/早期分支），不是符号反转也不是状态残留。
- 修复：加一行 `if not slice_length or slice_length <= 0: slice_length = len(data)`。

**一个可迁移的信号**：断言直接是数值不等、没有 traceback → 先看它**紧邻的、通过的**测试，那条
测试往往已经替你排除了一半的可能性；异常有完整 traceback、栈顶直接指向一行 → 别再往上翻栈找"更
根本的原因"，先看这一行上面的 docstring/注释，代码和它自己声明的契约不一致，往往就是全部根因。

## 6. 面试里怎么说
- 复现完先客观描述：「两个测试红，一个是数值不对没异常，一个是 `TypeError` 有完整栈。我先看第一个，
  因为它旁边那条通过的测试已经帮我排除了'长度算错'这个可能性。」
- 提出假设时说出来：「`Content-Length` 对但 body 是空的，说明问题不在算长度，而在算完长度之后
  这个流的状态被谁改过——我去看 `super_len` 怎么测量这个流的。」
- 讲第二个 bug 时点出"代码和文档不一致"：「docstring 说 `None` 应该是'整段当一块'，代码却直接
  拿它去做加法——这不是一个需要猜的 bug，栈顶和文档已经把答案摆在那了。」
- 交付时说清验证范围：「两个红的现在都绿了，我又跑了一遍全部 25 个确认没有新的失败；这两个 bug
  改动都是一行，我没有碰 `super_len` 的整体分派顺序或 `iter_slices` 的循环结构。」

## 7. 常见跑偏
- **在 `prepare_body()` 里把流整个读进内存来"绕过"bug 1**：这样确实能让测试过，但丢掉了"流式
  发送、不整体读入内存"这个设计目的，而且没有修到真正的问题（`super_len` 的副作用）——这是"改
  了调用方掩盖问题"，不是"改了问题本身"。
- **给 `iter_content()` 一个非 `None` 默认值来"绕过"bug 2**：`iter_slices` 是一个通用工具函数，
  自己的文档承诺了 `None` 该怎么处理；只改调用方，`iter_slices` 本身对任何其他依赖这个默认值的
  调用方依然是坏的。
- **改测试放宽断言**：把 `assert 0 == 11` 改成宽松匹配，或者给 `iter_content()` 包一层
  `pytest.raises(TypeError)`——测试就是这道题的 spec，改测试等于绕过题目。
- **过度修复**：给 `super_len` 的可 seek 分支包一层 `try/except`，或者重写 `iter_slices` 的整体
  分派顺序——两个 bug 的修复都只有一行，改动范围应该跟 bug 的范围成正比。

## 8. 真实库对应 + 延伸练习
这两个 bug 都对应 `requests` 库真实的历史 issue：

- **Bug 1** 几乎是 [`psf/requests` issue #2589](https://github.com/psf/requests/issues/2589)
  的重现：`BytesIO` 类 body 因为没有 `.name`/`__len__`，长度探测的方式让流的位置留在了错误的地方，
  导致上传截断/失败；真实修复也是"测完之后 seek 回原位置"这一行。
- **Bug 2** 几乎是 [`psf/requests` issue #3369`](https://github.com/psf/requests/issues/3369)
  的重现：`iter_slices(iterator, slice_length=None)` 缺一个 `None` 保护，调用方依赖文档里的
  默认值就会崩。
- 两者共同的模式：**函数自己的文档/命名承诺了一个行为，实现里少做了那一步**——这类 bug 在任何
  "有默认参数、默认值有特殊含义"的函数里都可能出现，遇到"文档说会怎样、代码没这么做"时，先信文档。
- 延伸练习：`python3 loop/mock.py start bs02` → `test` → `ref`，第二遍给自己 20 分钟而不是 60
  分钟，专门练"分辨值不对 vs 崩溃两种失败该用不同读法"这件事的速度。
