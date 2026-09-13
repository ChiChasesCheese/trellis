# int03 · Multi-JSON ETL：三份长得不一样的 JSON，练的是"先定一个统一模型，再写两边的映射函数"

> [!tldr]
> - 这题考的是：把三份字段名、结构都不一样的 JSON 文件（当前系统导出 / 旧系统导出 / 订单）读进来，统一成
>   一份"客户"数据，再按客户 join 订单、输出报告——不是算法题，是**数据契约**题
> - 三步套路：先画一张"字段映射表"把三份原始 schema 抽成一个统一的 `Customer` 模型 → 让 Part 1 只做"读取
>   + 映射 + 去重"、不碰订单 → Part 2/3 在这个统一模型上叠加 join、双向转换、报告
> - 最值得带走的一个模式：**中间模型（intermediate model）**——多个异构数据源汇入一处时，先定一个和任何
>   源格式都无关的中间结构，所有源各自写"源 → 中间模型"的映射函数，下游逻辑只认中间模型，不摸任何一个源
>   的原始字段名

## 1. 题目在说什么（人话版）
Stripe 内部经常要把"现在用的系统"和"正在往新系统迁移的旧系统"的数据对账：字段名不一样（一边叫
`email`，一边叫 `mail`），有的记录缺字段，同一个人可能两边各有一条记录。这题模拟这个场景，外加一份订单
数据要 join 进来算报表。三份文件全是本地磁盘上的 JSON，没有网络请求，纯粹考"读文档、建模、分层写代码"
这套基本功。

小例子：`customers.json` 里有 `{"email": "Alice@Ex.com ", "created": "2024-03-01"}`，`legacy_export.json`
里同一个人是 `{"cust": {"mail": "alice@ex.com", "signup_date": "2023-11-20"}}`——邮箱大小写/空格不同、
字段名也不同，但这是同一个人，`created` 更早的那条（`2023-11-20`）应该胜出，成为统一记录里唯一的
"alice@ex.com"。

## 2. 读题：把文字变成模型
- **实体**：`Customer`（统一后的客户）、`Order`（订单，只在 Part 2 才和 Customer 发生关系）、
  `Anomaly`（一条异常记录：`type`/`source`/`ref`/`detail`，四类：`missing_email` /
  `duplicate_customer` / `orphan_order` / `duplicate_order`）。
- **输入长什么样**：三份文件，字段名各不相同——`customers.json` 是扁平列表（`id`/`email`/`name`/
  `created`）；`legacy_export.json` 是嵌套字典（`records.<legacy_id>.cust.{mail,full_name,
  signup_date}`）；`orders.json` 是订单列表，靠 `customer_email` 关联客户。读题第一件事不是猜字段怎么对
  应，是**把 problem.md 里的"数据字典"表格抄一遍**：`email` ← `email`/`cust.mail`，`name` ←
  `name`/`cust.full_name`，`created` ← `created`/`cust.signup_date`。这张表就是整道题的地基。
- **输出要什么**：`report.json`（按 email 排序）+ `anomalies.csv`（表头固定 `type,source,ref,detail`，
  顺序即产生顺序，不额外排序）。
- **状态**：处理过程中要记住"目前每个 email 见过的最佳记录是哪条"（Part 1 的 `dict[email, Customer]`）、
  "目前每个 order_id 出现了几次"（Part 2 判重复用的计数 dict）。都是 dict，因为都是按 key 查找/更新，不
  是顺序扫描。
- **一句话建模**：**先定一个和任何原始 JSON 结构都无关的统一 `Customer` 模型（`{id, email, name,
  created}` 四个键，不多不少），三份数据源各自写一个"源 → Customer"的映射函数，下游的去重/join/报告全部
  只对着这个统一模型工作，谁都不直接伸手摸原始 JSON 的字段名。**

> [!note] 为什么选"中间模型"这个结构
> 候选方案是"每次要用哪个字段就现从原始 dict 里 `.get()`"，省了定义一层模型，但后果是 `unify_customers`/
> `join_orders`/`build_report` 里到处出现 `rec.get("email")` 还是 `rec["cust"]["mail"]`，两份数据源的字段
> 名差异会渗透到每一处下游逻辑里，改一个字段名要满仓库找。中间模型把"字段名差异"这件事焊死在两个函数
> （`parse_customers`、`parse_legacy`）里，出了这两个函数，字段名永远是 `id/email/name/created` 四个键，
> 下游代码因此变得和数据源数量无关——这也是 `unify_customers(*customer_lists)` 敢用可变参数的原因：
> 它根本不关心传进来的列表原本是从哪个文件读出来的。

