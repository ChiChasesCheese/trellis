# LeetCode Project 映射到 low-level-design 知识树

范围：`leetcode.com/project` 的 31 个项目（2026-11-16 从公开列表与概览接口取得；每个项目只读到题面概览，没有读到隐藏测试与工作区）。题面句子没有照抄，考点用自己的话重述。叶子卡片数来自 `trellis --domain low-level-design stats` 与卡片文件的 `node:` 字段（2026-11-16）。

结论一行：39 个规范考点（另有 1 个格式层面的考点「指挥并验证编程智能体」，31 个项目全部具备，不计入权重）；covered 11 / thin 16 / gap 12。总权重 210（各考点项目数之和）。

说明几点：

- 「thin」包含两种情况：叶子存在但卡片没讲到这个角度；叶子存在但是空叶子（0 张卡片）。后一种在表里写明「(0)」。low-level-design 的 `fluency`、`data`、`api`、`fsm`、`concurrency-depth`、`errors`、`parsing-io`、`reading`、`refactoring`、`review`、`performance`、`ai` 等十几个根都还没有卡片，所以这些根下的叶子一律不算「covered」。
- 「gap」指整棵树里没有任何叶子教这个角度。
- 括号里的数字是该叶子的卡片数。证据只引用卡片的问题句，没有引用答案。

## Projects

类型：build（从零实现，接口已给）、repair（修已有的坏实现）、incident（线上事故，需调查并修现网数据）。分钟是官方估计解题时间，也是练习时限（接口里 `practiceMaxMinutes` 与之相同）。考点用规范名，代号见下一节。

