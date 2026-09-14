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
| [od11_dynamic_blacklist_filter](od11_dynamic_blacklist_filter.md) | `../../loop/rounds/04_ood/od11_dynamic_blacklist_filter/` | OOD | 合并两条乱序流时，"同一时刻两件事谁先生效"不是可以模糊带过的实现细节，是必须显式写进契约、决定整个系统语义的规则 |
| [od12_top_k_book_sales](od12_top_k_book_sales.md) | `../../loop/rounds/04_ood/od12_top_k_book_sales/` | OOD | 当数据结构原生不支持某个操作时不必换数据结构——让"过期"记录留着，查询时验证、丢弃无效的、塞回有效的，均摊成本几乎不变 |
| [od13_dictionary_trie_codec](od13_dictionary_trie_codec.md) | `../../loop/rounds/04_ood/od13_dictionary_trie_codec/` | OOD | 设计自定义序列化格式时，先证明"控制字符"和"数据字符"的字符集互不相交，编码就天然无歧义、不需要任何转义 |
| [od14_durable_kv_serialization](od14_durable_kv_serialization.md) | `../../loop/rounds/04_ood/od14_durable_kv_serialization/` | OOD | 任何版本号/生成号类的协调状态，权威来源必须是持久层本身而不是内存计数器——内存状态可能在对象重建时归零，进而撞车覆盖已提交的数据 |
| [od15_json_parser](od15_json_parser.md) | `../../loop/rounds/04_ood/od15_json_parser/` | OOD | "最小化输出"只针对空白，不针对数据本身的文本表示——数字必须原样保留源文本，解析时过早转换成 float 会造成不可逆的信息丢失 |
| [pc11_character_frequencies](pc11_character_frequencies.md) | `../../loop/rounds/03_phone_coding/pc11_character_frequencies/` | 电面 coding | 任意深度嵌套结构（来自不受信任的输入）绝不能用递归展开——用一个显式栈 + `iter()` 存"当前遍历到哪一层的哪个位置"，栈深度不受 Python 调用栈限制 |
| [pc12_top_two_users_by_purchase](pc12_top_two_users_by_purchase.md) | `../../loop/rounds/03_phone_coding/pc12_top_two_users_by_purchase/` | 电面 coding | 涉及金额的题永远先把字符串转成整数最小单位（分），全程不经过 `float`——浮点数不能精确表示大多数十进制小数，累加误差会在数据量大时真的改变排名 |
| [pc13_service_startup_order](pc13_service_startup_order.md) | `../../loop/rounds/03_phone_coding/pc13_service_startup_order/` | 电面 coding | 拓扑排序卡住时，"还没启动的服务"里有些只是在等一个环、自己并不在环上——报错要指名道姓找出真正互相依赖的那一圈，而不是把所有卡住的都算成"有问题" |
| [pc16_reverse_alphanumeric_segments](pc16_reverse_alphanumeric_segments.md) | `../../loop/rounds/03_phone_coding/pc16_reverse_alphanumeric_segments/` | 电面 coding | Python 的 `str` 不可变，"原地 O(1) 空间"这个追问永远意味着 API 要从 `str -> str` 换成 `list[str] -> None`——空间复杂度的降低往往先要求接口签名跟着变 |
| [pc17_forest_parent_array_delete](pc17_forest_parent_array_delete.md) | `../../loop/rounds/03_phone_coding/pc17_forest_parent_array_delete/` | 电面 coding | 批量"同时"删除要看原始结构里最近的存活祖先，不能靠重放单次删除的连续效果——"依次"和"同时"在有传递性的操作下经常给出不同答案 |
| [pc18_number_transformation_path](pc18_number_transformation_path.md) | `../../loop/rounds/03_phone_coding/pc18_number_transformation_path/` | 电面 coding | 遇到数值可能无界的隐式图，先找一个不变量证明可达性边界，再给一个可论证的有限上界做有界 BFS，而不是无脑套无界搜索 |
| [pc19_rewrite_tree_subtree_sums](pc19_rewrite_tree_subtree_sums.md) | `../../loop/rounds/03_phone_coding/pc19_rewrite_tree_subtree_sums/` | 电面 coding | 满二叉树数组的下标单调性能把后序处理压成一次反向扫描；当规模逼得表示法本身撑不住时，才换成节点对象 + 显式栈的迭代后序 |
| [pc20_connect_four](pc20_connect_four.md) | `../../loop/rounds/03_phone_coding/pc20_connect_four/` | 电面 coding | 小型 OOD 设计把"判定"、"执行动作"、"整局状态机"拆成三层递进，每一层只服务自己的职责，非法操作必须在状态改变前被拒绝 |
| [pc21_accumulator_interpreter](pc21_accumulator_interpreter.md) | `../../loop/rounds/03_phone_coding/pc21_accumulator_interpreter/` | 电面 coding | 可结合的运算（仿射变换）复合后仍是同类运算，可以只算一次整体效果并记忆化，把 O(count) 的暴力循环压成 O(log count) 的快速幂 |
| [pc22_document_predicate_search](pc22_document_predicate_search.md) | `../../loop/rounds/03_phone_coding/pc22_document_predicate_search/` | 电面 coding | 倒排索引把查询开销从"文档总数"降到"命中词的倒排表大小"，AND/OR/NOT 天然对应集合的交/并/补运算，不需要逐文档扫描 |
| [pc23_min_coins_with_change](pc23_min_coins_with_change.md) | `../../loop/rounds/03_phone_coding/pc23_min_coins_with_change/` | 电面 coding | 面额集合不保证 canonical 时贪心可能不是最优解，一律换成 DP；证不出严格上界就用经验验证 + 更宽窗口的回归测试兜底，诚实说明证明的边界 |
| [pc24_service_failure_forensics](pc24_service_failure_forensics.md) | `../../loop/rounds/03_phone_coding/pc24_service_failure_forensics/` | 电面 coding | 在有环图上，"最长路径"这种概念本身没有良定义，显式判环并报错，比强行给出一个误导性的数字更诚实 |
| [pc25_grep_with_context](pc25_grep_with_context.md) | `../../loop/rounds/03_phone_coding/pc25_grep_with_context/` | 电面 coding | 区间标记 + 并集是滑窗合并的通用技巧；流式版本用"延迟定案"模式（固定大小环形缓冲）替代无界累积状态 |
| [pc26_top_k_hashtags](pc26_top_k_hashtags.md) | `../../loop/rounds/03_phone_coding/pc26_top_k_hashtags/` | 电面 coding | 去重计数必须维护成员关系（集合），不能只用计数器增量维护；滑动窗口的边界要用闭区间处理"窗口为 0"这类退化情况 |
| [pc27_recipe_sequence_matcher](pc27_recipe_sequence_matcher.md) | `../../loop/rounds/03_phone_coding/pc27_recipe_sequence_matcher/` | 电面 coding | "额外空间"是个可以精确到"随输入规模增长的辅助结构"的硬约束，O(1) 时必须把哈希表/失配表真的删掉，不能换个名字继续偷偷用等价的东西 |
| [pc28_preorder_without_invalid_nodes](pc28_preorder_without_invalid_nodes.md) | `../../loop/rounds/03_phone_coding/pc28_preorder_without_invalid_nodes/` | 电面 coding | 拿到一句有歧义的需求时，先枚举可能的读法，再找一个能让这些读法"分道扬镳"的极端输入去验证理解，而不是选一种就自信地写下去 |
| [pc29_valid_tic_tac_toe_nk](pc29_valid_tic_tac_toe_nk.md) | `../../loop/rounds/03_phone_coding/pc29_valid_tic_tac_toe_nk/` | 电面 coding | "所有 N 个对象两两满足某关系"不等价于"存在一个点同时满足全部对象"——N≥3 时必须直接对全体求交集，两两检查是看似合理、实则不完整的充分条件 |
| [q20_sequential_string](q20_sequential_string.md) | `../../problems/q20_sequential_string/` | OA | "能不能拼出某个排列"永远是计数问题、跟顺序无关——把它当子序列匹配去找，会系统性地把答案判得更小甚至判成不可能 |
| [q21_max_profit_query_selection](q21_max_profit_query_selection.md) | `../../problems/q21_max_profit_query_selection/` | OA | "只挑收益率最高的选项"不是正确贪心——收益率高但用不满预算会浪费余量，往往不如换一种搭配把预算用满 |
| [q22_dropped_requests](q22_dropped_requests.md) | `../../problems/q22_dropped_requests/` | OA | 滑动窗口限流题里，"窗口计数是否包含被自己拒绝的请求"是一个题面经常不说、但答案会分叉的隐藏假设——写代码前先问出来 |
| [q23_work_schedule](q23_work_schedule.md) | `../../problems/q23_work_schedule/` | OA | "按数值/位置升序生成"本身就是排序，不需要事后再 `sorted()`——只要生成顺序和目标顺序对应，就不要多此一举 |
| [q24_maximum_throughput](q24_maximum_throughput.md) | `../../problems/q24_maximum_throughput/` | OA | "最大化最小值/最小化最大值"系列问题，只要能写出关于候选答案单调的可行性判断，就应该二分答案而不是直接构造 |
| [q25_distance_to_nearest_two](q25_distance_to_nearest_two.md) | `../../problems/q25_distance_to_nearest_two/` | OA | "每个点到最近的一批源点的距离"永远可以用多源 BFS 解决；维度低（比如一维）时可以把 BFS 特化成更省常数的两遍扫描，但本质是同一个算法 |

