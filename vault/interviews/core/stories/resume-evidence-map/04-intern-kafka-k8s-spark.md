# 学习画像 04 — Spring / Kafka / Kubernetes / Spark（事件驱动清结算 + 计费）

> **用途**：学习画像,不是简历审计。这一份把 Chi 简历里 intern 三条 bullet(Kotlin/Spring B2B 计费+compliance report、Kafka message queue + Kafka proxies in K8s、Airflow DAG 调度 Spark 做 verification/settlement/chargeback/audit)对应的**整套技术栈**讲透——从 Chi 已经碰过的 baseline,到 Braintree 生态里这些技术**最精华的实现**,让 Chi 知道往哪看齐、学到能自己讲透的程度。
> **覆盖范围**:Spring Boot(Kotlin)服务结构 + JPA、Kafka(producer/consumer/Connect sink/CDC)、Kubernetes(Deployment/水平扩展/probe/proxy)、Spark/Airflow 批处理校验。

---

## 1. 主题定位:一笔交易怎么变成一条"费用",整条事件流

Braintree 的清结算/计费生态是**事件驱动**的。把一笔 transaction 从产生到费用落库看成一条传送带:

```
Gateway 结算一笔交易
   │  往 Kafka 打 protobuf transaction event
   ▼
topic: events_entity_transaction_global   (旧版 eventstream_global)
   │
   ├──────────────► Pricing 服务(Kotlin + Spring Kafka)
   │                  @KafkaListener 批量消费 → 查 merchant_account
   │                  → 落 Transaction 表(幂等去重)→ 算 BT fee
   │                  → 再往 Kafka 发一条 fee event
   │                       topic: pricing_bt_fee_events_global
   │                       (被 Funding 订阅,partner 出款用)
   │
   └──────────────► Snowglobe(Chi 的地盘)
                      Kafka Connect **sink** connector
                      + Snowpipe Streaming
                      → 实时落进 Snowflake 表
                      → 下游 SQL 做对账 / fee 计算 / 质检 / settlement

旁路:Funding MySQL 的 CDC 变更流(datastream_funding_global)
      也经 Kafka Connect sink 落进 Snowflake,给 Snowglobe 当参照数据
```

各角色一句话:

- **Kafka = 系统间的异步消息总线**。transaction event、fee event、CDC 变更、disputes 全是 topic。生产者/消费者解耦,可削峰、可回放、at-least-once 投递。
- **Spring 服务(Pricing)= 事件的处理者**。它既是 transaction event 的 **consumer**,又是 fee event 的 **producer**——Kafka 在这里就是"交易进来 → 算费 → 费用出去"的传送带。
- **Kafka Connect = 零代码的搬运框架**。sink connector 订阅 topic,每条消息过一个 `Converter` 反序列化、可选 `Transform` 过滤,再写进 Snowflake。Chi 的 Snowglobe 靠它把十几个 topic + CDC 流实时同步进数据仓。
- **Kubernetes = 所有这些消费者/connector 的运行平台**。每个 consumer / 每个 connector = 一个 `Deployment`,靠 `replicas` 做水平扩展(多 pod = 一个 consumer group 里多个成员并行分 partition),pod 挂了 K8s 自动重建 = "distributed node operations and stability"。
- **Spark / Airflow = 事件流之外的批处理校验层**。EOD(每日收尾)跑 Spark job 校验 pricing schedule 的创建来源是否合规、settlement/audit 数据是否对得上,结果告警到 Slack。

**记住一个关键分界**:实时链路(Kafka + Connect,秒级)负责"把数据搬进来、算出来";批处理链路(Spark + Airflow,天级)负责"事后校验搬进来的数据对不对"。这两层合起来才是完整的清结算准确性保障。

---

## 2. Baseline — Chi 已有实现(自信陈述)

### 2.1 REST Log Module —— Kotlin / Spring Boot / JPA 审计日志(pricing repo)
Chi 在 pricing 服务里从零建了一个 **compliance-flow 的请求/响应审计日志模块**:给 pricing schedule 的 compliance 相关 API(Get/Create/Delete/Validate)做端到端请求/响应入库,可追溯每一次调用。