| slug | 类型 | 难度 | 分钟 | 免费/付费 | 考点（规范名） | 隐藏测试可能钉死的歧义 |
|---|---|---|---|---|---|---|
| rate-limiter | build | INTERMEDIATE | 45 | 免费 | 共享可变状态的线程安全与复合操作、按键、按实例、按调用隔离状态、时间：注入时钟、有效期窗口、aware 与 naive datetime、边界值与区间开闭、限流算法：滑动窗口与令牌桶、计数器与统计的准确性 | 被拒请求是否消耗额度、是否计入统计；窗口边界：恰好满一个窗口的旧请求算过期还是仍在窗口内；「恢复时间」对令牌桶是攒够一个令牌，对滑动窗口是最老记录过期；不同客户端、不同资源的状态互不影响，统计按谁聚合 |
| comments-replies | build | INTERMEDIATE | 45 | 付费 | 返回值与输入的拷贝隔离、按键、按实例、按调用隔离状态、共享可变状态的线程安全与复合操作、输入校验与类型检查、确定性顺序：平局规则、插入序、保序输出、Top-k、ID 与令牌的分配 | 评论与回复的自增 ID 是否各自从 1 开始、互不共享计数；回复指向的父评论不属于该帖子时的错误类型；创建顺序按插入顺序，不按时间戳排序；校验失败的请求是否消耗 ID |
| url-shortener | build | ADVANCED | 60 | 付费 | 共享可变状态的线程安全与复合操作、输入校验与类型检查、HTTP 状态码与 JSON 契约、授权与资源归属、数据库持久化：提交、重开可见、连接管理、唯一约束、数据库层并发：原子条件更新、唯一约束、防超卖、哈希：确定性分桶、短码、内容摘要与碰撞、时间：注入时钟、有效期窗口、aware 与 naive datetime、计数器与统计的准确性、ID 与令牌的分配、SQL 查询：聚合、Top-k、参数化、过滤与排序下推 | 恰好到过期时刻是否已过期；已过期访问回 404 还是 410，是否计入点击；自定义短码冲突与自动生成碰撞的状态码和重试次数；非所有者删除回 403 还是 404；命中计数的读改写在并发下不能丢 |
| reservation-service | incident | ADVANCED | 60 | 付费 | 数据库层并发：原子条件更新、唯一约束、防超卖、数据库持久化：提交、重开可见、连接管理、唯一约束、现网数据原地修复：预演、备份、验证、留记录、读懂陌生代码、按书面规则定位根因并补回归测试、生命周期与状态转移、批量与多步操作的原子性 | 剩余容量以计数列还是以有效预订数为准（谁是真相源）；重复取消、取消已取消的预订是否幂等；满员时的预订返回哪种结果，页面各处是否一致；历史坏数据修复后保留哪些记录当审计，修复脚本能否重复运行 |
| file-deduplication | build | ADVANCED | 60 | 付费 | 有界并发：worker 上限、保序结果、FIFO 准入、内存预算、惰性迭代、单次遍历输入与有界内存、哈希：确定性分桶、短码、内容摘要与碰撞、文件遍历、符号链接与硬链接、流式 I/O、批处理中单项失败隔离、确定性顺序：平局规则、插入序、保序输出、Top-k、计数器与统计的准确性 | 硬链接（同一 inode）算不算重复；符号链接是否跟随；组内路径排序和组间排序的确定性规则；读取失败的文件从哪个阶段起计入错误、是否影响其余文件分组；空文件与哈希碰撞时必须逐字节比较 |
| feature-flag | build | ADVANCED | 60 | 付费 | 返回值与输入的拷贝隔离、共享可变状态的线程安全与复合操作、输入校验与类型检查、按固定顺序求值的规则与分级、哈希：确定性分桶、短码、内容摘要与碰撞、配置的读取、校验、规范化与原子更新、HTTP 状态码与 JSON 契约 | 规则内条件为 AND、规则之间先匹配先赢；属性缺失时条件是否匹配；百分比 0 与 100 的端点，提高百分比后已入组用户是否保持；更新时配置的规范化（大小写、去重）与未知变体的报错；删除后评估返回什么 |
| image-transform-pipeline | build | ADVANCED | 45 | 付费 | 有界并发：worker 上限、保序结果、FIFO 准入、内存预算、惰性迭代、单次遍历输入与有界内存、确定性顺序：平局规则、插入序、保序输出、Top-k、批处理中单项失败隔离 | 队首任务因内存预算放不下时，后面的小任务能否插队（FIFO 要求不能）；单个任务大于总预算时怎么办；结果按输入顺序而非完成顺序；某张图失败后预算立即归还；输入迭代器是否被提前耗尽 |
| loan-management | repair | ADVANCED | 60 | 付费 | 读懂陌生代码、按书面规则定位根因并补回归测试、共享可变状态的线程安全与复合操作、批量与多步操作的原子性、生命周期与状态转移、返回值与输入的拷贝隔离、按键、按实例、按调用隔离状态、输入校验与类型检查 | 状态只能 pending→active→repaid，非法跳转的错误与余额是否不变；超额还款、部分资助是否允许；转账两端余额之和守恒，失败时两端都不变；金额 0、负数、布尔值的校验 |
| return-fraud-risk | repair | INTERMEDIATE | 45 | 付费 | 读懂陌生代码、按书面规则定位根因并补回归测试、输入校验与类型检查、边界值与区间开闭、按固定顺序求值的规则与分级、批处理中单项失败隔离、惰性迭代、单次遍历输入与有界内存、按键、按实例、按调用隔离状态、返回值与输入的拷贝隔离、确定性顺序：平局规则、插入序、保序输出、Top-k | True/False 是否被当作整数 1/0；各阈值是 >= 还是 >，账龄与金额的边界；批量中一项非法：逐项报错且保序，不拖累其余；输入是只能遍历一次的迭代器 |
| review-moderation | repair | ADVANCED | 60 | 付费 | 读懂陌生代码、按书面规则定位根因并补回归测试、输入校验与类型检查、错误优先级与校验顺序、生命周期与状态转移、授权与资源归属、共享可变状态的线程安全与复合操作、批量与多步操作的原子性、ID 与令牌的分配、返回值与输入的拷贝隔离 | 校验、归属、审核三步的先后决定错误类型；第三次被拒是这一次就拦下，还是下一次；被拒绝的评论是否占用 ID；审核器抛异常时评论、违规数、ID 都不变 |
| issue-creation-api | build | EXPERT | 75 | 付费 | 幂等键与重试安全、乐观锁与版本检查、授权与资源归属、共享可变状态的线程安全与复合操作、批量与多步操作的原子性、分页游标与结果集上限、HTTP 状态码与 JSON 契约、输入校验与类型检查、返回值与输入的拷贝隔离、生命周期与状态转移、错误优先级与校验顺序 | 同键同体重放返回原响应；同键异体回 409 还是 422；版本不匹配回 409 还是 412；跨项目访问回 404 还是 403；游标分页在翻页途中有新建时是否稳定；状态转移图中哪些转移合法 |
| movie-recommendations | repair | ADVANCED | 60 | 付费 | 读懂陌生代码、按书面规则定位根因并补回归测试、输入校验与类型检查、确定性顺序：平局规则、插入序、保序输出、Top-k、返回值与输入的拷贝隔离、HTTP 状态码与 JSON 契约、边界值与区间开闭 | 排序键与平局规则（得分相同时按什么排）；冷启动用户（无偏好）退回什么排序；已评分、已看、不可用三类过滤的先后与 limit 的边界（0、超大）；类型偏好分的聚合方式 |
| keyword-user-blocklists | build | ADVANCED | 60 | 付费 | 输入校验与类型检查、字符串规范化与匹配、生命周期与状态转移、共享可变状态的线程安全与复合操作、批量与多步操作的原子性、返回值与输入的拷贝隔离、惰性迭代、单次遍历输入与有界内存、计数器与统计的准确性、配置的读取、校验、规范化与原子更新 | 大小写折叠（casefold 与 lower）、首尾空白、空关键词；命中是子串还是整词；第 N 次违规才封禁（含等号），封禁后是否继续计数；更新配置整体原子替换；关键词输入可能是一次性迭代器 |
| movie-watchlists | repair | ADVANCED | 60 | 付费 | 读懂陌生代码、按书面规则定位根因并补回归测试、数据库持久化：提交、重开可见、连接管理、唯一约束、授权与资源归属、共享可变状态的线程安全与复合操作、返回值与输入的拷贝隔离、HTTP 状态码与 JSON 契约、幂等键与重试安全、数据库层并发：原子条件更新、唯一约束、防超卖、输入校验与类型检查 | 重复添加电影是 200 幂等还是 409；访问他人清单是 403 还是 404；删除清单时成员行一并清理；写后立即 commit，新连接可见；重命名为已存在的名字 |
| password-reset | repair | INTERMEDIATE | 45 | 付费 | 读懂陌生代码、按书面规则定位根因并补回归测试、时间：注入时钟、有效期窗口、aware 与 naive datetime、边界值与区间开闭、生命周期与状态转移、配置的读取、校验、规范化与原子更新、按键、按实例、按调用隔离状态、数据库持久化：提交、重开可见、连接管理、唯一约束、ID 与令牌的分配 | 恰好 30 秒时是否仍有效（端点含不含）；naive 时间戳按 UTC 还是本地时间解释；已用过的码重放、重新申请是否使旧码失效；配置在构造时快照，还是每次读环境变量 |
| payment-reconcile-api | build | ADVANCED | 60 | 免费 | 批量与多步操作的原子性、幂等键与重试安全、共享可变状态的线程安全与复合操作、输入校验与类型检查、严格解析与批量记录解析、按固定顺序求值的规则与分级、确定性顺序：平局规则、插入序、保序输出、Top-k、数值精度：整数分、取整方向、范围上限、浮点容差、HTTP 状态码与 JSON 契约 | 三级匹配的优先级；容差边界含不含；多张发票条件相同的平局规则（金额、日期、ID）；同幂等键不同请求体的状态码；重放返回原结果；付款批次任一笔失败则整批回滚，含已结清标记 |
| scheduled-banking | build | ADVANCED | 60 | 付费 | 批量与多步操作的原子性、定时事件与任意历史时点查询、时间：注入时钟、有效期窗口、aware 与 naive datetime、确定性顺序：平局规则、插入序、保序输出、Top-k | 到期支付与同一时间戳的请求谁先处理；到期时刻恰等于查询时刻是否已结算；转账批次第几笔失败都整批回滚，且不触发调度；排名并列的次序；查询早于首个事件 |
| stack-trace-stream | build | ADVANCED | 60 | 付费 | 惰性迭代、单次遍历输入与有界内存、流式状态的检查点与恢复、输入校验与类型检查、批量与多步操作的原子性、确定性顺序：平局规则、插入序、保序输出、Top-k | 帧身份是完整调用路径，不是函数名；同一步里 end 与 start 的先后顺序（end 逆序）；N 次连续确认的计数在栈中途变化时是否清零；非法样本不得改变任何状态；快照恢复后输出与不中断逐字相同 |
| tool-call-agent | build | ADVANCED | 60 | 付费 | 工具调用循环：协议校验、预算、重放缓存、有界并发：worker 上限、保序结果、FIFO 准入、内存预算、幂等键与重试安全、输入校验与类型检查、批处理中单项失败隔离、确定性顺序：平局规则、插入序、保序输出、Top-k、返回值与输入的拷贝隔离 | 同一 call ID 重复出现时命中缓存、不再执行；工具抛异常转成错误结果，不终止循环；回合或工具调用预算用尽时如何退出、转录里记什么；同批并发结果按调用顺序而非完成顺序入转录 |
| actor-follow-notifications | repair | ADVANCED | 60 | 付费 | 读懂陌生代码、按书面规则定位根因并补回归测试、发布订阅扇出与去重通知、幂等键与重试安全、批量与多步操作的原子性、输入校验与类型检查、共享可变状态的线程安全与复合操作、返回值与输入的拷贝隔离、确定性顺序：平局规则、插入序、保序输出、Top-k | 用户关注同一部电影的多位演员，只通知一次；取消关注后不再通知，已有收件箱保留；相同导入为无操作；冲突导入被拒且状态不变；收件箱按插入顺序，返回独立快照 |
| stockroom-inventory | repair | EXPERT | 75 | 免费 | 读懂陌生代码、按书面规则定位根因并补回归测试、数据库持久化：提交、重开可见、连接管理、唯一约束、授权与资源归属、乐观锁与版本检查、数据库层并发：原子条件更新、唯一约束、防超卖、输入校验与类型检查、HTTP 状态码与 JSON 契约 | 未认证 401；访问他人物品回 404 还是 403；同一版本上并发编辑只成功一次，失败状态码（409）；(owner, sku) 唯一冲突映射为哪个状态码；创建与更新返回数据库里实际存的内容，版本递增必须原子 |
| parcel-return-policy | repair | EXPERT | 75 | 免费 | 读懂陌生代码、按书面规则定位根因并补回归测试、严格解析与批量记录解析、输入校验与类型检查、边界值与区间开闭、数值精度：整数分、取整方向、范围上限、浮点容差、按固定顺序求值的规则与分级、错误优先级与校验顺序、批处理中单项失败隔离 | 重复键一律拒绝、转义序列只接受规定集合；64 位整数的上下界，不能溢出也不能静默变浮点；评分阈值含不含等号；多条拒绝规则同时命中时报哪一条；坏行只产生错误结果，不影响后续行 |
| event-campaigns | repair | ADVANCED | 60 | 免费 | 读懂陌生代码、按书面规则定位根因并补回归测试、按键、按实例、按调用隔离状态、按固定顺序求值的规则与分级、边界值与区间开闭、时间：注入时钟、有效期窗口、aware 与 naive datetime | 「本周末」含周日，日界按哪个时区；「低于 50 美元」是严格小于，售罄排除；共享地点优先于常住城市；规则组合与复用时不能把一位客户的状态带给另一位；分级、上限、兜底 |
| apparel-shopping-cart | build | ADVANCED | 60 | 付费 | 确定性顺序：平局规则、插入序、保序输出、Top-k、数值精度：整数分、取整方向、范围上限、浮点容差、边界值与区间开闭、返回值与输入的拷贝隔离 | 已有行再次添加是累加还是覆盖，位置是否保持；数量设为 0 即删除；负数、非整数、未知商品；总价超过 32 位也要精确；目录顺序与购物车插入顺序，快照互相独立 |
| currency-conversion | build | INTERMEDIATE | 60 | 付费 | 严格解析与批量记录解析、输入校验与类型检查、批量与多步操作的原子性、图的路径搜索、数值精度：整数分、取整方向、范围上限、浮点容差、确定性顺序：平局规则、插入序、保序输出、Top-k、错误优先级与校验顺序、返回值与输入的拷贝隔离 | 错误优先级（格式、币种、数值）；容差内的最优路径：更少跳数优先，再按路径字典序；自环、零与负汇率；重复报价覆盖还是拒绝；整批原子，快照互相独立 |
| payment-form-validation | build | ADVANCED | 60 | 付费 | 输入校验与类型检查、生命周期与状态转移、边界值与区间开闭、时间：注入时钟、有效期窗口、aware 与 naive datetime、返回值与输入的拷贝隔离 | 卡号是否允许空格与连字符，长度边界；年份窗口两端含不含，基于注入的当前年份；touched 仅在失焦时置位，错误信息在 touched 之后才出现；值原样保存不 trim；重置清空 touched |
| payments-api | build | ADVANCED | 60 | 付费 | 数据库持久化：提交、重开可见、连接管理、唯一约束、SQL 查询：聚合、Top-k、参数化、过滤与排序下推、批量与多步操作的原子性、ID 与令牌的分配、按键、按实例、按调用隔离状态 | 缺失账户上的付款不改变任何数据，也不消耗 ID；无付款账户余额为 0，余额含负数金额；关闭重开数据库后，ID 序列接着走；不同数据库实例互不共享状态 |
| transactions-list | build | ADVANCED | 60 | 付费 | 返回值与输入的拷贝隔离、确定性顺序：平局规则、插入序、保序输出、Top-k | 展示字符串逐字复制，不重新格式化；金额为 0 归 credit 还是 debit；替换列表时保持当前过滤；快照对输入、对后续操作、彼此都独立；空列表 |
| shipping-cost | build | ADVANCED | 60 | 付费 | 严格解析与批量记录解析、输入校验与类型检查、批量与多步操作的原子性、错误优先级与校验顺序、数值精度：整数分、取整方向、范围上限、浮点容差、边界值与区间开闭、按固定顺序求值的规则与分级 | 阶梯无缝隙、不重叠、从第 1 件起到无上界；批次只替换被提到的（国家、商品），其余保留；先合并同商品再逐阶填充；到达的每一阶的固定费都计入；总价上限用精确算术检查；错误优先级 |
| sales-reporting | build | ADVANCED | 60 | 付费 | SQL 查询：聚合、Top-k、参数化、过滤与排序下推、输入校验与类型检查、确定性顺序：平局规则、插入序、保序输出、Top-k、边界值与区间开闭、分页游标与结果集上限、按复合键分组汇总 | 日期范围两端含不含；「活跃客户」去重口径；Top-k 并列规则；k 的上限与总行数上限；过滤条件缺省时等于不过滤 |
| receivable-allocation | build | ADVANCED | 60 | 付费 | 数值精度：整数分、取整方向、范围上限、浮点容差、边界值与区间开闭、按固定顺序求值的规则与分级、确定性顺序：平局规则、插入序、保序输出、Top-k、按复合键分组汇总 | 百分比向下取整后的零头归商户余额；固定金额合同请求超过剩余时只拿剩余；零余额也要输出商户余额行；输入顺序决定分配先后 |

