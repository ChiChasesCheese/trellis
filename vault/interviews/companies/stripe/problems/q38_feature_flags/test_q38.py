import random
import zlib

import pytest


def check(impl, lines):
    return impl.process(lines)


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_boolean_allow_deny(impl):
    out = check(impl, ["FLAG,dark,on", "FLAG,killed,off,allow=alice", "FLAG,vip,on,allow=alice|bob,deny=bob",
                       "CHECK,dark,alice", "CHECK,killed,alice", "CHECK,vip,alice", "CHECK,vip,bob",
                       "CHECK,vip,carol", "CHECK,nope,alice"])
    assert out == ["dark,alice,ON", "killed,alice,OFF", "vip,alice,ON", "vip,bob,OFF",
                   "vip,carol,ON", "nope,alice,OFF"]


@pytest.mark.part1
@pytest.mark.edge
def test_off_beats_allow_and_deny_beats_allow(impl):
    ff = impl.FeatureFlags()
    ff.add_flag(impl.Flag("f", False, allow=frozenset({"a"})))
    assert ff.is_enabled("f", "a") is False
    ff.add_flag(impl.Flag("f", True, allow=frozenset({"a"}), deny=frozenset({"a"})))
    assert ff.is_enabled("f", "a") is False
    assert ff.is_enabled("f", "b") is True     # nobody else is denied; no other rule


