# int01 · BikeMap：给一个陌生的 HTTP 地图服务写客户端，练的是"网络调用封装 + 坐标顺序防御"这一个模型

> [!tldr]
> - 这题考的是：把一条 GeoJSON 骑行轨迹变成一连串对"面试官提供的地图渲染 HTTP 服务"的调用——解析坐标、
>   POST 拿回 PNG 落盘、标最近地标、包装成带缓存的批处理 CLI。不考算法，考你面对陌生 API 文档和真实网络
>   调用时的工程习惯。
> - 三步套路：读 API 文档，把"请求长什么样、响应长什么样、会返回哪些错误"抄成一张表 → 用最小的一次
>   HTTP 请求把项目跑通（不写业务代码）→ 按 Part 1→5 叠加，Part n 直接调用 Part n-1 的函数。
> - 最值得带走的一个模式：把 HTTP 调用封装成唯一一个碰 `urllib` 的函数，网络错误在这一层就收敛成一个
>   自定义异常；业务函数（解析、计算最近点、CLI 编排）只传普通数据、只处理这个异常，从不直接面对
>   `urllib.error` 的一堆子类。

## 1. 题目在说什么（人话版）
Stripe 内部有个骑行路线可视化工具（BikeMap）。产品经理给你一份用户骑车轨迹的 GeoJSON 文件，你要做四件
事：① 把轨迹坐标解析出来；② 调用一个已经部署好的地图渲染后端，把轨迹画成一张 PNG 图片存到本地；③ 在图
上标出附近的地标（餐厅、地铁站之类），同时要防着这个后端偶尔抽风返回一坨不是图片的东西；④ 算出轨迹上
离每个地标最近的点，方便后续做"你在骑行第几公里经过了这个地标"这种功能；⑤ 把前面这些包装成一个能批量
处理多个路线文件、还带缓存的命令行工具。全程没有一行需要动脑子的算法，但需要你在 60 分钟内读懂一份陌生
的 HTTP API 文档、写出干净的错误处理、并且不在最经典的坐标顺序陷阱上摔跤。

一个 3 行小例子：GeoJSON 里一段轨迹 `coordinates: [[13.4, 52.5], [13.41, 52.51]]`（GeoJSON 标准顺序
`[lng, lat]`，经度在前）；`load_coordinates` 读出来后要变成 `[(52.5, 13.4), (52.51, 13.41)]`（`(lat,
lng)`，纬度在前）；再把这个坐标序列发给渲染服务时，请求体里的 `points` 又要是 `[[52.5, 13.4], ...]`
这种"人类习惯"的顺序——一来一回，一道题里刚好把两种主流坐标序都过了一遍。

## 2. 读题：把文字变成模型
- **实体**：路线（一串 `(lat, lng)` 坐标）、地标（`{name, lat, lng}`）、一次渲染请求/响应（HTTP，PNG
  字节）。没有更复杂的领域对象了。
- **输入长什么样**：`data/ride-simple.json` 是标准 GeoJSON `FeatureCollection`，只取
  `features[0].geometry.coordinates`，每个点是 `[lng, lat]`；`data/landmarks.json` 是一个地标数组。
  API 文档另外给出 `/render` 的请求/响应形状——这份"文档"本身也是要读的输入，不比 JSON 数据地位低。
- **输出要什么**：Part 1 是格式化字符串列表（`"lat,lng"` 6 位小数）；Part 2/3 是写到磁盘的 PNG 文件 +
  一个字节数/校验结果；Part 4 是 `{地标名: (最近点下标, 距离米)}`；Part 5 是打印到 stdout 的批处理摘要。
  四种完全不同的输出形状，说明这题的"整合"考点就是把它们用同一套坐标数据串起来。
- **状态**：单次调用内几乎没有累积状态——每个 part 都是"转换一次、算一次、发一次请求"。唯一跨调用的状
  态在 Part 5：`--cache-dir` 下的 `index.json`，记录"这份坐标内容的哈希 → 已经渲染过的 PNG"，这是唯一
  需要在磁盘上维护的持久状态。
- **一句话建模**：这是一个 **外部 HTTP 服务的客户端封装** 问题——解析、网络 IO、纯计算、CLI 编排四层
  各管各的，Part n 只是在某一层上加一个新方法。

> [!note] 为什么把 HTTP 调用单独封装成一个函数
> 候选方案是"每个要发请求的 part 各写一遍 `urllib.request.urlopen(...)` + `try/except`"，或者"写一个
> `_post_json(base_url, path, payload) -> bytes` 统一发请求、统一把 `urllib.error.*`/`OSError` 收敛成
> 一个 `MapError`"。选前者的话，Part 2 的错误处理逻辑到 Part 3 要原样抄一遍；选后者，`render_map` 和
> `render_route` 唯一的区别就是"要不要带 markers、要不要校验响应是不是 PNG"，网络层的重试/超时/错误分
> 类只需要改一处。这也是这题面试官最想看到的分层判断力：HTTP 客户端细节和业务逻辑不应该长在同一个函数
> 里。

