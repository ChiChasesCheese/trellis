# AI 行业与趋势（AI Industry）：读懂这个行业

术语规则：技术术语一律用英文原词，正文用中文（Chi 2026-11-20）

决定：**新建独立领域，不作为 ai-literacy「行业版图」分支的加深。** 理由：（1）那一支 9 个叶子是概念层（四层结构、实验室、芯片、推理经济学各一页），这里需要 40 多个带数字、会过期的叶子，放进去会压垮那个通识领域的节奏；（2）本域内容按季度更新，需要独立的更新与「核对日期」机制，通识层应保持稳定；（3）这里要加的是读数据、读财报、批判地读趋势的方法，不只是知识点。对应的 ai-literacy 叶子保持为入门，本域每个分支开头链回。

读者：资深后端工程师，在 AI 团队或围绕 AI 做决策时要能读懂行业、不被炒作带跑。
所有数字都要在做卡时对原始数据当次核对并记日期。
记号：`*` = 帕累托核心；`(需先: …)` = 真依赖。

## 1. Value chain 与钱怎么流动
- * Value chain 全景：chips → foundry 与 packaging → cloud 与 data center → model labs → applications — 每一层谁收钱、谁付钱、利润在哪里集中
- * 谁赚钱谁烧钱：各层 gross margin 与 cash flow 的差别 — 芯片设计高毛利；云靠折旧与利用率；实验室训练成本巨大；应用层毛利受推理成本挤压
- * Circular financing 与交叉持股的结构 — 芯片商投资实验室、实验室买芯片与云；怎么判断需求是真实终端需求还是循环
- * 怎么读 financial statements：10-K 与 10-Q 的阅读顺序 — 收入分部、剩余履约义务（RPO）、资本开支、折旧年限、客户集中度、风险因素
- * 看 NVIDIA 财报：data center revenue、gross margin、customer concentration — 哪些行是 AI 需求的直接指标 (需先: 怎么读 financial statements)
- * 看 hyperscaler 财报：cloud revenue growth、backlog、capex guidance — 数据中心资本开支与云收入的比值
- Compute 的 unit economics：GPU-hour 成本与 payback period — 购置成本、电力、折旧年限；折旧年限假设对利润的影响
- Valuation 与 bubble 信号：revenue multiple、capex-to-revenue ratio — 与历史上铁路、光纤泡沫的相同与不同

## 2. Chips 与 supply chain
- * GPU 之外的格局：NVIDIA、AMD、Google TPU、Amazon Trainium 与其他 custom silicon — 通用与定制的取舍；各家大客户与份额趋势
- * Software moat：CUDA 与替代路线 — 生态锁定的来源；ROCm、编译器路线能撼动多少
- * HBM（High Bandwidth Memory）：为什么是瓶颈 — 带宽决定解码速度；供应商只有三家、产能与堆叠层数；价格与短缺周期
- * Advanced packaging 与 foundry：CoWoS 与 TSMC — 产能分配决定芯片出货；先进制程集中度
- Interconnect 与 networking：NVLink、Ethernet 与 InfiniBand — 集群规模靠网络；光模块与交换机供应商也是受益者
- * Chip 代际节奏与 depreciation — 新一代带来的性能价格比；旧芯片的残值
- * Export controls 与 geopolitics — 管制的演变、对中国算力的影响、绕行与走私的报道怎么读
- Inference chips 与 accelerator 新进入者 — 晶圆级、片上 SRAM 路线等；它们切入的是哪一段延迟与成本曲线（→ llm-inference:accelerators）

## 3. Compute、power 与 data centers
- * Capex 规模与 guidance：hyperscaler 的数字 — 年度资本开支量级、同比增速、占经营现金流比重（做卡时核对最新财报）
- * Power 是新瓶颈 — 吉瓦（GW）量级的园区、并网排队、变压器与燃气轮机交付周期；为什么电力比芯片更难扩
- * Training compute 的增长趋势（Epoch AI） — 前沿训练算力每年增长倍数、成本、能耗；趋势能延续多久的约束
- Data center 的建设周期与 financing — 租赁、表外融资、私募信贷；融资结构的脆弱点
- 水、土地与 local opposition — 社区反对与审批对进度的影响
- Cooling 与能效：liquid cooling、PUE — 机架功率密度上升带来的工程变化
- 能源路线：nuclear、natural gas、renewables 与 grid — 各自的交付时间与成本
- Data wall 与 synthetic data：数据会不会用完 — 公开文本存量的估计、多模态与合成数据的补充