@pytest.mark.part1
@pytest.mark.edge
def test_empty_unknown_and_redeclare(impl):
    assert check(impl, []) == []
    assert check(impl, ["CHECK,f,u"]) == ["f,u,OFF"]
    assert check(impl, ["FLAG,f,on", "FLAG,f,off", "CHECK,f,u"]) == ["f,u,OFF"]
    assert check(impl, ["FLAG,f,off", "FLAG,f,on", "CHECK,f,u"]) == ["f,u,ON"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_rollout_50(impl):
    out = check(impl, ["FLAG,newui,on,rollout=50", "CHECK,newui,alice", "CHECK,newui,bob",
                       "CHECK,newui,carol", "CHECK,newui,dave"])
    assert out == ["newui,alice,ON", "newui,bob,ON", "newui,carol,ON", "newui,dave,OFF"]


@pytest.mark.part2
@pytest.mark.edge
def test_rollout_boundary_is_strict(impl):
    assert impl.bucket("newui", "u1") == 54 == zlib.crc32(b"newui:u1") % 100
    ff = impl.FeatureFlags()
    ff.add_flag(impl.Flag("newui", True, rollout=54))
    assert ff.is_enabled("newui", "u1") is False
    ff.add_flag(impl.Flag("newui", True, rollout=55))
    assert ff.is_enabled("newui", "u1") is True


@pytest.mark.part2
@pytest.mark.edge
def test_rollout_zero_and_hundred_and_per_flag_buckets(impl):
    ff = impl.FeatureFlags()
    ff.add_flag(impl.Flag("a", True, rollout=0))
    ff.add_flag(impl.Flag("b", True, rollout=100))
    assert all(ff.is_enabled("a", f"u{i}") is False for i in range(50))
    assert all(ff.is_enabled("b", f"u{i}") is True for i in range(50))
    assert impl.bucket("newui", "carol") == 5 and impl.bucket("beta", "carol") == 2


@pytest.mark.part2
def test_rollout_matches_crc_for_many_users(impl):
    ff = impl.FeatureFlags()
    ff.add_flag(impl.Flag("x", True, rollout=30))
    for i in range(200):
        u = f"user{i}"
        assert ff.is_enabled("x", u) is (zlib.crc32(f"x:{u}".encode()) % 100 < 30)


@pytest.mark.part2
@pytest.mark.edge
def test_allowlist_bypasses_rollout(impl):
    ff = impl.FeatureFlags()
    ff.add_flag(impl.Flag("newui", True, rollout=0, allow=frozenset({"dave"})))
    assert ff.is_enabled("newui", "dave") is True


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_attributes(impl):
    out = check(impl, ["USER,alice,country=US,plan=pro", "USER,bob,country=DE,plan=pro", "USER,carol,country=US",
                       "FLAG,tax,on,country=US|CA,plan=pro|enterprise",
                       "CHECK,tax,alice", "CHECK,tax,bob", "CHECK,tax,carol",
                       "FLAG,ab,on,ab=even", "CHECK,ab,u2", "CHECK,ab,u3"])
    assert out == ["tax,alice,ON", "tax,bob,OFF", "tax,carol,OFF", "ab,u2,ON", "ab,u3,OFF"]


@pytest.mark.part3
@pytest.mark.edge
def test_or_within_key_and_unknown_user(impl):
    lines = ["USER,ca,country=CA,plan=enterprise", "FLAG,tax,on,country=US|CA,plan=pro|enterprise",
             "CHECK,tax,ca", "CHECK,tax,ghost"]
    assert check(impl, lines) == ["tax,ca,ON", "tax,ghost,OFF"]


@pytest.mark.part3
@pytest.mark.edge
def test_ab_even_variant_edges(impl):
    ff = impl.FeatureFlags()
    ff.add_flag(impl.Flag("ab", True, rules={"ab": {"even"}}))
    assert ff.is_enabled("ab", "0") is True
    assert ff.is_enabled("ab", "user10") is True
    assert ff.is_enabled("ab", "user7") is False
    assert ff.is_enabled("ab", "nodigits") is False


@pytest.mark.part3
def test_parse_flag_options(impl):
    f = impl.parse_flag(["newui", "on", "rollout=25", "allow=a|b", "deny=c", "requires=x|y", "country=US"])
    assert f.name == "newui" and f.on and f.rollout == 25
    assert f.allow == {"a", "b"} and f.deny == {"c"} and tuple(f.requires) == ("x", "y")
    assert f.rules == {"country": {"US"}}


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_dependencies(impl):
    out = check(impl, ["FLAG,base,on,country=US", "FLAG,addon,on,requires=base,allow=bob",
                       "USER,alice,country=US", "USER,bob,country=DE",
                       "CHECK,addon,alice", "CHECK,addon,bob",
                       "FLAG,x,on,requires=y", "FLAG,y,on,requires=x", "CHECK,x,alice"])
    assert out == ["addon,alice,ON", "addon,bob,OFF", "x,alice,OFF"]


@pytest.mark.part4
@pytest.mark.edge
def test_missing_dependency_chain_and_self_cycle(impl):
    assert check(impl, ["FLAG,a,on,requires=missing", "CHECK,a,u"]) == ["a,u,OFF"]
    lines = ["FLAG,c,on,rollout=0", "FLAG,b,on,requires=c", "FLAG,a,on,requires=b", "CHECK,a,u",
             "FLAG,c,on", "CHECK,a,u", "FLAG,s,on,requires=s", "CHECK,s,u"]
    assert check(impl, lines) == ["a,u,OFF", "a,u,ON", "s,u,OFF"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("FLAG,newui,on,rollout=50\n\nCHECK,newui,alice\nCHECK,newui,dave\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "newui,alice,ON\nnewui,dave,OFF\n"
    assert run_script("").stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_checks(run_script):
    rng = random.Random(0)
    lines = [f"USER,u{i},country={rng.choice(['US', 'CA', 'DE'])},plan={rng.choice(['free', 'pro'])}"
             for i in range(10_000)]
    lines.append("FLAG,base,on,country=US|CA,rollout=80")
    for i in range(10):   # dependency chain 10 deep: f9 -> f8 -> ... -> f0 -> base
        lines.append(f"FLAG,f{i},on,requires={'base' if i == 0 else f'f{i - 1}'},rollout={rng.randrange(90, 101)}")
    lines += [f"CHECK,f{rng.randrange(10)},u{rng.randrange(10_000)}" for _ in range(100_000)]
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_000 and ",ON" in r.stdout and ",OFF" in r.stdout
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