## Exam points (80/20)

按项目数从多到少。「叶子」列写出现有叶子 id 与卡片数；证据列给一张卡片的问题，或写清缺什么。

| # | 规范考点 | 项目数 | 项目 | 叶子（卡片数） | 结论 | 证据卡片问题 / 缺什么 |
|---|---|---|---|---|---|---|
| 0 | 指挥并验证编程智能体（directing and verifying an agent）（格式层面，不计权重） | 31 | 全部（题型都是 AI_COLLABORATION；reservation-service 与 event-campaigns 的题面明说「怎么指挥、怎么验证」也被评分） | rounds.ai-assisted(6), review.ai-code(0), ai.*(0) | thin | rounds-ai-assisted-verify-polished-mistake：「每拿到一段 AI 生成的 diff 要查什么？什么是“看起来很对的错误”，怎样抓到它？」；rounds.ai-assisted 有 6 张，ai 分支 8 个叶子全空 |
| 1 | 输入校验与类型检查（bool 不是 int、边界处校验） [VALID] | 20 | comments-replies、url-shortener、feature-flag、loan-management、return-fraud-risk、review-moderation、issue-creation-api、movie-recommendations、keyword-user-blocklists、movie-watchlists、payment-reconcile-api、stack-trace-stream、tool-call-agent、actor-follow-notifications、stockroom-inventory、parcel-return-policy、currency-conversion、payment-form-validation、shipping-cost、sales-reporting | quality.errors(6), testing.partitioning(3); errors.boundary-validation(0) | thin | quality-validate-boundary 讲「在边界处校验、parse don't validate」；缺：Python 里 bool 是 int 的子类、数字字符串、NaN、空串这类具体的类型坑，以及校验失败返回什么；errors.boundary-validation 是空叶子 |
| 2 | 确定性顺序：平局规则、插入序、保序输出、Top-k（deterministic ordering） [ORDER] | 15 | comments-replies、file-deduplication、image-transform-pipeline、return-fraud-risk、movie-recommendations、payment-reconcile-api、scheduled-banking、stack-trace-stream、tool-call-agent、actor-follow-notifications、apparel-shopping-cart、currency-conversion、transactions-list、sales-reporting、receivable-allocation | amazon.amz-closest-store(9), problems.marketplaces.bank-account(8), problems.components.thread-pool(8); fluency.collections(0) | thin | problems-bank-account-top-spenders-tie-break：「第 2 关的排行查询“按支出总额取前 N 个账户”，如果两个账户的支出总额完全相等，排序结果应该怎么确定？」只在具体题里出现；缺：多键排序键的构造、升降序混合、稳定排序、dict/set 的迭代顺序保证 |
| 3 | 返回值与输入的拷贝隔离（defensive copy, detached snapshot） [SNAP] | 15 | comments-replies、feature-flag、loan-management、return-fraud-risk、review-moderation、issue-creation-api、movie-recommendations、keyword-user-blocklists、movie-watchlists、tool-call-agent、actor-follow-notifications、apparel-shopping-cart、currency-conversion、payment-form-validation、transactions-list | oop.pillars(5), structure.api(4), oop.values(5); data.defensive-copy(0) | thin | structure-api-leaking-internals：「`items()` 这样直接返回内部列表会有什么故障模式？方法应该怎么改？」只教返回侧；缺：入参侧拷贝（调用方事后改入参）、嵌套结构深拷贝、「快照对输入、对后续操作、彼此都独立」的测试写法；data.defensive-copy 是空叶子 |
| 4 | 批量与多步操作的原子性（all-or-nothing, 失败不留痕） [ATOM] | 12 | reservation-service、loan-management、review-moderation、issue-creation-api、keyword-user-blocklists、payment-reconcile-api、scheduled-banking、stack-trace-stream、actor-follow-notifications、currency-conversion、payments-api、shipping-cost | problems.components.kv-store(8), amazon.amz-in-memory-db(9), problems.marketplaces.digital-wallet(8), problems.booking.airline(8), problems.components.in-memory-file-system(8); errors.cleanup(0) | thin | amz-in-memory-db-failure-update-is-atomic：「`UPDATE users SET id = 50 WHERE city = 'sf'` 命中两行会发生什么？怎么保证失败时表不变？」和 problems-in-memory-file-system-move-validate-before-detach（先校验再摘除）只在各自题里教；缺：先整批校验再提交、暂存副本、失败批次不消耗 ID/计数/统计这条通用做法 |
| 5 | 边界值与区间开闭（boundary inclusivity, thresholds） [BOUND] | 11 | rate-limiter、return-fraud-risk、movie-recommendations、password-reset、parcel-return-policy、event-campaigns、apparel-shopping-cart、payment-form-validation、shipping-cost、sales-reporting、receivable-allocation | testing.partitioning(3), rounds.bug-bash(5) | covered | testing-partitioning-equivalence-boundaries：「一个接口参数 `max_tokens` 的规格是「整数，1 到 4096，含两端；不传时默认 256」。用等价类划分…和边界值分析…挑出最少的测试用例」 |
| 6 | 读懂陌生代码、按书面规则定位根因并补回归测试（repair & regression test） [DEBUG] | 11 | reservation-service、loan-management、return-fraud-risk、review-moderation、movie-recommendations、movie-watchlists、password-reset、actor-follow-notifications、stockroom-inventory、parcel-return-policy、event-campaigns | rounds.bug-bash(5), debugging.bisect(4), debugging.heisenbugs(3), rounds.ai-assisted(6); reading.*(0), debugging.hypothesis/prevent(0), testing.test-first(0) | thin | rounds-bug-bash-bug-classes：「在陌生的 Python 代码里找缺陷，要按哪几类逐一扫？每一类在代码里长什么样、怎么快速确认？」；缺：对照 README 里的产品规则逐条核对、先写失败测试再修、修完查同类 |
| 7 | 共享可变状态的线程安全与复合操作（thread safety, check-then-act） [LOCK] | 11 | rate-limiter、comments-replies、url-shortener、feature-flag、loan-management、review-moderation、issue-creation-api、keyword-user-blocklists、movie-watchlists、payment-reconcile-api、actor-follow-notifications | concurrency.model(6), concurrency.primitives(5), problems.components.rate-limiter(8), structure.storage(4); concurrency-depth.compound-actions(0) | covered | problems-rate-limiter-sharded-lock：「多线程限流器（Rate Limiter）的锁该怎么加？「每个 key 一把锁」为什么是个陷阱？Python 的 GIL 在这里帮得上忙吗？」 |
| 8 | 生命周期与状态转移（一次性令牌、计数器阈值、状态门控） [FSM] | 7 | reservation-service、loan-management、review-moderation、issue-creation-api、keyword-user-blocklists、password-reset、payment-form-validation | structure.state-machines(5), patterns.state(6), problems.booking.hotel-booking(8); fsm.*(0) | covered | structure-state-guards-and-illegal-events：「「订单只有在每个行项都有库存时才能从 PAID 变成 SHIPPED」——为什么一张简单的「状态→状态」表表达不了这条规则？拒绝的转移应该怎样上报？」 |
| 9 | HTTP 状态码与 JSON 契约（HTTP status & error mapping） [HTTP] | 7 | url-shortener、feature-flag、issue-creation-api、movie-recommendations、movie-watchlists、payment-reconcile-api、stockroom-inventory | —（parsing-io.http-client(0) 是客户端；api.error-contract(0) 是进程内） | gap | 没有叶子教服务端把校验失败、冲突、未找到、重放映射到哪个状态码；rounds.practical 叶子 0 张卡片 |
| 10 | 按键、按实例、按调用隔离状态（no shared mutable state） [ISO] | 7 | rate-limiter、comments-replies、loan-management、return-fraud-risk、password-reset、event-campaigns、payments-api | python.dataclasses-enums(6), patterns.strategy(5), amazon.amz-rate-limiter(5); fluency.mutability(0) | thin | python-dataclass-default-factory 教可变默认值；amz-rate-limiter-per-key-isolation-and-memory 教按 key 隔离；缺：规则/服务对象被复用或组合时不把一个调用的状态带给下一个（无状态设计）、两个实例不共享类属性与模块全局；fluency.mutability 是空叶子 |
| 11 | 按固定顺序求值的规则与分级（first-match, 兜底, 顺序分配） [RULES] | 7 | feature-flag、return-fraud-risk、payment-reconcile-api、parcel-return-policy、event-campaigns、shipping-cost、receivable-allocation | patterns.strategy(5), patterns.behavioral(7), amazon.amz-discount-engine(9); bank.machine-coding.rule-engine(0) | covered | amz-discount-engine-stacking-and-clamp（折扣叠加与封顶的求值顺序）和 patterns-chain-of-responsibility（先匹配先处理）；规则对象可插拔、顺序可控已有；「同时命中多条拒绝规则时报哪一条」靠题面，不是知识点 |
| 12 | 数据库持久化：提交、重开可见、连接管理、唯一约束（SQL/ORM/Mongo persistence） [DB] | 6 | url-shortener、reservation-service、movie-watchlists、password-reset、stockroom-inventory、payments-api | —（structure.storage(4) 只讲内存仓储） | gap | 全部 809 张卡片里没有出现 sqlite3、commit；amz-in-memory-db 是自己实现数据库，没有一张教使用真实数据库：commit、连接生命周期、重开后 ID 序列延续 |
| 13 | 数值精度：整数分、取整方向、范围上限、浮点容差（exact arithmetic） [NUM] | 6 | payment-reconcile-api、parcel-return-policy、apparel-shopping-cart、currency-conversion、shipping-cost、receivable-allocation | amazon.amz-wallet(6), amazon.amz-aws-billing(9), amazon.amz-splitwise(6), amazon.amz-discount-engine(9); fluency.time-numbers(0) | thin | amz-wallet-money-integer-minor-units：「金额为什么用整数最小单位（分）而不是浮点数？怎么防止币种混加？」；amz-splitwise-remainder-largest-remainder 教零头分摊；缺：规格强加的 32/64 位上限检查、向下取整与四舍五入的区别、`math.isclose` 式容差比较 |
| 14 | 时间：注入时钟、有效期窗口、aware 与 naive datetime [TIME] | 6 | rate-limiter、url-shortener、password-reset、scheduled-banking、event-campaigns、payment-form-validation | problems.components.ttl-cache(8), problems.components.rate-limiter(8), problems.booking.meeting-scheduler(8), quality.testability(4); fluency.time-numbers(0) | thin | problems-ttl-cache-absolute-deadline-not-remaining、quality-constructor-injection 教注入时钟与绝对到期时刻；problems-meeting-scheduler-local-time-plus-zone 触及时区；缺：aware 与 naive 混用抛 TypeError、统一转 UTC、「恰好 N 秒」是否仍有效的端点约定 |
| 15 | 授权与资源归属（ownership scoping, 403 vs 404） [AUTHZ] | 5 | url-shortener、review-moderation、issue-creation-api、movie-watchlists、stockroom-inventory | —（bank.practical.permissions(0) 是层级权限继承，不是归属） | gap | 没有卡片讲「每次读写都按所有者限定、他人资源回 404 以免泄露存在性」 |
| 16 | 批处理中单项失败隔离（per-item error result） [FAILISO] | 5 | file-deduplication、image-transform-pipeline、return-fraud-risk、tool-call-agent、parcel-return-policy | amazon.amz-emergency-pubsub(9), problems.components.thread-pool(8), problems.components.pub-sub(10); errors.exceptions-vs-values(0) | covered | amz-emergency-pubsub-failure-boundary-in-subscription：「「一个订阅者抛异常不能拖累其他人」这条保证应该放在哪一层实现？有哪些选择？」；problems-thread-pool-base-exception-in-worker（任务异常不杀死 worker） |
| 17 | 幂等键与重试安全（重放、冲突检测） [IDEM] | 5 | issue-creation-api、movie-watchlists、payment-reconcile-api、tool-call-agent、actor-follow-notifications | problems.marketplaces.digital-wallet(8), problems.components.notification-service(10), problems.machines.atm(12); errors.retry(0) | covered | problems-digital-wallet-idempotency-conflict：「数字钱包的幂等检查如果只看 client_key 是否出现过、命中就直接返回缓存的回执，会漏掉什么风险？应该怎么补？」另有 idempotency-reuses-account-lock（并发重试）与 ledger-append-only-idempotency-purged（缓存清理）；缺 HTTP 层表现（重放返回什么状态码），并入 api.http-contract |
| 18 | ID 与令牌的分配（自增、不复用、失败不消耗、随机唯一） [IDGEN] | 5 | comments-replies、url-shortener、review-moderation、password-reset、payments-api | structure.storage(4), problems.marketplaces.bank-account(8) | covered | structure-storage-id-generation：`self._next_id += 1` 并发下丢失更新，改用 `itertools.count()` 加锁或 `uuid.uuid4()`；bank-account 的 problems-bank-account-id-never-reused。缺「校验失败不消耗 ID」这一个角度 |
| 19 | 错误优先级与校验顺序（error precedence, validation order） [PREC] | 5 | review-moderation、issue-creation-api、parcel-return-policy、currency-conversion、shipping-cost | —（errors.boundary-validation(0), api.error-contract(0) 只覆盖大方向） | gap | 没有任何叶子或卡片教「多条规则同时违反时先报哪一条」；quality.errors 的 6 张卡片里没有这个角度 |
| 20 | 惰性迭代、单次遍历输入与有界内存（lazy, one-pass, bounded memory） [STREAM] | 5 | file-deduplication、image-transform-pipeline、return-fraud-risk、keyword-user-blocklists、stack-trace-stream | python.context-iterators(6), amazon.amz-linux-find(9); parsing-io.streams(0), fluency.iteration(0) | thin | python-context-class-vs-generator：「什么时候一个惰性序列必须写成带 `__iter__` 的类，而不能只写一个生成器函数？」；amz-linux-find-lazy-walk-and-symlink-loops 教惰性遍历；缺：入参可能是一次性迭代器（不能 len、不能遍历两次）、有界内存的缓冲与分块 |
| 21 | 数据库层并发：原子条件更新、唯一约束、防超卖（isolation, atomic update） [DBCONC] | 4 | url-shortener、reservation-service、movie-watchlists、stockroom-inventory | —（concurrency-depth.compound-actions(0) 与 structure-storage-chm-compound-ops 只管进程内） | gap | 没有卡片讲读已提交下两个事务同时扣减库存会怎样、`UPDATE … WHERE version = ?` 与唯一索引如何当锁用 |
| 22 | 严格解析与批量记录解析（strict parsing） [PARSE] | 4 | payment-reconcile-api、parcel-return-policy、currency-conversion、shipping-cost | amazon.amz-in-memory-db(9), amazon.amz-logger(4); parsing-io.tokenizer/formats/parse-errors(0) | thin | amz-in-memory-db-followup-sql-text-parser 教递归下降与优先级；缺：只接受 JSON 子集、重复键、严格转义、64 位整数不溢出；parsing-io 整个分支没有卡片 |
| 23 | 计数器与统计的准确性（hit count, error accounting） [STATS] | 4 | rate-limiter、url-shortener、file-deduplication、keyword-user-blocklists | problems.machines.coffee-machine(13), concurrency.model(6) | covered | problems-coffee-machine-counter-not-atomic 与 concurrency-augmented-assignment-not-atomic（`x += 1` 不是原子操作） |
| 24 | 有界并发：worker 上限、保序结果、FIFO 准入、内存预算（bounded concurrency） [BCONC] | 3 | file-deduplication、image-transform-pipeline、tool-call-agent | concurrency.patterns(6), problems.components.thread-pool(8), problems.components.bounded-blocking-queue(8); bank.concurrency.task-executor(0), concurrency-depth.cancel-shutdown(0) | thin | problems-thread-pool-backpressure-semaphore-not-queue-maxsize、problems-thread-pool-admission-release-on-dequeue 教信号量背压；缺：结果按输入顺序而非完成顺序、按字节预算的加权准入、惰性消费输入时只保持有限个在途任务（见 Python 版本注） |
| 25 | 配置的读取、校验、规范化与原子更新（configuration snapshot） [CONFIG] | 3 | feature-flag、keyword-user-blocklists、password-reset | — | gap | 没有叶子或卡片讲环境变量在构造时快照还是每次读取，也没有讲配置整体替换的原子性 |
| 26 | 哈希：确定性分桶、短码、内容摘要与碰撞（stable hashing） [HASH] | 3 | url-shortener、file-deduplication、feature-flag | —（python.data-model 的 4 张哈希卡讲 `__hash__` 契约，不讲摘要与分桶） | gap | python-data-model-hash-eq-contract 是 `__eq__`/`__hash__` 契约；没有卡片讲 `hash()` 每个进程加盐所以不能用来分桶、`hashlib` 摘要、百分比放量时用户保持稳定 |
| 27 | SQL 查询：聚合、Top-k、参数化、过滤与排序下推（SQL aggregation） [SQLQ] | 3 | url-shortener、payments-api、sales-reporting | —（amz-in-memory-db 是手写 SQL 引擎，不是使用 SQL） | gap | 只有 amz-occupancy-tracker-sql-version-and-scale 一张写了 SQL（`SUM(delta)` 窗口函数）；amz-in-memory-db-followup-sql-text-parser 教解析 SQL；没有卡片讲 `GROUP BY … ORDER BY … LIMIT`、占位符、库内排序 |
| 28 | 按复合键分组汇总（group-by aggregation） [AGG] | 2 | sales-reporting、receivable-allocation | amazon.amz-aws-billing(9); fluency.collections(0) | thin | amz-aws-billing-aggregate-before-tiering：「阶梯价应对每条用量记录分别计算，还是先按月聚合再计算？」讲先聚合再计价；缺：`defaultdict`/`Counter` 复合键写法 |
| 29 | 乐观锁与版本检查（optimistic locking, compare-and-set） [OPT] | 2 | issue-creation-api、stockroom-inventory | — | gap | 全部卡片里只有 amz-occupancy-tracker-sql-version-and-scale 提到 version，且是另一个意思；concurrency-depth.atomics(0) 讲 CAS 但在进程内 |
| 30 | 分页游标与结果集上限（pagination, row cap） [PAGE] | 2 | issue-creation-api、sales-reporting | problems.components.pub-sub(10), structure.api(4); api.paging-iteration(0) | thin | problems-pub-sub-cursor-owned-by-topic 讲位点归谁，不是 HTTP 分页游标；缺：游标是否在中途插入时稳定、总行数预算；api.paging-iteration 是空叶子 |
| 31 | 工具调用循环：协议校验、预算、重放缓存（agent loop） [AGENT] | 1 | tool-call-agent | —（rounds.ai-assisted(6) 讲的是用 AI 做题，不是写智能体） | gap | ai 分支教的是与 AI 工具协作；没有叶子教自己实现模型—工具循环 |
| 32 | 定时事件与任意历史时点查询（scheduled events, as-of query） [ASOF] | 1 | scheduled-banking | problems.marketplaces.bank-account(8), amazon.amz-occupancy-tracker(9) | covered | problems-bank-account-read-write-timestamp-split：「为什么写操作…要求时间戳不能比上一次调用还早，而查余额这个只读操作却必须允许传入比之前调用更早的时间戳？」 |
| 33 | 流式状态的检查点与恢复（checkpoint, resume） [CKPT] | 1 | stack-trace-stream | problems.components.text-editor(10), problems.games.chess(8); fsm.persistence(0) | thin | problems-chess-make-unmake-memento 教备忘录；缺：快照后恢复要与不中断逐字相同的输出、哪些状态必须进快照；fsm.persistence 是空叶子 |
| 34 | 文件遍历、符号链接与硬链接、流式 I/O（file system edge cases） [FILEIO] | 1 | file-deduplication | amazon.amz-linux-find(9), problems.components.in-memory-file-system(8); parsing-io.streams(0), bank.progressive-oa.file-storage(0) | thin | amz-linux-find-lazy-walk-and-symlink-loops：「遍历为什么用生成器加显式栈？跟随符号链接时怎么检测环？」；缺：硬链接按 inode 去重、分块读文件算摘要、文件系统错误的分类计数 |
| 35 | 图的路径搜索（simple paths, best route） [GRAPH] | 1 | currency-conversion | —（算法题，在 LeetCode 树里，不在本领域） | gap | 1 个项目，属于算法而非低层设计；不新增叶子 |
| 36 | 现网数据原地修复：预演、备份、验证、留记录（production data repair） [PRODREPAIR] | 1 | reservation-service | —（debugging.prevent(0) 只管防复发） | gap | 没有叶子教对没有重置路径的生产库做修复；debugging 分支 9 个叶子里 7 个空 |
| 37 | 发布订阅扇出与去重通知（pub/sub fan-out, exactly once） [PUBSUB] | 1 | actor-follow-notifications | problems.components.pub-sub(10), patterns.observer(5), amazon.amz-emergency-pubsub(9) | covered | problems-pub-sub-failing-subscriber-isolation：「进程内 Pub-Sub 里，一个订阅者的处理函数抛异常。必须保证哪两件事？代码上怎么写？」 |
| 38 | 限流算法：滑动窗口与令牌桶（sliding window, token bucket） [RATELIM] | 1 | rate-limiter | problems.components.rate-limiter(8), amazon.amz-rate-limiter(5) | covered | problems-rate-limiter-fixed-window-boundary-burst、problems-rate-limiter-token-bucket-lazy-refill（为什么令牌桶不能用后台线程补充） |
| 39 | 字符串规范化与匹配（casefold, substring match） [STRNORM] | 1 | keyword-user-blocklists | fluency.strings-bytes(0) | thin | 整个 fluency 分支没有卡片；amz-logger-parse-log-lines 只涉及行解析 |

