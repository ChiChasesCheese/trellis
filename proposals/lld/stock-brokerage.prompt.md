You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
设计题（Design Problems） › 交易与撮合 › 股票交易系统（Stock Brokerage）
限价单与市价单、订单簿的价格-时间优先撮合、持仓与资金校验。

## Position in the knowledge map
Prerequisites (assume known):
  - 内存持久化（In-Memory Persistence）: 仓储（repository）模式、id 生成、二级索引，以及线程安全的内存存储。
Sibling topics (OUT of scope):
  - 分账（Splitwise）: 均分/按额/按比例的拆分策略、余额图与债务简化。
  - 在线购物（Amazon）: 商品目录、购物车、订单状态机与库存扣减。
  - 网约车（Uber）: 乘客-司机匹配策略、行程状态机与计价。
  - 外卖配送（Food Delivery）: 餐厅-订单-骑手三方的订单流转与派单策略。
  - 在线拍卖（Online Auction）: 出价校验、最高价维护、到期结算与并发出价。
  - 数字钱包（Digital Wallet）: 充值、转账、交易记录，余额不能为负且转账两边一致。
  - 银行账户系统（Bank Account System）: 分关递进的机考题型：开户与转账 → 排名统计 → 定时支付 → 账户合并。

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
  {"id": "example-qa-card", "node": "problems.marketplaces.stock-brokerage", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.marketplaces.stock-brokerage", "type": "cloze",
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
