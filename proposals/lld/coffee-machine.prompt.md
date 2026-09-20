You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
设计题（Design Problems） › 设备与状态机 › 咖啡机（Coffee Machine）
配方、原料库存的原子扣减与补货告警，多出口并发制作。

## Position in the knowledge map
Prerequisites (assume known):
  - 同步原语（threading）: `Lock`、`RLock`、`Condition`、`Semaphore`、`Event`、`queue.Queue`：各自解决的问题与误用方式。
Sibling topics (OUT of scope):
  - 停车场（Parking Lot）: 多楼层、多车型车位的分配与释放，计费策略可换，出入口并发。
  - 电梯系统（Elevator System）: 多部电梯的请求调度：状态机、调度策略、方向与停靠队列。
  - 自动售货机（Vending Machine）: 投币、选货、出货、找零的状态机，库存与找零不足的失败路径。
  - ATM 取款机: 认证、取款、存款、查询的会话状态机，现钞面额分配与账户一致性。
  - 快递柜（Amazon Locker）: 按包裹尺寸分配柜格、取件码与过期回收。
  - 交通信号灯（Traffic Signal）: 路口多相位信号的定时状态机、紧急车辆抢占与可配置时序。

## Rules
- Write 8 cards for THIS topic only. Sibling topics listed above are
  out of scope — never restate their material.
- One card = one retrievable fact, mechanism, trade-off, or number. If an
  answer needs more than ~4 sentences, split the card.
- Prefer questions that force discrimination ("when would you choose X
  over Y") over definitions, except for terms of art.
- Use `type: "cloze"` with {{c1::...}} syntax for formulas, sequences,
  and lists; `type: "qa"` otherwise.
- Markdown allowed in q/a/text (code spans, tables, lists).
- id: lowercase-hyphenated slug, unique, descriptive, stable.

## Output format (JSON array only, no prose)
[
  {"id": "example-qa-card", "node": "problems.machines.coffee-machine", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.machines.coffee-machine", "type": "cloze",
    "text": "The formula is {{c1::W + R > N}}.", "tags": []}
]

## Language and self-containment
- Write every card in Chinese (简体中文). Terms of art stay in English (the reader will
  meet them in code, configs and docs): write the English term and gloss
  it in Chinese (简体中文) once per card, e.g. `consumer group（消费者群组）`.
- SELF-CONTAINED. A reader who has never heard of 低层设计（LLD） must understand
  the card from the card alone: the question carries the situation it is
  asking about, the answer defines every term it uses and says WHY, not
  only what. Never "as discussed", "the book says", "see chapter 3" — nor
  their equivalents ("书中建议", "本书", "如前所述"): the importer refuses a
  card that leans on its source. State the advice as a fact.
- Prefer questions whose answer is a mechanism or a decision ("what happens
  when…", "why would you set…") over ones whose answer is a name.
- Do not set `source`; the importer records where these cards came from.