按考点权重累计，前 20 个考点（共 39 个）覆盖 80% 的总权重 210。

### 各项目延伸的经典题（题库里已有）

| 项目 | 延伸的经典题 |
|---|---|
| rate-limiter | problems.components.rate-limiter（8）、amazon.amz-rate-limiter（5）、problems.components.ttl-cache |
| comments-replies | problems.social.stack-overflow（问答评论）、problems.social.task-management |
| url-shortener | problems.components.ttl-cache（过期）；没有短链经典题 |
| reservation-service | problems.booking.hotel-booking、problems.booking.movie-booking（不重复预订） |
| file-deduplication | amazon.amz-linux-find、problems.components.in-memory-file-system、bank.progressive-oa.file-storage（0） |
| feature-flag | problems.components.kv-store（配置存储）；没有 A/B 放量经典题 |
| image-transform-pipeline | problems.components.thread-pool、bank.practical.data-pipeline（0）、bank.concurrency.task-executor（0） |
| loan-management | problems.marketplaces.digital-wallet、problems.marketplaces.bank-account |
| return-fraud-risk | amazon.amz-discount-engine（分级规则）、bank.machine-coding.rule-engine（0） |
| review-moderation | problems.social.stack-overflow、problems.components.notification-service |
| issue-creation-api | problems.social.task-management、problems.marketplaces.digital-wallet（幂等） |
| movie-recommendations | problems.social.music-streaming、amazon.amz-playlist-dj |
| keyword-user-blocklists | problems.components.rate-limiter（按用户计数）、problems.social.chat-room |
| movie-watchlists | problems.social.music-streaming（播放列表） |
| password-reset | problems.components.ttl-cache（过期）、problems.machines.atm（PIN 计数） |
| payment-reconcile-api | problems.marketplaces.digital-wallet（幂等）、problems.marketplaces.splitwise |
| scheduled-banking | problems.marketplaces.bank-account（同一道分关题）、amazon.amz-wallet |
| stack-trace-stream | bank.structures.iterators（0）；没有对应经典题 |
| tool-call-agent | problems.components.thread-pool、problems.components.task-scheduler；没有智能体经典题 |
| actor-follow-notifications | problems.components.pub-sub、patterns.observer、problems.social.social-network |
| stockroom-inventory | problems.marketplaces.online-shopping（库存扣减） |
| parcel-return-policy | bank.practical.parser-toolkit（0）、amazon.amz-in-memory-db（SQL 文本解析） |
| event-campaigns | patterns.strategy、amazon.amz-discount-engine（规则可组合） |
| apparel-shopping-cart | problems.marketplaces.online-shopping、amazon.amz-discount-engine |
| currency-conversion | 无（图算法在 LeetCode 树）；amazon.amz-aws-billing（精度与原子批次的邻近） |
| payment-form-validation | quality.errors、testing.partitioning（边界）；没有表单经典题 |
| payments-api | problems.marketplaces.digital-wallet、problems.marketplaces.bank-account（账本与余额） |
| transactions-list | problems.marketplaces.digital-wallet（交易记录） |
| shipping-cost | amazon.amz-aws-billing（阶梯价）、amazon.amz-train-fare |
| sales-reporting | amazon.amz-aws-billing（聚合）、amazon.amz-occupancy-tracker（SQL 写法） |
| receivable-allocation | problems.marketplaces.splitwise、amazon.amz-splitwise（零头分摊） |

