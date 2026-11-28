---
id: qi-execution-microstructure-fragmentation-5
node: execution.microstructure.fragmentation
type: cloze
anki: 1787523288231
---
美股在十几家明面交易所之外还分散在多个暗池里交易，因此存在两套基础设施，让参与者能获得一个统一的市场视图。{{c1::综合行情带（consolidated tape / SIP）}}把每一家交易所的报价和成交汇总成一份官方的 NBBO 数据流，但构建和传输这份汇总数据需要真实的处理和网络时间，这使它{{c2::比每家交易所自己的直连行情（direct feed）更慢}}，差距历史上大致在个位数到十位数毫秒之间。{{c3::直连行情（direct feed）}}是每家交易所直接从自己的撮合引擎卖出的专有行情数据，让订阅者能以比综合视图更低的延迟看到该交易所的盘口。Regulation NMS 的{{c4::委托保护规则（order protection rule）}}要求交易场所不得以劣于另一交易所显示的**受保护报价（protected quote）**的价格成交——但由于这条规则是依据交易所自己（快速、由直连行情驱动）看到的其他交易所报价来执行的，而不是依据一个只用 SIP 的参与者当下看到的报价，所以一个依赖较慢的综合行情带的参与者，仍然可能把单子路由到一个{{c5::到委托实际到达时已经不复存在}}的价格上。
