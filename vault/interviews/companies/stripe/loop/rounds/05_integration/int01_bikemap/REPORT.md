# int01 BikeMap — report

## Summary
Stripe 目前被报道最频繁的 Integration 例题（Stripe 员工亲述题库随机抽题时点名它作为参照）。核心不是算法，
是三件事：① 陌生数据格式的坑（GeoJSON 坐标顺序 `[lng, lat]`）；② HTTP 客户端的错误归一化（网络错误 / 非
200 / 响应体不可信，全部收敛成一个 `MapError`）；③ 需求逐步加码时函数之间的复用关系（Part n 直接调用
Part n-1 的产出，不重写）。Part 5 的批处理 + 缓存 CLI 是"几乎没人做完"的部分，用来考察时间管理和工程判断
（先把前几个 part 做扎实，而不是平均分配时间导致每个 part 都是半成品）。

## Sources & confidence
High for 5-part 结构：oavoservice.com 的逐 part 拆解文章与 learncswithus.com 的 VO 面经独立给出几乎相同的
5 part 顺序（解析 → POST 拿 PNG → 渲染路线 → 标最近地标 → 批处理/缓存），且 Stripe 员工在 Blind
（`h8lemeaq`）亲口确认 BikeMap 是题库里被抽到的真实题目之一。**具体数据不是原题数据**——Stripe 出题仓库不
允许下载/复制题面（`cn_forums.md` 已确认），`data/ride-simple.json`/`data/landmarks.json` 是本仓库按来源
描述的结构（GeoJSON、约 500 点）用 `random.Random(0)` 重新生成的等价数据；`/render` 接口的具体字段名、错
误码、限流是本仓库设计（源材料只说"POST + JSON body + PNG 响应"）。

## Part-by-part approach
1. `load_coordinates`：读 `features[0].geometry.coordinates`（`[lng,lat]`），swap 成 `(lat,lng)`；对空
   `features`/非 `LineString`/少于 2 点显式抛 `ValueError`，不返回空列表掩盖问题。`first_n` 只是格式化，
   6 位小数、`lat,lng` 无空格。
2. `render_map`：`urllib.request` POST JSON，`urllib.error.HTTPError`（非 2xx）和 `URLError`/`OSError`
   （连接失败）统一包成 `MapError`，调用方不需要知道底层用的是哪个 HTTP 库。
3. `render_route`：复用 `_post_json`，额外把 `landmarks` 转成 `markers`；**在写盘前先检查 8 字节 PNG 魔数**
   ——状态码 200 不代表 body 可信，这是所有"调用外部服务后落盘"代码的通用防御模式。
4. `nearest_point`/`nearest_for_all`：教科书 Haversine（`R=6,371,000`），线性扫描；严格 `<` 比较保证并列
   时取最小下标。10 万点 × 10 地标在 O(n×m) 下仍 < 2s（见 perf），面试官追问会引导到 KD-tree/网格分桶的
   优化方向。
5. `cli`：`argparse` 定义 5 个 flag；缓存 key 是坐标内容的 sha256 前 16 位（不是文件路径），这样同一条路线
   换个文件名也能命中缓存；`index.json` 记录 hash → 来源路径，命中时直接从 `<hash>.png` 复制。

## Pitfalls hidden tests target
- GeoJSON 坐标顺序原样返回（不 swap）—— `test_lng_lat_order_is_swapped_not_identity`
- `load_coordinates` 对畸形输入返回空列表而不是报错，掩盖上游数据问题 —— `test_fewer_than_two_points_raises`
- 把 `urllib.error.URLError`/`HTTPError` 原样冒泡给调用方，而不是统一成 `MapError` —— 两个
  `test_render_map_*_raises_maperror`
- `render_route` 只看状态码 200 就直接落盘，不校验 body 真的是 PNG —— `test_render_route_rejects_non_png_response`
  （用一个假的本地 HTTP server 返回 200 + JSON body 来触发）
- Haversine 距离并列时下标选择不确定（`<=` vs `<`）—— `test_nearest_point_ties_pick_first_index`
- CLI 缓存按文件路径而不是坐标内容做 key，导致同内容换名字不能命中缓存 —— `test_cli_cache_hit_avoids_second_render`
- `--landmarks` 缺省时崩溃（试图打开 `None` 路径）—— 未显式建测例，但 `test_cli_renders_and_prints_summary`
  的姊妹调用路径（`test_cli_batch_multiple_inputs` 不传 `--landmarks`）间接覆盖
