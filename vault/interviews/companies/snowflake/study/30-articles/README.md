# study/30-articles — 每题一篇中文题解

> **先做题再读**：题解是验收用的，不是读着爽的。格式见 `_TEMPLATE.md`；每篇的代码骨架与该题 `solution.py` 一致（简化，不矛盾）。

| 文章 | 题目目录 | 轮次 | 最值得带走的一个模式 |
|---|---|---|---|
| [od01_priority_task_scheduler](od01_priority_task_scheduler.md) | `../../loop/rounds/04_ood/od01_priority_task_scheduler/` | OOD | **堆不支持 O(1) 更新/删除某个元素，用一个版本号让旧堆项自然过期**——不需要物理删除，弹出时发现版本号不匹配就跳过 |
| [od02_in_memory_file_system](od02_in_memory_file_system.md) | `../../loop/rounds/04_ood/od02_in_memory_file_system/` | OOD | **目录树的结构变更需要一把粗锁，但文件内容的追加不需要跟着这把粗锁走**——找到节点这一步锁树，写内容这一步只锁这个文件自己，无关路径的写操作互不阻塞 |
| [od03_transactional_kv_store](od03_transactional_kv_store.md) | `../../loop/rounds/04_ood/od03_transactional_kv_store/` | OOD | **每层事务只记录自己碰过的 key 的新值，不需要额外的 undo-log**——因为"这一层的帧"本身就是"进入这层之后的全部修改"，`rollback` 直接丢弃整个帧就够了 |
| [od04_rate_limiter](od04_rate_limiter.md) | `../../loop/rounds/04_ood/od04_rate_limiter/` | OOD | **被拒绝/失败的请求永远不占用窗口名额**——这是本题反复强调、也是最容易被无意识做错的一条规则 |
| [od05_cron_scheduler](od05_cron_scheduler.md) | `../../loop/rounds/04_ood/od05_cron_scheduler/` | OOD | **"认领"这个动作要么用本地锁保证原子，要么委托给一个外部共享存储的"第一个写入者赢"操作**——两者是同一个思路（compare-and-set）在单机/分布式两种场景下的不同 |
| [od06_query_audit_log](od06_query_audit_log.md) | `../../loop/rounds/04_ood/od06_query_audit_log/` | OOD | **总记录数和 distinct key 数是两个不同量级，效率要求要按"该扫哪一个"来设计数据结构**——range 查询按 name 分片二分，"多久未访问"只扫 distin |
| [od08_lru_ttl_cache](od08_lru_ttl_cache.md) | `../../loop/rounds/04_ood/od08_lru_ttl_cache/` | OOD | **过期腾出的空间不该逼着系统淘汰一个仍然有效的条目**——容量超出时优先清理过期记录，清理后仍超容量才走标准 LRU 淘汰 |
| [od09_queue_to_service](od09_queue_to_service.md) | `../../loop/rounds/04_ood/od09_queue_to_service/` | OOD | **"交给消费者"和"从系统里删除"是两个动作**，中间隔着一个 ack；所有故障语义都发生在这个缝里 |
| [od10_student_result_oop](od10_student_result_oop.md) | `../../loop/rounds/04_ood/od10_student_result_oop/` | OOD | **成绩、金额、阈值比较一律 `Decimal` 或整数**——`33.33` 这种阈值用 float 比较迟早出错 |
| [pc01_rbac_dag_permissions](pc01_rbac_dag_permissions.md) | `../../loop/rounds/03_phone_coding/pc01_rbac_dag_permissions/` | 电面 coding | **多父 DAG 上的继承 = 拓扑序 DP**，父节点先结算，子节点读到的就是完整祖先并集，不用往上爬 |
| [pc02_closest_facility_grid](pc02_closest_facility_grid.md) | `../../loop/rounds/03_phone_coding/pc02_closest_facility_grid/` | 电面 coding | **并列时的赢家必须由显式比较决定**，不能由"谁先入队"决定——换一种写法答案就变了 |
| [pc03_recent_event_stream](pc03_recent_event_stream.md) | `../../loop/rounds/03_phone_coding/pc03_recent_event_stream/` | 电面 coding | **窗口的"进"和"出"是对称的两段代码**，计数的增减必须成对出现；只写"进"不写"出"是这类题最常见的 bug |
| [pc04_wiki_shortest_click_path](pc04_wiki_shortest_click_path.md) | `../../loop/rounds/03_phone_coding/pc04_wiki_shortest_click_path/` | 电面 coding | **"正向贪心每步选最小邻居"是错的**——它可能走进死胡同；反向距离表保证每一步都还在某条最短路上 |
| [pc05_max_events_ii](pc05_max_events_ii.md) | `../../loop/rounds/03_phone_coding/pc05_max_events_ii/` | 电面 coding | **闭区间用 `bisect_right`，半开区间用 `bisect_left`**——这一个字母就是 off-by-one |
| [pc06_happy_number](pc06_happy_number.md) | `../../loop/rounds/03_phone_coding/pc06_happy_number/` | 电面 coding | **任何"反复套一个函数"的序列都是一条隐式链表**，判环、找环长、找入口都能用快慢指针在 O(1) 空间完成 |
| [pc10_distributed_tree_count](pc10_distributed_tree_count.md) | `../../loop/rounds/03_phone_coding/pc10_distributed_tree_count/` | 电面 coding | **分布式聚合的正确性不依赖投递顺序，只依赖每条消息恰好一次**——所以用一个队列模拟就足以证明协议对 |
| [q01_task_scheduling_paid_free_server](q01_task_scheduling_paid_free_server.md) | `../../problems/q01_task_scheduling_paid_free_server/` | OA | **贪心会在这题上出错**——"能白嫖就白嫖"在某些输入下比"多花一点排队"更贵，必须让 DP 去比较两条路 |
| [q02_vowel_run_dp](q02_vowel_run_dp.md) | `../../problems/q02_vowel_run_dp/` | OA | **状态设计定了，剩下的都是工程约束的排列组合**——大整数精度、取模、O(n) 扫描本质上是同一个 DP 换了三种落地方式 |
| [q03_tree_height_reduction](q03_tree_height_reduction.md) | `../../problems/q03_tree_height_reduction/` | OA | **多个 part 共享一个主题但契约不同时，写代码前先把契约表格写出来**——这题最容易失分的地方不是算法难，是把三套约定搞混 |
| [q04_maximum_order_volume](q04_maximum_order_volume.md) | `../../problems/q04_maximum_order_volume/` | OA | **零时长区间是空集，不参与任何冲突判断**——这是本题唯一真正的"坑"，不是算法难，是边界语义容易想当然 |
| [q05_paint_the_ceiling](q05_paint_the_ceiling.md) | `../../problems/q05_paint_the_ceiling/` | OA | **乘积不等式在正整数域可以转成除法阈值**——`x*y<=a` 等价于 `y<=a//x`，转成阈值之后就能排序+二分/双指针，是一类计数题的通用跳板 |
| [q06_patching_array](q06_patching_array.md) | `../../problems/q06_patching_array/` | OA | **同一个贪心循环，Part 2 只是把"计数"换成"收集打补丁前的值"**——两个 part 共享一份循环体，不要写两份贪心逻辑 |
| [q07_inorder_morris](q07_inorder_morris.md) | `../../problems/q07_inorder_morris/` | OA | **Morris 遍历靠"临时改树"换空间**——用中序前驱的空闲右指针搭一条临时线索，走完就拆掉，全程 O(1) 额外空间 |
| [q08_course_schedule_ii](q08_course_schedule_ii.md) | `../../problems/q08_course_schedule_ii/` | OA | **两个 part 故意用不同的编号方向和 0/1-indexed 约定**——这是本题设计上刻意保留的坑，写代码前先把两套约定分开写清楚 |
| [q09_server_selection](q09_server_selection.md) | `../../problems/q09_server_selection/` | OA |  |
| [q10_wiki_min_clicks](q10_wiki_min_clicks.md) | `../../problems/q10_wiki_min_clicks/` | OA | **多个节点同时并列最短时，路径不是唯一的——必须约定一套确定性 tie-break**（FIFO 出队顺序 + 邻居字母序）才能让重建的路径可测试 |
| [q19_maximize_or_sum](q19_maximize_or_sum.md) | `../../problems/q19_maximize_or_sum/` | OA | **原帖作者"全给最大元素"的贪心是错的，也过了 HackerRank 测试**——测试没抓到不代表对，面试官会给反例 |

共 27 篇。尚无文章的题：无。
