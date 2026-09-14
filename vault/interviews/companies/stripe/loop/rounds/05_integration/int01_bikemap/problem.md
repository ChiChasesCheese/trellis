# int01 · BikeMap — GeoJSON 骑行路线解析 → 地图渲染 → 最近地标 → 批处理 CLI
<!-- mockserver: maps -->

**Type:** onsite Integration（真实 HTTP 调用，非算法题） · **Stage:** 60 min，5 part · **Last asked:** 2026-06-07（oavoservice 逐 part 拆解文章）；learncswithus 2025-11-11 VO 面经给出同款 5-part 拆解
**Frequency:** 目前中英文报告中**最常被点名的 Integration 例题**——`teamblind h8lemeaq`（Stripe 员工亲述题库随机抽题，"If you can do bikemap then you should be able to do the other ones too"）、`1point3acres bba4944f`、`learncswithus.com`、`oavoservice.com`、`prachub.com` 均独立提到 · **Confidence:** high for 5-part 结构与每个 part 的一句话主题（4 篇独立来源交叉一致）；`ride-simple.json` 具体点数/城市、mockserver API 形状是本仓库复刻，不是题面原文（Stripe 出题仓库不允许候选人下载/复制，见 Sources）。

## Context
Stripe 的这道 Integration 题模拟一个骑行路线可视化服务：候选人拿到一份 GeoJSON 格式的骑行轨迹数据，需要解析坐标、调用一个（面试环境提供的）地图渲染后端把路线画成图片、叠加地标标注、计算路线上离每个地标最近的点，最后把整个流程封装成一个可重复使用、有缓存的命令行工具。**不考算法**——考察的是读文档的速度、HTTP 客户端的错误处理、对陌生数据结构（GeoJSON 的坐标顺序）的警惕性，以及代码在"需求还会继续加码"时的模块化程度。据多份面经，多数候选人在 60 分钟内做不完全部 5 个 part；Part 1-2 的实现质量、代码整洁度比"做完几个 part"更被看重。

本仓库用 `loop/mockserver/maps.py`（stdlib `http.server`，零依赖）复刻题面描述的地图渲染后端：`POST /render` 接受 `{"points": [[lat,lng],...], "markers"?: [...]}\`，返回一张真正的 PNG（`loop/mockserver/_png.py` 手写编码器，无 PIL）。

## API 文档（面试官给的"地图渲染服务"文档，已按 mockserver 实现整理）
```
POST /render
  body (JSON): {
    "points":  [[lat, lng], ...]              必填，至少 2 个点
    "markers"?: [[lat, lng, "label"], ...]     可选，每个地标画一个小圆点
    "width"?: int, "height"?: int              可选，默认 400x300，范围 [1, 4000]
  }
  200 image/png   -- 渲染成功，把路线连成折线，markers 画成小圆点
  400 {"error": {"type": "invalid_request_error", "message": "..."}}
                  -- body 不是合法 JSON / 不是对象 / points 缺失或少于 2 个点
  413 {"error": {"type": "invalid_request_error", "message": "..."}}
                  -- points 超过 10000 个

GET /health
  200 {"ok": true}
