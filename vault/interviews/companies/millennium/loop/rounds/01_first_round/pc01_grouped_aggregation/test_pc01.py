import random
from decimal import Decimal

import pytest

WORKED_LINES = ["A,10.50", "B,5.25", "A,3.75", "C,100", "B,0.75"]
WORKED_PART1 = ["A,14.25", "B,6.00", "C,100.00"]

WORKED_PART3_LINES = [
    "A,groceries,10.50",
    "A,transport,4.00",
    "A,groceries,3.75",
    "B,groceries,100",
    "A,groceries,-1.25",
]
WORKED_PART3 = [
    "A,groceries,13.00,3,10.50",
    "A,transport,4.00,1,4.00",
    "B,groceries,100.00,1,100.00",
]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_part1(impl):
    assert impl.part1(WORKED_LINES) == WORKED_PART1


@pytest.mark.part1
@pytest.mark.edge
def test_part1_empty_input(impl):
    assert impl.group_sum_streaming([]) == {}
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_part1_single_record(impl):
    assert impl.group_sum_streaming(["A,10"]) == {"A": Decimal("10.00")}


@pytest.mark.part1
@pytest.mark.edge
def test_part1_duplicate_ids_accumulate(impl):
    totals = impl.group_sum_streaming(["A,1", "A,2", "A,3"])
    assert totals == {"A": Decimal("6.00")}


@pytest.mark.part1
@pytest.mark.edge
def test_part1_negative_amounts(impl):
    totals = impl.group_sum_streaming(["A,10", "A,-4.50"])
    assert totals == {"A": Decimal("5.50")}


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "bad_lines",
    [["A"], ["A,1,2"], ["A,not-a-number"], [",10"], ["A,"]],
)
def test_part1_invalid_rows_raise(impl, bad_lines):
    with pytest.raises(ValueError):
        impl.group_sum_streaming(bad_lines)


@pytest.mark.part1
@pytest.mark.fmt
def test_part1_output_sorted_and_two_decimals(impl):
    out = impl.part1(["C,1", "A,2.5", "B,3"])
    assert out == ["A,2.50", "B,3.00", "C,1.00"]


@pytest.mark.part1
@pytest.mark.io
def test_part1_io(run_script):
    r = run_script("PART 1\nA,10.50\nB,5.25\nA,3.75\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A,14.25\nB,5.25\n"


@pytest.mark.part1
@pytest.mark.edge
def test_group_sum_matches_pandas_groupby(impl):
    pd = pytest.importorskip("pandas")
    import io as _io

    rng = random.Random(3)
    ids = [f"id{i}" for i in range(20)]
    rows = [(rng.choice(ids), rng.randint(1, 10_000) / 100) for _ in range(2000)]
    lines = [f"{k},{v:.2f}" for k, v in rows]

    got = impl.group_sum_streaming(lines)

    csv_text = "id,amount\n" + "\n".join(lines)
    df = pd.read_csv(_io.StringIO(csv_text))
    expected = df.groupby("id")["amount"].sum()
    for key, total in got.items():
        assert float(total) == pytest.approx(float(expected[key]), abs=0.01)
    assert set(got) == set(expected.index)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_part2(impl):
    lines = ["CHUNK_SIZE 2"] + WORKED_LINES
    assert impl.part2(lines) == WORKED_PART1


@pytest.mark.part2
@pytest.mark.edge
@pytest.mark.parametrize("chunk_size", [1, 2, 3, 5, 100])
def test_chunked_matches_streaming_for_various_chunk_sizes(impl, chunk_size):
    expected = impl.group_sum_streaming(WORKED_LINES)
    got = impl.chunked_group_sum(WORKED_LINES, chunk_size)
    assert got == expected


@pytest.mark.part2
@pytest.mark.edge
def test_chunked_with_workers_matches_sequential(impl):
    rng = random.Random(1)
    ids = [f"id{i}" for i in range(50)]
    lines = [f"{rng.choice(ids)},{rng.randint(1, 100_00) / 100:.2f}" for _ in range(5000)]
    sequential = impl.chunked_group_sum(lines, chunk_size=200, workers=1)
    parallel = impl.chunked_group_sum(lines, chunk_size=200, workers=4)
    assert parallel == sequential


@pytest.mark.part2
@pytest.mark.edge
def test_chunked_empty_input(impl):
    assert impl.chunked_group_sum([], chunk_size=10) == {}


@pytest.mark.part2
@pytest.mark.edge
@pytest.mark.parametrize("bad_chunk_size", [0, -1])
def test_chunk_size_must_be_positive(impl, bad_chunk_size):
    with pytest.raises(ValueError):
        impl.chunked_group_sum(WORKED_LINES, chunk_size=bad_chunk_size)


@pytest.mark.part2
@pytest.mark.edge
def test_workers_must_be_positive(impl):
    with pytest.raises(ValueError):
        impl.chunked_group_sum(WORKED_LINES, chunk_size=2, workers=0)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_500k_rows_chunked(impl):
    import time

    rng = random.Random(0)
    ids = [f"id{i}" for i in range(2000)]
    rows = [f"{rng.choice(ids)},{rng.randint(1, 100_000) / 100:.2f}" for _ in range(500_000)]

    t0 = time.perf_counter()
    totals = impl.chunked_group_sum(rows, chunk_size=50_000, workers=4)
    elapsed = time.perf_counter() - t0

    assert len(totals) == 2000
    assert elapsed < 2.0, f"took {elapsed:.2f}s"


@pytest.mark.part2
@pytest.mark.io
def test_part2_io(run_script):
    r = run_script("PART 2\nCHUNK_SIZE 2\nA,10.50\nB,5.25\nA,3.75\nC,1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A,14.25\nB,5.25\nC,1.00\n"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_part3(impl):
    assert impl.part3(WORKED_PART3_LINES) == WORKED_PART3


@pytest.mark.part3
@pytest.mark.edge
def test_part3_sum_count_max_single_group(impl):
    groups = impl.multi_key_aggregate(["A,g,1", "A,g,2", "A,g,3"])
    assert groups[("A", "g")] == {"sum": Decimal("6.00"), "count": 3, "max": Decimal("3.00")}


@pytest.mark.part3
@pytest.mark.edge
def test_part3_empty_input(impl):
    assert impl.multi_key_aggregate([]) == {}
    assert impl.part3([]) == []


@pytest.mark.part3
@pytest.mark.edge
@pytest.mark.parametrize(
    "bad_lines",
    [["A,g"], ["A,g,1,2"], ["A,g,xyz"], [",g,1"], ["A,,1"]],
)
def test_part3_invalid_rows_raise(impl, bad_lines):
    with pytest.raises(ValueError):
        impl.multi_key_aggregate(bad_lines)


@pytest.mark.part3
@pytest.mark.fmt
def test_part3_output_sorted_by_composite_key(impl):
    out = impl.part3(["B,x,1", "A,y,1", "A,x,1"])
    assert out == ["A,x,1.00,1,1.00", "A,y,1.00,1,1.00", "B,x,1.00,1,1.00"]


@pytest.mark.part3
@pytest.mark.io
def test_part3_io(run_script):
    r = run_script("PART 3\nA,g,1\nA,g,2\nB,h,5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A,g,3.00,2,2.00\nB,h,5.00,1,5.00\n"
