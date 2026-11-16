import importlib
import os
import random
import sys
import threading
from collections import deque
import unicodedata

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ServiceError = impl.ServiceError
BlocklistService = impl.BlocklistService


def fails(status, code, fn, *args):
    """调用必须抛 ServiceError(status, code)。"""
    with pytest.raises(ServiceError) as info:
        fn(*args)
    assert (info.value.status, info.value.code) == (status, code)


def rejected(matches, strikes):
    return {"allowed": False, "reason": "keyword", "matches": matches, "strikes": strikes}


def blocked(strikes):
    return {"allowed": False, "reason": "user_blocked", "matches": [], "strikes": strikes}


def clean(strikes):
    return {"allowed": True, "reason": None, "matches": [], "strikes": strikes}


class Boom(Exception):
    """迭代配置时自己抛出的异常，必须原样传出。"""


def exploding(*items):
    yield from items
    raise Boom("iterator failed")


# ---- README 里的例子 ----

def test_readme_example():
    service = BlocklistService([" SPAM "])
    assert service.check("alice", "SPAM offer") == rejected(["spam"], 1)
    assert service.check("alice", "hello") == clean(1)


def test_readme_manual_block_example():
    assert BlocklistService([], ["alice"]).check("alice", "hello") == blocked(0)


# ---- 配置校验 ----

@pytest.mark.parametrize("bad", ["spam", b"spam", bytearray(b"spam"), None, 5])
def test_bare_string_bytes_or_non_iterable_is_rejected(bad):
    service = BlocklistService(["spam"], ["bob"])
    fails(400, "invalid_keywords", service.replace_keywords, bad)
    fails(400, "invalid_users", service.replace_blocked_users, bad)
    fails(400, "invalid_keywords", BlocklistService, bad)
    fails(400, "invalid_users", BlocklistService, [], bad)


@pytest.mark.parametrize("entry", [5, None, b"spam", 1.5, True, ("a",), "", " ", "\t\n", "　", "\xa0"])
def test_non_string_or_blank_entry_is_rejected(entry):
    service = BlocklistService(["spam"], ["bob"])
    fails(400, "invalid_keywords", service.replace_keywords, ["fine", entry])
    fails(400, "invalid_users", service.replace_blocked_users, ["fine", entry])
    fails(400, "invalid_keywords", BlocklistService, ["fine", entry])
    fails(400, "invalid_users", BlocklistService, ["x"], ["fine", entry])


def test_zero_width_space_is_not_blank():
    # strip() 不认零宽空格为空白，所以它是合法的关键词和用户 ID
    assert not "​".strip()  is False
    service = BlocklistService(["​"], ["​"])
    assert service.check("​", "x") == blocked(0)


def test_failed_replacement_leaves_previous_configuration_intact():
    service = BlocklistService(["spam"], ["bob"])
    fails(400, "invalid_keywords", service.replace_keywords, ["new", 5])
    fails(400, "invalid_users", service.replace_blocked_users, ["carol", ""])
    assert service.keywords == ["spam"]
    assert service.blocked_users == ["bob"]
    assert service.check("alice", "SPAM") == rejected(["spam"], 1)
    assert service.check("bob", "hello") == blocked(0)
    assert service.check("carol", "hello") == clean(0)


def test_iteration_error_propagates_unchanged_and_keeps_configuration():
    service = BlocklistService(["spam"], ["bob"])
    with pytest.raises(Boom):
        service.replace_keywords(exploding("new"))
    with pytest.raises(Boom):
        service.replace_blocked_users(exploding("carol"))
    with pytest.raises(Boom):
        BlocklistService(exploding("a"))
    with pytest.raises(Boom):
        BlocklistService(["a"], exploding("b"))
    assert service.keywords == ["spam"]
    assert service.blocked_users == ["bob"]


def test_iteration_error_wins_over_an_earlier_invalid_entry():
    # 生成器在非法条目之后才出错：条目校验是在整份读完之后做的，所以先看到的是迭代错误
    def late_failure():
        yield 5
        raise Boom("after a bad entry")

    with pytest.raises(Boom):
        BlocklistService().replace_keywords(late_failure())


def test_one_pass_iterables_are_supported_and_inputs_are_snapshotted():
    source = ["Spam", "scam"]
    service = BlocklistService(iter(source), (u for u in ["bob"]))
    source.append("fraud")
    source[0] = "other"
    assert service.keywords == ["scam", "spam"]
    assert service.check("bob", "x") == blocked(0)
    users = ["carol"]
    service.replace_blocked_users(users)
    users.clear()
    assert service.check("carol", "x") == blocked(0)
    keywords = {"a", "b"}
    service.replace_keywords(keywords)
    keywords.add("c")
    assert service.keywords == ["a", "b"]