- **技术栈**:Kotlin + Spring Boot + JPA/Hibernate + `CriteriaBuilder`(动态查询)+ Thymeleaf(日志浏览 UI)。
- **Entity** `PricingScheduleEventRestLog` → 表 `pricing_schedule_event_rest_log`:字段含 `merchant_account_unique_id`、`pp_debug_id`(PayPal Debug-ID,default `"NotAvailable"`)、`method`、`request_uri`、`request_body`、`response_code`、`exception_message`、`response_body`、`created_at`;索引在 merchant id + debug id 上。
- **拦截层**:`HttpServletRequestFilter`(用自定义 RequestWrapper 抓 request body、安全截断大 body)在请求阶段建日志,`HttpServletResponseFilter` 在响应阶段回填 response code/body。
- **查询层**:`PricingScheduleEventRestLogService.getAllLogsFiltered(...)` → `JpaSpecificationExecutor` + `CriteriaBuilder` 动态拼过滤条件(URI/异常部分匹配、response code 区间、带时区的时间窗),带分页 `Page`/`PageRequest`。文档里明确写了从"硬编码 `@Query` 注解"重构成动态 CriteriaBuilder。
- **前端**:Thymeleaf 表格,分页 + 全局搜索 + 列过滤 + UTC→本地时区转换 + 请求/响应体展开/复制,navbar 加 "Pricing Flows" 入口。
- **锚点**:Confluence 966206164(Chi 亲笔);PR pricing #2306/#2339/#2402;源码 `pricing/src/main/kotlin/com/braintree/pricing/{common/data/PricingScheduleEventRestLog.kt, api/PricingScheduleEventRestLogService.kt, controllers/PricingScheduleEventRestLogController.kt}`。

### 2.2 Spark Validators —— Java Spark EOD 合规校验器
Chi 建了 3 个 Java Spark validator,挂进 **EodValidator Job**,每日/每周校验 merchant pricing schedule 的创建来源是否合规,查 BigQuery、告警到 Slack `#treasury-pricing_app`:

1. **PartnerPricingScheduleValidator**(DTBTPRWIZ-39):抓 partner 里经 TRINITY/SALESFORCE 创建的 pricing schedule(合规要求应走 FundingUI/DefaultPricing,避免重复 PS),输出 Created_By/Created_Via/Merchant_Account_Unique_ID/Effective_Date。
2. **UsePricingAppFlippedBackValidator**(DTBTPRWIZ-53):每周查最近 7 天 `use_pricing_app_fees` 从 True 翻回 False 的 merchant(翻回会导致错误计费),翻回即告警。
3. **PriceUpdateCreatedViaValidator**(DTBTPRWIZ-54):US/EU 非 partner merchant 的 PS 不应经已弃用的 FundingUI 创建,监控漏网的。

- **锚点**:Confluence 966731781(Chi 亲笔);DTBTPRWIZ-39/53/54;repo `BigDataInfraEng/pricing-spark` PR #42/#44/#45。数据源 BigQuery 表 `pypl-edl.braintree_raw_views.funding_pricing_schedules`;pricing 团队用 Airflow + EMR 调度这些 Spark job(`pricing/oncall/AirflowDagLogs.md`)。

### 2.3 Kafka CDC 白名单扩展 —— fee-validation 的实时数据管线(DTBTTFOUND-2355,FT 期)
Chi 给 **Snowglobe-shadowed 商户的 pricing-schedule fee validation** 扩展了 Kafka Connect 的 CDC → Snowflake 摄取管线:在 CDC sink connector 的表级过滤白名单里放行 4 张 Funding 源表,让它们的实时镜像流进 Snowflake 供校验 SQL 消费。

- **改动**(`kafka-snowflake-connector/docker/connector/cdc/funding.properties`):往 `Filter$Value` transform 的 JSONPath 白名单加 4 张表:
  ```
  || @.table == 'merchant_accounts'
  || @.table == 'processor_settings'
  || @.table == 'pricing_schedules'
  || @.table == 'pricing_schedule_fees'
  ```
- **理解链条**(面试要能完整讲):要校验 shadowed 商户的费用配置,得先在 Snowflake 里有 Funding 侧的商户主档(`merchant_accounts`)、处理器配置(`processor_settings`)、定价档(`pricing_schedules`)、定价档费项(`pricing_schedule_fees`)的**实时镜像**;Chi 做的就是把这 4 张表接进 CDC(change-data-capture)→ Snowpipe Streaming → Snowflake。要懂 CDC envelope 长什么样(`@.table`/`@.kind`)、为什么 `@.kind != 'delete'`(只要 upsert 不要删除事件)、落进 `datastream_funding_global` 后下游怎么建 fee-validation 表。
- **锚点**:commit `ceb0f8b`(2025-08-07)、`2084d66`(2025-08-11),Jira DTBTTFOUND-2355。这是配置层的管线扩展,归属 Chi 的 fee/settlement 领域。

**这三块合起来正好横跨本主题四大技术**:Spring/JPA(REST Log)、Spark/Airflow(Validators)、Kafka Connect/CDC(2355)。下面是往上看齐的部分。

---

## 3. ★ 往哪里看齐 —— repo 最精华实现(重点)

这一节是学习的核心。从 pricing / kafka-snowflake-connector / event_protos 三个 repo 里挑出 **8 个最值得学的实现**,每个说清:精华在哪、为什么算 Sr 级、路径 + 锚点、学到什么程度。

