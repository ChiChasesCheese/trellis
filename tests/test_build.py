

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
    assert '<div class="fig tappable" onclick="this.classList.toggle(\'zoom\')"><svg viewBox="0 0 10 10"><text>a；b</text></svg></div>' in html


def test_example_section_is_folded_to_the_end():
    from trellis.build import _html
    html = _html("**为什么。** 因为。\n\n**例题：** LC 1 两数之和\n\n给数组。\n\n```python\nx = 1\n```\n")
    assert '<details class="example"><summary><span class="label">例题</span>LC 1 两数之和</summary>' in html
    assert html.rstrip().endswith("</details>")
    assert html.index("因为") < html.index("<details")


def test_double_brackets_inside_code_are_not_wikilinks():
    from trellis.build import _html
    html = _html("`a = [[0]] * 3` 与 [[note|链接]]\n\n```python\ngrid = [[0] * 3 for _ in range(2)]\nx = [[1]]\n```\n")
    assert "<code>a = [[0]] * 3</code>" in html
    assert '<span class="ref">链接</span>' in html
    assert 'class="ref">1<' not in html


def test_several_examples_fold_separately():
    from trellis.build import _html
    html = _html("**信号。** 甲\n\n**例题：** LC 1\n\n```python\nalpha = 1\n```\n\n**例题：** LC 2\n\n```python\nbeta = 2\n```\n")
    assert html.count('<details class="example">') == 2
    assert html.index("LC 1") < html.index("alpha") < html.index("LC 2") < html.index("beta")
    assert html.index("alpha") < html.index("</details>") < html.index("LC 2")


def test_example_opens_inside_the_list_item_that_names_it():
    from trellis.build import _html
    md = ("**子集。**\n\n- LC 78 子集\n- LC 90 子集 II（未配例题）\n- 有效括号字符串：判断（高频）\n\n"
          "**例题：** LC 78 子集\n\n题意。\n\n```python\nalpha = 1\n```\n\n"
          "**例题：** 有效括号字符串：判断\n\n题意二。\n\n```python\nbeta = 2\n```\n\n"
          "**例题：** LC 5 最长回文\n\n```python\ngamma = 3\n```\n")
    html = _html(md)
    assert '<li><details class="inline-example"><summary>LC 78 子集</summary>' in html
    assert html.index("alpha") < html.index("LC 90")
    assert '<summary>有效括号字符串：判断（高频）</summary>' in html
    assert html.count('<details class="example">') == 1 and html.index("gamma") > html.index("</ul>")


def test_related_problems_open_in_place():
    from trellis.build import _html
    related = {154: ("LC 154 最小值 II", "<p>题意。</p><pre>code154</pre>"), 33: ("LC 33 搜索", "<p>s</p><pre>code33</pre>")}
    html = _html("**同模式。** LC 154 最小值 II、LC 33 搜索旋转排序数组、LC 162 峰值。\n\n- LC 33：先判断哪段有序\n- LC 999 未知\n",
                 related, {153})
    assert '<ul class="related">' in html and html.count("code154") == 1
    assert "<li>LC 162 峰值</li>" in html
    assert html.count("code33") == 2 and "LC 999 未知</li>" in html


def test_core_problem_list_opens_in_place():
    from trellis.build import _html
    related = {315: ("LC 315 右侧小于当前元素的个数", "<p>题意。</p><pre>code315</pre>")}
    html = _html("**核心题。**\n\n- LC 315 右侧小于当前元素的个数（Hot 100）：逆序对计数的模板\n", related, {4099})
    assert '<details class="inline-example"><summary>' in html and "code315" in html


def test_related_problem_shows_the_main_solution_not_the_simple_one(tmp_path):
    from trellis.build import load_related
    (tmp_path / "x").mkdir()
    (tmp_path / "x" / "tlc-k-0-whole.md").write_text(
        "---\nid: tlc-k-0-whole\nnode: a.k\ntype: qa\n---\n## Q\n**LC 215 第 K 大**｜Medium\n\n题意。\n\n## A\n"
        "**简单解法。** 排序。\n\n```python\nsimple = 1\n```\n\n最优解：\n\n```python\nquick = 2\n```\n", encoding="utf-8")
    html = load_related(tmp_path)[215][1]
    assert "quick" in html and "simple" not in html


def test_fold_turns_sections_and_bullets_into_an_outline():
    from trellis.build import _html
    md = ("**一句话。** 难点。\n\n**需求。**\n- 功能：发消息\n- 估算（1 亿日活）：每天 100 亿条，平均 11.6 万条/秒，峰值 35 万条/秒，"
          "历史必须分层存储，单台网关扛 25 万连接。\n  - 子项一\n\n**深入。**\n1. 顺序：同一会话按 seq 排序。\n  - 细节\n")
    h = _html(md, fold=True)
    assert '<details class="sec"' in h and "<summary><span class=\"label\">需求</span>" in h
    assert '<details class="pt"' in h and "<summary>估算（1 亿日活）</summary>" in h
    assert "<li>子项一</li>" in h  # 2-space sub-bullets nest instead of running into the parent text
    assert "<summary>功能</summary>" in h and "发消息" in h  # the phrase is what shows, the rest opens from it


