"""NextFrame 电影推荐服务（待修复）。公开 API 与 `solution.py` 一致；放进真实工作区时，把 `ServiceError` 换成 `from models import ServiceError`。

这份代码能跑，却会返回空的、排错序的、甚至不该出现的结果：它就是要你修的东西。规则（每一条都有测试）：

1. 目录与用户数据可信：电影有唯一正整数 id、字符串标题、字符串列表 genres（可重复）、非负整数 popularity、布尔 available；
   ratings 是 {用户: {电影 id: 1..5}}，history 是 {用户: [电影 id]}，里面的 id 可能指向已从目录删除的电影。
   构造时复制所有嵌套输入；之后调用方改自己的对象，不影响服务。
2. 请求校验：limit 必须恰好是 `int`（bool 不算），范围 1..50（含 50），否则 `ServiceError(400, "invalid_limit")`；
   通过后再看 user：必须是 `str` 且 `strip()` 之后非空，否则 `ServiceError(400, "invalid_user")`。两项都错时报 limit。
   没出现过的非空用户是合法的冷启动用户；user 不做 strip 归一。
3. 候选集：目录里所有 `available` 为真、且 id 不在「该用户评过分的 id 并上看过的 id」里的电影。
   评过分就排除，与分数高低、是否在 history 里无关；只看这个用户自己的数据。
4. 偏好：该用户每条评分，若电影还在目录里，就给这部电影每个不同的类型加 `rating - 3`；已下架但还在目录里的电影照样贡献；
   目录里已经没有的 id 忽略；history 不产生权重。候选的分数是它每个不同类型当前权重之和；分数可以是负数或零，不能丢掉候选。
5. 排序与结果：按 分数降序、popularity 降序、id 升序 排；最多返回 limit 条；每条恰好是 {id, title, score, popularity}；
   目录为空或全部看过返回 []；冷启动用户分数全是 0。返回值是新对象：改它不影响服务，服务也不改传入的数据。
6. HTTP 适配器是固定的（下面的 `dispatch` 已经写好，不用改）。

Python 3.11，只用标准库。
"""

from __future__ import annotations

from collections.abc import Container, Iterator, Mapping
from dataclasses import dataclass
from typing import Any

MAX_LIMIT = 50
NEUTRAL_RATING = 3
DEFAULT_LIMIT = "10"
ROUTE = "/recommendations"


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class Movie:
    id: int
    title: str
    genres: frozenset[str]
    popularity: int
    available: bool

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Movie:
        return cls(record["id"], record["title"], frozenset(record["genres"]), record["popularity"], record["available"])


class Catalogue:
    def __init__(self, records: list[dict]) -> None:
        self._by_id = {record["id"]: Movie.from_record(record) for record in records}

    def get(self, movie_id: int) -> Movie | None:
        return self._by_id.get(movie_id)

    def candidates(self, excluded: Container[int]) -> Iterator[Movie]:
        return (movie for movie in self._by_id.values() if movie.available and movie.id not in excluded)


@dataclass(frozen=True)
class TasteProfile:
    weights: Mapping[str, int]

    @classmethod
    def build(cls, catalogue: Catalogue, ratings: Mapping[int, int]) -> TasteProfile:
        weights: dict[str, int] = {}
        for movie_id, rating in ratings.items():
            movie = catalogue.get(movie_id)
            if movie is None:
                continue
            for genre in movie.genres:
                weights[genre] = weights.get(genre, 0) + rating
        return cls(weights)

    def score(self, movie: Movie) -> int:
        return sum(self.weights.get(genre, 0) for genre in movie.genres)


@dataclass(frozen=True, slots=True)
class Scored:
    movie: Movie
    score: int

    @property
    def order_key(self) -> tuple[int, int, int]:
        return (-self.score, -self.movie.popularity, -self.movie.id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.movie.id,
            "title": self.movie.title,
            "score": self.score,
            "popularity": self.movie.popularity,
        }


@dataclass(frozen=True, slots=True)
class Viewer:
    ratings: Mapping[int, int]
    watched: frozenset[int]

    @property
    def seen(self) -> frozenset[int]:
        return self.watched


def valid_user(user: object) -> bool:
    return isinstance(user, str) and user.strip() != ""  # 只校验，不归一：查数据时仍用原样的字符串


def error_reply(status: int, code: str) -> tuple[int, dict]:
    return status, {"error": code}


def valid_limit(limit: object) -> bool:
    return type(limit) is int and 1 <= limit < MAX_LIMIT


class RecommendationService:
    def __init__(self, movies: list[dict], ratings: dict, history: dict) -> None:
        self._catalogue = Catalogue(movies)
        self._ratings = {user: dict(given) for user, given in ratings.items()}
        self._history = {user: frozenset(watched) for user, watched in history.items()}

    def _viewer(self, user: str) -> Viewer:
        return Viewer(self._ratings.get(user, {}), self._history.get(user, frozenset()))

    def recommend(self, user: str, limit: int = 10) -> list[dict]:
        if not valid_limit(limit):
            raise ServiceError(400, "invalid_limit")
        if not valid_user(user):
            raise ServiceError(400, "invalid_user")
        viewer = self._viewer(user)
        profile = TasteProfile.build(self._catalogue, viewer.ratings)
        candidates = [Scored(movie, profile.score(movie)) for movie in self._catalogue.candidates(viewer.seen)]
        candidates.sort(key=lambda item: item.order_key)
        return [item.to_dict() for item in candidates]


def parse_limit(query: Mapping[str, str] | None) -> int | None:
    try:
        return int((query or {}).get("limit", DEFAULT_LIMIT))
    except ValueError:
        return None


def dispatch(
    service: RecommendationService,
    method: str,
    path: str,
    user: str | None,
    body: object = None,
    query: Mapping[str, str] | None = None,
    key: str | None = None,
) -> tuple[int, dict]:
    if path != ROUTE:
        return error_reply(404, "not_found")
    if method != "GET":
        return error_reply(405, "method_not_allowed")
    if not valid_user(user):
        return error_reply(401, "unauthorized")
    limit = parse_limit(query)
    if limit is None:
        return error_reply(400, "invalid_limit")
    try:
        return 200, {"recommendations": service.recommend(user, limit)}
    except ServiceError as error:
        return error_reply(error.status, error.code)