## 3. 下笔顺序（面试里就按这个时间轴敲，60 分钟对着 int01 的 5 个 part）
- **0–5 读题确认**：把 API 文档里 `/render` 的请求字段（`points`/`markers`/`width`/`height`）、成功响
  应（`200 image/png`）、错误响应（`400`/`413`）抄成脑内一张表；**当场大声确认坐标顺序**——"GeoJSON 是
  `[lng, lat]`，但 `/render` 的 `points` 是 `[lat, lng]`，我会在 `load_coordinates` 里做一次显式
  swap"。这是本题唯一真正的读题陷阱，5 分钟内必须自己动手转换一次验证，不要凭印象。
- **5–15 跑通项目**：起 mockserver（`python3 loop/mock.py serve int01 --port 0`），用 `curl` 或者五行
  Python 脚本发一个最小的 `POST /render` 请求，确认能拿到 PNG 字节、能用 `"wb"` 落盘、文件能打开。这一
  步的目的不是写业务代码，是确认"我真的理解这个 HTTP 服务的契约"——跳过这步直接写 `render_map` 的人，
  往往在 Part 2 卡在 `urllib.request` 的用法上，反而挤占了后面调试坐标顺序的时间。
- **15–35 happy path**：先写 Part 1（`load_coordinates` + `first_n`），立刻用题面 worked example 自测
  坐标顺序对不对；再写 Part 2（`render_map`，把刚才跑通的最小请求脚本搬进 `_post_json`）；然后 Part 3
  （`render_route`，复用 `_post_json`，加 markers 和 PNG 魔数校验）；最后 Part 4（`nearest_point`，教
  科书 Haversine）。这一段是全题分值的主体，Part 1-3 做扎实比多做一个 part 更重要。
- **35–48 错误处理**：回头给 `render_map`/`render_route` 补齐 `MapError` 归一化——连接失败、非 200、响
  应不是 PNG 这三类分别测一遍；`load_coordinates` 对畸形输入要报错而不是返回空列表。这一段决定了这题是
  "能跑的 demo"还是"过关的实现"。
- **48–55 清理**：确认 `_post_json` 是唯一碰 `urllib` 的地方；`nearest_for_all` 有没有复用
  `nearest_point`；有没有函数超过 40 行（`cli` 最容易超标，拆出 `_parse_cli_args`/`_render_or_reuse`
  两个 helper 就能压下来）；删掉调试用的 `print`。
- **55–60 总结**：如果 Part 5 没写完，口头讲清楚设计——"缓存 key 是坐标内容的哈希，不是文件路径";顺
  便主动带出一两个优化方向（大规模最近点用 KD-tree、超过 10000 点做客户端降采样），让面试官看到你知道
  "先能跑"和"能扩展"是两件事。

