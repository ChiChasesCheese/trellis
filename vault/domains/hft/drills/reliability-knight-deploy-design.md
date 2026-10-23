---
nodes: [reliability.knight-capital, reliability.kill-switch, reliability.deploy-testing, reliability.monitoring]
tags: [drill]
---
# 练习：明天开盘前要部署 8 台服务器，怎样保证漏装一台也亏不起

明早开盘前，你要把新版交易软件部署到 8 台服务器。主管问：如果有 1 台漏装，会发生什么？你怎么保证损失被止住？一次真实事故里，正是 8 台漏装 1 台，旧代码被一个复用的旧标志位唤醒，约 45 分钟亏了约 4.4 亿美元。

**要你给出的**
- 算这次事故平均每秒亏多少；如果靠人工 5 分钟后才反应，会多亏多少。
- 给部署流程写 5 条规矩，每条对应一个具体失误。
- 设计自动熔断开关（kill switch）：选 3 个触发指标，说明"预警"和"硬停"两档怎么分工，触发后系统做哪几件事，为什么不自动恢复。
- 回答：熔断既怕误触发又怕漏触发，怎样降低两类错误的代价；为什么控制本身必须独立于出问题的代码。

**评分要点**
- 事故经过：手工部署漏装 1 台，新代码复用的旧标志位在旧服务器上唤醒了早已停用的测试功能，开盘后疯狂买高卖低，涉及上百只股票 ([[hft-reliability-knight-capital-what-happened]])
- 速度：4.4 亿 ÷ 2700 秒 ≈ 16 万美元每秒；人工 5 分钟 = 300 秒，约再亏 4900 万美元。人的反应以分钟计、亏损按秒累积，所以保护必须自动 ([[hft-reliability-knight-capital-speed-of-loss]])
- 具体失误和对应规矩：手工部署没有校验（自动化并逐台校验）；复用旧标志位加保留死代码（不复用标志位、删除废弃代码）；告警邮件没人当紧急事件（每条告警有负责人和手册）；处置失误把新版本从另外 7 台撤掉反而激活旧代码（回滚演练过）；没有一键停止 ([[hft-reliability-knight-capital-root-causes]])
- 版本和配置要绑成一个发布包一起发布、一起回滚，配置变更双人复核，校验每台服务器上的版本或校验和 ([[hft-reliability-deploy-testing-version-and-config-together]])
- 硬指标（持仓、订单速率、亏损超限）自动熔断，偏离但不确定的（延迟略升、偶发丢包）告警给值班人员；告警每条都要可执行，否则只是噪音 ([[hft-reliability-monitoring-alert-vs-auto-stop]], [[hft-reliability-monitoring-what-to-monitor]])
- 熔断触发后：撤销所有未成交订单、禁止发新单、继续收行情和回报以便查原因和平仓、恢复需人工确认；热路径每单只读一个标志位 ([[hft-reliability-kill-switch-what-it-does]])
- 误触发（白白停止赚钱）和漏触发（损失累积）：错单的代价远大于停摆，宁可倾向触发；分级熔断缩小影响范围，每个指标设预警与硬停两档，定期演练真的按一次开关 ([[hft-reliability-kill-switch-false-trigger-tradeoff]])
- 控制要独立于出问题的代码：进程内闸门、独立风控进程、交易所侧限额与断线撤单，再加 drop copy 独立核对持仓；新版本还要先灰度一个品种、小限额 ([[hft-reliability-knight-capital-would-controls-have-helped]], [[hft-reliability-kill-switch-drop-copy]], [[hft-reliability-deploy-testing-canary-by-symbol]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