def test_other_iterable_types_are_accepted():
    service = BlocklistService(("a",), frozenset({"bob"}))
    service.replace_keywords({"b": 1, "c": 2})  # 字典按键迭代
    assert service.keywords == ["b", "c"]
    service.replace_keywords(iter(()))
    assert service.keywords == []


# ---- 关键词规范化与匹配 ----

def test_keywords_are_stripped_casefolded_and_deduplicated():
    service = BlocklistService([" SPAM ", "spam", "Spam", "\tspam\n"])
    assert service.keywords == ["spam"]
    assert service.check("alice", "SPAM spam Spam") == rejected(["spam"], 1)


def test_keyword_is_stripped_but_content_is_not():
    service = BlocklistService([" a b "])
    assert service.check("u1", "xABy") == clean(0)  # 内部的空格要原样出现
    assert service.check("u2", "xA By") == rejected(["a b"], 1)
    padded = BlocklistService(["spam"])
    assert padded.check("u", "  SPAM  ") == rejected(["spam"], 1)  # 内容两端的空白不影响命中


def test_matching_is_literal_substring_not_word_or_regex():
    service = BlocklistService(["ass", "a.c", "^spam", "(x"])
    assert service.check("u1", "Classic") == rejected(["ass"], 1)  # 词中间也算命中
    assert service.check("u2", "abc") == clean(0)  # "." 不是通配
    assert service.check("u3", "a.c") == rejected(["a.c"], 1)
    assert service.check("u4", "say ^SPAM now") == rejected(["^spam"], 1)  # "^" 不是锚点
    assert service.check("u5", "f(x)") == rejected(["(x"], 1)  # 括号不会触发正则错误


def test_matches_are_unique_overlapping_and_sorted():
    service = BlocklistService(["foobar", "oba", "foo", "bar", "FOO"])
    assert service.check("u", "FooBar") == rejected(["bar", "foo", "foobar", "oba"], 1)
    spread = BlocklistService(["b", "a", "ab"])
    assert spread.check("u", "AB ab ab") == rejected(["a", "ab", "b"], 1)


def test_matches_follow_python_string_order_not_locale():
    service = BlocklistService(["é", "z", "ß", "Z", "a"])  # ß 先折成 ss，再参与排序
    result = service.check("u", "é z ß a")["matches"]
    assert result == sorted(result) == ["a", "ss", "z", "é"]


def test_empty_and_blank_content_is_valid_and_matches_nothing():
    service = BlocklistService(["spam"])
    assert service.check("alice", "") == clean(0)
    assert service.check("alice", "   ") == clean(0)
    assert service.state("alice") == {"strikes": 0, "blocked": False}


def test_empty_keyword_list_allows_everything():
    service = BlocklistService()
    assert service.check("alice", "anything at all") == clean(0)


def test_casefold_is_used_not_lower():
    # casefold 把 ß 折成 ss，lower 不会；希腊词尾 ς 折成 σ
    assert "ß".casefold() == "ss" and "ß".lower() == "ß"
    service = BlocklistService(["straße", "οδος"])
    assert service.keywords == ["strasse", "οδοσ"]
    assert service.check("u1", "STRASSE") == rejected(["strasse"], 1)
    assert service.check("u2", "ΟΔΟΣ") == rejected(["οδοσ"], 1)
    assert BlocklistService(["ss"]).check("u", "Straße") == rejected(["ss"], 1)  # 折叠后的子串也算


def test_no_unicode_normalization_beyond_casefold():
    nfc, nfd = "é", "é"
    assert unicodedata.normalize("NFD", nfc) == nfd
    assert BlocklistService([nfc]).check("u", nfd) == clean(0)  # 预组合与组合序列不互认
    assert BlocklistService([nfd]).check("u", nfc) == clean(0)
    assert BlocklistService(["e"]).check("u", nfd) == rejected(["e"], 1)  # 但基字符是子串
    # İ 折成 i + 组合点，所以 "i" 命中，"istanbul" 不命中
    assert BlocklistService(["i"]).check("u", "İstanbul") == rejected(["i"], 1)
    assert BlocklistService(["istanbul"]).check("u", "İstanbul") == clean(0)


# ---- 用户校验与状态 ----

@pytest.mark.parametrize("user", [None, 5, b"alice", "", " ", "\t\n", ["alice"]])
def test_invalid_user_is_rejected_before_any_accounting(user):
    service = BlocklistService(["spam"])
    fails(400, "invalid_input", service.check, user, "spam")
    fails(400, "invalid_input", service.state, user)
    assert service.state("alice") == {"strikes": 0, "blocked": False}