---

### ★1. Kafka Connect sink 的 Converter 层设计(protobuf → JSON → schematize)
**路径**:`kafka-snowflake-connector/src/main/java/com/braintreepayments/ProtobufConverter.java`(基类)+ `TransactionStatusChangeEventProtobufConverter.java`(具体实现)+ 17 个同族 converter。

**精华在哪**:一个干净的模板方法(template-method)基类,把所有 protobuf→JSON 的通用逻辑收进 `ProtobufConverter`,子类只写"解析哪个 message"这一件事。基类的 `getJson()` 用 `JsonFormat.printer()` 配了四个关键选项——`preservingProtoFieldNames()`(保留 proto 原字段名,让 Snowflake 列名和 proto 对齐)、`includingDefaultValueFields()`(默认值字段也输出,避免 schema 缺列)、`omittingInsignificantWhitespace()`(压缩体积)。子类只有十几行:
```java
final TransactionEvent message = TransactionEvent.parseFrom(value);
if (message.hasStatusChange()) {
    return converter.toConnectData(topic, getJson(message.getStatusChange()).getBytes());
} else {
    return SchemaAndValue.NULL;   // 不是我关心的 message 类型 → 交给下游 tombstone handler 丢弃
}
```

**为什么 Sr 级**:
- **一条脏消息不能毒死整个 task**:catch `InvalidProtocolBufferException` → log severe → 返回 `SchemaAndValue.NULL`,而不是抛异常让 connector task 挂掉。这是流式管线的命门——poison message 隔离。
- **oneof 分派**:`TransactionEvent` 是一个 `oneof`(status_change / refund_created / installment_change...共 8 种),converter 只挑自己 topic 需要的那一种,其余返回 NULL。这是"一个大 proto、多个 topic 各取所需"的干净解法。
- **schematization 配合**:converter 只负责转成 JSON,`snowflake.enable.schematization=TRUE` 让 Snowflake 自动把 JSON 字段展开成列。converter 保留字段名 → 列名可预测。

**学到什么程度**:能画出 "bytes → parseFrom → oneof 分派 → JsonFormat 打印 → JsonConverter → schematize 落列" 的完整链条,能解释每个 `JsonFormat` 选项为什么这么设、坏消息为什么返回 NULL 而不是抛错。看那个 12.8K 的 `PricingScheduleEventProtobufConverter.java`(最复杂的一个)理解嵌套结构怎么摊平。

---

### ★2. sink connector 的配置模式(Snowpipe Streaming + buffer 权衡)
**路径**:`kafka-snowflake-connector/docker/connector/eventstream_v2.properties`(典型 sink);同目录 17+ 个 `.properties`。

**精华在哪**:一套所有 sink 共享的配置骨架,把"延迟 vs 吞吐 vs 成本"的权衡全摆在 properties 里:
```
connector.class=com.snowflake.kafka.connector.SnowflakeSinkConnector
tasks.max=4                                  # 一个 connector 拆成最多 4 个 task 并行
topics=events_entity_transaction_global
snowflake.topic2table.map=events_entity_transaction_global:eventstream_transaction_status_events
snowflake.ingestion.method=SNOWPIPE_STREAMING   # 低延迟流式,不是批 COPY
buffer.count.records=100000                   # 攒够 10 万条
buffer.flush.time=60                          # 或攒够 60 秒,先到先 flush
value.converter=com.braintreepayments.TransactionStatusChangeEventProtobufConverter
transforms=tombstoneHandler                   # 丢弃 null value 的墓碑消息
snowflake.enable.schematization=TRUE          # JSON 字段自动展开成列
enable.streaming.client.optimization=TRUE
```

**为什么 Sr 级**:`buffer.count.records` × `buffer.flush.time` 是延迟和吞吐的旋钮——攒批大 = 吞吐高、延迟大、Snowflake 调用次数少(省钱);攒批小 = 实时性好但更贵。`tasks.max=4` 决定并行度上限。`topic2table.map` 让"两个 topic 落同一张表"成为可能(见 CDC 那条)。理解 Snowpipe Streaming 和传统 Snowpipe(文件批量 COPY)的区别:前者是行级流式 API,秒级可见;后者是攒文件再 COPY,分钟级。

**学到什么程度**:给你一个新 topic 要落 Snowflake,你能独立写出一份 sink properties,并解释每个 buffer/tasks 参数怎么定、为什么选 Snowpipe Streaming。

---

### ★3. CDC 表级过滤 transform(Chi 的 2355 就长在这上面)
**路径**:`kafka-snowflake-connector/docker/connector/cdc/funding.properties`。

