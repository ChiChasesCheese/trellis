

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


def test_svg_fence_becomes_inline_figure_and_keeps_semicolons():
    from trellis.build import _html
    html = _html('**结构。** 树。\n\n```svg\n<svg viewBox="0 0 10 10"><text>a；b</text></svg>\n```\n')
    assert '<div class="fig"><svg viewBox="0 0 10 10"><text>a；b</text></svg></div>' in html


def test_example_section_is_folded_to_the_end():
    from trellis.build import _html
    html = _html("**为什么。** 因为。\n\n**例题：** LC 1 两数之和\n\n给数组。\n\n```python\nx = 1\n```\n")
    assert '<details class="example"><summary><span class="label">例题</span>LC 1 两数之和</summary>' in html
    assert html.rstrip().endswith("</details>")
    assert html.index("因为") < html.index("<details")
