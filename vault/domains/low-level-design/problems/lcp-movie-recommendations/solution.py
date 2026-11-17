"""NextFrame 电影推荐修复：参考解。放进真实工作区时，把下面的 `ServiceError` 换成 `from models import ServiceError`。

产品规则（编号即测试编号；全部来自合同，每一条都有测试）：

1. 目录与用户数据可信：电影有唯一正整数 id、字符串标题、字符串列表 genres（可重复）、非负整数 popularity、布尔 available；
   ratings 是 {用户: {电影 id: 1..5}}，history 是 {用户: [电影 id]}，里面的 id 可能指向已下架并从目录删除的电影。
   构造时把嵌套的输入全部复制一份；之后调用方怎么改自己的对象，都不影响服务。
2. 请求校验：limit 必须恰好是 `int`（bool 不算），范围 1..50（含 50），否则 `ServiceError(400, "invalid_limit")`；
   通过后再看 user：必须是 `str` 且 `strip()` 之后非空，否则 `ServiceError(400, "invalid_user")`。两项都错时报 limit。
   没出现过的非空用户是合法的冷启动用户；user 不做 strip 归一，`"bob "` 与 `"bob"` 是两个用户。
3. 候选集：目录里所有 `available` 为真、且 id 不在「该用户评过分的 id 并上看过的 id」里的电影。
   评过分就排除，与分数高低、是否在 history 里无关；只看这个用户自己的数据。
4. 偏好：该用户每条评分，若电影还在目录里，就给这部电影每个**不同**的类型加 `rating - 3`
   （3 分不加不减，1 分是 -2，5 分是 +2）；已下架但还在目录里的电影照样贡献；目录里已经没有的 id 直接忽略；
   history 不产生任何权重。候选的分数是它每个不同类型当前权重之和；分数可以是负数或零，不能因此丢掉候选。
5. 排序与结果：按 分数降序、popularity 降序、id 升序 排；最多返回 limit 条，不够就少返回；
   每条恰好是 {id, title, score, popularity}；目录为空或全部看过则返回 []；冷启动用户分数全是 0，
   所以只由 popularity 与 id 决定顺序。返回值是新对象：改它不影响服务，服务也不改传入的数据。
6. HTTP：`GET /recommendations?limit=10`，请求头 `X-User-ID`，成功 200 `{"recommendations": [...]}`；
   limit 缺省为 10，按整数解析，解析不了是 400 invalid_limit；缺失或空白的用户是 401 unauthorized；
   `ServiceError` 变成 `{"error": code}`；其他路径 404 not_found，其他方法 405 method_not_allowed（先看路径，再看方法，最后看用户）。
"""

from __future__ import annotations

import heapq
from collections.abc import Container, Iterator, Mapping
from dataclasses import dataclass
from operator import attrgetter
from typing import Any

MAX_LIMIT = 50
NEUTRAL_RATING = 3  # 打 3 分表示"无所谓"：权重是 rating 减去它
DEFAULT_LIMIT = "10"
ROUTE = "/recommendations"


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class Movie:
    """目录里的一部电影。冻结，类型集合是 frozenset：类型只关心"有没有"，重复写几次都一样。"""

    id: int
    title: str
    genres: frozenset[str]
    popularity: int
    available: bool

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Movie:
        return cls(record["id"], record["title"], frozenset(record["genres"]), record["popularity"], record["available"])


class Catalogue:
    """目录：按 id 持有全部电影（含已下架的），并回答"谁有资格被推荐"。排除只在这里发生，打分与它无关。"""

    def __init__(self, records: list[dict]) -> None:
        self._by_id = {record["id"]: Movie.from_record(record) for record in records}

    def get(self, movie_id: int) -> Movie | None:
        return self._by_id.get(movie_id)

    def candidates(self, excluded: Container[int]) -> Iterator[Movie]:
        """在架、且不在排除集里的电影。"""
        return (movie for movie in self._by_id.values() if movie.available and movie.id not in excluded)