def test_two_space_sub_bullets_nest_without_fold():
    from trellis.build import _html
    assert "<li>b</li>" in _html("- a\n  - b\n")


def test_video_embed_plays_in_anki(monkeypatch, tmp_path):
    import trellis.build as b
    clip = tmp_path / "bb-euro-step.mp4"
    clip.write_bytes(b"\x00")
    monkeypatch.setattr(b, "_VAULT_MEDIA", {"bb-euro-step.mp4": clip})
    b._MEDIA_USED.clear()
    h = b._html("要点。\n\n![[bb-euro-step.mp4]]\n")
    assert '<video class="clip" src="bb-euro-step.mp4"' in h and clip in b._MEDIA_USED
    assert '<span class="ref">nope.mp4</span>' in b._html("![[nope.mp4]]")


def test_fold_keeps_code_indentation_under_a_bullet():
    from trellis.build import _html
    md = ("**一句话。** 难点。\n\n**需求。** 短。\n\n**实现。**\n1. 词法：把字符串切成 token，这一步要处理引号、数字和关键字，长度超过阈值所以会折叠起来显示。\n\n"
          "```python\ndef f() -> int:\n    return 1\n```\n")
    h = _html(md, fold=True)
    assert "    <span" in h or "\n    " in h, h


def test_fold_keeps_indentation_of_an_indented_fence():
    from trellis.build import _fold_bullets
    out = _fold_bullets("- 这一条很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长\n\n    ```python\n    def f() -> int:\n        return 1\n    ```\n")
    assert "\n    return 1\n" in out


def test_long_code_folds_only_past_the_limit():
    from trellis.build import _html
    short = "```python\nx = 1\n```"
    long = "```python\n" + "\n".join(f"x{i} = {i}" for i in range(30)) + "\n```"
    assert "<details" not in _html(short, fold_code=25)
    assert '<summary>代码（30 行）</summary>' in _html(long, fold_code=25)
    assert "<details" not in _html(long)


def test_bullet_head_is_a_phrase_never_cut_or_repeated():
    from trellis.build import _head
    ref = '<span class="ref">Elasticsearch 倒排索引</span>'
    head, rest = _head(f"为什么搜索快、新帖多久可见 → 倒排索引，1 秒 refresh 的准实时，{ref}")
    assert head == "为什么搜索快、新帖多久可见"
    assert rest.startswith("倒排索引") and ref in rest and "…" not in head + rest
    assert _head("**幂等键：** 客户端生成，服务端唯一约束") == ("幂等键", "客户端生成，服务端唯一约束")
    long = "一" * 40 + "，" + "二" * 40  # no phrase to lead with: stays whole, never truncated
    assert _head(long) == (long, "")
    assert _head("`a，b` 的取舍：看场景")[0] == "`a，b` 的取舍"  # separators inside code do not split


def test_outline_sections_open_and_details_closed():
    from trellis.build import _html
    md = "**基本回答。** 短答案。\n\n**为什么。**\n- 第一点是什么：解释第一点的原因和细节\n\n**扩展点。**\n- 第二点：细节\n"
    h = _html(md, fold=True)
    assert '<details class="sec" open' in h and '<details class="pt">' in h and "<summary>第一点是什么</summary>" in h


def test_wikilink_to_a_card_jumps_and_lists_it_at_the_end():
    from trellis.build import _html
    links = {"a.redis.zset": {"node": "a.redis.zset", "tag": "bagu::a::redis::zset", "answer": "跳表加哈希。"}}
    h = _html("**基本回答。** 见 [[a.redis.zset|ZSet 与跳表]]，还有 [[nowhere|别处]]。", links=links, node="links.top-k")
    assert 'href="anki://x-callback-url/search?query=tag%3Abagu%3A%3Aa%3A%3Aredis%3A%3Azset"' in h
    assert '<span class="ref">别处</span>' in h  # a note with no card stays plain text
    assert "相关知识点" in h and "跳表加哈希" in h
    assert "相关知识点" not in _html("见 [[a.redis.zset|自己]]。", links=links, node="a.redis.zset")  # a card never lists itself


def test_short_card_bullets_are_phrases_too():
    from trellis.build import _html
    h = _html("- **摘要要点：** 这里是具体内容\n- 第二点 → 也放进折叠\n", fold=True)
    assert "<summary>摘要要点</summary>" in h and "<summary>第二点</summary>" in h and "具体内容" in h


