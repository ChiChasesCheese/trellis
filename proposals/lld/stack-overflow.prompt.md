You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
设计题（Design Problems） › 社区与内容 › 问答社区（Stack Overflow）
问题-回答-评论、投票与声望、标签与搜索。

## Position in the knowledge map
Prerequisites (assume known):
  - 类之间的关系（Class Relationships）: 关联、聚合、组合、依赖的区别；生命周期归属，以及各自的 UML 箭头。
Sibling topics (OUT of scope):
  - 社交网络（Social Network）: 好友关系、发帖与信息流、隐私可见性规则。
  - 职业社交（LinkedIn）: 个人档案、人脉连接请求、职位发布与申请。
  - 聊天室（Chat Room）: 单聊与群聊、消息投递与已读、在线状态。
  - 任务看板（Trello / Jira）: 看板-列-卡片、工作流状态转移、指派与活动记录。
  - 音乐流媒体（Spotify）: 曲库、播放列表、播放队列与播放器状态。

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
  {"id": "example-qa-card", "node": "problems.social.stack-overflow", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.social.stack-overflow", "type": "cloze",
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