共 27 篇。尚无文章的题：无。

## LeetCode 原题题集（不写题解）

这些题是 LeetCode 原题（或只加了重建的追问 Part），题解去 LeetCode 讨论区看；本 kit 只提供带测试的题集与追问。Snowflake 全部 LeetCode 公司标签题见 [`core/leetcode/companies/snowflake.md`](../../../../core/leetcode/companies/snowflake.md)。

| 题集 | LeetCode | 目录 |
|---|---|---|
| q12_merge_intervals | [LC 56](https://leetcode.com/problems/merge-intervals/) | `../../problems/q12_merge_intervals/` |
| q13_min_interval_each_query | [LC 1851](https://leetcode.com/problems/minimum-interval-to-include-each-query/) | `../../problems/q13_min_interval_each_query/` |
| q14_palindromic_subsequences_product | [LC 2002](https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/) | `../../problems/q14_palindromic_subsequences_product/` |
| q15_graph_valid_tree | [LC 261](https://leetcode.com/problems/graph-valid-tree/) | `../../problems/q15_graph_valid_tree/` |
| q16_form_target_from_dictionary | [LC 1639](https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/) | `../../problems/q16_form_target_from_dictionary/` |
| q17_remove_stones_minimize_total | [LC 1962](https://leetcode.com/problems/remove-stones-to-minimize-the-total/) | `../../problems/q17_remove_stones_minimize_total/` |
| pc07_word_search_ii | [LC 212](https://leetcode.com/problems/word-search-ii/) | `../../loop/rounds/03_phone_coding/pc07_word_search_ii/` |
| pc09_parallel_courses_iii | [LC 2050](https://leetcode.com/problems/parallel-courses-iii/) | `../../loop/rounds/03_phone_coding/pc09_parallel_courses_iii/` |
| pc14_meeting_rooms_ii | [LC 253](https://leetcode.com/problems/meeting-rooms-ii/) | `../../loop/rounds/03_phone_coding/pc14_meeting_rooms_ii/` |
| pc15_parentheses_matching | [LC 20 / 921 / 32](https://leetcode.com/problems/valid-parentheses/) | `../../loop/rounds/03_phone_coding/pc15_parentheses_matching/` |
| od07_throne_inheritance | [LC 1600](https://leetcode.com/problems/throne-inheritance/) | `../../loop/rounds/04_ood/od07_throne_inheritance/` |