**精华在哪**:用 Confluent 的 `Filter$Value` transform + JSONPath 条件,在 sink 侧做**声明式白名单**,只放行需要的表、只要 upsert 不要 delete:
```
transforms=filterCdcTables
transforms.filterCdcTables.type=io.confluent.connect.transforms.Filter$Value
transforms.filterCdcTables.filter.condition=$[?( (@.table=='gateway_transactions' \
  || @.table=='merchant_accounts' || @.table=='pricing_schedules' \
  || @.table=='pricing_schedule_fees' || ... ) && @.kind != 'delete')]
transforms.filterCdcTables.filter.type=include
transforms.filterCdcTables.missing.or.null.behavior=exclude
snowflake.topic2table.map=datastream_funding_global:datastream_funding_global,ds_funding_cdc_legacy_global:datastream_funding_global
```

**为什么 Sr 级**:CDC(Debezium 风格)envelope 是 `{table, kind, before, after}`;上游把 Funding MySQL 一整库的变更全打进一个 topic,下游用 SMT(Single Message Transform)在 connector 里过滤,**不需要写一行代码**。`@.kind != 'delete'` 是业务判断——对账/校验只关心记录的当前状态,不想被删除事件扰动。两个 topic(新流 + legacy)用 `topic2table.map` 映到同一张 Snowflake 表,做无缝迁移。`missing.or.null.behavior=exclude` 防止字段缺失时误放行。

**学到什么程度**:能解释 CDC 是什么、envelope 结构、为什么在 sink 侧用 SMT 过滤而不是在源头或下游 SQL 过滤(答:省 Snowflake 摄取量和存储成本、下游拿到的就是干净数据)。这正是 Chi 2355 改动的上下文——学透它 = 把自己那 4 行改动讲成有深度的架构理解。

---

### ★4. K8s Deployment manifest — 一份模板生成 20+ connector 部署(replicas × tasks 的并行度模型)
**路径**:`kafka-snowflake-connector/kubernetes/application.yaml.erb`。

**精华在哪**:一个 ERB 模板,用一个 `connector_configs` 数组(每个元素是一个 connector 的规格)循环生成 20+ 个 `apps/v1 Deployment`。每个 connector 独立部署、独立 replicas、独立 Snowflake role/warehouse。关键片段:
```yaml
spec:
  replicas: <%= connector_config.fetch(:replicas) %>   # eventstream=4, disputes=2, cdc=4...
  template:
    spec:
      containers:
      - name: kafka-connect
        livenessProbe:
          exec: { command: ["/liveness.sh"] }          # 挂了自动重启
          failureThreshold: 2
          periodSeconds: 30
        lifecycle:
          preStop:
            exec: { command: ["/bin/sleep", "2"] }      # 优雅下线,让 in-flight 消息 commit
        resources:
          requests: { cpu: "4000m", memory: "8724Mi" }  # eventstream 单 pod 4 核 8.7Gi
        volumeMounts:
          - { name: secrets-vault, mountPath: "/etc/secrets-vault", readOnly: true }  # 凭据走 vault
```

**为什么 Sr 级**——理解**两级并行度**是关键:
- **replicas**(K8s 层):起 N 个 pod,进同一个 consumer group,Kafka 把 partition 分给它们(rebalance)。加 replica = 加吞吐 + 加冗余。
- **tasks.max=4**(Connect 层):Connect 把一个 connector 拆成最多 4 个 task 分到 worker 上,按 topic partition 并行。
- **真实并行度 = replicas × tasks,上限被 topic partition 数卡住**(partition 是并行消费的最小单位——10 个 partition 最多 10 个消费者并行,再多的消费者只能空等)。
- **稳定性三件套**:`livenessProbe`(pod hang 住 → 重启)、`preStop sleep`(优雅下线,不丢/不重放 in-flight)、consumer group rebalance(pod 挂了它的 partition 自动让给活的成员)。这就是简历那句 "distributed node operations and stability" 的真实底座。
- 每个 connector 用独立 Snowflake role(最小权限)、独立 warehouse(计算隔离/成本归因)、vault 挂密钥。这是生产级多租户隔离。

**学到什么程度**:能对着这份 manifest 讲清 replicas / tasks.max / partition 三者关系,能解释 liveness probe 和 preStop 各防什么故障,能说出"为什么每个 connector 独立 Deployment 而不是塞一个大 pod"(隔离故障域、独立扩缩、独立权限)。

---

### ★5. @KafkaListener 批量消费者 + 幂等计费(计费准确性的命门)
**路径**:`pricing/src/main/kotlin/com/braintree/pricing/events/transactions/TransactionEventConsumer.kt`。