## 4. Model labs 与 business models
- * Frontier labs 的格局与竞争轴 — 能力、价格、生态、分发；领先者轮换得有多快（用榜单排名间隔数据说话）
- * Business model 分类：subscription、usage-based API、enterprise、ads 与 revenue share — 各类收入占比、客户获取与留存
- * Inference 的 gross margin 与 price decline — 同等能力的单价下降速度（斯坦福 AI Index：GPT-3.5 级别 2022 年 11 月至 2024 年 10 月降低 280 倍以上）；降价与用量增长的相互抵消
- * Application layer 的利润被谁吃掉 — 模型供应商提价或自己做应用的风险；编程工具的毛利压力
- * Open weights vs closed：差距、动机与商业逻辑 — 差距缩小的数据（AI Index：部分基准上 8% 缩至 1.7%）；开放的企业为什么开放；对价格的压制
- * Lab revenue 与 valuation 的数据来源与读法 — 年化收入口径、融资轮次、传闻与官方披露的区别
- * Enterprise adoption 的真实状况：pilots 多、scale 少 — 采用率、投资回报的调查证据；调查的口径与偏差
- Platform 与 distribution：谁拥有用户入口 — 搜索、操作系统、办公套件与聊天入口的竞争
- Agents 与「AI-native」公司的 economics — 按结果收费、按席位收费的转变；毛利与规模化
- Open-source 生态的经济：Hugging Face、model licenses — 许可证类型、商用限制、衍生模型

## 5. 中国生态
- * 中国 model labs 与 open-weights 路线 — 主要玩家、发布节奏、与美国前沿的差距（AI Index：主要基准上接近持平）
- * Compute constraints 下的工程取舍 — 出口管制、国产芯片、效率型架构与训练技巧；成本曲线为什么更陡
- 应用与监管环境 — 备案、内容规则、应用落地的主要场景
- 国产 chips 与 supply chain — 昇腾等；制程、HBM 与封装的短板
- Price war 与 open-source 策略 — 低价、免费策略与海外采用
- 对比：中美投资规模与 R&D 产出 — 私人投资数额差距（AI Index 2025：美国约 1091 亿美元对中国约 93 亿美元）与不同资本结构的解读

## 6. Labor market 与岗位
- * Job exposure 怎么测：task decomposition 与 usage data — Anthropic 经济指数与类似研究；自动化与增强的占比及其随时间的摆动
- * 已有的就业证据：entry-level 岗位与年轻员工的变化 — 实证研究的结论、方法（差分比较）与局限；因果还是巧合
- * 会增长的岗位族与会收缩的岗位族 — 客服、初级编码、翻译、内容类任务受冲击较早；AI 基础设施、数据中心建设、安全与评测需求增长
- * Software engineering 岗位的变化 — 招聘需求、层级结构、技能要求；与 ai-dev 角色转变一叶联动
- Skills 与 wage premium — 带 AI 技能岗位的薪酬数据与来源可靠性
- Productivity 宏观数据：为什么还看不见 — 历史上电力与计算机的滞后；统计口径
- 教育与技能培养 — 学生与新人路径；证据有限处明说
- 地区与行业差异 — 不同国家的采用与暴露度