## 3. 下笔顺序（面试里就按这个 60 分钟走）
1. **0–5 读题确认**：把"数据字典"表格在心里（或纸上）过一遍，口头向面试官复述一句："`customers.json`
   的 `email` 和 `legacy_export.json` 的 `cust.mail` 是同一个东西，对吧？"——这题最容易在这一步理解偏，
   宁可多问一句。
2. **5–15 跑通项目**：**先把三份 JSON 用 `json.load` 读进来 `print` 一眼实际长什么样**，而不是凭 problem.md
   的文字描述在脑子里臆测 schema——尤其 `legacy_export.json` 那层 `records.<id>.cust` 嵌套，肉眼看一遍比
   读三行文字描述可靠得多。同时把 `main()`/`load_all` 的骨架搭起来，返回空结构，确认能跑、能被测试收集到。
3. **15–35 happy path**：先写 `parse_customers`、`parse_legacy`——只处理"字段都在"的正常记录，先不管缺
   字段。立刻写好这两个函数就手动构造一个 worked example（题面给的那三份小文件）跑一遍，肉眼核对统一后的
   `Customer` 字典对不对。再写 `unify_customers`（按 email 合并，`created` 早的赢）、`join_orders`（按
   email 挂订单）、`build_report`。Happy path 走完，三个 Part 的主干都能跑了。
4. **35–48 错误处理**：回头补"字段缺失/为空/空白"三种"无邮箱"判定、`load_json_file` 把裸异常包成
   `EtlError`（带文件名和行列号）、`customers.json` 顶层类型不对时显式 `raise` 而不是让遍历深处抛出语义
   不清的 `TypeError`、重复 email 时"缺失 created 不能靠字符串比较意外获胜"这个哨兵值技巧。这一段是这题
   真正的得分点——"三份数据字段名/类型不一致"这句题眼就是冲着这段来的。
5. **48–55 清理**：抽公共的异常构造函数（避免五处地方手写同一个 `{"type":..,"source":..}` 字典）、把
   `parse_legacy` 和 `from_legacy` 共用的字段映射合并成一个私有 helper，检查有没有函数超过 40 行。
6. **55–60 总结**：跑一遍 worked example 全部三个 Part，口头过一遍"如果时间不够我会先保证 Part 1/2 的正
   确性，`main_cli` 的参数校验可以放最后"。

## 4. 代码怎么组织
```
normalize_email(raw) -> str                 # 邮箱规范化，三份数据源共用
parse_customers(raw) -> (list[Customer], list[Anomaly])   # 数据源1 -> Customer，只认 customers.json 的字段名
parse_legacy(raw)    -> (list[Customer], list[Anomaly])   # 数据源2 -> Customer，只认 legacy_export.json 的字段名
unify_customers(*lists) -> (dict[email,Customer], list[Anomaly])  # 只认 Customer，按 email 去重
join_orders(customers, orders) -> (dict[email,Customer+orders], list[Anomaly])  # 只认 Customer，挂订单
build_report(joined) -> dict[email, {...}]   # 只认 Customer，格式化成报告
to_legacy(customer) / from_legacy(record)    # Customer <-> legacy 格式，互为逆运算
write_outputs(out_dir, report, anomalies)    # 落盘，格式化集中一处
main(stdin, stdout)                          # 只做分发
```
拆分原则和 HTTP 类题目里"把网络调用封装成一个函数，业务逻辑不碰网络"是同一个思路的变体：这里换成
**"把原始 JSON 结构封装在两个解析函数里，业务逻辑不碰原始 JSON"**。`unify_customers`/`join_orders`/
`build_report` 这三层完全不知道数据是从哪个文件、用什么字段名读出来的——它们的函数签名里只有
`Customer`/`dict[email,Customer]`，这就是"中间模型"带来的解耦：面试官问"如果要接入第三份数据源"，你
只需要新写一个 `parse_xxx`，下游一行都不用改。`to_legacy`/`from_legacy` 也是同一个模型的两个方向：
Customer 到 legacy 格式，legacy 格式回 Customer，而 `parse_legacy` 内部的字段映射和 `from_legacy` 复用
同一个私有 helper（方向是 Part 2 复用 Part 1，不是反过来），避免两处各写一遍容易日后漂移。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：两个"源 -> Customer"映射 + 一个去重层 + 一个 join 层。省略字段缺失/类型校验的细节判断。
def parse_customers(raw):                      # 数据源 1：扁平列表，字段名就是 Customer 的字段名
    customers, anomalies = [], []
    for rec in raw:
        email = normalize_email(rec.get("email"))
        if not email:
            anomalies.append(_anomaly("missing_email", "customers", str(rec["id"]), "..."))
            continue
        customers.append({"id": str(rec["id"]), "email": email,
                           "name": rec.get("name", ""), "created": rec.get("created", "")})
    return customers, anomalies