**精华在哪**:Spring Kafka 的批量消费者,处理"transaction event → 算 fee → 发 fee event"的核心,防重复计费的手法极干净:
```kotlin
@KafkaListener(topics = ["\${pricing.kafka.transaction-events.topic}"],
               containerFactory = TRANSACTION_EVENTS_KAFKA_LISTENER_CONTAINER_FACTORY)
fun consume(messages: List<ConsumerRecord<String, String>>) {
    for (message in messages) {
        try { processRecord(message.value()) }
        catch (e: Exception) { throw BatchListenerFailedException(e.message ?: "", message) }  // 精确指向失败那条
    }
}

private fun save(transactions: List<Transaction>) {
    transactions.chunked(BATCH_SIZE).forEach { batch ->
        try {
            val existingIds = transactionRepository.findExistingTransactionIdsInBatches(batch.map { it.publicId })
            transactionRepository.saveAll(batch.filter { it.publicId !in existingIds })   // 先查后存,批量去重
        } catch (e: DataIntegrityViolationException) {
            batch.forEach { try { transactionRepository.save(it) }                          // 兜底:逐条存
                            catch (e: DataIntegrityViolationException) { /* 重复,skip */ } }  // DB 唯一约束兜住并发
        }
    }
}
```

**为什么 Sr 级**——这就是 "**Kafka 是 at-least-once,消费侧必须幂等**" 的教科书实现:
- Kafka 默认 at-least-once:commit offset 前崩溃会**重投**同一条消息。计费系统若不防重就**重复计费**。
- 三层防线:(1) 落库前 `findExistingTransactionIdsInBatches` 批量去重;(2) DB 唯一约束 + catch `DataIntegrityViolationException` 兜住并发插入;(3) `BatchListenerFailedException` 让 Spring 精确重投失败那一条,而不是整批重放。**at-least-once 传输 + 幂等消费 ≈ effectively-once 效果**——面试问"怎么保证费用不多算/不少算",答这个。
- 算完 fee 后 `btFeeProducer.publish(feeEventArray)` 再发一条 fee event 到 `pricing_bt_fee_events_global`——**consumer 同时是 producer**,这就是事件流的接力。
- 全程打 metric(`registry.counter` 带 received/saved/skipped/published tag),可观测性内建。

**学到什么程度**:能讲清 at-least-once 为什么导致重复、幂等消费的三种做法(去重查询 / 唯一约束 / 幂等键),能解释 `BatchListenerFailedException` 相比整批重放的好处。这是本主题**面试最高频**的点。

---

### ★6. Spring Kafka 的 ContainerFactory + 错误处理 / 重试 / DLQ 策略
**路径**:`pricing/src/main/kotlin/com/braintree/pricing/events/config/KafkaConsumerConfiguration.kt`。

**精华在哪**:一个可复用的 `getKafkaListenerContainerFactory(...)` 工厂,把消费者的横切关注点集中配置:
```kotlin
factory.setConcurrency(concurrency)      // 单 pod 内起多个 listener 线程(pod 内并行)
factory.setAutoStartup(false)            // 手动控制启动时机
val errorHandler = DefaultErrorHandler({ record, ex -> messageErrorHandler(...) },
                                        FixedBackOff(5000L, 2L))   // 失败重试 2 次,间隔 5s
// 不可重试的异常:直接进 errorHandler,不浪费重试
notRetryableExceptions = [DataIntegrityViolationException, IllegalStateException, InvalidProtocolBufferException]
```
配合 `ErrorHandlingDeserializer`——反序列化失败不让整个消费者崩,包成可处理的错误记录。

**为什么 Sr 级**:
- **两级并行**:`concurrency`(单 pod 内 listener 线程数)× K8s `replicas`(pod 数)= 总消费并行度,同样受 partition 数上限约束。
- **重试策略要区分异常类型**:`DataIntegrityViolationException`(重复数据)、`InvalidProtocolBufferException`(脏消息)重试没意义 → 列入 not-retryable 直接走错误处理;瞬时故障(网络/DB 抖动)才 backoff 重试。盲目重试脏消息 = 无限循环卡死消费。
- `KafkaMessageLog` 把处理失败的消息记进 DB(轻量 DLQ)——可事后重放。

**学到什么程度**:能解释 concurrency vs replicas vs partition 三层的关系,能说清"哪些异常该重试、哪些不该"以及为什么,理解 DLQ / 死信队列的作用。

---

### ★7. "Kafka proxy within Kubernetes" 的真实机制(SASL SCRAM + TLS)
**路径**:`pricing/kafka-proxy-pod.sh`(grepplabs kafka-proxy)+ `pricing/kafka-proxy-cpair.sh`(kubectl port-forward)。

