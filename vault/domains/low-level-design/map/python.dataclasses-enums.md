%% trellis:begin %%
# dataclass 与 Enum
*Python 对象模型与惯用法（Pythonic Design）*

`@dataclass(frozen, slots, order)`、`field(default_factory)`、带行为的 `Enum`：值对象与有限状态的标准写法。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/python.data-model|数据模型与特殊方法（Data Model）]]

**Unlocks:** [[domains/low-level-design/map/oop.values|值对象与不可变性（Value Objects）]], [[domains/low-level-design/map/patterns.state|状态模式（State）]], [[domains/low-level-design/map/problems.games.deck-of-cards|扑克牌与二十一点（Deck of Cards / Blackjack）]]

## Drills
- [[design-deck-of-cards|Drill：扑克牌与二十一点（Deck of Cards / Blackjack）]]

## Cards (6)
1. [[python-dataclass-hash-rule]]
2. [[python-dataclass-default-factory]]
3. [[python-dataclass-frozen-post-init]]
4. [[python-dataclass-shallow-frozen]]
5. [[python-dataclass-slots-cost]]
6. [[python-dataclass-enum-behavior]]
%% trellis:end %%

## Notes