@dataclass(frozen=True)
class TasteProfile:
    """一个用户的类型权重。它只由评分算出，和"要不要排除"无关。"""

    weights: Mapping[str, int]

    @classmethod
    def build(cls, catalogue: Catalogue, ratings: Mapping[int, int]) -> TasteProfile:
        weights: dict[str, int] = {}
        for movie_id, rating in ratings.items():
            movie = catalogue.get(movie_id)
            if movie is None:  # 目录里已经没有的电影：评分无处可挂
                continue
            for genre in movie.genres:  # 下架的电影照样贡献，所以这里不看 available
                weights[genre] = weights.get(genre, 0) + rating - NEUTRAL_RATING
        return cls(weights)

    def score(self, movie: Movie) -> int:
        return sum(self.weights.get(genre, 0) for genre in movie.genres)


@dataclass(frozen=True, slots=True)
class Scored:
    """一个打好分的候选：排序键和输出形状都由它负责。"""

    movie: Movie
    score: int

    @property
    def order_key(self) -> tuple[int, int, int]:
        # 分数、热度取负数来表示降序；id 本身升序。id 唯一，所以这是全序，没有平局
        return (-self.score, -self.movie.popularity, self.movie.id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.movie.id,
            "title": self.movie.title,
            "score": self.score,
            "popularity": self.movie.popularity,
        }


@dataclass(frozen=True, slots=True)
class Viewer:
    """一个用户自己的数据：评分与看过的片子。排除集和偏好都只从它取，别的用户的数据到不了这里。"""

    ratings: Mapping[int, int]
    watched: frozenset[int]

    @property
    def seen(self) -> frozenset[int]:
        """评过分的并上看过的：这些电影不再推荐。"""
        return frozenset(self.ratings) | self.watched


def valid_user(user: object) -> bool:
    return isinstance(user, str) and user.strip() != ""  # 只校验，不归一：查数据时仍用原样的字符串


def error_reply(status: int, code: str) -> tuple[int, dict]:
    return status, {"error": code}


def valid_limit(limit: object) -> bool:
    return type(limit) is int and 1 <= limit <= MAX_LIMIT  # type() 而不是 isinstance：True 是 int 的实例


class RecommendationService:
    """构造之后不可变，所以多个线程并发调用 `recommend` 不需要锁。"""

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
        profile = TasteProfile.build(self._catalogue, viewer.ratings)  # 偏好：只看评分，下架的也算
        eligible = self._catalogue.candidates(viewer.seen)  # 排除：评过的、看过的、已下架的
        scored = (Scored(movie, profile.score(movie)) for movie in eligible)
        best = heapq.nsmallest(limit, scored, key=attrgetter("order_key"))  # 前 limit 名，不必排完全部
        return [item.to_dict() for item in best]


def parse_limit(query: Mapping[str, str] | None) -> int | None:
    """适配器的 limit 解析：缺省 10，用 `int()` 读文本；读不出来返回 None。"""
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
    """HTTP 适配器的行为：路径 → 方法 → 用户 → limit → 服务；服务的 ServiceError 变成错误体。"""
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


if __name__ == "__main__":
    shows = [
        {"id": 1, "title": "Gold Rush", "genres": ["western", "comedy"], "popularity": 40, "available": True},
        {"id": 2, "title": "Dust Road", "genres": ["western"], "popularity": 25, "available": True},
        {"id": 3, "title": "Quiet Lab", "genres": ["scifi"], "popularity": 90, "available": True},
        {"id": 4, "title": "Slow Joke", "genres": ["comedy"], "popularity": 10, "available": True},
    ]
    demo = RecommendationService(shows, {"ana": {1: 5}}, {"ana": [2]})
    print(demo.recommend("ana"))  # Slow Joke 得 2 分排第一；Gold Rush 评过、Dust Road 看过，都不出现
    print(demo.recommend("newcomer", 2))  # 冷启动：按热度，Quiet Lab 与 Gold Rush
