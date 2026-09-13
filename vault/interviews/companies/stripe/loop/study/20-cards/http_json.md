# 卡片 · HTTP / JSON / 文件 IO（Integration 轮的手速）

> Integration 轮 60 分钟里，**时间不该花在"怎么发请求"上**。这份卡片要练到闭眼能写。
> 全部纯标准库——面试环境可能没有 `requests`，而且题面常明说只能用 stdlib。
> 可跑的对照实现：`loop/mockserver/`（`maps.py` / `payments.py`）与 `int01`–`int04` 的 `solution.py`。
> 格式：`| Q | A | 出处 |`

## urllib：发请求

| Q | A | 出处 |
|---|---|---|
| 纯 stdlib 发一个 GET 并读文本？ | `with urllib.request.urlopen(url, timeout=10) as r: body = r.read().decode()` | stdlib |
| POST 一个 JSON body 的完整写法？ | `req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")` 然后 `urlopen(req)` | stdlib |
| 忘了 `.encode()` 会怎样？ | `TypeError`：`data` 必须是 bytes，不能是 str | stdlib |
| 不写 `method=` 会怎样？ | 带 `data` 时默认就是 POST；不带 data 是 GET。要 PUT/DELETE 必须显式写 | stdlib |
| 怎么加自定义 header？ | `Request(url, headers={...})`，或 `req.add_header("Authorization", "Bearer ...")` | stdlib |
| 4xx/5xx 会怎样？ | **抛 `urllib.error.HTTPError`**，不是返回。它同时也是个 response 对象，`e.read()` 能拿到错误 body、`e.code` 是状态码 | stdlib |
| 连不上（DNS/拒绝连接）抛什么？ | `urllib.error.URLError`（`HTTPError` 是它的子类，先 catch `HTTPError`） | stdlib |
| 怎么读响应状态码和 header？ | `r.status`；`r.headers.get("Retry-After")`（header 名大小写不敏感） | stdlib |
| 超时怎么设？ | `urlopen(req, timeout=10)`。**不设的话会永久挂住**——面试里挂住比报错更糟 | stdlib |
| 查询参数怎么拼？ | `urllib.parse.urlencode({"limit": 100, "starting_after": cid})`，再 `f"{url}?{qs}"` | stdlib |
| 路径里有特殊字符怎么办？ | `urllib.parse.quote(seg, safe="")` | stdlib |

## 响应处理

| Q | A | 出处 |
|---|---|---|
| 解析 JSON 响应？ | `json.loads(r.read().decode("utf-8"))` | stdlib |
| 二进制内容（PNG 等）怎么落盘？ | `open(path, "wb").write(r.read())`——**`"wb"` 不是 `"w"`**，写二进制不能用文本模式 | int01 |
| 怎么判断响应是不是 JSON？ | 看 `r.headers.get("Content-Type", "")`，`application/json` 才解析；错误响应可能是 HTML | stdlib |
| 大响应要流式读怎么办？ | `for chunk in iter(lambda: r.read(8192), b""):` | stdlib |

## 重试与退避

| Q | A | 出处 |
|---|---|---|
| 指数退避的最小实现？ | `for i in range(n): try: return call() except Retryable: time.sleep(base * 2 ** i)` | 通用 |
| 为什么必须加抖动（jitter）？ | 所有客户端同时退避会同时重来（雷鸣群效应）。`time.sleep(base * 2**i * (0.5 + random.random()))` | Stripe rate-limits |
| 429 该等多久？ | 优先读 `Retry-After` header；没有再用退避 | Stripe rate-limits |
| 哪些错误**不该**重试？ | 4xx 里的 400/401/403/404——重试多少次都一样。5xx 和 429 才重试 | 通用 |
| 重试 POST 要注意什么？ | 带上**同一个 Idempotency-Key**，否则可能重复扣款 | Stripe idempotency |
| 重试次数上限没设会怎样？ | 无限重试会把 60 分钟耗光。面试里固定 3 次即可，并说出这个数字 | 本仓库 int02 |

