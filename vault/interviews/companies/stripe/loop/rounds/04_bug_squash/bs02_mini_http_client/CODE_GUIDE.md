# minihttp 代码导读

面向"没读过 HTTP 客户端库源码"的人。目的是让你看懂这份代码在干什么、模块之间怎么调，**不是**帮你定位这道题的 bug——
找 bug 的过程本身就是这轮练习的价值所在，所以下文不会提这份代码哪里有问题。

## 数据流

```
调用方
  │  Session.get(url, params=...) / .post(url, json=...) / .post(url, data=..., files=...)
  ▼
sessions.Session.request()
  │  把 method/url/headers/params/data/json/files 打包成一个 models.Request
  ▼
models.Request.prepare()
  │  ├─ prepare_url()      合并 params 到查询字符串
  │  ├─ prepare_headers()  合并 Session 默认头 + 调用方传入头
  │  └─ prepare_body()     根据 data/json/files 的类型选一种编码方式，产出 body + Content-Length
  │        │
  │        ├─ files 非空          → multipart.encode_multipart_formdata()
  │        ├─ json 非空           → json.dumps()
  │        ├─ data 是 dict        → urlencode()（表单）
  │        └─ data 是别的东西      → 原样传下去，长度靠 length.super_len() 探测
  ▼
models.PreparedRequest（method / url / headers / body 都已经是"上线可发"的样子）
  ▼
adapters.HTTPAdapter.send()
  │  用标准库 http.client 真正开一条 TCP 连接，发出去，读回响应
  ▼
models.Response（status_code / headers / content，外加 .text / .json() / .iter_content() 三个读法）
  ▲
  │  如果 Response.status_code 命中 retry.Retry 的 status_forcelist（例如 503），
  │  Session.request() 的循环会按 Retry.backoff_time() 睡一会儿，重新走一遍上面的流程
```

## 逐模块

### `length.py` —— 请求体有多长？
`super_len(o)` 只做一件事：给你一个东西（可能是 `bytes`、`dict` 编完的字符串、一个打开的文件、一个
`io.BytesIO`……），尽量猜出它有多少字节，猜不出就返回 `None`。因为不同类型的对象暴露"长度"的方式完全不同：
- `bytes`/`str`/`list` 有 `__len__`，直接 `len()`。
- 有的第三方对象习惯用 `.len` 属性而不是 `__len__`。
- 打开的文件可以用 `os.fstat(fileno).st_size` 拿到磁盘上的真实大小。
- 剩下的（比如 `io.BytesIO`）只有 `.tell()`/`.seek()`，唯一的办法是"跳到文件末尾，看当前位置是第几个字
  节，这就是长度"。

`Session.request()` 之所以要提前知道长度，是因为 HTTP 需要在发送 body **之前**就把 `Content-Length`
头写进去（除非改用 chunked 传输，这个库没实现）。

### `multipart.py` —— 把数据切块 / 拼成一份表单请求体
这个文件放了两个各自独立的东西：
- `iter_slices(data, slice_length)`：把一段 `bytes` 从左到右切成固定大小的小块，返回一个生成器
  （`yield` 逐块产出，不会一次性在内存里复制出一份新的）。`slice_length=None` 的约定是"整段当一块"。
- `encode_multipart_formdata(fields, files)`：`multipart/form-data` 请求体的组装器——普通字段和文件
  字段各自拼成一段 MIME part，用一个随机 boundary 隔开，末尾加一个 `--boundary--` 结束标记。`iter_slices`
  在这里被用来分块读文件内容，避免大文件在内存里被复制两份。

### `retry.py` —— 重试策略（纯计算，不含"睡多久"之外的副作用）
`Retry` 只回答两个问题："这个状态码要不要重试"（`is_retryable_status`）和"第 N 次重试前要睡几秒"
（`backoff_time`，指数退避：`backoff_factor * 2**(attempt-1)`）。它自己不发请求、不睡觉——这样它可以脱离
网络单独测试。