## 4. 代码怎么组织
```
_post_json(base_url, path, payload) -> bytes        # 唯一碰 urllib 的地方，网络错误在这里收敛成 MapError
render_map(base_url, coords, out_path) -> int        # 调 _post_json，落盘，Part 2
render_route(base_url, coords, landmarks, out_path)  # 调 _post_json，多带 markers + PNG 魔数校验，Part 3
  -> bytes
_haversine_m(lat1, lng1, lat2, lng2) -> float        # 纯数学，不知道 HTTP、不知道文件系统
nearest_point(coords, landmark) -> (idx, dist)       # 纯计算，Part 4
nearest_for_all(coords, landmarks) -> dict           # 复用 nearest_point
_render_or_reuse(...) -> (status, n_bytes)           # 一个文件"渲染还是走缓存"的判定，Part 5 内部 helper
cli(argv) -> int                                     # 批处理循环 + 打印，只编排，不碰 urllib
main(stdin, stdout)                                  # 按 'PART n' 分发
```
拆分原则：**"会不会调用网络"是最高优先级的分割线**。`_post_json` 之下是网络细节；`render_map`/
`render_route` 只关心"给坐标要 PNG"，完全不知道超时、重试、状态码这些概念该怎么处理，因为这些已经被
`_post_json` 挡掉了。`nearest_point`/`nearest_for_all` 这条线甚至连"网络"两个字都没见过——它们的输入是
纯 Python 数据，单测的时候完全不需要起 mockserver。这样拆的直接好处是：面试官问"如果渲染服务换成
`requests` 库怎么办"，你能明确说"只改 `_post_json` 一个函数"；问"如果最近点计算要单独跑在一个离线批处
理任务里"，你也能说"`nearest_point` 本来就不依赖任何 IO，直接搬走就行"。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：网络封装 → 业务调用 → 纯计算。省略 HTTPError/URLError 的具体 except 分支与 CLI 编排。
def _post_json(base_url: str, path: str, payload: dict) -> bytes:
    req = urllib.request.Request(
        base_url.rstrip("/") + path, data=json.dumps(payload).encode(),
        method="POST", headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise MapError(f"maps server returned HTTP {resp.status}")
            return resp.read()
    except (urllib.error.URLError, OSError) as e:      # 连不上 / 超时 / 非 2xx，统一收敛
        raise MapError(f"network error talking to maps server: {e}") from e

def render_route(base_url, coords, landmarks, out_path) -> bytes:
    markers = [[lm["lat"], lm["lng"], lm.get("name", "")] for lm in landmarks]
    png_bytes = _post_json(base_url, "/render",
                            {"points": [[lat, lng] for lat, lng in coords], "markers": markers})
    if png_bytes[:8] != PNG_MAGIC:                      # 状态码 200 不代表 body 可信
        raise MapError("response did not look like a PNG (bad magic number)")
    Path(out_path).write_bytes(png_bytes)                # 校验通过才落盘，不留半成品文件
    return png_bytes

def nearest_point(coords, landmark) -> tuple[int, float]:   # 纯计算，不知道 HTTP 的存在
    best_idx, best_dist = 0, math.inf
    for i, (lat, lng) in enumerate(coords):
        d = _haversine_m(landmark["lat"], landmark["lng"], lat, lng)
        if d < best_dist:                                # 严格小于：并列时保留更早的下标
            best_idx, best_dist = i, d
    return best_idx, best_dist
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下坐标顺序——GeoJSON 标准是 `[lng, lat]`，但文档里 `/render` 的 `points` 是
  `[lat, lng]`，我会在 `load_coordinates` 里做一次显式 swap，并且写清楚注释，防止我自己后面写着写着又
  搞反。」
- 跑通项目时：「我先发一个最小的请求确认这个服务的契约，再开始写业务代码，免得等真写 Part 2 的时候在
  `urllib` 用法上卡住。」
- 写 `render_map` 时：「网络调用我封装进一个 `_post_json`，`MapError` 是唯一往外抛的异常类型——调用方
  不需要知道我用的是 `urllib` 还是别的 HTTP 库，也不用挨个 catch `URLError`/`HTTPError`。」
- 写 `render_route` 时：「状态码 200 不代表响应体一定是我期望的格式，尤其这是二进制响应，我加一个最小
  的 PNG 魔数校验，校验通过了才落盘，避免把半成品或者错误 JSON 写进 `out_path`。」
- 写 `nearest_point` 时：「用 Haversine 因为地球是球面，经度 1° 对应的实际距离随纬度变化，欧氏距离在
  高纬度会系统性失真；当前是线性扫描 O(n×m)，如果规模再大一个量级，可以聊 KD-tree 或者按经纬度做网格
  分桶。」
- 交付时：「Part 1-3 我做完并且测过了，包括网络失败和响应不是 PNG 这两条错误路径；Part 5 的缓存设计我
  口头讲一下——key 是坐标内容的哈希而不是文件路径，这样同一条路线换个文件名也能命中缓存。」

## 7. 常见跑偏（方法层面，3 条）
- **没跑通项目就直接写业务逻辑**：一上来就写 `render_map`，第一次真正发请求是在写完整个函数之后，结果
  在 Part 2 才发现 `urllib.request.Request` 的 `data` 参数要传 `bytes` 不是 `dict`——调试 HTTP 库用法
  的时间挤占了本该花在坐标顺序和错误处理上的时间。先用五行脚本把请求-响应跑通，再回来写函数。
- **把 `urllib` 的异常类型直接暴露给调用方**：`render_map` 里裸 `try/except urllib.error.URLError`
  没有包一层，调用方（Part 5 的 `cli`）也要 `import urllib.error` 才能 catch——网络库的选择泄漏到了业
  务代码里。先定义好 `MapError`，所有网络相关的 part 都只抛这一种异常。
- **为了赶完成度，在 Part 1 就吞掉畸形输入**：`features` 为空或者坐标少于 2 个点时 `return []` 而不是
  报错，短期内能让程序"看起来正常运行"，但后续所有 part 都会拿到一个空列表继续跑，最终在很远的地方才
  报错甚至悄悄输出错误答案。Part 1-2 的正确性和错误处理是本题权重最高的部分，别为了往后赶而牺牲这里。

## 8. 同族题 / 延伸
- 同一轮的 int02（payments reconciliation）是另一道 Integration 题，考的是分页/限流/幂等/webhook 签
  名验证而不是坐标转换，但方法论完全一样：把 HTTP 调用封装成一个函数，业务逻辑只处理已经归一化过的数
  据和异常。
- 延伸思考：如果 `/render` 要求鉴权，只需要在 `_post_json` 里加一个 `Authorization` header，业务函数
  一行都不用改——这正是分层设计的价值；如果面试官追问"两次调用之间渲染服务的响应变了，缓存还该复用旧
  结果吗"，可以聊按响应内容哈希（而不只是输入内容哈希）做二级缓存 key。
- 练习命令：`python3 loop/mock.py serve int01 --port 0`（起 mockserver，Ctrl-C 停止）；
  `IMPL=starter python3 -m pytest loop/rounds/05_integration/int01_bikemap`（对着 `starter.py` 练习，
  绿了几个 part 就说明写对了几个 part）。