```
所有响应都带 `Request-Id: req_<hex>` header（可忽略）。**注意坐标顺序**：这个 `/render` 接口的 `points`/`markers` 用的是人类习惯的 `[lat, lng]` 顺序——但你读取的输入文件 `ride-simple.json` 是标准 **GeoJSON**，GeoJSON 规范规定坐标数组是 `[lng, lat]`（经度在前）。这两者顺序相反，是这道题最经典的坑。

## 输入数据
- `data/ride-simple.json`：一个 GeoJSON `FeatureCollection`，恰好 1 个 `Feature`，`geometry.type == "LineString"`，`geometry.coordinates` 是 500 个 `[lng, lat]` 点，围绕柏林市中心（约 52.51°N, 13.39°E）用 `random.Random(0)` 生成的一条平滑骑行路线（每步前进 18 米，朝向做小幅随机游走 + 缓慢周期性漂移，模拟真实骑行轨迹而非直线或纯随机噪声）。
- `data/landmarks.json`：9 个地标 `[{"name": str, "lat": float, "lng": float}, ...]`，每个都以路线上某个点为基准加 10–150 米随机偏移生成，因此"最近点"距离都在几米到一百多米这个量级（不是几公里外的无关地标）。

## Rules
### Part 1 — 解析 GeoJSON，取前 N 个坐标
`load_coordinates(path: str) -> list[tuple[float, float]]`：读取 GeoJSON 文件，从 `features[0].geometry.coordinates` 取出坐标，**把 `[lng, lat]` 换成 `(lat, lng)`** 返回（后续所有 part 统一用 `(lat, lng)` 元组）。文件不含 `features`、geometry 不是 `LineString`、坐标少于 2 个点，都应该报错（抛异常，不静默返回空列表）。

`first_n(coords, n=10) -> list[str]`：把前 `n` 个坐标格式化成 `"lat,lng"`，**保留 6 位小数**（`f"{lat:.6f},{lng:.6f}"`）；如果坐标总数少于 `n`，全部返回。

### Part 2 — POST 取回 PNG 并存盘
`render_map(base_url, coords, out_path) -> int`：把 `coords` 组装成 `{"points": [[lat,lng],...]}`，`POST {base_url}/render`，把响应体（PNG 字节）用 `"wb"` 模式写入 `out_path`，返回写入的字节数。**任何网络错误（连不上、超时）或非 200 状态码都要抛 `MapError`**（自定义异常，包一层，不要让 `urllib` 的原始异常类型泄漏给调用方）。

### Part 3 — 带地标标注渲染，防御性校验响应
`render_route(base_url, coords, landmarks, out_path) -> bytes`：和 Part 2 一样发路线点，同时把 `landmarks` 转成 `markers: [[lat,lng,name],...]` 一起发送。**在写文件之前先校验响应真的是 PNG**（检查开头 8 字节魔数 `\x89PNG\r\n\x1a\n`）——如果服务端返回了 200 但 body 不是图片（比如一个错误 JSON），要抛 `MapError`，**不能把垃圾数据写进 `out_path`**。返回值是 PNG 字节本身（不只是字节数），方便调用方复用响应体。

### Part 4 — 最近地标
`nearest_point(coords, landmark) -> (index, distance_m)`：用 **Haversine 公式**（地球半径取 `6,371,000` 米）计算 `landmark` 到 `coords` 中每个点的大圆距离，返回最近点在 `coords` 里的下标（0-based）和距离（米，浮点）。**距离相等时取下标最小的点**（第一次严格小于才更新最优解）。

`nearest_for_all(coords, landmarks) -> dict[str, tuple[int, float]]`：对 `landmarks` 里每个地标调用 `nearest_point`，返回 `{地标名: (index, distance_m)}`。

### Part 5 — 批处理 + 缓存 CLI
`cli(argv) -> int`：
```
--input       一个或多个 GeoJSON 路线文件（nargs='+'）
--server      地图渲染服务的 base URL
--out         渲染结果输出目录（每个 --input 生成一个 '<文件名去扩展名>.png'）
--landmarks   地标 JSON 路径（可选；不给就跳过最近地标输出）
--cache-dir   缓存目录：'<hash>.png' + 'index.json'（hash -> 来源输入路径），不存在则创建
```
对每个 `--input` 文件：算出坐标集合的内容哈希（**内容哈希，不是文件路径哈希**——同样坐标、不同文件名要命中同一条缓存），如果缓存目录里已经有这个哈希对应的 PNG，直接复制过去，打印 `"{input}: cached ({n} bytes)"`；否则调用 `render_map` 真正渲染，把结果也写进缓存，打印 `"{input}: rendered ({n} bytes)"`。如果给了 `--landmarks`，每个输入文件渲染完之后再打印它的最近地标摘要，每行 `"  {name}: index={idx} distance_m={dist:.1f}"`。

### `main()` / `PART n` 驱动（供 io 测试）
第一行 `PART n`，后续每行是该 part 的参数（顺序固定，见下）：
```
PART 1
<input_path>
[<n>]                       可选，缺省 10

PART 2
<server_url>
<input_path>
<out_path>                  输出: "{n_bytes} bytes"

PART 3
<server_url>
<input_path>
<landmarks_path>
<out_path>                  输出: "{n_bytes} bytes"（校验通过）或 "NOT_PNG"

PART 4
<input_path>
<landmarks_path>            对每个地标输出一行 "{name}: index={idx} distance_m={dist:.1f}"