## 7. 批判地读趋势与炒作
- * 读 leaderboard 与 benchmark 的方法：saturation、contamination、gaming — 新基准几个月到顶；怎么看趋势而不是看名次
- * 读融资新闻与 ARR（annualized revenue） — 口径、一次性与可重复收入、烧钱率
- * 预测的记分：State of AI 的上年预测自评 — 命中、部分命中、落空的比例；用来校准对预测的信任
- * 识别 primary 与 secondary 数据 — 官方报告、财报、数据库对媒体转述；每个数字追到源头
- * 读大型趋势报告：AI Index、State of AI、Meeker 的立场与盲区 — 学术、从业者、风险投资三种视角的偏向
- Capability curve 与 extrapolation 的陷阱 — 指数、S 曲线、天花板；任务时长类指标的含义与局限
- Vendor blog 与 research paper 的利益相关 — 自家评测、挑选对比对象
- 恐慌与狂热新闻的拆解方法 — 先问样本、条件、基线、谁受益
- 做自己的行业 dashboard：该盯的十个指标 — 资本开支指引、GPU 租价、token 单价、收入年化、电力并网、基准前沿、开源差距、招聘数据等

## 8. Governance 与 industrial policy
- * 美国、欧盟、中国的 regulation 路线差异 — 欧盟 AI 法案的分级、美国行政令与州法、中国备案制
- 数据 copyright 诉讼与 licensing deal — 主要案件的走向与对数据成本的影响
- Sovereign AI 与各国 industrial policy 投资 — 各国资金承诺与实际落地的差距
- Safety incidents 与行业 self-regulation — 事故报告、前沿安全框架、预警机制（对应 ai-literacy:safety.governance，只讲对产业的影响）

## 不收（out of scope）
- 模型原理、训练方法 — llm-inference 与 ai-literacy:models
- 如何搭建 LLM 应用 — ai-eng
- 个股推荐、投资建议与价格预测 — 不是技术学习目标，且易过期
- 通用人工智能时间表与存在性风险辩论 — ai-literacy:industry.agi-debate 已覆盖；这里只讲如何读这类预测
- 加密货币与非 AI 半导体周期 — 无关
- 单个产品的功能比较 — 变化太快

## 与已有领域的重叠
| 已有叶子 | 处理 | 说明 |
|---|---|---|
| ai-literacy:industry.stack | 链接 + 更深 | 四层图作入口；本域加每层的利润与现金流结构 |
| ai-literacy:industry.labs / industry.timeline | 跳过 | 名录与时间线在通识领域；这里只讲竞争格局与数据读法 |
| ai-literacy:industry.open-china | 更深 | 拆成开放对闭源的经济学与中国生态两支，加数据与约束 |
| ai-literacy:industry.products | 更深 | 加收入占比、留存、毛利、智能体定价 |
| ai-literacy:industry.chips | 更深 | 加 HBM、封装、互联、定制芯片、折旧与出口管制 |
| ai-literacy:industry.inference-economics | 更深 | 加价格下降与用量抵消、GPU 小时单位经济、读财报 |
| ai-literacy:industry.datacenters | 更深 | 加电力、融资、本地反对、能源路线 |
| ai-literacy:industry.agi-debate | 链接 | 只保留「怎么批判地读」 |
| ai-literacy:work.reading-news / work.sde-impact | 链接 + 更深 | 通识层给判断清单；本域给方法与数据源，岗位变化加经济指数与就业实证 |
| ai-literacy:safety.governance / safety.data-rights | 链接 | 本域只讲产业影响 |
| llm-inference:accelerators.* | 链接 | 芯片技术细节在那边；这里只讲产业含义 |
| ml-system-design:llm-platform.multi-region-capacity | 链接 | 容量规划的设计题与产业层的算力约束互相引用 |

## 卡片格式建议
- **自包含（Chi 2026-11-21）：** 卡里出现的每个术语，要么在更靠前的叶子里教过（按卡组顺序），要么在这张卡里用一句话定义；靠前的叶子按教科书写，不默认读者有背景。
- 每张卡一个可核对的数字加来源与年份（「AI Index 2025：……」），并写明口径；卡上标「核对日期」，过期要刷新。
- 结构卡用表格：层级 × 谁收钱 × 毛利 × 主要风险；对比卡列开放对闭源、美国对中国。
- 方法卡教读法：给一页财报或一条新闻，列出该看的行与该问的三个问题，不只给结论。
- 至少 25% 带图：价值链资金流向图、资本开支与收入的趋势示意、芯片供应链瓶颈图。
- 不写价格预测与买卖建议；预测类内容写成「谁在预测、依据、历史命中率」。
