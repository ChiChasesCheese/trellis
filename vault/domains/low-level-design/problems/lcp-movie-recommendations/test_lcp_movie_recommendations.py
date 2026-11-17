import copy
import importlib
import os
import random
import threading
from collections import Counter

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Service = impl.RecommendationService
ServiceError = impl.ServiceError


def film(movie_id, genres, popularity=0, available=True):
    return {"id": movie_id, "title": f"film-{movie_id}", "genres": list(genres), "popularity": popularity, "available": available}


def ids(rows):
    return [row["id"] for row in rows]


def failure(call, *args):
    with pytest.raises(ServiceError) as caught:
        call(*args)
    return caught.value.status, caught.value.code


def row(movie_id, score, popularity):
    return {"id": movie_id, "title": f"film-{movie_id}", "score": score, "popularity": popularity}


# ---- 规则 5：合同里的例子 ----

def test_liked_genre_scores_and_rated_film_is_left_out():
    movies = [film(10, ["noir"], 3), film(11, ["noir"], 8)]
    service = Service(movies, {"kim": {10: 5}}, {})
    assert service.recommend("kim") == [row(11, 2, 8)]


def test_empty_catalogue_and_everything_seen_give_empty_list():
    assert Service([], {}, {}).recommend("anyone") == []
    movies = [film(1, ["a"]), film(2, ["a"])]
    assert Service(movies, {"u": {1: 4}}, {"u": [2]}).recommend("u") == []


# ---- 规则 2：请求校验 ----

@pytest.mark.parametrize("bad", [0, -1, 51, 1000, True, False, 2.0, "5", None, [5]])
def test_limit_outside_one_to_fifty_or_not_an_int_is_rejected(bad):
    assert failure(Service([], {}, {}).recommend, "u", bad) == (400, "invalid_limit")


def test_limit_bounds_are_inclusive_and_cap_the_result():
    movies = [film(i, ["g"], i) for i in range(1, 61)]
    service = Service(movies, {}, {})
    assert len(service.recommend("u", 50)) == 50
    assert len(service.recommend("u", 1)) == 1
    assert len(service.recommend("u")) == 10  # 默认值


@pytest.mark.parametrize("bad", [None, "", "   ", "\t\n", 7, b"bob", ["bob"]])
def test_blank_or_non_string_user_is_rejected(bad):
    assert failure(Service([], {}, {}).recommend, bad, 5) == (400, "invalid_user")


def test_limit_error_wins_when_both_arguments_are_bad():
    assert failure(Service([], {}, {}).recommend, "", 0) == (400, "invalid_limit")
    assert failure(Service([], {}, {}).recommend, None, True) == (400, "invalid_limit")


def test_unknown_user_is_a_valid_cold_start_and_names_are_not_trimmed():
    movies = [film(1, ["a"], 5), film(2, ["a"], 9)]
    service = Service(movies, {"bob": {2: 5}}, {"bob": [1]})
    assert ids(service.recommend("bob ")) == [2, 1]  # "bob " 不是 "bob"：没有任何偏好和已看
    assert ids(service.recommend("bob")) == []


# ---- 规则 3：候选集 ----

def test_rated_films_are_excluded_whatever_the_rating_and_history():
    movies = [film(i, ["g"], i) for i in range(1, 7)]
    ratings = {"u": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}}
    service = Service(movies, ratings, {"u": [1, 3]})
    assert ids(service.recommend("u")) == [6]


def test_watched_and_unavailable_films_are_excluded():
    movies = [film(1, ["g"], 1), film(2, ["g"], 2), film(3, ["g"], 3, available=False), film(4, ["g"], 4)]
    service = Service(movies, {}, {"u": [4, 99]})
    assert ids(service.recommend("u")) == [2, 1]


def test_only_this_users_data_counts():
    movies = [film(1, ["a"], 1), film(2, ["a"], 2), film(3, ["b"], 3)]
    service = Service(movies, {"other": {1: 5, 3: 1}}, {"other": [2]})
    assert service.recommend("me") == [row(3, 0, 3), row(2, 0, 2), row(1, 0, 1)]


# ---- 规则 4：偏好与分数 ----