### `models.py` —— Request / PreparedRequest / Response 三种数据形态
- `Request`：调用方原始传的参数的容器，还没变成"上线可发"的样子。
- `PreparedRequest`：`.prepare_method()/.prepare_url()/.prepare_headers()/.prepare_body()` 依次把
  `Request` 变成最终的 `method`/`url`/`headers`/`body`。`prepare_body()` 是这个文件里逻辑最重的一段，
  按 `files` → `json` → `dict data` → 其他 的顺序判断用哪种编码。
- `Response`：`status_code`/`headers`/`content` 三个基本字段，外加 `.text`（按 `Content-Type` 里的
  `charset` 解码）、`.json()`、`.iter_content(chunk_size)`（内部调用 `multipart.iter_slices`）。

### `adapters.py` —— 唯一碰 socket 的地方
`HTTPAdapter.send()` 用标准库 `http.client.HTTPConnection`/`HTTPSConnection` 真正发出请求、读回响应，
包成一个 `Response`。之所以单独抽出这一个文件，是为了让其余模块（`models`/`retry`/`multipart`/
`length`）完全不依赖网络，可以在没有服务器的情况下被单元测试直接调用。

### `sessions.py` —— 调用方看到的入口
`Session.request()` 把 `Request.prepare()` 的结果交给 `adapter.send()`，如果响应状态码命中
`Retry.status_forcelist`（或者发送时抛出 `OSError` 这类连接错误），就按 `Retry.backoff_time()` 睡一
下、再试一次，直到用完 `Retry.total` 次机会。`.get()`/`.post()`/`.put()`/`.delete()` 只是
`.request(method, ...)` 的简写。

## 读这份代码时容易误解的地方（语言机制，不是这道题的 bug）

- **`hasattr(o, "len")` 检查的是属性 `.len`，不是内置函数 `len()`。** 两者长得像但完全是两回事：
  `hasattr(o, "__len__")` 才是在问"`len(o)` 能不能用"；`hasattr(o, "len")` 是在问"这个对象有没有一个
  叫 `len` 的属性/字段"。写惯了别的语言的人容易把这两行看成重复代码。
- **生成器函数体不会在调用时立刻执行。** `iter_slices(data, n)` 这一行本身什么都不做，只是造出一个
  生成器对象；函数体里的代码要等第一次 `next()`（比如 `for` 循环第一次取值，或者 `list(...)` 开始消费）
  才会真正跑起来。如果你在函数体最前面加一行校验逻辑，那行代码同样要等第一次被消费时才执行，不是
  "定义即执行"。
- **`prepared.body` 可能是 `bytes`，也可能是一个还没被读过的文件对象。** `prepare_body()` 对于
  `dict`/`json`/`files` 这三种情况会立刻把 body 编码成 `bytes`；但对于"其他东西"（比如一个
  `io.BytesIO`），它只是把原对象原样存进 `self.body`，并没有读取它——真正的读取发生在 `adapter.send()`
  里。这是"能流式发送、不必整个装进内存"的设计，但也意味着 `prepared.body` 的类型在不同分支下不一致，
  别假设它总是 `bytes`。
- **`dict.setdefault(key, value)` 只在 key 不存在时才写入。** `prepare_body()` 里多处用
  `self.headers.setdefault("Content-Type", ...)`，如果调用方自己已经传了 `Content-Type`，这里不会覆盖
  它——这是有意为之，不是遗漏了赋值。
- **`Retry` 和 `Session` 之间是策略与执行的分工，不是继承关系。** `Retry` 不认识 `Session`，也不知道
  自己被谁用；反过来 `Session` 也不关心 `Retry` 内部怎么算。两者之间只通过
  `is_retryable_status()`/`backoff_time()` 两个方法通信。如果你想改重试行为，先想清楚是策略问题（该不
  该重试、睡多久）还是执行问题（重试循环本身怎么写），两者分别在 `retry.py` 和 `sessions.py` 里。

---
真实面试里没有这份指南。第二遍练这道题时，跳过这一节直接看代码。