## Gaps and proposed leaves

提议的叶子只给「至少两个项目需要」，或「一个项目加至少两处独立来源」的缺口。全部放在已有的根下，没有放进 `lcproject`。可粘贴的 YAML 在 `new_leaves.yaml`。

| 叶子 id | 标题 | 需要它的项目 | requires | 最好的来源 | 备注 |
|---|---|---|---|---|---|
| errors.atomic-batches | 批处理的原子与隔离（All-or-Nothing vs Per-Item Failure） | 17：actor-follow-notifications、currency-conversion、file-deduplication、image-transform-pipeline、issue-creation-api、keyword-user-blocklists、loan-management、parcel-return-policy、payment-reconcile-api、payments-api、reservation-service、return-fraud-risk、review-moderation、scheduled-banking、shipping-cost、stack-trace-stream、tool-call-agent | errors.boundary-validation, errors.cleanup | https://www.sqlite.org/atomiccommit.html ；代码层写法：https://docs.python.org/3/library/sqlite3.html（连接作上下文管理器：成功提交、异常回滚） | 12 个项目需要原子批次；经典题里只有 kv-store、in-memory-db 等在各自语境讲过 |
| errors.validation-precedence | 校验顺序与错误优先级（Validation Order & Error Precedence） | 5：currency-conversion、issue-creation-api、parcel-return-policy、review-moderation、shipping-cost | errors.boundary-validation, api.error-contract | https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.4（403 与 404 的取舍） ；https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ | 没有找到把「错误优先级」当作独立主题来讲的来源，上面两处只给出相邻的原则；这一叶要靠项目题面自己归纳 |
| api.http-contract | HTTP 状态码与错误映射（HTTP Status & Error Mapping） | 7：feature-flag、issue-creation-api、movie-recommendations、movie-watchlists、payment-reconcile-api、stockroom-inventory、url-shortener | api.error-contract | https://www.rfc-editor.org/rfc/rfc9110.html（§15.5 客户端错误；§9.2.2 幂等方法）；幂等重放与冲突：https://docs.stripe.com/api/idempotent_requests 、https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ | 同一叶子吸收「幂等键在 HTTP 层怎么表现」（重放返回原响应、同键异体 422、并发在途 409） |
| api.authorization-scoping | 资源归属与授权（Ownership Scoping） | 5：issue-creation-api、movie-watchlists、review-moderation、stockroom-inventory、url-shortener | api.error-contract | https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization ；https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.4 |  |
| api.configuration | 配置的读取、校验与原子更新（Configuration Snapshots） | 3：feature-flag、keyword-user-blocklists、password-reset | errors.boundary-validation, data.defensive-copy | https://12factor.net/config | 只找到 12-factor 一处可读来源；「配置更新的原子性」没有找到专门来源 |
| data.sql-queries | SQL 查询：聚合、Top-k 与参数化（SQL Queries in Code） | 3：payments-api、sales-reporting、url-shortener | errors.boundary-validation | https://docs.python.org/3/library/sqlite3.html（占位符与字符串拼接） | 聚合与 Top-k 的机制级来源没有读到，建议补读 SQLite 官方 SELECT 与聚合函数页（本次未访问） |
| data.sql-persistence | SQL 持久化：提交、约束与重开（SQL Persistence） | 6：movie-watchlists、password-reset、payments-api、reservation-service、stockroom-inventory、url-shortener | errors.cleanup, structure.storage | https://docs.python.org/3/library/sqlite3.html ；https://www.sqlite.org/isolation.html | MongoDB 与 PostgreSQL ORM 的项目（stockroom、reservation）用同一套思维，但驱动细节不在本叶 |
| data.deterministic-hashing | 确定性哈希（Stable Hashing） | 3：feature-flag、file-deduplication、url-shortener | python.data-model | https://docs.growthbook.io/lib/build-your-own ；https://docs.getunleash.io/concepts/stickiness ；https://docs.python.org/3/reference/datamodel.html（hash 随机化）；https://github.com/pkolaczk/fclones（去重分阶段） | 三个项目用法不同：分桶、短码、内容摘要；共同点是「哈希必须可重复且要处理碰撞」 |
| concurrency-depth.optimistic-locking | 乐观锁与版本检查（Optimistic Locking） | 2：issue-creation-api、stockroom-inventory | concurrency-depth.compound-actions | https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html ；https://www.rfc-editor.org/rfc/rfc9110.html（§13.1.1 If-Match，§15.5.13 412） |  |
| concurrency-depth.db-transactions | 数据库层的并发（Isolation & Atomic Updates） | 4：movie-watchlists、reservation-service、stockroom-inventory、url-shortener | concurrency-depth.compound-actions, structure.storage | https://www.postgresql.org/docs/current/transaction-iso.html ；https://www.postgresql.org/docs/current/explicit-locking.html ；https://www.sqlite.org/isolation.html |  |
| concurrency-depth.bounded-pipeline | 有界并发流水线（Bounded Ordered Pipeline） | 3：file-deduplication、image-transform-pipeline、tool-call-agent | concurrency.patterns, python.context-iterators | https://docs.python.org/3/library/concurrent.futures.html ；https://docs.python.org/3/library/threading.html（Semaphore） | Python 3.14 才给 `Executor.map` 加了 `buffersize` 限制在途任务数；LeetCode Project 的 Python 环境是 3.11，必须手写有界窗口 |
| fluency.deterministic-ordering | 确定性顺序与平局（Total Order & Tie-Breaking） | 15：actor-follow-notifications、apparel-shopping-cart、comments-replies、currency-conversion、file-deduplication、image-transform-pipeline、movie-recommendations、payment-reconcile-api、receivable-allocation、return-fraud-risk、sales-reporting、scheduled-banking、stack-trace-stream、tool-call-agent、transactions-list | fluency.collections | https://docs.python.org/3/howto/sorting.html | 14 个项目都有排序或保序要求，是需求最广的一个缺口 |
| fluency.exact-arithmetic | 精确算术：取整、分摊与范围检查（Exact Arithmetic） | 6：apparel-shopping-cart、currency-conversion、parcel-return-policy、payment-reconcile-api、receivable-allocation、shipping-cost | fluency.time-numbers | https://docs.python.org/3/tutorial/floatingpoint.html | `decimal` 官方页本次没有读 |
| ai.agent-loop | 工具调用循环（Tool-Calling Agent Loop） | 1：tool-call-agent | ai.tools-automation, errors.boundary-validation | https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls ；https://www.anthropic.com/engineering/building-effective-agents | 只有 1 个项目；依据「一个项目加至少两处独立来源」成立 |
| debugging.data-repair | 现网数据原地修复（In-Place Data Repair） | 1：reservation-service | debugging.hypothesis, debugging.prevent | https://sre.google/sre-book/data-integrity/ ；https://stripe.com/blog/online-migrations | 只有 1 个项目（reservation-service）；两处来源都是相邻主题，没有找到「原地修复坏数据」的专门文章 |
| parsing-io.strict-json | 严格 JSON 子集解析（Strict JSON Subset） | 4：currency-conversion、parcel-return-policy、payment-reconcile-api、shipping-cost | parsing-io.tokenizer, parsing-io.formats | https://www.rfc-editor.org/rfc/rfc8259 （名字应当唯一，§4）；https://www.rfc-editor.org/rfc/rfc7493 （I-JSON：重复名字禁止）；https://docs.python.org/3/library/json.html（`object_pairs_hook`、`parse_constant`、`parse_int`） | 只有 parcel-return-policy 一个项目；依据「一个项目加至少两处独立来源」成立，优先级最低 |