def test_weight_is_rating_minus_three_per_distinct_genre():
    movies = [film(1, ["a"]), film(2, ["b"]), film(3, ["c"]), film(10, ["a"], 1), film(11, ["b"], 1), film(12, ["c"], 1)]
    service = Service(movies, {"u": {1: 5, 2: 3, 3: 1}}, {})
    assert {r["id"]: r["score"] for r in service.recommend("u")} == {10: 2, 11: 0, 12: -2}


def test_duplicate_genres_count_once_on_both_sides():
    movies = [film(1, ["a", "a", "b"]), film(2, ["a", "a", "a"], 1), film(3, ["b", "a", "b"], 1)]
    service = Service(movies, {"u": {1: 5}}, {})
    scores = {r["id"]: r["score"] for r in service.recommend("u")}
    assert scores == {2: 2, 3: 4}


def test_ratings_add_up_across_films_and_negative_scores_are_kept():
    movies = [film(1, ["a"]), film(2, ["a"]), film(3, ["b"]), film(10, ["a"], 5), film(11, ["a", "b"], 5), film(12, ["z"], 1)]
    service = Service(movies, {"u": {1: 1, 2: 2, 3: 5}}, {})
    assert service.recommend("u") == [row(12, 0, 1), row(11, -1, 5), row(10, -3, 5)]


def test_unavailable_rated_film_still_contributes_but_orphans_do_not():
    movies = [film(1, ["a"], 1, available=False), film(2, ["a"], 1), film(3, ["b"], 1)]
    service = Service(movies, {"u": {1: 5, 404: 5}}, {})
    assert service.recommend("u") == [row(2, 2, 1), row(3, 0, 1)]


def test_history_alone_gives_no_weights():
    movies = [film(1, ["a"], 1), film(2, ["a"], 2), film(3, ["b"], 3)]
    service = Service(movies, {}, {"u": [1]})
    assert service.recommend("u") == [row(3, 0, 3), row(2, 0, 2)]


# ---- 规则 5：排序 ----

def test_ordering_is_score_then_popularity_then_id_ascending():
    movies = [
        film(1, ["a"]),
        film(30, ["a"], 7), film(20, ["a"], 7), film(25, ["a"], 9),
        film(40, ["b"], 100),
        film(50, ["c"], 7),
    ]
    service = Service(movies, {"u": {1: 4}}, {})
    assert ids(service.recommend("u")) == [25, 20, 30, 40, 50]


def test_cold_start_orders_by_popularity_then_id():
    movies = [film(3, ["x"], 5), film(1, ["y"], 5), film(2, ["x"], 6), film(4, [], 0)]
    assert ids(Service(movies, {}, {}).recommend("new")) == [2, 1, 3, 4]


def test_film_without_genres_scores_zero_and_stays_a_candidate():
    movies = [film(1, ["a"]), film(2, [], 4)]
    assert Service(movies, {"u": {1: 5}}, {}).recommend("u") == [row(2, 0, 4)]


def test_limit_takes_the_top_of_the_ranking():
    movies = [film(i, ["g"], 100 - i) for i in range(1, 8)]
    service = Service(movies, {}, {})
    assert ids(service.recommend("u", 3)) == [1, 2, 3]
    assert len(service.recommend("u", 50)) == 7  # 不够就少返回


def test_top_k_matches_a_full_sort_over_random_catalogues():
    for seed in range(40):
        rng = random.Random(seed)
        genres = ["a", "b", "c", "d"]
        movies = [film(i, rng.sample(genres, rng.randint(0, 3)), rng.randint(0, 5), rng.random() < 0.8) for i in range(1, 40)]
        ratings = {"u": {rng.randint(1, 45): rng.randint(1, 5) for _ in range(6)}}
        history = {"u": [rng.randint(1, 45) for _ in range(5)]}
        service = Service(movies, ratings, history)
        by_id = {m["id"]: m for m in movies}
        weights: Counter = Counter()
        for movie_id, given in ratings["u"].items():
            genres_of_rated = by_id[movie_id]["genres"] if movie_id in by_id else []
            weights.update({genre: given - 3 for genre in set(genres_of_rated)})
        seen = set(ratings["u"]) | set(history["u"])
        expected = sorted(
            (-sum(weights[g] for g in set(m["genres"])), -m["popularity"], m["id"])
            for m in movies if m["available"] and m["id"] not in seen
        )
        for limit in (1, 3, 50):
            assert [r["id"] for r in service.recommend("u", limit)] == [key[2] for key in expected[:limit]]


