---
id: bagu-rabbitmq-1-model-ack
node: b.mq.rabbitmq
type: qa
step: 1
---
## Q
**RabbitMQ · 核心模型、ack 与崩溃后的行为**｜追问

面试官：「构建任务用 RabbitMQ 分发给 worker。讲讲它的模型；worker 处理到一半崩溃，任务会丢吗？」

## A
**基本回答。** 生产者（producer）不直接把消息塞进队列，而是发给交换机（Exchange）；交换机按绑定（Binding）和路由键（routing key）决定投进哪个队列，消费者再从队列里取。交换机类型有 direct、topic、fanout、headers 四种。消费者要处理完再手动 ack（acknowledge，确认）；处理到一半崩溃、连接断开时，没 ack 的消息会重新入队：不会丢，但会被再投一次，所以会重复。
四种交换机：direct 按路由键精确匹配；topic 按通配符匹配（`*` 一个词，`#` 零或多个词）；fanout 广播给所有绑定的队列；headers 按消息头匹配，少用。生产端要发布确认（Broker 落盘后才回确认）加 durable 队列加持久化消息，三者缺一不可。处理失败用 `nack` 且不重新入队，交给死信交换机，避免坏消息无限 requeue。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 292">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">① 路由：生产者只认交换机</text>
<rect x="6" y="36" width="62" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生产者</text>
<rect x="94" y="36" width="70" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="129" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">交换机</text>
<text x="129" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Exchange</text>
<line x1="68" y1="58" x2="87" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="94.0,58.0 87.0,61.2 87.0,54.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="206" y="24" width="70" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="241" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 A</text>
<rect x="206" y="66" width="70" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="241" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 B</text>
<line x1="164" y1="58" x2="185" y2="58" stroke-width="1.2" stroke="currentColor"/>
<line x1="185" y1="38" x2="199" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,38.0 199.0,41.2 199.0,34.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="185" y1="38" x2="185" y2="80" stroke-width="1.2" stroke="currentColor"/>
<line x1="185" y1="80" x2="199" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,80.0 199.0,83.2 199.0,76.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="94" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按绑定 + 路由键分发</text>
<line x1="276" y1="38" x2="289" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296.0,38.0 289.0,41.2 289.0,34.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="296" y="24" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="315" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取走</text>
<text x="8" y="134" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">② 消费者一侧：处理完才 ack</text>
<rect x="6" y="148" width="94" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">投递给 worker</text>
<text x="53" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（未确认）</text>
<rect x="122" y="148" width="94" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理业务</text>
<rect x="238" y="148" width="96" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">手动 ack</text>
<text x="286" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker 才删</text>
<line x1="100" y1="166" x2="115" y2="166" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122.0,166.0 115.0,169.2 115.0,162.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="216" y1="166" x2="231" y2="166" stroke-width="1.2" stroke="currentColor"/>
<polygon points="238.0,166.0 231.0,169.2 231.0,162.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="214" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">③ 中途崩溃：连接断开</text>
<rect x="6" y="228" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="81" y="244.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker 崩溃</text>
<text x="81" y="259.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（没来得及 ack）</text>
<rect x="184" y="228" width="150" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="259" y="244.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息重新入队</text>
<text x="259" y="259.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再投给别的 worker</text>
<line x1="156" y1="248" x2="177" y2="248" stroke-width="1.2" stroke="currentColor"/>
<polygon points="184.0,248.0 177.0,251.2 177.0,244.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="286" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">不丢，但会重复 → 消费必须幂等</text>
</svg>
第一层是消息怎么被路由到队列；中间一层是 ack 之后 Broker 才删除；最下面是崩溃后消息重新入队，所以是「不丢但重复」。
**举个例子。** 构建任务 build-4812 要分发给 worker：
1. **发布：** 生产者把任务发到交换机 `build`，路由键是 `linux`；绑定把它路由进队列 `build.linux`。发布确认回来，说明 Broker 已落盘。
2. **投递：** worker A 取到任务，此时消息状态是「未确认」，队列里还留着记录。
3. **崩溃：** worker A 构建到一半进程被杀，连接断开，没来得及 ack。
4. **重新入队：** Broker 把 build-4812 放回队列，worker B 取到并从头构建，完成后手动 ack，Broker 才删除它。同一个任务被构建了两次，所以构建步骤要幂等。
5. **对比：** 如果开了自动 ack，投递的瞬间消息就被删，worker A 崩溃后这个任务永远丢了。
**容易错。**
- **以为自动 ack 更省事：** 自动 ack 在投递时就删消息，消费者崩溃会直接丢任务；要手动 ack。
- **以为 durable 队列就不会丢：** 还要消息本身持久化，生产者还要开发布确认，缺一个都可能丢。
- **以为不丢就等于只执行一次：** 重新入队意味着可能重复，要靠幂等，不是靠 RabbitMQ。
- **失败就一直 requeue：** 一条处理不了的坏消息会反复入队，要走 `nack` 不重入队加死信交换机。
- **继续用镜像队列：** 4.0 已经移除，高可用用 quorum queue。