没有提议新叶子的缺口与原因：

- 图的路径搜索（currency-conversion）：算法题，属于 LeetCode 树，不属于本领域。
- 字符串规范化（keyword-user-blocklists）：`fluency.strings-bytes` 已有叶子，只是 0 张卡片，填卡即可。
- 幂等键：经典题 digital-wallet、notification-service、atm 已有 7 张卡，不新增叶子；HTTP 层表现并入 `api.http-contract`。
- 空叶子需要填卡而不是新增叶子：`data.defensive-copy`、`fluency.time-numbers`、`fluency.collections`、`fluency.iteration`、`errors.boundary-validation`、`errors.cleanup`、`api.paging-iteration`、`fsm.persistence`、`parsing-io.streams`、`parsing-io.formats`、`parsing-io.tokenizer`。这些是本次 thin 考点的主要落点，应先于新叶子填卡。

### 与已有「相邻叶子」可能重复的两处

- `fluency.exact-arithmetic` 与 `fluency.time-numbers` 的 Decimal/整数分部分重叠；若不想拆，可把取整、范围检查并入后者。
- `errors.atomic-batches` 与 `errors.cleanup` 重叠在「异常路径上状态回到一致」；区别是前者讲整批语义与副作用（ID、统计）。

## Study order

规则：下一个项目是「尚未覆盖的考点权重之和」最大的那个；并列时先难度低、再免费。权重＝考点的项目数；总权重 210。「累计权重」是已学项目所覆盖的考点权重之和（每个考点只算一次，覆盖了一个考点＝拿到它的全部项目数）。「配对」列：与前面某个项目的考点集合重合度（Jaccard）≥ 0.5 才标注，表示这两个项目基本是同一套技能，成对学。

