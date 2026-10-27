

def test_card_html_lists_labels_title_and_highlighting():
    from trellis.build import _html
    q = _html("**LC 3 无重复字符的最长子串**｜Medium · TikTok 高频\n\n给字符串 `s`。")
    assert '<p class="title">LC 3 无重复字符的最长子串<span class="meta">Medium · TikTok 高频</span></p>' in q
    a = _html("**易错点。**\n- 一\n- 二\n\n```python\ndef f(x: int) -> int:\n    return x\n```")
    assert '<span class="label">易错点</span>' in a
    assert "<ul>" in a and a.count("<li>") == 2           # the list is not merged into the paragraph
    assert 'class="hl"' in a and 'class="k"' in a          # pygments highlighted the code
    plain = _html("**冻结是一条带状态的记录**，不是分录。")
    assert "label" not in plain                            # only a short lead ending in 。/： is a label


def test_full_width_semicolons_break_lines_outside_code():
    from trellis.build import _html
    a = _html("**复杂度。** 窗口：`O(1)`；令牌桶：`O(1)；x`。")
    assert "窗口：<code>O(1)</code>；<br>令牌桶" in a
    assert "<code>O(1)；x</code>" in a                      # inside code untouched
