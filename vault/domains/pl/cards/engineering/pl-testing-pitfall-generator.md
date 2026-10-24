---
id: pl-testing-pitfall-generator
node: engineering.testing
type: qa
step: 10
---
## Q
属性测试通过了，是否说明没有 bug？用 Hypothesis 的一个实验说明生成器会怎样让测试「假通过」。

## A
不能。属性测试能找到的 bug 被**生成器的分布**限制：它只能在生成得出来的输入里找反例。

**实验**：`slug(s)` 把首尾空白去掉、转小写、把空格换成连字符。性质：输入里没有连字符时，输出里也不该有连续两个连字符。真实 bug 是输入含连续两个空格。

```python
def slug(s): return s.strip().lower().replace(" ", "-")

def check(s):
    if "-" not in s:
        assert "--" not in slug(s)

@given(st.text())                    # broad
def test_broad(s): check(s)

@given(st.text(alphabet="a -"))      # narrow
def test_narrow(s): check(s)
```

Hypothesis 默认每个测试生成 100 个样例。各运行 20 次（每次清掉缓存的失败样例）：

```text
broad:  0 次发现 bug
narrow: 13 次发现 bug，缩小后的反例为 'a  a'
```

宽泛的 `st.text()` 在整个 Unicode 里取字符，「恰好连续出现两个空格」的概率太低；窄字母表把搜索集中在相关字符上，多数运行就能命中。两个版本检验的是同一条性质，写对性质也不等于测对。

**怎么办**：
- 针对被测逻辑关心的字符、范围、结构去定制生成器，别只用默认的最宽分布；
- 把已知的重要边界作为显式示例保留（Hypothesis 用 `@example`），不要指望随机命中；
- 提高样例数，并在 CI 里长期运行以累积发现的反例；
- 与示例测试互补：属性测试覆盖想不到的输入，示例测试钉死已知的角落。