| 顺序 | 项目 | 难度 | 免费 | 新增权重 | 累计权重 | 累计占比 | 新增的考点 | 配对 |
|---|---|---|---|---|---|---|---|---|
| 1 | return-fraud-risk | INTERMEDIATE | 否 | 96 | 96 | 46% | 边界值与区间开闭、读懂陌生代码、按书面规则定位根因并补回归测试、批处理中单项失败隔离、按键、按实例、按调用隔离状态、确定性顺序：平局规则、插入序、保序输出、Top-k、按固定顺序求值的规则与分级、返回值与输入的拷贝隔离、惰性迭代、单次遍历输入与有界内存、输入校验与类型检查 |  |
| 2 | issue-creation-api | EXPERT | 否 | 56 | 152 | 72% | 批量与多步操作的原子性、授权与资源归属、生命周期与状态转移、HTTP 状态码与 JSON 契约、幂等键与重试安全、共享可变状态的线程安全与复合操作、乐观锁与版本检查、分页游标与结果集上限、错误优先级与校验顺序 |  |
| 3 | url-shortener | ADVANCED | 否 | 31 | 183 | 87% | 数据库持久化：提交、重开可见、连接管理、唯一约束、数据库层并发：原子条件更新、唯一约束、防超卖、哈希：确定性分桶、短码、内容摘要与碰撞、ID 与令牌的分配、SQL 查询：聚合、Top-k、参数化、过滤与排序下推、计数器与统计的准确性、时间：注入时钟、有效期窗口、aware 与 naive datetime |  |
| 4 | currency-conversion | INTERMEDIATE | 否 | 11 | 194 | 92% | 图的路径搜索、数值精度：整数分、取整方向、范围上限、浮点容差、严格解析与批量记录解析 |  |
| 5 | file-deduplication | ADVANCED | 否 | 4 | 198 | 94% | 有界并发：worker 上限、保序结果、FIFO 准入、内存预算、文件遍历、符号链接与硬链接、流式 I/O |  |
| 6 | keyword-user-blocklists | ADVANCED | 否 | 4 | 202 | 96% | 配置的读取、校验、规范化与原子更新、字符串规范化与匹配 |  |
| 7 | receivable-allocation | ADVANCED | 否 | 2 | 204 | 97% | 按复合键分组汇总 |  |
| 8 | rate-limiter | INTERMEDIATE | 是 | 1 | 205 | 98% | 限流算法：滑动窗口与令牌桶 |  |
| 9 | actor-follow-notifications | ADVANCED | 否 | 1 | 206 | 98% | 发布订阅扇出与去重通知 |  |
| 10 | reservation-service | ADVANCED | 否 | 1 | 207 | 99% | 现网数据原地修复：预演、备份、验证、留记录 |  |
| 11 | scheduled-banking | ADVANCED | 否 | 1 | 208 | 99% | 定时事件与任意历史时点查询 |  |
| 12 | stack-trace-stream | ADVANCED | 否 | 1 | 209 | 100% | 流式状态的检查点与恢复 |  |
| 13 | tool-call-agent | ADVANCED | 否 | 1 | 210 | 100% | 工具调用循环：协议校验、预算、重放缓存 |  |
| 14 | comments-replies | INTERMEDIATE | 否 | 0 | 210 | 100% | （无） |  |
| 15 | password-reset | INTERMEDIATE | 否 | 0 | 210 | 100% | （无） |  |
| 16 | event-campaigns | ADVANCED | 是 | 0 | 210 | 100% | （无） |  |
| 17 | payment-reconcile-api | ADVANCED | 是 | 0 | 210 | 100% | （无） |  |
| 18 | apparel-shopping-cart | ADVANCED | 否 | 0 | 210 | 100% | （无） | 与 receivable-allocation 同一套技能（重合 0.50） |
| 19 | feature-flag | ADVANCED | 否 | 0 | 210 | 100% | （无） |  |
| 20 | image-transform-pipeline | ADVANCED | 否 | 0 | 210 | 100% | （无） | 与 file-deduplication 同一套技能（重合 0.57） |
| 21 | loan-management | ADVANCED | 否 | 0 | 210 | 100% | （无） | 与 actor-follow-notifications 同一套技能（重合 0.50） |
| 22 | movie-recommendations | ADVANCED | 否 | 0 | 210 | 100% | （无） | 与 return-fraud-risk 同一套技能（重合 0.50） |
| 23 | movie-watchlists | ADVANCED | 否 | 0 | 210 | 100% | （无） |  |
| 24 | payment-form-validation | ADVANCED | 否 | 0 | 210 | 100% | （无） |  |
| 25 | payments-api | ADVANCED | 否 | 0 | 210 | 100% | （无） |  |
| 26 | review-moderation | ADVANCED | 否 | 0 | 210 | 100% | （无） | 与 loan-management 同一套技能（重合 0.60） |
| 27 | sales-reporting | ADVANCED | 否 | 0 | 210 | 100% | （无） |  |
| 28 | shipping-cost | ADVANCED | 否 | 0 | 210 | 100% | （无） | 与 currency-conversion 同一套技能（重合 0.50） |
| 29 | transactions-list | ADVANCED | 否 | 0 | 210 | 100% | （无） | 与 apparel-shopping-cart 同一套技能（重合 0.50） |
| 30 | parcel-return-policy | EXPERT | 是 | 0 | 210 | 100% | （无） | 与 shipping-cost 同一套技能（重合 0.67） |
| 31 | stockroom-inventory | EXPERT | 是 | 0 | 210 | 100% | （无） | 与 movie-watchlists 同一套技能（重合 0.60） |