**精华在哪**:简历那句 "Kafka proxies within Kubernetes" 对应的真实东西——一个跑在 K8s pod 里、放在 Kafka broker 集群前面的**认证代理**:
```bash
kafka-proxy server \
  --bootstrap-server-mapping "${KAFKA_HOSTS[0]},0.0.0.0:32500" \   # 3 个 broker 各映一个本地端口
  --bootstrap-server-mapping "${KAFKA_HOSTS[1]},0.0.0.0:32501" \
  --bootstrap-server-mapping "${KAFKA_HOSTS[2]},0.0.0.0:32502" \
  --sasl-enable --sasl-method "SCRAM-SHA-512" \                    # SASL SCRAM 认证
  --sasl-username "$(...jq .username)" --sasl-password "$(...jq .password)" \
  --tls-enable \                                                    # 双向 TLS
  --tls-client-cert-file "..." --tls-client-key-file "..."
```
开发/测试时用 `kubectl port-forward` 把本机连到这个 pod,就能安全地连到生产 Kafka 集群。

**为什么 Sr 级**:理解 Kafka 的认证栈——**SASL/SCRAM**(用户名/密码质询-响应,不明文传密码)+ **TLS**(传输加密 + 客户端证书双向认证)。proxy 模式的价值:把认证/TLS/broker 寻址的复杂性收到一个 pod 里,客户端只连本地端口。凭据全走 vault 挂载(`/etc/secrets-vault/...`),不进代码不进镜像。

**避雷**:别把这个和 connector repo 里的 `internetproxy-snowglobe`(出网代理,让 pod 通过公司代理访问 Snowflake JDBC)搞混——那不是 Kafka proxy。面试被追问 "Kafka proxy 是什么" 就答 grepplabs kafka-proxy(SASL/TLS 到 broker 的代理,跑在 K8s pod 里)。

**学到什么程度**:能解释 SASL SCRAM-SHA-512 和 TLS 各解决什么(认证 vs 加密),能说清 proxy 模式相比客户端直连 broker 的好处,不会把 Kafka proxy 和 egress proxy 混为一谈。

---

### ★8. proto schema —— 事件流的上游合约(event_protos)
**路径**:`event_protos/proto/entity/processing/transaction_event.proto`。

**精华在哪**:整个事件流的**契约**。一个 `TransactionEvent` 用 `oneof` 承载 8 种子事件,`StatusChange` 是最主要的一种,携带 40+ 字段(交易金额/币种/结算日/商户账户/处理器/chargeback protection level/3DS/退款关联...):
```protobuf
message TransactionEvent {
  Header header = 1;
  oneof message {
    StatusChange status_change = 2;
    RefundCreated refund_created = 11;
    InstallmentChange installment_change = 6;
    // ...共 8 种
  }
  message StatusChange {
    string transaction_public_id = 2;
    string merchant_account_unique_identifier = 5;
    string transaction_amount = 6;
    string settlement_date = 15;
    ChargebackProtectionLevel chargeback_protection_level = 34;
    // ...40+ 字段
  }
}
```

**为什么 Sr 级**:这是**schema-first / contract-first** 的事件设计。`oneof` 让一个 topic 承载多种语义相关的事件、消费方各取所需(呼应 ★1 converter 的 oneof 分派)。protobuf 的向后兼容规则(字段号只增不改、不复用删掉的号)是跨团队演进事件的基础——上游加字段,下游不用改代码。字段全用 tag number 标识,新增字段老消费者自动忽略。

**学到什么程度**:能解释为什么用 protobuf 而不是 JSON 做事件契约(强类型、体积小、向后兼容规则明确、代码生成),能读懂 `oneof` 的语义,知道 proto 演进的兼容性规则。Chi 是这个 schema 的**消费方**(Snowglobe 落它、Pricing 解它),讲"熟悉这套契约、下游怎么依赖它"站得住。

---

### 加分参考:Spring Boot 计费服务结构 + Spark validator 模式(baseline 的看齐版)
- **Spring Boot 服务分层**(pricing repo):`controllers/`(REST 入口)→ `api/`(service 层,如 REST Log 的 Service)→ `common/data/`(JPA entity + repository)→ `events/`(Kafka consumer/producer)→ `worker/`(fee 计算)。看齐点:service 层用 `JpaSpecificationExecutor` + `CriteriaBuilder` 做动态查询(比硬编码 `@Query` 灵活),repository 用 `findExistingIdsInBatches` 批量查询避免 N+1,异常统一包成有意义的 domain exception。
- **Spark validator 模式**(pricing-spark):EOD job 读 BigQuery 大表 → 用 Spark DataFrame 做合规规则过滤 → 命中即告警到 Slack。看齐点:批处理校验用"最近 N 天时间窗"保证幂等可重跑,校验结果推 Slack 做可观测性,而不是默默写日志。这正是 Chi 那 3 个 validator 的模式——学透它 = 理解"实时链路算数、批处理链路验数"的分工。

---

## 4. 知识点体系(Chi 要能开口讲)