PART 5
<cli 的其余参数，逐行，等价于 argv 列表>
                             cli() 直接 print 到真实 stdout（不经过 main() 的 stdout 参数）
```

## Worked examples
`data/ride-simple.json` 的前 10 个坐标（`PART 1` / `first_n(coords, 10)`）：
```
52.514000,13.390000
52.514043,13.390256
52.514075,13.390517
52.514111,13.390776
52.514156,13.391031
52.514200,13.391287
52.514247,13.391541
52.514284,13.391799
52.514328,13.392055
52.514372,13.392311
```
`nearest_for_all(coords, landmarks)`（`data/landmarks.json` 全部 9 个地标）：
```
Rathaus: index=11 distance_m=56.8
Stadtpark: index=58 distance_m=39.8
Bahnhof Nord: index=124 distance_m=132.9
Museumsufer: index=189 distance_m=2.6
Alte Brücke: index=251 distance_m=31.4
Marktplatz: index=304 distance_m=11.3
Uferpromenade: index=369 distance_m=11.3
Sportzentrum: index=427 distance_m=28.4
Kanalschleuse: index=465 distance_m=45.2
```
一个最小 GeoJSON 演示坐标顺序陷阱（`load_coordinates`）：
```
输入 geometry.coordinates: [[13.4, 52.5], [13.41, 52.51]]     (GeoJSON: [lng, lat])
输出 coords:                [(52.5, 13.4), (52.51, 13.41)]     ((lat, lng)，已交换)
```

## Edge cases hidden tests are known to target
- GeoJSON 坐标顺序陷阱：`[lng, lat]` 原样返回（不交换）是最常见的错误实现
- `features` 为空 / `geometry.type` 不是 `LineString` / 坐标少于 2 个点 → 应该报错，不是返回空列表或崩溃成未捕获异常类型
- `render_map`/`render_route` 连接被拒绝（端口不存在）→ `MapError`，不是让 `urllib.error.URLError` 原样冒泡
- `> 10000` 个点触发 mockserver 的 `413` → 同样要归一化成 `MapError`
- `render_route` 的响应是 200 但不是 PNG（防御性解析：不能只信任状态码）→ `MapError`，且**不能**把非法内容写到 `out_path`
- Haversine 距离相等时取最小下标（同一坐标出现两次的退化情形）
- `nearest_for_all` 的 key 是地标名，顺序应该覆盖输入的所有地标，即使某个地标离路线很远
- CLI 缓存按**坐标内容哈希**、不是按输入文件路径——同样坐标换个文件名应该命中缓存而不是重新渲染
- CLI 处理多个 `--input`（批处理），每个都要单独产出 `<stem>.png`
- `--landmarks` 缺省时 CLI 不应该尝试读取地标文件或崩溃
- `first_n` 在坐标总数小于 `n` 时返回全部，不补空行、不报错
- `main()` 空 stdin（无 `PART` 行）应该什么都不打印、正常退出（returncode 0）

## Variants seen in the wild
- oavoservice 版本用 `staticmap`（PyPI 第三方库，`github.com/komoot/staticmap`，`(lon, lat)` 顺序、Pillow 渲染）而不是自建 HTTP 服务；这里为了 60 分钟内可离线复现，换成本仓库 `loop/mockserver/maps.py` 这个"面试官提供的地图渲染 API"，`points`/`markers` 顺序统一改成人类习惯的 `[lat, lng]`（`staticmap` 本身是 `(lon, lat)`，这是另一处容易混淆的地方，本版本刻意避开）。
- learncswithus 版本 Part 4 是"标注地标 + 计算最近点"合并成一步；本版本拆成 Part 4（纯计算）和已经在 Part 3 完成的"标注"（渲染时传 markers），顺序略有调整但覆盖同样的两个能力点。
- 实习生版本（`1point3acres interview/thread/1096856`）据报道只要求做到 Part 3（渲染），Part 4-5（最近点、批处理 CLI）是正式工程师版本才要求的加码。

## What this tests
skills: S02 解析嵌套 JSON/GeoJSON · S18 网络错误的分类与归一化（MapError 包装） · S19 增量设计（Part n 复用 Part n-1 的函数） · S20 自测（用面试官给的坐标顺序陷阱自己先验证一遍） · S24 领域知识（HTTP 客户端 ergonomics：防御性响应校验、内容哈希缓存）

## 面试官追问（不少于 6 个）
1. "如果 `render_map` 中途网络断开、已经写了一半文件怎么办？" —— 期待：先写临时文件再原子 rename，或者失败时删除半成品文件，不留下损坏的 PNG。
2. "1 万个点的路线要渲染，`/render` 只接受 10000 个点，你会怎么处理？" —— 期待：识别 413，做客户端分段/降采样（比如按等距抽稀）而不是让请求直接失败。
3. "`nearest_point` 对 10 万个坐标点、10 个地标要跑多快？能不能不用暴力 O(n×m)？" —— 期待：能讨论空间索引（KD-tree/网格分桶）作为下一步优化方向，即使当前实现是线性扫描。
4. "如果两次调用 `cli` 之间地图渲染服务的返回内容变了（比如换了配色），缓存还应该复用旧结果吗？" —— 期待：讨论缓存失效策略（按服务版本/响应哈希而不仅是输入内容哈希）。
5. "为什么用 Haversine 而不是欧几里得距离直接算经纬度差？" —— 期待：地球是球面，经度 1° 对应的实际距离随纬度变化，欧氏距离在高纬度会系统性失真。
6. "`render_route` 校验了 PNG 魔数，还应该校验什么？" —— 期待：Content-Length 是否与实际读到的字节数一致（防止连接中断导致的截断响应）、Content-Type header。
7. "CLI 的 `--cache-dir` 如果被多个进程并发写，会不会出问题？" —— 期待：`index.json` 的读-改-写不是原子的，讨论文件锁或者每个 `<hash>.png` 用先写临时文件再 rename 的方式规避半写文件。
8. "GeoJSON 坐标顺序这个坑，你在代码里怎么防止未来自己或者同事再犯？" —— 期待：在 `load_coordinates` 里写清楚注释/类型别名，甚至用 `NamedTuple(lat, lng)` 而不是裸 `tuple`，让顺序在类型层面显式。

## Sources
- https://oavoservice.com/en/articles/stripe-integration-bikemap-geojson-http-staticmap-nearest-landmark（逐 part 拆解，访问 2026-06-07；`loop/raw/github_repos.md` §3.1 复述）
- learncswithus.com《Stripe SDE VO 面经｜Integration怎么考｜VO 全套真题分享》2025-11-11（`loop/raw/cn_forums.md` 第 87–99 行，5-part 拆解与 oavoservice 独立交叉一致）
- https://www.teamblind.com/post/is-stripe-integration-always-bikemap-for-java-h8lemeaq（Stripe 员工确认题库随机抽题，BikeMap 是其中一个）
- https://www.1point3acres.com/interview/problems/bba4944f-e065-4b5f-91be-f3564b9fd691（"Integration Exercise: BikeMap API Integration"）
- https://prachub.com/interview-questions/design-ledger-and-bikemap-integration（2025-07-29，作为 onsite 综合题收录）
- `github.com/komoot/staticmap` README（`(lon, lat)` API 用法参考，本题未直接使用该库，见 Variants）
- `loop/mockserver/README.md` §maps.py（本仓库对地图渲染后端的复刻实现，作为本题的 mockserver）

## Clarifications（本仓库自定，非题面原文）
- Stripe 出题仓库不允许候选人下载/复制题面（`cn_forums.md` 已确认"故意设置为不可复制/不可直接粘贴"），因此没有任何来源给出 `ride-simple.json` 的原始字节内容；本仓库的 `data/ride-simple.json` 是按 oavoservice 描述的结构（GeoJSON、约 500 点）用 `random.Random(0)` **重新生成**的等价数据，不是原题数据。
- `/render` 接口的具体 JSON 形状（`points`/`markers`/`width`/`height`）、错误码、限流是本仓库设计（`loop/mockserver/maps.py`），源材料只说"POST 请求、JSON body、PNG 响应"，没有给出字段名。
- Part 5 "批处理 + 缓存 + 模块化成 CLI" 的具体验收标准（内容哈希缓存、`index.json` 结构）是本仓库补全；oavoservice 原文只说这是"几乎没人做完"的加分项，没有给出验收细节。
