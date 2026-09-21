%% trellis:begin %%
# 枚举（Enum）：`Enum`/`IntEnum`/`StrEnum`/`Flag`、`auto()` 与唯一性
*类、协议与元编程*

理解枚举成员是类属性求值后由元类替换成的单例、`auto()` 与 `_generate_next_value_` 的取值规则、`@unique` 与别名、`Flag` 的位运算组合，以及什么时候该用 `StrEnum`/`IntEnum` 而不是裸常量。

**Core** — part of the first pass through this subject.

## Readings
- [[pydocs-enum-howto|Enum HOWTO：枚举成员是类的单例实例]]

## Cards (7)
1. [[auto-generate-next-value-override]]
2. [[enum-alias-same-value-different-name]]
3. [[enum-members-are-singletons]]
4. [[enum-not-orderable-only-eq]]
5. [[flag-zero-value-falsy]]
6. [[intenum-strenum-vs-flag-when-to-use]]
7. [[unique-decorator-forbids-alias]]
%% trellis:end %%

## Notes