**Kafka 基础**
- **topic / partition / consumer group**:partition 是并行的最小单位;一个 consumer group 内,一个 partition 只被一个成员消费;消费者数 > partition 数时多的空转。加吞吐 = 加 partition + 加消费者。
- **offset / rebalance**:offset 记录消费进度,存在 `__consumer_offsets`;消费者增减触发 rebalance,partition 重新分配。
- **at-least-once vs exactly-once vs at-most-once**:默认 at-least-once(commit 前崩溃会重投);exactly-once 靠事务或幂等消费达到;计费系统选 **at-least-once 传输 + 幂等消费**(见 ★5)。

**Kafka Connect**
- 官方零代码搬运框架。**source connector** 把外部系统数据打进 Kafka,**sink connector** 把 topic 落到外部系统。
- 流水线:消息 → `Converter`(反序列化)→ `Transform`(SMT,过滤/改形)→ 写目标。connector 拆成 `tasks.max` 个 task 分到 worker 并行,offset 由 Connect 托管、支持断点续传。
- **SMT(Single Message Transform)**:声明式改单条消息(Filter/Mask/Route...),无需写代码。CDC 白名单就是 `Filter$Value`。

**Snowpipe Streaming**
- Snowflake 的行级低延迟摄取 API(对比传统 Snowpipe 的文件批量 COPY)。秒级可见。`buffer.count.records`/`buffer.flush.time` 控攒批与延迟/成本的权衡。`schematization=TRUE` 让半结构化 JSON/proto 字段自动映射成表列。

**Schema / Converter**
- BT 事件是 protobuf。converter 链:`parseFrom(bytes)` → `JsonFormat.printer()` 转 JSON → Connect 的 `JsonConverter` → schematize 落列。
- **必守规矩**:catch `InvalidProtocolBufferException`、坏消息返回 `SchemaAndValue.NULL`(不让一条脏消息毒死 task)、每个 converter 配 snapshot 测试。

**Kubernetes 部署与水平扩展**
- 每个 consumer/connector = 一个 `Deployment`;`replicas` 控 pod 数;consumer group rebalance 让加 pod = 加吞吐 + 加冗余。
- **两级/三级并行度**:K8s replicas × (Connect tasks.max 或 Spring concurrency),上限 = topic partition 数。
- **稳定性**:`livenessProbe`(hang 住重启)、`readinessProbe`(未就绪不接流量)、`preStop`(优雅下线让 in-flight commit)、resource requests/limits(调度 + OOM 保护)、vault 挂密钥。

**Spring Boot + JPA**
- 分层:controller → service → repository → entity。`@KafkaListener` + `ConcurrentKafkaListenerContainerFactory` 做消费,`KafkaTemplate` 做生产。
- JPA:静态 `@Query` vs 动态 `CriteriaBuilder`/`JpaSpecificationExecutor`(过滤条件运行时才知道时用后者);批量查询避免 N+1;唯一约束 + catch `DataIntegrityViolationException` 做幂等。
- servlet filter 抓 request body 要用 RequestWrapper(输入流只能读一次)。
- 错误处理:`DefaultErrorHandler` + `FixedBackOff` 重试,区分可重试/不可重试异常,`ErrorHandlingDeserializer` 兜反序列化失败。

**Spark / Airflow 批处理校验**
- Spark 读大表(BigQuery/Snowflake)做 DataFrame 规则校验,适合 EOD 全量扫描;Airflow DAG 调度、定时(cron/weekly)、依赖编排。
- 幂等设计:用"最近 N 天时间窗"保证可重跑;结果推 Slack 做可观测性。
- **分工**:实时链路(Kafka+Connect)算数、落数;批处理链路(Spark+Airflow)事后验数——两层合起来才是完整的清结算准确性保障。

---

## 5. 学习锚点表

