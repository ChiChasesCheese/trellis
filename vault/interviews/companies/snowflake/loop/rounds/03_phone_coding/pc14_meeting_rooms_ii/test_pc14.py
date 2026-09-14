import random

import pytest


def _brute_min_rooms(intervals):
    """Independent event-sweep re-implementation (not the two-pointer algorithm under test)."""
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()  # ties: -1 (end) sorts before +1 (start) at the same timestamp -- half-open
    cur = best = 0
    for _, delta in events:
        cur += delta
        best = max(best, cur)
    return best


def _overlaps(a, b):
    return max(a[0], b[0]) < min(a[1], b[1])


def _brute_capacity_assign(meetings, capacities):
    """Independent re-implementation of the documented Part3 greedy, using plain loops instead of
    comprehensions/heaps, to catch implementation-specific bugs rather than algorithm-design bugs."""
    order = sorted(range(len(meetings)), key=lambda i: (meetings[i][0], i))
    free_at = [0 for _ in capacities]
    result = [None] * len(meetings)
    for i in order:
        start, end, size = meetings[i]
        best_room = None
        for r in range(len(capacities)):
            if capacities[r] < size or free_at[r] > start:
                continue
            if best_room is None or (capacities[r], r) < (capacities[best_room], best_room):
                best_room = r
        if best_room is not None:
            result[i] = best_room
            free_at[best_room] = end
    return result


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2


@pytest.mark.part1
def test_worked_example_2(impl):
    assert impl.min_meeting_rooms([[7, 10], [2, 4]]) == 1


@pytest.mark.part1
def test_touching_endpoints_do_not_conflict(impl):
    assert impl.min_meeting_rooms([[1, 5], [5, 10]]) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_empty_intervals(impl):
    assert impl.min_meeting_rooms([]) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_zero_or_negative_duration_raises(impl):
    with pytest.raises(ValueError):
        impl.min_meeting_rooms([[5, 5]])


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_interval_raises(impl):
    with pytest.raises(ValueError):
        impl.min_meeting_rooms([[5, 3]])
    with pytest.raises(ValueError):
        impl.min_meeting_rooms([[1, 2, 3]])


@pytest.mark.part1
@pytest.mark.edge
def test_all_overlap_needs_n_rooms(impl):
    assert impl.min_meeting_rooms([[0, 10]] * 5) == 5


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_event_sweep(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(0, 10)
        intervals = []
        for _ in range(n):
            st = rng.randint(0, 20)
            intervals.append([st, st + rng.randint(1, 10)])
        assert impl.min_meeting_rooms(intervals) == _brute_min_rooms(intervals), intervals


@pytest.mark.part1
@pytest.mark.perf
def test_perf_200000_intervals(run_script):
    rng = random.Random(0)
    n = 200_000
    lines = [f"N {n}"]
    for _ in range(n):
        st = rng.randint(0, 10**9)
        lines.append(f"{st} {st + rng.randint(1, 1000)}")
    r = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example_1(impl):
    assert impl.assign_rooms([[0, 30], [5, 10], [15, 20]]) == [0, 1, 1]


@pytest.mark.part2
def test_part2_worked_example_4_lowest_free_room_id(impl):
    assert impl.assign_rooms([[0, 5], [0, 5], [1, 2], [6, 7]]) == [0, 1, 2, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_empty(impl):
    assert impl.assign_rooms([]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_uses_exactly_min_rooms_and_no_overlap_shares_a_room(impl):
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 10)
        intervals = []
        for _ in range(n):
            st = rng.randint(0, 20)
            intervals.append([st, st + rng.randint(1, 10)])
        assignment = impl.assign_rooms(intervals)
        expected_rooms = impl.min_meeting_rooms(intervals)
        assert (max(assignment) + 1 if assignment else 0) == expected_rooms
        for i in range(n):
            for j in range(i + 1, n):
                if assignment[i] == assignment[j]:
                    assert not _overlaps(intervals[i], intervals[j]), (intervals, assignment)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_deterministic(impl):
    intervals = [[0, 5], [0, 5], [1, 2], [6, 7]]
    assert impl.assign_rooms(intervals) == impl.assign_rooms(intervals)


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_lines(impl):
    assert impl.part2(["N 3", "0 30", "5 10", "15 20"]) == ["0", "1", "1"]


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_example_5(impl):
    meetings = [(0, 10, 3), (1, 2, 1), (2, 3, 1)]
    assert impl.assign_rooms_with_capacity(meetings, [1, 3]) == [1, 0, 0]


@pytest.mark.part3
def test_part3_worked_example_6_unschedulable(impl):
    meetings = [(0, 5, 3), (0, 5, 3), (0, 5, 3)]
    assert impl.assign_rooms_with_capacity(meetings, [3, 3]) == [0, 1, None]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_empty(impl):
    assert impl.assign_rooms_with_capacity([], []) == []


@pytest.mark.part3
@pytest.mark.edge
def test_part3_no_rooms_all_unschedulable(impl):
    assert impl.assign_rooms_with_capacity([(0, 1, 1)], []) == [None]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_negative_capacity_raises(impl):
    with pytest.raises(ValueError):
        impl.assign_rooms_with_capacity([(0, 1, 1)], [-1])


@pytest.mark.part3
@pytest.mark.edge
def test_part3_nonpositive_size_raises(impl):
    with pytest.raises(ValueError):
        impl.assign_rooms_with_capacity([(0, 1, 0)], [1])


@pytest.mark.part3
@pytest.mark.edge
def test_part3_invalid_meeting_raises(impl):
    with pytest.raises(ValueError):
        impl.assign_rooms_with_capacity([(5, 3, 1)], [1])


@pytest.mark.part3
@pytest.mark.edge
def test_part3_matches_documented_greedy_on_random_inputs(impl):
    rng = random.Random(2)
    for _ in range(300):
        n_meetings = rng.randint(0, 8)
        n_rooms = rng.randint(0, 4)
        capacities = [rng.randint(1, 5) for _ in range(n_rooms)]
        meetings = []
        for _ in range(n_meetings):
            st = rng.randint(0, 10)
            en = st + rng.randint(1, 5)
            meetings.append((st, en, rng.randint(1, 5)))
        assert impl.assign_rooms_with_capacity(meetings, capacities) == _brute_capacity_assign(
            meetings, capacities
        ), (meetings, capacities)


@pytest.mark.part3
@pytest.mark.fmt
def test_part3_output_lines(impl):
    lines = ["N 3", "0 10 3", "1 2 1", "2 3 1", "C 2", "1", "3"]
    assert impl.part3(lines) == ["1", "0", "0"]


@pytest.mark.part3
@pytest.mark.perf
def test_perf_part3_20000_meetings(run_script):
    rng = random.Random(0)
    n = 20_000
    rooms = 50
    lines = [f"N {n}"]
    for _ in range(n):
        st = rng.randint(0, 100_000)
        lines.append(f"{st} {st + rng.randint(1, 100)} {rng.randint(1, 10)}")
    lines.append(f"C {rooms}")
    lines.extend(str(rng.randint(1, 10)) for _ in range(rooms))
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nN 3\n0 30\n5 10\n15 20\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\nN 3\n0 30\n5 10\n15 20\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n1\n1\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\nN 3\n0 10 3\n1 2 1\n2 3 1\nC 2\n1\n3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n0\n0\n"