@pytest.mark.parametrize("content", [None, 5, b"spam", ["spam"]])
def test_invalid_content_is_rejected_before_matching_and_accounting(content):
    service = BlocklistService(["spam"], ["bob"])
    fails(400, "invalid_input", service.check, "alice", content)
    fails(400, "invalid_input", service.check, "bob", content)  # 被封的用户也先校验输入
    assert service.state("alice") == {"strikes": 0, "blocked": False}
    assert service.state("bob") == {"strikes": 0, "blocked": True}


def test_user_ids_are_case_sensitive_and_kept_exactly():
    service = BlocklistService(["spam"], [" bob "])
    assert service.check("bob", "hi") == clean(0)  # 名单里是 " bob "，不是 "bob"
    assert service.check(" bob ", "hi") == blocked(0)
    assert service.check("Alice", "spam") == rejected(["spam"], 1)
    assert service.check("alice", "spam") == rejected(["spam"], 1)
    assert service.check(" alice", "spam") == rejected(["spam"], 1)
    assert service.check("Alice", "spam") == rejected(["spam"], 2)
    assert service.state("Alice")["strikes"] == 2
    assert service.state("alice")["strikes"] == 1
    assert service.state(" alice")["strikes"] == 1
    assert service.state("ALICE")["strikes"] == 0


def test_state_shape_for_unknown_user_and_returns_a_fresh_dict():
    service = BlocklistService(["spam"])
    snapshot = service.state("nobody")
    assert snapshot == {"strikes": 0, "blocked": False}
    assert type(snapshot["strikes"]) is int and type(snapshot["blocked"]) is bool
    snapshot["strikes"] = 99
    snapshot["blocked"] = True
    assert service.state("nobody") == {"strikes": 0, "blocked": False}


def test_state_does_not_change_anything():
    service = BlocklistService(["spam"])
    for _ in range(5):
        service.state("alice")
    assert service.check("alice", "spam") == rejected(["spam"], 1)


# ---- 违规计数与封禁 ----

def test_third_rejection_is_still_keyword_then_blocked():
    service = BlocklistService(["spam"])
    assert service.check("alice", "spam") == rejected(["spam"], 1)
    assert service.check("alice", "spam") == rejected(["spam"], 2)
    assert service.check("alice", "spam") == rejected(["spam"], 3)
    assert service.state("alice") == {"strikes": 3, "blocked": True}
    assert service.check("alice", "spam") == blocked(3)
    assert service.check("alice", "hello") == blocked(3)  # 干净内容也被拒
    assert service.check("alice", "") == blocked(3)
    assert service.state("alice") == {"strikes": 3, "blocked": True}  # 次数不再增加


def test_one_strike_per_rejected_request_whatever_the_matches():
    service = BlocklistService(["spam", "scam", "fraud"])
    assert service.check("alice", "spam scam fraud spam spam") == rejected(["fraud", "scam", "spam"], 1)
    assert service.state("alice")["strikes"] == 1


def test_clean_request_neither_resets_nor_adds():
    service = BlocklistService(["spam"])
    assert service.check("alice", "spam") == rejected(["spam"], 1)
    assert service.check("alice", "hello") == clean(1)
    assert service.check("alice", "hello again") == clean(1)
    assert service.check("alice", "spam") == rejected(["spam"], 2)


def test_manual_block_wins_over_keyword_and_adds_no_strike():
    service = BlocklistService(["spam"], ["alice"])
    assert service.check("alice", "spam spam") == blocked(0)
    assert service.state("alice") == {"strikes": 0, "blocked": True}
    # 别的用户不受影响
    assert service.check("bob", "spam") == rejected(["spam"], 1)


def test_manual_block_keeps_the_strikes_already_counted():
    service = BlocklistService(["spam"])
    service.check("alice", "spam")
    service.check("alice", "spam")
    service.replace_blocked_users(["alice"])
    assert service.check("alice", "spam") == blocked(2)
    assert service.state("alice") == {"strikes": 2, "blocked": True}


# ---- 配置更新 ----

def test_replace_keywords_replaces_the_whole_set_and_empty_clears():
    service = BlocklistService(["spam"])
    service.replace_keywords(["scam"])
    assert service.check("u1", "spam") == clean(0)
    assert service.check("u2", "SCAM") == rejected(["scam"], 1)
    service.replace_keywords([])
    assert service.check("u3", "scam") == clean(0)
    assert service.keywords == []