| 要学的东西 | 看齐的精华实现(路径) | 锚点 / 备注 |
|---|---|---|
| Converter 模板方法 + poison-message 隔离 | `kafka-snowflake-connector/src/.../ProtobufConverter.java` + `TransactionStatusChangeEventProtobufConverter.java` | 基类 `getJson()` 的 4 个 JsonFormat 选项;坏消息返回 `SchemaAndValue.NULL` |
| sink connector 配置 + Snowpipe Streaming | `kafka-snowflake-connector/docker/connector/eventstream_v2.properties` | buffer/tasks/schematization 权衡 |
| CDC 白名单 SMT(Chi 2355 的上下文) | `kafka-snowflake-connector/docker/connector/cdc/funding.properties` | `Filter$Value` + JSONPath;`@.kind != 'delete'`;DTBTTFOUND-2355 |
| K8s connector 部署 + replicas×tasks 并行度 | `kafka-snowflake-connector/kubernetes/application.yaml.erb` | livenessProbe / preStop / vault / 每 connector 独立 role+wh |
| @KafkaListener 批量消费 + 幂等计费 | `pricing/.../events/transactions/TransactionEventConsumer.kt` | 去重查询 + 唯一约束 + `BatchListenerFailedException`;consumer 兼 producer |
| ContainerFactory 错误处理/重试/DLQ | `pricing/.../events/config/KafkaConsumerConfiguration.kt` | concurrency、`DefaultErrorHandler`+`FixedBackOff`、not-retryable 异常 |
| Kafka proxy(SASL SCRAM + TLS) | `pricing/kafka-proxy-pod.sh`、`kafka-proxy-cpair.sh` | grepplabs kafka-proxy;别和 egress proxy 混 |
| proto 事件契约(oneof + 兼容规则) | `event_protos/proto/entity/processing/transaction_event.proto` | `TransactionEvent` oneof 8 种;`StatusChange` 40+ 字段 |
| K8s 消费者部署(replicas:10) | `pricing/kubernetes/kafka-transactions.yaml.erb` | 一 topic 一 Deployment;`./start.sh --kafka-transactions` |
| Spring Boot 分层 + JPA 动态查询 | `pricing/.../api/PricingScheduleEventRestLogService.kt`(Chi 亲写) | `JpaSpecificationExecutor` + `CriteriaBuilder`;Confluence 966206164 |
| Spark EOD 合规校验模式 | `BigDataInfraEng/pricing-spark`(Chi 亲写 3 个)| DTBTPRWIZ-39/53/54;Confluence 966731781 |

---

## 6. 面试怎么讲(把整套事件流 + 部署讲成 Chi 懂透的东西)

**30–60 秒总览**:
> "我们的清结算/计费生态是事件驱动的。一笔交易在 gateway 结算时会往 Kafka 打一条 protobuf transaction event。Pricing 服务(Kotlin + Spring Kafka)用 `@KafkaListener` 批量消费它,查商户账户、幂等地落库、算出 Braintree fee,再往另一个 Kafka topic 发一条 fee event 给 Funding 出款用。我这边的 Snowglobe 用 Kafka Connect 的 sink connector 配 Snowpipe Streaming,把这些 topic 以及 Funding 的 CDC 变更流实时落进 Snowflake,做对账、费用计算和质检。所有这些 connector 和消费者都跑在 Kubernetes 上,每个是一个 Deployment,靠 replicas 做水平扩展、靠 consumer group rebalance 和 liveness probe 保稳定。事件流之外还有一层 Spark + Airflow 的 EOD 批处理,校验 pricing schedule 创建来源、settlement 数据是否合规。我具体做过的:给 fee-validation 扩展 CDC 摄取管线、写 Spring/JPA 的 compliance 审计日志模块、写 Spark 合规校验器。"

**被追问点,一句话应对**:
- **"怎么保证费用不重复算/不漏算?"** → Kafka 是 at-least-once,会重投,所以消费侧必须幂等:落库前批量去重、DB 唯一约束兜并发、catch `DataIntegrityViolationException` 跳过重复、用 `BatchListenerFailedException` 精确重投失败那条。at-least-once + 幂等 ≈ effectively-once。
- **"Kafka Connect 怎么扩展?"** → 两级并行:K8s replicas × connector tasks.max,上限被 topic partition 数卡住。加吞吐要同时看 partition 够不够。
- **"Kafka proxy 是什么?"** → grepplabs kafka-proxy,跑在 K8s pod 里、放在 broker 前面做 SASL SCRAM-SHA-512 认证 + 双向 TLS 的代理,凭据走 vault。别答成出网代理。
- **"CDC 怎么做的?"** → Funding MySQL 变更以 `{table, kind, before, after}` envelope 打进 Kafka,sink connector 用 `Filter$Value` SMT 按 JSONPath 白名单过滤表、只要 upsert 不要 delete,落进 Snowflake 给下游 SQL。
- **"proto 事件怎么落成 Snowflake 表?"** → 自定义 Converter `parseFrom` → `JsonFormat` 转 JSON(保留字段名)→ Snowflake schematization 自动展开成列;坏消息返回 NULL 不毒死 task。
- **"实时和批处理怎么分工?"** → 实时(Kafka+Connect,秒级)负责搬数据、算费用;批处理(Spark+Airflow,天级)负责事后校验数据对不对、创建来源合不合规。

**避雷**:说"我拥有/扩展了消费侧和 sink 侧的管线、写了 Spring 审计日志和 Spark 校验器",不说"我从零搭了 Kafka 集群/从零写了整个 connector"——broker 和 proxy 基础设施是平台团队管的,Chi 真正的地盘是**消费/落库/校验侧**:连哪个 topic、落哪张表、consumer group/offset/replicas 怎么调、CDC 过滤怎么配、幂等怎么保。这个边界讲清楚反而显专业。