## JSON 取值

| Q | A | 出处 |
|---|---|---|
| 嵌套取值怎么写才不炸？ | `d.get("a", {}).get("b")` 逐层兜底；或 `try/except (KeyError, TypeError)` | stdlib |
| `d["k"]` 和 `d.get("k")` 什么时候用哪个？ | 缺 key 属于数据错误 → `[]` 让它响亮地炸；缺 key 是正常情况 → `.get()` | 通用 |
| 怎么区分"值是 None"和"key 不存在"？ | 用哨兵：`_MISSING = object()`；`d.get(k, _MISSING) is _MISSING` | 通用 |
| JSON 里的数字读进来是什么类型？ | 有小数点或指数 → `float`，否则 `int`。**金额别让它变 float** | stdlib |
| 金额字段怎么安全读？ | 用 `Decimal(str(v))` 或直接要求整数分。`float("0.1")+float("0.2") != 0.3` | Stripe currencies |
| 一个文件里多个 JSON 对象（JSONL）怎么读？ | 逐行 `json.loads(line)`，不是一次 `json.load(f)` | int03 |
| 输出 JSON 想稳定可比对？ | `json.dumps(obj, sort_keys=True, separators=(",", ":"))` | stdlib |
| 中文被转成 `\uXXXX` 怎么办？ | `json.dumps(obj, ensure_ascii=False)` | stdlib |

## CSV

| Q | A | 出处 |
|---|---|---|
| 为什么不能用 `line.split(",")`？ | 带引号的字段里可能含逗号和转义引号，split 会切错 | ps12 |
| 按列名取值的标准写法？ | `csv.DictReader(f)`，然后 `row["merchant_id"]`——列顺序变了也不受影响 | q20 |
| 从字符串（不是文件）读 CSV？ | `csv.reader(io.StringIO(text))` | stdlib |
| 写 CSV 时怎么避免多出空行？ | `open(path, "w", newline="")` | stdlib |
| 文件可能有 BOM 怎么办？ | `encoding="utf-8-sig"` | stdlib |

## 本地服务与调试

| Q | A | 出处 |
|---|---|---|
| 纯 stdlib 起一个 HTTP 服务？ | `http.server.HTTPServer(("127.0.0.1", 0), Handler)`，端口传 `0` = 让系统分配 | loop/mockserver |
| 测试里起服务怎么不占固定端口？ | 端口传 `0`，再从 `server.server_address[1]` 读实际端口 | loop/mockserver |
| 怎么在不联网的机器上调通？ | 先 `python3 loop/mock.py serve int01` 起本地 mockserver，再跑题 | 本仓库 |
| 调试请求时想看真实发出去了什么？ | 打到 **stderr**：`print(req.full_url, req.headers, file=sys.stderr)` | 本仓库 CONVENTIONS |
| GeoJSON 的坐标顺序是？ | **`[lng, lat]`（经度在前）**，跟人类习惯的 `[lat, lng]` 相反——int01 最经典的坑 | int01 |

## Integration 轮的时间账

| Q | A | 出处 |
|---|---|---|
| 60 分钟怎么分？ | 0–5 读题确认假设 · 5–15 跑通项目定位代码 · 15–35 happy path · 35–48 错误处理/边界 · 48–55 清理 · 55–60 总结 | LOOP_GUIDE §5 |
| 这轮的通过线？ | 2/5、2.5/5（有提示）、3/5 都有人过；共识是"integration 没做完**或** bug squash 差，二选一还能过" | LOOP_GUIDE §5 |
| 这轮最大的挂点是什么？ | 没搞清**输出格式**就开写；其次是环境配置吃掉时间 | LOOP_GUIDE §5 |
| 能联网查文档吗？ | 能，这轮是 open-book。但**禁 AI** | LOOP_GUIDE §5 |
| 为什么"简单"反而危险？ | 一手评价："very easy api calling but easy for everyone so you have to be perfect" | LOOP_GUIDE §5 |