def test_replace_keywords_keeps_strikes_and_automatic_blocks():
    service = BlocklistService(["spam"])
    for _ in range(3):
        service.check("alice", "spam")
    service.check("bob", "spam")
    service.replace_keywords([])
    assert service.state("alice") == {"strikes": 3, "blocked": True}
    assert service.state("bob") == {"strikes": 1, "blocked": False}
    assert service.check("alice", "hello") == blocked(3)
    service.replace_keywords(["hello"])
    assert service.check("bob", "hello") == rejected(["hello"], 2)


def test_replace_blocked_users_replaces_the_whole_set_and_empty_clears():
    service = BlocklistService([], ["alice", "bob"])
    service.replace_blocked_users(["carol"])
    assert service.check("alice", "x") == clean(0)
    assert service.check("carol", "x") == blocked(0)
    service.replace_blocked_users([])
    assert service.check("carol", "x") == clean(0)
    assert service.blocked_users == []


def test_removing_a_manual_block_unblocks_only_below_three_strikes():
    service = BlocklistService(["spam"])
    for _ in range(3):
        service.check("bob", "spam")
    service.replace_blocked_users(["alice", "bob"])
    assert service.check("alice", "hello") == blocked(0)
    service.replace_blocked_users([])
    assert service.state("bob") == {"strikes": 3, "blocked": True}  # 次数够了，移出名单也没用
    assert service.check("bob", "hello") == blocked(3)
    assert service.state("alice") == {"strikes": 0, "blocked": False}  # 次数不够，移出名单就解封
    assert service.check("alice", "hello") == clean(0)


def test_manual_block_added_later_applies_immediately():
    service = BlocklistService(["spam"])
    assert service.check("alice", "hello") == clean(0)
    service.replace_blocked_users(["alice"])
    assert service.check("alice", "hello") == blocked(0)


# ---- 隔离 ----

def test_instances_do_not_share_state():
    first, second = BlocklistService(["spam"], ["bob"]), BlocklistService(["spam"])
    for _ in range(3):
        first.check("alice", "spam")
    assert second.state("alice") == {"strikes": 0, "blocked": False}
    assert second.check("bob", "hi") == clean(0)
    first.replace_keywords([])
    assert second.check("carol", "spam") == rejected(["spam"], 1)
    assert BlocklistService().keywords == []  # 默认参数不是共享的可变对象


def test_returned_values_are_snapshots():
    service = BlocklistService(["spam", "scam"], ["bob"])
    first = service.check("alice", "spam scam")
    first["matches"].append("injected")
    first["strikes"] = 99
    second = service.check("carol", "spam scam")
    assert second == rejected(["scam", "spam"], 1)
    assert second["matches"] is not first["matches"]
    names = service.keywords
    names.append("injected")
    service.blocked_users.append("injected")
    assert service.keywords == ["scam", "spam"]
    assert service.blocked_users == ["bob"]
    assert service.check("dave", "injected") == clean(0)


def test_blocked_and_clean_results_are_fresh_each_time():
    service = BlocklistService(["spam"], ["bob"])
    one, two = service.check("bob", "x"), service.check("bob", "x")
    assert one == two and one is not two and one["matches"] is not two["matches"]
    three, four = service.check("u", "x"), service.check("u", "x")
    three["matches"].append("x")
    assert four["matches"] == []


# ---- 并发 ----

@pytest.fixture
def fast_switching():
    """把线程切换间隔压到最小，让没有锁保护的检查再动作更容易露馅。"""
    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    yield
    sys.setswitchinterval(old)


def run_threads(count, target):
    """用屏障让线程同时起跑，返回每个线程 target(i) 的结果。"""
    barrier = threading.Barrier(count)
    results = [None] * count
    errors = []

    def worker(i):
        try:
            barrier.wait()
            results[i] = target(i)
        except BaseException as exc:  # 线程里的失败要带回主线程
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors, errors
    return results


def test_concurrent_rejections_for_one_user_stop_at_exactly_three_strikes(fast_switching):
    for round_no in range(30):  # 竞争窗口很窄，多跑几轮，每轮一个全新的服务
        service = BlocklistService(["spam"])
        batches = run_threads(40, lambda i: [service.check("alice", "spam") for _ in range(5)])
        results = [r for batch in batches for r in batch]
        keyword = [r for r in results if r["reason"] == "keyword"]
        assert sorted(r["strikes"] for r in keyword) == [1, 2, 3]
        assert all(r == blocked(3) for r in results if r["reason"] == "user_blocked")
        assert len(results) == 200
        assert service.state("alice") == {"strikes": 3, "blocked": True}


