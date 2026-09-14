import random

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    out = impl.part1(
        ["PUT a 1", "PUT b hello", "SHUTDOWN", "GET a", "RESTORE", "GET a", "GET missing"]
    )
    assert out == ["1", "1", "None"]


@pytest.mark.part1
def test_basic_put_get(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    assert store.get("x") is None
    store.put("x", "1")
    assert store.get("x") == "1"
    store.put("x", "2")
    assert store.get("x") == "2"


@pytest.mark.part1
def test_shutdown_restore_roundtrip(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    store.put("a", "1")
    store.put("b", "hello world")
    store.shutdown()

    store2 = impl.KVStore(fs)
    store2.restore()
    assert store2.get("a") == "1"
    assert store2.get("b") == "hello world"
    assert store2.get("missing") is None


@pytest.mark.part1
@pytest.mark.edge
def test_restore_with_no_prior_shutdown_is_empty(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    store.restore()
    assert store.get("anything") is None


@pytest.mark.part1
@pytest.mark.edge
def test_arbitrary_characters_in_keys_and_values(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    store.put("key:with:colons", "val\nwith\nnewlines")
    store.put("unicodeé中文", "你好世界\U0001f389")
    store.put("", "empty key")
    store.put("empty value", "")
    store.shutdown()

    store2 = impl.KVStore(fs)
    store2.restore()
    assert store2.get("key:with:colons") == "val\nwith\nnewlines"
    assert store2.get("unicodeé中文") == "你好世界\U0001f389"
    assert store2.get("") == "empty key"
    assert store2.get("empty value") == ""


@pytest.mark.part1
@pytest.mark.edge
def test_shutdown_overwrites_previous_value_of_same_key(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    store.put("a", "1")
    store.shutdown()
    store.put("a", "2")
    store.shutdown()

    store2 = impl.KVStore(fs)
    store2.restore()
    assert store2.get("a") == "2"


# ------------------------------------------------------------------------ Part 2 (chunking)
@pytest.mark.part2
def test_empty_store_shutdown_and_restore(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    store.shutdown()
    store2 = impl.KVStore(fs)
    store2.restore()
    assert store2.get("anything") is None


@pytest.mark.part2
def test_large_store_spans_multiple_chunks_and_roundtrips(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    for i in range(200):
        store.put(f"key{i}", "x" * 50)
    store.shutdown()

    files = fs.list_files()
    chunk_files = [f for f in files if "chunk" in f]
    assert len(chunk_files) > 1, "this much data must not fit in a single 1024-byte blob"
    for f in files:
        assert len(fs.get_blob(f)) <= 1024

    store2 = impl.KVStore(fs)
    store2.restore()
    for i in range(200):
        assert store2.get(f"key{i}") == "x" * 50


@pytest.mark.part2
@pytest.mark.edge
def test_stale_chunks_from_larger_snapshot_do_not_corrupt_restore(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    for i in range(100):
        store.put(f"k{i}", "z" * 40)
    store.shutdown()
    files_after_big_snapshot = set(fs.list_files())
    big_chunk_count = len([f for f in files_after_big_snapshot if "chunk" in f])
    assert big_chunk_count > 1

    # a brand-new store instance, replacing all data with something far smaller
    store2 = impl.KVStore(fs)
    store2.put("only", "x")
    store2.shutdown()

    # the old snapshot's chunk files are still sitting in fs, untouched
    assert files_after_big_snapshot.issubset(set(fs.list_files()))

    store3 = impl.KVStore(fs)
    store3.restore()
    assert store3.get("only") == "x"
    assert store3.get("k0") is None  # superseded snapshot must not leak through


@pytest.mark.part2
@pytest.mark.edge
def test_utf8_multibyte_character_may_straddle_a_chunk_boundary(impl):
    """Force a chunk boundary to fall in the middle of a value made almost entirely of a
    multi-byte character, then confirm the roundtrip still decodes correctly."""
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    # each "中" ("中") is 3 bytes in UTF-8; use enough of them to straddle CHUNK_SIZE=1024
    long_value = "中" * 500
    store.put("padding", "p" * 1000)
    store.put("cjk", long_value)
    store.shutdown()

    files = fs.list_files()
    assert len([f for f in files if "chunk" in f]) > 1

    store2 = impl.KVStore(fs)
    store2.restore()
    assert store2.get("cjk") == long_value
    assert store2.get("padding") == "p" * 1000


@pytest.mark.part2
@pytest.mark.perf
def test_perf_large_number_of_keys(run_script):
    rng = random.Random(0)
    lines = ["PART 2"]
    n = 3000
    for i in range(n):
        lines.append(f"PUT k{i} {'v' * rng.randint(1, 20)}")
    lines.append("SHUTDOWN")
    lines.append("RESTORE")
    lines.append("GET k0")
    r = run_script("\n".join(lines) + "\n", timeout=15)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 3 (crash atomicity)
@pytest.mark.part3
def test_fresh_instance_never_calling_restore_does_not_collide_with_committed_generation(impl):
    """A brand-new KVStore(fs) that never restored must still pick a generation number that does
    not collide with (and therefore corrupt) whatever fs already has committed."""
    fs = impl.FileSystem()
    store1 = impl.KVStore(fs)
    for i in range(100):
        store1.put(f"k{i}", "z" * 40)
    store1.shutdown()

    store2 = impl.KVStore(fs)  # simulates a fresh process; never called restore()
    store2.put("only", "x")
    store2.shutdown()

    store3 = impl.KVStore(fs)
    store3.restore()
    assert store3.get("only") == "x"
    assert store3.get("k0") is None  # store2's shutdown superseded store1's snapshot


@pytest.mark.part3
def test_crash_mid_shutdown_leaves_previous_snapshot_intact(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    store.put("a", "1")
    store.shutdown()  # generation 1 committed

    real_save_blob = fs.save_blob
    calls = {"n": 0}

    def flaky_save_blob(filename, data):
        calls["n"] += 1
        if calls["n"] > 1:
            raise OSError("simulated crash mid-shutdown")
        real_save_blob(filename, data)

    fs.save_blob = flaky_save_blob
    store.put("b", "2")
    with pytest.raises(OSError):
        store.shutdown()  # crashes after 1 successful blob write, before metadata commits

    fs.save_blob = real_save_blob
    fresh = impl.KVStore(fs)
    fresh.restore()
    assert fresh.get("a") == "1"
    assert fresh.get("b") is None  # generation 2 never committed


@pytest.mark.part3
@pytest.mark.edge
def test_crash_then_successful_retry_commits_correctly(impl):
    """After a crashed shutdown, a subsequent successful shutdown must still work (the retry is
    not permanently blocked by the earlier failure)."""
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    store.put("a", "1")
    store.shutdown()

    real_save_blob = fs.save_blob
    calls = {"n": 0}

    def flaky_save_blob(filename, data):
        calls["n"] += 1
        if calls["n"] == 2:
            raise OSError("simulated crash")
        real_save_blob(filename, data)

    fs.save_blob = flaky_save_blob
    store.put("b", "2")
    with pytest.raises(OSError):
        store.shutdown()
    fs.save_blob = real_save_blob

    store.shutdown()  # retry, no more flakiness
    fresh = impl.KVStore(fs)
    fresh.restore()
    assert fresh.get("a") == "1"
    assert fresh.get("b") == "2"


@pytest.mark.part3
@pytest.mark.edge
def test_multiple_generations_do_not_accumulate_unbounded_confusion(impl):
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    for gen in range(5):
        store.put(f"gen{gen}", str(gen))
        store.shutdown()
    fresh = impl.KVStore(fs)
    fresh.restore()
    for gen in range(5):
        assert fresh.get(f"gen{gen}") == str(gen)


@pytest.mark.part3
def test_random_cross_check_put_shutdown_restore(impl):
    rng = random.Random(0)
    fs = impl.FileSystem()
    store = impl.KVStore(fs)
    model: dict[str, str] = {}
    for _ in range(200):
        key = f"k{rng.randint(0, 30)}"
        value = "".join(rng.choice("abcXYZ \n:") for _ in range(rng.randint(0, 15)))
        store.put(key, value)
        model[key] = value
        if rng.random() < 0.15:
            store.shutdown()
            fresh = impl.KVStore(fs)
            fresh.restore()
            for k, v in model.items():
                assert fresh.get(k) == v


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_get_missing_key_literal_none_string_in_command_stream(impl):
    assert impl.part1(["GET x"]) == ["None"]


@pytest.mark.part2
@pytest.mark.fmt
def test_files_command_dash_when_empty(impl):
    assert impl.part2(["FILES"]) == ["-"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script(
        "PART 1\nPUT a 1\nPUT b hello\nSHUTDOWN\nGET a\nRESTORE\nGET a\nGET missing\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n1\nNone\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2_files(run_script):
    r = run_script("PART 2\nPUT a 1\nSHUTDOWN\nFILES\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.strip().splitlines()
    assert len(lines) == 1  # PUT and SHUTDOWN produce no output; only FILES does
    assert "meta" in lines[0]
    assert "chunk" in lines[0]