# ---- 规则 1 与 5：输入输出隔离 ----

def test_result_rows_have_exactly_four_keys():
    rows = Service([film(1, ["a"], 2)], {}, {}).recommend("u")
    assert set(rows[0]) == {"id", "title", "score", "popularity"}


def test_mutating_a_result_does_not_change_later_results():
    service = Service([film(1, ["a"], 2)], {}, {})
    first = service.recommend("u")
    first[0]["title"] = "tampered"
    first.append({"id": 99})
    assert service.recommend("u") == [row(1, 0, 2)]


def test_constructor_copies_nested_inputs_and_calls_leave_them_untouched():
    movies = [film(1, ["a"], 1), film(2, ["a"], 2)]
    ratings = {"u": {1: 5}}
    history = {"u": [2]}
    snapshot = copy.deepcopy((movies, ratings, history))
    service = Service(movies, ratings, history)
    service.recommend("u")
    service.recommend("v", 5)
    assert (movies, ratings, history) == snapshot
    movies[0]["available"] = False
    movies[1]["genres"].append("zzz")
    ratings["u"][2] = 1
    history["u"].clear()
    ratings["w"] = {2: 5}
    assert Service(*copy.deepcopy(snapshot)).recommend("u") == service.recommend("u") == []
    assert service.recommend("v") == [row(2, 0, 2), row(1, 0, 1)]


def test_concurrent_reads_all_see_the_same_answer():
    movies = [film(i, ["a", "b"][: 1 + i % 2], i % 5) for i in range(1, 30)]
    service = Service(movies, {"u": {1: 5, 2: 2}}, {"u": [3]})
    expected = service.recommend("u", 8)
    barrier = threading.Barrier(8)
    outcomes: list[list[dict]] = []

    def worker():
        barrier.wait()
        outcomes.extend([service.recommend("u", 8) for _ in range(50)])

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(outcomes) == 400 and all(o == expected for o in outcomes)


# ---- 规则 6：HTTP ----

def make_http_service():
    movies = [film(1, ["a"], 4), film(2, ["a"], 9), film(3, ["b"], 6)]
    return Service(movies, {"ann": {1: 5}}, {})


def test_http_success_and_default_limit():
    service = make_http_service()
    assert impl.dispatch(service, "GET", "/recommendations", "ann") == (200, {"recommendations": [row(2, 2, 9), row(3, 0, 6)]})
    status, payload = impl.dispatch(service, "GET", "/recommendations", "ann", None, {"limit": "1"})
    assert (status, ids(payload["recommendations"])) == (200, [2])


@pytest.mark.parametrize("text", ["abc", "", "2.5", "1e1", "ten"])
def test_http_malformed_limit_is_400(text):
    assert impl.dispatch(make_http_service(), "GET", "/recommendations", "ann", None, {"limit": text}) == (400, {"error": "invalid_limit"})


@pytest.mark.parametrize("text", ["0", "51", "-3"])
def test_http_service_limit_errors_map_to_their_codes(text):
    assert impl.dispatch(make_http_service(), "GET", "/recommendations", "ann", None, {"limit": text}) == (400, {"error": "invalid_limit"})


def test_http_limit_fifty_is_accepted():
    status, payload = impl.dispatch(make_http_service(), "GET", "/recommendations", "ann", None, {"limit": "50"})
    assert status == 200 and len(payload["recommendations"]) == 2


@pytest.mark.parametrize("user", [None, "", "  "])
def test_http_missing_or_blank_user_is_401(user):
    assert impl.dispatch(make_http_service(), "GET", "/recommendations", user) == (401, {"error": "unauthorized"})


def test_http_unknown_route_is_404_and_other_methods_are_405():
    service = make_http_service()
    assert impl.dispatch(service, "GET", "/nope", "ann") == (404, {"error": "not_found"})
    assert impl.dispatch(service, "POST", "/nope", "ann") == (404, {"error": "not_found"})
    for method in ("POST", "PUT", "DELETE", "PATCH"):
        assert impl.dispatch(service, method, "/recommendations", "ann") == (405, {"error": "method_not_allowed"})
