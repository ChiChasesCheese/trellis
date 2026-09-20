---
nodes: [problems.marketplaces.bank-account]
url: https://github.com/kumaransg/LLD/tree/main/ledger_company_navi
tags: [no-archive]
---
# LLD / ledger_company_navi

值得读：kumaransg/LLD 仓库里对 Navi（印度金融科技公司）一道分级机考题的公开复现，
展示了"开户/存款/转账 → 排行 → 定时支付 → 合并"这一整条分关节奏的真实样例。它的账本
是每个账户一个可变余额字段加一份单独维护的交易列表，排行和历史查询需要另写遍历逻辑；
本文把余额、排行、历史时点查询统一成对同一份只增不减的事件日志的不同归约，没有可变的
余额字段，合并账户因此不需要搬迁任何历史数据。