- 批处理时多个 `--input` 只处理了第一个，或者输出文件名冲突 —— `test_cli_batch_multiple_inputs`

## Complexity + measured time/memory
`nearest_point` / `nearest_for_all`：O(n) 每个地标，O(n×m) 总体（n=路线点数，m=地标数），纯 Python 循环 +
`math.asin/sqrt`，无第三方依赖。测得：10 万点 × 10 地标 < 1s（本机测量，预算 2s，见 `test_perf_nearest_for_all_100k_points`）。
`render_map`/`render_route` 的耗时由 mockserver 决定（本地环回，单次请求通常 < 50ms）；`cli` 的整体开销
随 `--input` 数量线性增长，每个输入独立走一次渲染或缓存命中。

## Test inventory
20 tests — part1: 7（1 worked example + 3 edge + 1 fmt + 2 io）· part2: 3（1 happy + 2 edge）·
part3: 2（1 happy + 1 edge）· part4: 5（3 happy/worked + 1 io + 1 perf）· part5: 3（1 happy + 1 edge +
1 batch）。
按 marker 统计：part1 7 · part2 3 · part3 2 · part4 5 · part5 3 · edge 7 · fmt 1 · io 3 · perf 1。
`rtk proxy python3 -m pytest loop/rounds/05_integration/int01_bikemap -q` → 20 passed；
`IMPL=starter` 同一命令 → 17 failed / 3 passed（`test_io_empty_stdin` 与
`test_nearest_point_ties_pick_first_index` 对空 starter 的默认返回值恰好也成立，其余全部按预期失败）。

## Skills exercised
S02 嵌套 JSON/GeoJSON 解析 · S18 网络错误分类与归一化（MapError） · S19 增量设计（Part n 复用 Part n-1）·
S20 自测（坐标顺序陷阱要自己先验证一遍再往下写）· S24 领域知识（HTTP 客户端 ergonomics：防御性响应校验、
内容哈希缓存），对照 `skills_matrix.md`。

## 边写边说什么（onsite 话术）
- 打开 `ride-simple.json` 第一件事复述给面试官确认坐标顺序："GeoJSON 标准是 `[lng, lat]`，我在
  `load_coordinates` 里会显式 swap 成 `(lat, lng)`，并在注释里写清楚，防止后面自己或者同事又搞反。"
- 写 `render_map` 时主动说明为什么要包一层 `MapError`："调用方不应该关心我用的是 `urllib` 还是别的 HTTP
  库，统一异常类型能让上层重试逻辑更简单。"
- Part 3 加 PNG 魔数校验时主动提："状态码 200 不代表响应体一定是我期望的格式，尤其是这种二进制响应，我加一
  个最小的防御性校验，避免把损坏文件写到磁盘上。"
- Part 4 讲复杂度时主动带出优化方向："当前是线性扫描 O(n×m)，如果地标或路线点规模再大一个量级，可以用网
  格分桶按经纬度粗筛，或者 KD-tree，把每次查询降到接近 O(log n)。"
- 时间不够时优先保证 Part 1-3 的正确性和错误处理完整，Part 5 的缓存/批处理宁可口头描述设计（内容哈希 key、
  `index.json` 结构）也不要仓促写一个有 bug 的实现——多份面经强调"前几个 part 的质量比做完几个 part 更重
  要"。


## Review（2026-09-02）

### F（必须修，已修）
1. **`main()` 的 `PART 3` 分支是死代码，响应非 PNG 时会直接崩溃而不是按 problem.md 输出 `NOT_PNG`。**
   `render_route` 在磁头校验失败时会 `raise MapError`（Part 3 要求的行为），但旧版 `main()` 里紧接着写了
   `out = [... if png_bytes[:8] == PNG_MAGIC else "NOT_PNG"]`——这一行永远走不到 `else`：只要
   `render_route` 校验失败，异常在这行代码执行前就已经把调用栈直接炸穿了，进程以非零 exit code 崩溃，
   stdout 是空的，`stderr` 是一截 traceback。实测复现：起一个返回 200+JSON 的假 server，`PART 3` 驱动
   直接 `Traceback ... MapError`，与题面「`NOT_PNG`」的约定不符。修法：`main()` 里 `try/except MapError`
   包住 `render_route` 调用，捕获到就输出 `NOT_PNG`，否则输出 `"{n} bytes"`（`solution.py`、
   `starter_template.py`、`starter.py` 三份文件的驱动代码是完全相同的样板，三处同步修了）。