def _legacy_cust_to_customer(legacy_id, cust):  # 字段映射表落地成代码，Part1/Part2 共用
    return {"id": legacy_id, "email": normalize_email(cust.get("mail")),
            "name": cust.get("full_name", ""), "created": cust.get("signup_date", "")}

def parse_legacy(raw):                          # 数据源 2：嵌套字典，字段名不同 -> 同一个 Customer 形状
    customers, anomalies = [], []
    for legacy_id, rec in raw.get("records", {}).items():
        customer = _legacy_cust_to_customer(legacy_id, rec.get("cust", {}))
        if not customer["email"]:
            anomalies.append(_anomaly("missing_email", "legacy", legacy_id, "..."))
            continue
        customers.append(customer)
    return customers, anomalies

def unify_customers(*customer_lists):           # 只认 Customer：按 email 合并，created 早的赢
    best, anomalies = {}, []
    for lst in customer_lists:
        for c in lst:
            existing = best.get(c["email"])
            if existing is None or c["created"] < existing["created"]:
                best[c["email"]] = c            # (缺失 created 的哨兵值处理略)
    return best, anomalies
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先把三份文件的字段映射抄一张表，不然容易在 `parse_legacy` 里手滑把 `mail` 写成
  `email`。」
- 写 `parse_customers`/`parse_legacy` 时：「这两个函数各管各的文件格式，输出统一是同一个四键 `Customer`
  字典，后面 join、去重、报告都不再关心数据到底是哪份文件来的。」
- 写 `unify_customers` 时：「缺失 `created` 不能直接拿空字符串去比较大小，那样字典序下它会意外'赢'，我
  用一个哨兵值让它永远排最后。」
- 写 `to_legacy`/`from_legacy` 时：「双向转换最容易犯的错是'看起来能转回去'但其实丢了信息，我会先写一
  个往返测试（`from_legacy(to_legacy(c)) == c`）再写实现，而不是眼看着像对的。」
- 交付时：「三个 Part 都过了 worked example；`EtlError` 我统一带上文件名和出错位置，方便排查是哪份文件
  第几行坏了。」

## 7. 常见跑偏（方法层面，3 条）
- **不先定中间模型，直接在 join/报告逻辑里现拆原始 JSON**：一开始觉得"反正就三份文件，直接
  `order["customer_email"]` 配 `customer["email"]` 得了"，结果第二份数据源接进来时才发现 join 逻辑里到
  处是 `.get("mail")` 还是 `.get("email")` 的判断，越改越乱。先写两个"源 → Customer"的纯映射函数，后面
  的每一层只认这一个统一形状，才不会越写越乱。
- **"往返转换"只测一个手工例子就当验证过了**：`to_legacy`/`from_legacy` 看起来对不代表真的可逆——常见
  漏洞是某个字段在其中一个方向被漏映射，只用一条数据测不出来。哪怕没时间上 `hypothesis`，也应该说一句
  "我会用几十条随机生成的数据跑一遍往返"，体现你知道"手工例子过了"和"真的可逆"是两件事。
- **异常处理留到最后、时间不够就跳过**：三份数据字段名/类型不一致本身就是这题的题眼，"防御性解析"不是
  加分项而是及格线。宁可 happy path 写得糙一点早点收尾，也要把"缺失字段/空字符串/类型不对"这几类边界
  在 35–48 分钟这一段里过一遍，而不是全指望 happy path 之后还有富余时间。

## 8. 同族题 / 延伸
- 其他轮：int01/int02 是"读一份本地文件 + 调外部 API"的变体，同样需要"原始响应结构不外泄到业务逻辑"，
  只是那边的"外部数据源"是 HTTP 响应而不是第二份 JSON 文件；把这题的 `parse_customers`/`parse_legacy`
  换成"parse HTTP response"、"parse local CSV"，骨架完全一样。
- 延伸思考：如果要接入第四份数据源（比如另一次系统迁移的导出），只需要新增一个 `parse_xxx` 函数，
  `unify_customers(*customer_lists)` 的可变参数签名已经为此留好了口子——这也是面试官追问"这个设计决定
  是为了什么"时的标准答案。
- 练习命令：`python3 -m pytest loop/rounds/05_integration/int03_multi_json_etl`（连跑两次确认不 flaky）；
  `IMPL=starter python3 -m pytest loop/rounds/05_integration/int03_multi_json_etl` 应该几乎全红。
