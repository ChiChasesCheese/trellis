# 一亩三分地 Stripe 内容的 GitHub 镜像（2026-09-03 收）

## 这是什么

`github.com/divyavenn/coding_problems` 的 `stripe/` 目录，**168 条**（155 道 coding + 13 道
system design）。每个文件是一道 1point3acres 题目的转录，文件名带日期和 1p3a 的 UUID/thread id。

## 为什么它重要

**1point3acres 是本题库最大的检索缺口** —— 全站被 Cloudflare 挡死，WebFetch / curl / r.jina.ai
三种方式都进不去（见 `catalog/SOURCES.md`）。这个仓库等于那批内容的一个可读镜像。

拿到的方式很朴素，值得记下来备用：**`api.github.com` 在本环境 403，`github.com` 的 HTML 页也
403，但 `git clone` 走 git smart-HTTP 是通的**。

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/divyavenn/coding_problems /tmp/dv
cd /tmp/dv && git sparse-checkout set stripe
```

## 内容分三档，**可信度差别很大，别混着用**

| 档 | 数量 | 内容 | 可信度 |
|---|---|---|---|
| **完整题面** | **10** | 题面正文 + part 划分 + 输入输出格式 + 样例，见 `full_statements/` | **medium** — 见下方警告 |
| 摘要 + 章节标题 | ~96 | 题目摘要与公开可见的章节小标题（正文在付费墙后） | medium-high（标题与结构属实） |
| 仅标题 | ~62 | 只有题名、日期、来源 UUID | high（存在性）/ 无（内容） |

### ⚠️ 关于那 10 份"完整题面"

它们的开头写的是 **"INTERVIEW PROMPT (as it would be delivered by the interviewer)"** ——
这是**转录者按题目重新组织/扩写**的版本，不是候选人逐字记录。上一轮排查 bitfont 时也注意到
同一现象（"详实到像面试官逐字讲稿，风格更像基于标题的合理重构"）。

所以：

- **题材、part 划分、考点方向**：可信，与 1p3a 的 UUID 一一对应
- **具体的输入输出格式、字段名、样例数值**：**不能当真题格式去背**
- 用它们出题时，按本仓库既有规矩加"重建题"警示块

## 10 份完整题面对应到我们的 catalog

| 文件 | 日期 | 对应 | 价值 |
|---|---|---|---|
| `transaction_fee_with_status_and_type_specific_rates` | 2026-04-20 | **C11** | catalog 原记"statement not public"，**现已有题面** |
| `parse_and_aggregate_records_with_potentially_unknown_fields` | 2026-04-13 | **无** | **新题**：`key=value` 松散记录解析 + 按币种聚合，重复 key 取最后一个 |
| `incremental_filtering_and_transformation_on_tabular_user_records` | 2026-04-11 | **无** | **新题**：表格记录的递进式过滤与变换 |
| `implement_a_rule_parser_and_evaluator` | 2026-04-30 | A5 附近 | 规则语法，与 Radar rules 同族 |
| `kyc_data_validation` | 2026-05-01 | q15 | 更完整的题面 |
| `payment_reconciliation_..._discrepancy_report` | 2026-04-23 | q20 P4 / q25 | 更完整的题面 |
| `design_a_registry_with_register_and_set_healthy_operations` | 2026-04-17 | q17 | 更完整的题面 |
| `chat_billing_compute_chat_usage_charges_from_event_logs` | 2026-04-17 | q03 | 更完整的题面 |
| `bike_map_multi_part_route_graph_problem` | 2026-04-04 | int01 | 更完整的题面 |
| `bitfont_repository_implement_decoders_and_compose_them` | 2026-04-23 | cd09 | 上一轮已用 |

## 索引里还有哪些我们没有的题名（待逐条核实）

`INDEX.md` 是全部 168 条。粗看这些题名在 catalog 里找不到对应：

- `hierarchical_string_compression_with_major_minor_parts_and_max_minor_segments`（2026-04-04）
- `csv_dataset_validation_multi_part`（2026-04-04）
- `compute_total_cost_from_two_tables_sql_aggregation_join_with_tiered_fees`（2026-03-30）
- `bug_bash_fix_301_redirect_handling_for_streaming_binary_post_requests`（2026-03-30，**bug squash**）
- `repo_debugging_fix_failing_tests_in_a_failsafe_project`（2026-04-04，**bug squash**，Failsafe 库）
- `integration_task_read_json_file_make_http_requests_compare_responses`（2026-02-17，**request replay**）
- `debugging_json_parser_issue_find_fix_bug`（2026-02-17）
- `add_moving_points_to_a_map_request_driven_updates`（2026-01-30）
- `replay_request_handling`（2026-01-25）
- `ordered_dictionary`（2026-01-16）· `domain_contact`（2026-01-16）· `message_processing_from_input`
- `bank_transaction_vo_coding` · `sendinvoicereminder` · `exception_handling_in_debugging`

**RBAC（C6）的真实结构也确认了**：Phase 1 直接角色查询 → Phase 2 继承 → **Phase 3 找出有某权限的所有用户**
→ **Phase 4 按角色过滤用户**。后两阶段是**反向查询**，跟我们 `ps10` 自拟的 part 3/4（通配符+deny、批量缓存）
**不一样** —— ps10 该按这个结构改。

## 复用与出处

原仓库是他人作品，这里只取与 Stripe 相关的部分作**个人备考参考**，出处逐条保留（每个文件头部都有
原始 1p3a URL）。不要把这些内容再分发出去。