**切线**：学到第 3 个项目（url-shortener）累计权重 183，达到 87%，首次越过 80%。切线以下的 28 个项目，大部分只是在已覆盖的考点上换业务场景，可以当作练手与复习。

读法提醒：

- 这是按「考点权重」的贪心，不是按难度的课程表。它有一个明显的副作用：一个考点只要碰过一个项目就算全额覆盖，所以三个项目之后几乎所有考点都「覆盖」了。这反映的是考点清单本身很集中（点与点高度重叠），而不是三个项目就够。下面补一张「每个考点至少练两个不同项目」的版本，更接近真实的练习量。
- 5 个免费项目是 rate-limiter、payment-reconcile-api、stockroom-inventory、parcel-return-policy、event-campaigns；它们的排名见上表。
- 项目只给了题面概览。真正的考点权重取决于隐藏测试，上面的歧义列表是推断，不是已验证事实。

### 每个考点练两次的版本

规则：一个考点第一次碰到记一半权重，第二次碰到记另一半（只有 1 个项目有的考点，第一次记全部）。同样贪心，并列时难度低、免费优先。

| 顺序 | 项目 | 难度 | 免费 | 新增权重 | 累计权重 | 累计占比 |
|---|---|---|---|---|---|---|
| 1 | return-fraud-risk | INTERMEDIATE | 否 | 48 | 48 | 23% |
| 2 | actor-follow-notifications | ADVANCED | 否 | 45.5 | 93.5 | 45% |
| 3 | issue-creation-api | EXPERT | 否 | 28 | 121.5 | 58% |
| 4 | password-reset | INTERMEDIATE | 否 | 22.5 | 144 | 69% |
| 5 | url-shortener | ADVANCED | 否 | 21.5 | 165.5 | 79% |
| 6 | parcel-return-policy | EXPERT | 是 | 13.5 | 179 | 85% |
| 7 | file-deduplication | ADVANCED | 否 | 8.5 | 187.5 | 89% |
| 8 | currency-conversion | INTERMEDIATE | 否 | 6 | 193.5 | 92% |
| 9 | sales-reporting | ADVANCED | 否 | 3.5 | 197 | 94% |
| 10 | reservation-service | ADVANCED | 否 | 3 | 200 | 95% |
| 11 | keyword-user-blocklists | ADVANCED | 否 | 2.5 | 202.5 | 96% |
| 12 | tool-call-agent | ADVANCED | 否 | 2.5 | 205 | 98% |
| 13 | rate-limiter | INTERMEDIATE | 是 | 1 | 206 | 98% |
| 14 | receivable-allocation | ADVANCED | 否 | 1 | 207 | 99% |
| 15 | scheduled-banking | ADVANCED | 否 | 1 | 208 | 99% |
| 16 | stack-trace-stream | ADVANCED | 否 | 1 | 209 | 100% |
| 17 | stockroom-inventory | EXPERT | 是 | 1 | 210 | 100% |
| 18 | comments-replies | INTERMEDIATE | 否 | 0 | 210 | 100% |
| 19 | event-campaigns | ADVANCED | 是 | 0 | 210 | 100% |
| 20 | payment-reconcile-api | ADVANCED | 是 | 0 | 210 | 100% |
| 21 | apparel-shopping-cart | ADVANCED | 否 | 0 | 210 | 100% |
| 22 | feature-flag | ADVANCED | 否 | 0 | 210 | 100% |
| 23 | image-transform-pipeline | ADVANCED | 否 | 0 | 210 | 100% |
| 24 | loan-management | ADVANCED | 否 | 0 | 210 | 100% |
| 25 | movie-recommendations | ADVANCED | 否 | 0 | 210 | 100% |
| 26 | movie-watchlists | ADVANCED | 否 | 0 | 210 | 100% |
| 27 | payment-form-validation | ADVANCED | 否 | 0 | 210 | 100% |
| 28 | payments-api | ADVANCED | 否 | 0 | 210 | 100% |
| 29 | review-moderation | ADVANCED | 否 | 0 | 210 | 100% |
| 30 | shipping-cost | ADVANCED | 否 | 0 | 210 | 100% |
| 31 | transactions-list | ADVANCED | 否 | 0 | 210 | 100% |

这个版本在第 6 个项目（parcel-return-policy）越过 80%（累计 179 / 210）。

## About LeetCode Project

能确认的（来自 LeetCode 自己的公开接口，2026-11-16 取得，每个项目页的网址形如 `https://leetcode.com/project/?detail=<slug>`）：

- 列表一次返回 31 个项目（`hasMore: false`），题型字段全部是 `AI_COLLABORATION`。来源：LeetCode 项目列表与详情接口（本机保存于 `sources/local/lc-project/raw/`），2026-11-16。
- 难度分三档：INTERMEDIATE、ADVANCED、EXPERT；估计时间 45、60、75 分钟，`practiceMaxMinutes` 与估计时间相同。同上来源。
- 31 个中只有 5 个免费（rate-limiter、payment-reconcile-api、stockroom-inventory、parcel-return-policy、event-campaigns）。同上来源。
- 每个项目可选运行时相同：Python 3.11、Java 21、C++20、Go、Node.js 24、TypeScript（Node.js 24）。同上来源。这决定了 Python 3.14 才有的标准库新特性（如 `Executor.map(buffersize=)`）在这里用不了。
- 31 个项目的 `interviewFrequency` 都是 0，`companyTags` 都是空：没有任何公司标签或频次统计。同上来源。
- 题面里 reservation-service 与 event-campaigns 明说：这是和编程智能体一起在真实工作区里完成的任务，「怎么拆解、给智能体什么上下文、决定权留在自己手里、验证节奏」本身被评分。reservation-service 还说明给出的材料有：README 里的产品规则、一小套测试、几条脱敏的客服工单与日志，数据库是真实数据且没有重置路径。来源：同上详情接口。
- 官方公告帖《📦 LeetCode Project is here!》（https://leetcode.com/discuss/post/8594774/leetcode-project-is-here-by-leetcode-otcm/）：本次读不到原文（403），只在搜索引擎的摘要里看到大意：从「做题」走向「构建」，与智能体一起处理真实工程挑战；功能包括构建系统、与智能体一起调试、发现盲点、练习来自大公司的项目；公告说邀请有工程经验的开发者参与改进产品。发布日期没有看到。这一条是二手摘要，不是原文。

找不到的（不要当作事实）：

- 评分方式：没有找到任何公开的评分细则、分数构成、是否看对话记录、隐藏测试数量。
- 工作区里的智能体是哪一个（模型、工具权限）、有没有额度或次数限制：没有找到。
- 是否强制计时、超时后会怎样：只有 `practiceMaxMinutes`，未见强制说明。
- 候选人写的体验帖（Reddit、LeetCode Discuss、博客）：搜索没有找到任何一篇讲 LeetCode Project 本身的；搜到的都是别的产品或泛泛的「AI 辅助编码面试」文章。
- 公司是否在真实面试里使用 LeetCode Project：没有找到。

## Not reached

- https://leetcode.com/project 与 https://leetcode.com/discuss/post/8594774/leetcode-project-is-here-by-leetcode-otcm/：WebFetch 返回 403。
- https://leetcode.com/discuss/post/5736503/feature-release-notes-by-leetcode-9awg/：403；只从搜索摘要看到其中有一节「Ask Leet & Coding Agent」（2026.5），不确定与 Project 是否相关。
- Reddit 与其他社区：几次搜索都没有出现与 LeetCode Project 有关的帖子。
- GitHub：`gh api search/repositories` 搜 `leetcode project ai collaboration`、`leetcode.com/project` 没有与该产品相关的仓库（结果是个人刷题仓库）。幂等、放量、限流的仓库有，但多是个人小项目，没有当作来源。`jbruchon/jdupes` 仓库地址返回 404，没有查。
- https://medium.com/…ai-enabled-coding-interview：只在搜索摘要里见到，没有打开，未引用其内容。
- 没有读的官方页：Python `decimal` 文档、SQLite 的 SELECT 与聚合函数页、PostgreSQL 的 `INSERT … ON CONFLICT`、Stripe 的 low-level error 页面。对应叶子在备注里标了。
- RFC 9110 的 HTML 页被截断，改用 RFC 文本版核对 §15.5.4 的措辞；其余条款只核对了章节号。
- 没有打开任何项目的真实工作区、起始代码或测试，上面的「隐藏测试歧义」都是从题面推断的。