def test_a_question_with_english_terms_is_still_a_phrase():
    from trellis.build import _head
    head, rest = _head("Function Calling 是模型在调函数吗？ → 不是。模型只生成调用意图。")
    assert head == "Function Calling 是模型在调函数吗？" and rest.startswith("不是")


def test_a_link_in_a_fold_title_is_a_link_not_text():
    from trellis.build import _html
    links = {"links.top-k": {"node": "links.top-k", "tag": "bagu::links::top-k", "answer": "地图"}}
    h = _html("**基本回答。** 短。\n\n**业务场景。** 短。\n\n**系统设计。** [[links.top-k|Top-K 榜]]：怎么分片再合并，第一步按用户分桶\n", fold=True, links=links, node="a.x")
    assert "&lt;a" not in h and 'class="ref" href="anki://' in h


def test_a_longer_bold_cue_still_folds():
    from trellis.build import _head
    head, rest = _head("**以为 MCP 取代了 Function Calling：**MCP 管工具怎么接入")
    assert head == "以为 MCP 取代了 Function Calling" and rest.startswith("MCP 管")


def test_long_trailing_comment_moves_above_on_a_phone():
    from trellis.build import _lift_comments
    code = "dead: Counter[int] = Counter()                 # 值 -> 还要丢弃几个\nx = 1  # 短\ns = '# 不是注释' + y\n"
    out = _lift_comments(code, "#").split("\n")
    assert out[0] == "# 值 -> 还要丢弃几个" and out[1] == "dead: Counter[int] = Counter()"
    assert out[2] == "x = 1  # 短" and out[3] == "s = '# 不是注释' + y"


def test_bare_problem_numbers_get_titles():
    from trellis import build as B
    B._LC_TITLES.update({"787": "K 站中转内最便宜的航班", "743": "网络延迟时间"})
    assert B._name_problems("例题（LC 787、743）。") == "例题（LC 787 K 站中转内最便宜的航班、LC 743 网络延迟时间）。"
    assert B._name_problems("LC 743 网络延迟时间") == "LC 743 网络延迟时间"  # already named
    assert "K 站" not in B._name_problems("`LC 787`")  # code stays as written


def test_bold_is_never_split_by_its_own_comma():
    from trellis.build import _head, _html
    assert _head("**深入一，位置存储（必讲）**") == ("深入一，位置存储（必讲）", "")
    assert _head("**写多读少，用 LSM** 而不是 B+ 树，原因是顺序写")[0] == "写多读少，用 LSM"
    h = _html("**深入。**\n- **深入一，位置存储（必讲）**\n  - 1000 万司机每 5 秒上报\n  - 用 Redis 地理类型\n", fold=True)
    assert "**" not in h and "<summary>深入一，位置存储（必讲）</summary>" in h



def test_deck_depth_files_deep_nodes_into_their_ancestor(tmp_path):
    from trellis.skeleton import load_skeleton
    y = tmp_path / "d.yaml"
    y.write_text("domain: d\ntitle: D\ndeck_depth: 2\nnodes:\n- id: a\n  title: A\n  children:\n  - id: a.b\n    title: B\n"
                 "    children:\n    - id: a.b.c\n      title: C\n", encoding="utf-8")
    sk = load_skeleton(y)
    assert sk.deck_name(sk.by_id["a.b.c"]) == "D::01 A::B"
    assert sk.deck_name(sk.by_id["a"]) == "D::01 A"


def test_include_loads_cards_from_other_folders(tmp_path):
    from trellis.project import load_project
    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "m.yaml").write_text(
        "domain: m\ntitle: M\nvault: domains/m\ninclude: [domains/x]\nanki_via: ''\nnodes:\n- id: n\n  title: N\n", encoding="utf-8")
    for folder, cid in (("m", "c1"), ("x", "c2")):
        d = tmp_path / "vault" / "domains" / folder / "cards"
        d.mkdir(parents=True)
        (d / f"{cid}.md").write_text(f"---\nid: {cid}\nnode: n\ntype: qa\n---\n## Q\nq\n\n## A\na\n", encoding="utf-8")
    project = load_project(tmp_path, "m")
    assert sorted(c.id for c in project.cards) == ["c1", "c2"]


def test_deck_moves_file_a_subtree_into_another_deck(tmp_path):
    from trellis.skeleton import load_skeleton
    y = tmp_path / "d.yaml"
    y.write_text("domain: d\ntitle: D\ndeck_depth: 2\ndeck_moves:\n  a: E::11 HI\nnodes:\n- id: a\n  title: A\n  children:\n  - id: a.b\n    title: B\n"
                 "    children:\n    - id: a.b.c\n      title: C\n- id: z\n  title: Z\n", encoding="utf-8")
    sk = load_skeleton(y)
    assert sk.deck_name(sk.by_id["a.b.c"]) == "E::11 HI::B"
    assert sk.deck_name(sk.by_id["a"]) == "E::11 HI"
    assert sk.deck_name(sk.by_id["z"]) == "D::02 Z"