def test_concurrent_checks_for_different_users_do_not_lose_strikes(fast_switching):
    service = BlocklistService(["spam"])
    users = [f"user{i}" for i in range(20)]
    run_threads(40, lambda i: [service.check(users[i % 20], "spam") for _ in range(2)])
    # 每个用户被两个线程各拒两次，共四次尝试：前三次 keyword，第四次 user_blocked
    assert all(service.state(user) == {"strikes": 3, "blocked": True} for user in users)


def test_concurrent_mixed_clean_and_bad_requests_count_only_the_bad_ones(fast_switching):
    service = BlocklistService(["spam"])
    run_threads(60, lambda i: service.check("alice", "spam" if i % 3 == 0 else "hello"))
    assert service.state("alice")["strikes"] == 3  # 20 个坏请求，只有 3 个落账，其余是 user_blocked 或 clean


def test_a_configuration_swap_is_seen_whole_by_every_check(fast_switching):
    service = BlocklistService(["a", "b"])
    sets = (["a", "b"], ["c", "d"])
    stop = threading.Event()

    def swapper():
        flip = 0
        while not stop.is_set():
            flip ^= 1
            service.replace_keywords(sets[flip])

    thread = threading.Thread(target=swapper)
    thread.start()
    try:
        results = run_threads(8, lambda i: [service.check(f"u{i}-{n}", "a b c d")["matches"] for n in range(300)])
    finally:
        stop.set()
        thread.join()
    seen = {tuple(m) for batch in results for m in batch}
    assert seen <= {("a", "b"), ("c", "d")}, seen  # 永远是整份旧表或整份新表，没有混合


def test_manual_block_swap_races_with_checks_without_corrupting_strikes(fast_switching):
    service = BlocklistService(["spam"])

    def work(i):
        if i == 0:
            for _ in range(200):
                service.replace_blocked_users(["alice"])
                service.replace_blocked_users([])
        else:
            return [service.check("alice", "spam")["strikes"] for _ in range(50)]

    results = run_threads(5, work)
    counts = [s for batch in results[1:] for s in batch]
    assert max(counts) <= 3
    assert service.state("alice")["strikes"] <= 3


# ---- 辅助类 ----

def test_strike_ledger_never_exceeds_its_limit():
    ledger = impl.StrikeLedger(2)
    assert (ledger.count("a"), ledger.exhausted("a")) == (0, False)
    assert ledger.add("a") == 1
    assert ledger.add("a") == 2 and ledger.exhausted("a")
    with pytest.raises(RuntimeError):
        ledger.add("a")
    assert ledger.count("a") == 2 and ledger.count("b") == 0


# ---- 扩展：关键词表很大时，自动机与逐词扫描给出同样的结果 ----

class Automaton:
    """Aho–Corasick：把所有关键词编成一棵带失败指针的字典树，扫一遍内容就得到全部命中。"""

    def __init__(self, words):
        self.goto, self.out, self.fail = [{}], [set()], [0]
        for word in words:
            node = 0
            for ch in word:
                if ch not in self.goto[node]:
                    self.goto.append({})
                    self.out.append(set())
                    self.fail.append(0)
                    self.goto[node][ch] = len(self.goto) - 1
                node = self.goto[node][ch]
            self.out[node].add(word)
        queue = deque(self.goto[0].values())
        while queue:  # 按层构造失败指针，并把失败链上的词并进 out
            node = queue.popleft()
            for ch, nxt in self.goto[node].items():
                back = self.fail[node]
                while back and ch not in self.goto[back]:
                    back = self.fail[back]
                self.fail[nxt] = self.goto[back].get(ch, 0)
                self.out[nxt] |= self.out[self.fail[nxt]]
                queue.append(nxt)

    def find(self, content):
        node, hits = 0, set()
        for ch in content.casefold():
            while node and ch not in self.goto[node]:
                node = self.fail[node]
            node = self.goto[node].get(ch, 0)
            hits |= self.out[node]
        return sorted(hits)


def test_automaton_finds_exactly_what_the_linear_scan_finds():
    rng = random.Random(7)  # 固定种子；随机的是输入，不是断言

    def word():
        return "".join(rng.choice("abcde") for _ in range(rng.randint(1, 6)))

    for _ in range(500):
        compiled = impl.Keywords.compile({word() for _ in range(rng.randint(1, 12))})
        content = "".join(rng.choice("abcdeABC ") for _ in range(rng.randint(0, 25)))
        assert Automaton(compiled.words).find(content) == compiled.find(content)