2. **`solution.py` 的 `main()` 里 `rc = cli(args)` 是从未使用的局部变量（flake8 F841）。** 改成
   `cli(args)` 不赋值，和 `starter_template.py`/`starter.py` 里同一处代码保持一致（这两份文件本来就没
   有赋值）。

### S（建议修，已按打磨）
- **`cli()` 拆分**：原来 54 行（含 14 行 docstring）挤在一个函数里，argparse 定义、单文件渲染/缓存判定、
  批处理循环揉在一起。拆成 `_parse_cli_args(argv)`（只管 argparse）和
  `_render_or_reuse(input_path, coords, server, out_dir, cache_dir, index) -> (status, n_bytes)`
  （只管"这一个文件要不要重新渲染"），`cli()` 本身现在只剩一个批处理循环 + 打印，20 行出头，符合
  "函数 ≤ 40 行、一个函数一件事"。副作用：`index.json` 从"每次渲染后立刻写一次"改成"整批处理完写一次"
  ——语义不变（下一次 `cli()` 调用读到的还是完整的 index），只是减少了重复的磁盘 I/O，不影响任何测试
  断言的时序。
- HTTP 调用已经封装在 `_post_json(base_url, path, payload) -> bytes` 里（`render_map`/`render_route`
  都只调用它，不直接碰 `urllib`），这部分沿用了原有设计，review 时确认它符合"业务逻辑不碰网络"的分层
  要求，未改动。
- 其余函数（`load_coordinates`/`first_n`/`nearest_point`/`nearest_for_all`/`_haversine_m`）逐一过了一遍
  ≤40 行、类型标注、一句话 docstring、无裸 `except`，均已经符合规范，未改动。

### 测试新增/改动
- 新增 `bad_png_server` fixture（一个返回 200+JSON 的假 HTTP server），把原来内联在
  `test_render_route_rejects_non_png_response` 里的 `_FakeHandler` 提出来复用，减少重复代码。
- 新增 `test_io_part3_happy`（`io`/`part3`）：通过 `run_script` 走 `PART 3` 驱动的正常路径，断言
  `stdout == "{n} bytes\n"` 且落盘文件是合法 PNG——覆盖了此前完全没有 io 测试碰过的 Part 3 驱动代码。
- 新增 `test_io_part3_not_png`（`io`/`part3`/`edge`）：用 `bad_png_server` 走 `PART 3` 驱动，直接命中上面
  修的那个 F 级 bug——断言 `returncode == 0`、`stdout == "NOT_PNG\n"`、且没有写坏文件到 `out_path`。这条
  测试在修复前会因为未捕获异常导致 `returncode != 0` 而失败，是这次 review 新增的、专门盯住这个 bug 的
  回归测试。
- 测试总数：20 → 22（`solution.py` 全绿；`IMPL=starter` 22 个里 20 个红、2 个绿——`test_io_empty_stdin`
  和 `test_nearest_point_ties_pick_first_index` 恰好被 starter 的默认返回值（空 list / `(0, 0.0)`）碰巧
  满足，这是已知情况，两条测试本身断言的是真实语义而非空洞占位，不需要额外收紧）。

### 遗留问题
- 无阻塞性遗留问题。`nearest_point` 仍是线性扫描（O(n×m)），`cli` 的 `index.json` 读-改-写不是原子/无锁
  的——这两点题面「面试官追问」第 3、7 条已经明确列为"讨论优化方向即可，不要求当场实现"，保持现状。

### mockserver bug
- 未发现 `loop/mockserver/maps.py` 本身的 bug。`README.md` 已知的"markers 的 label 文本不渲染"是文档里
  明确写出的已知限制（`_png.py` 手写编码器没有字体渲染），不影响 int01 的任何 part（Part 3 只要求"发送
  marker"，不要求验证 PNG 上真的画出了文字）。
