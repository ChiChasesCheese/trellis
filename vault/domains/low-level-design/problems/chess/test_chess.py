"""国际象棋参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

WHITE, BLACK = None, None   # 在 setup_module 里绑定，避免 starter 导入期就崩


def setup_module(module) -> None:
    global WHITE, BLACK
    WHITE, BLACK = impl.Color.WHITE, impl.Color.BLACK


def board(pieces: dict[str, object], **kwargs) -> object:
    """用 `{"e1": King(WHITE)}` 这样的字面量摆一个局面，省掉一长串开局走法。"""
    return impl.Board(pieces, **kwargs)


def targets(b, square: str) -> set[str]:
    """某一格上的子按自身走法能到的所有格子（伪合法），用格子名表示。"""
    origin = impl.Square.of(square)
    piece = b.piece_at(origin)
    return {s.name for s in piece.destinations(b, origin)}


def legal_targets(game, square: str) -> set[str]:
    return {m.target.name for m in game.legal_moves() if m.origin == impl.Square.of(square)}


FEN_CLASSES = {"p": "Pawn", "n": "Knight", "b": "Bishop", "r": "Rook", "q": "Queen", "k": "King"}


def from_fen(fen: str):
    """只用公开 API 把一行 FEN 摆成棋盘，好引用棋界公认的走法生成自检局面。"""
    placement, _side, rights, en_passant = fen.split()[:4]
    squares = {}
    for row, line in enumerate(placement.split("/")):
        col = 0
        for char in line:
            if char.isdigit():
                col += int(char)
            else:
                kind = getattr(impl, FEN_CLASSES[char.lower()])
                squares[impl.Square(7 - row, col)] = kind(
                    impl.Color.WHITE if char.isupper() else impl.Color.BLACK)
                col += 1
    return impl.Board(squares, rights="" if rights == "-" else rights,
                      en_passant=None if en_passant == "-" else en_passant)


def perft(b, color, depth: int) -> int:
    """走法生成的标准自检：数出深度 `depth` 的叶子局面个数。"""
    if depth == 0:
        return 1
    total = 0
    for move in b.legal_moves(color):
        b.apply(move)
        total += perft(b, color.opponent, depth - 1)
        b.unapply(move)
    return total


# ---- 第 1 关：棋盘、棋子与伪合法走法 ----------------------------------------


def test_initial_board_has_thirty_two_pieces_and_all_castling_rights():
    game = impl.Game()
    assert game.board.piece_count == 32
    assert game.board.castling_rights == frozenset("KQkq")
    assert game.to_move is WHITE
    assert game.board.rows()[0] == "rnbqkbnr"
    assert game.board.rows()[7] == "RNBQKBNR"


def test_knight_jumps_over_its_own_pieces():
    game = impl.Game()
    assert targets(game.board, "b1") == {"a3", "c3"}


def test_a_sliding_piece_stops_at_its_own_piece_and_captures_the_enemy():
    b = board({"a1": impl.Rook(impl.Color.WHITE), "a4": impl.Pawn(impl.Color.WHITE),
               "d1": impl.Pawn(impl.Color.BLACK)})
    assert targets(b, "a1") == {"a2", "a3", "b1", "c1", "d1"}   # a4 是自己人，d1 吃掉后停


def test_queen_is_exactly_rook_plus_bishop():
    rook = board({"d4": impl.Rook(impl.Color.WHITE)})
    bishop = board({"d4": impl.Bishop(impl.Color.WHITE)})
    queen = board({"d4": impl.Queen(impl.Color.WHITE)})
    assert targets(queen, "d4") == targets(rook, "d4") | targets(bishop, "d4")


def test_pawn_pushes_one_or_two_from_home_and_is_blocked_by_any_piece():
    b = board({"e2": impl.Pawn(impl.Color.WHITE), "d3": impl.Pawn(impl.Color.BLACK)})
    assert targets(b, "e2") == {"e3", "e4", "d3"}
    blocked = board({"e2": impl.Pawn(impl.Color.WHITE), "e3": impl.Pawn(impl.Color.BLACK)})
    assert targets(blocked, "e2") == set()      # 正前方有子，连双步也没了


def test_a_pawn_attacks_diagonally_even_onto_empty_squares_but_never_straight_ahead():
    b = board({"e4": impl.Pawn(impl.Color.WHITE)})
    assert b.is_attacked(impl.Square.of("d5"), WHITE)
    assert b.is_attacked(impl.Square.of("f5"), WHITE)
    assert not b.is_attacked(impl.Square.of("e5"), WHITE)
    assert targets(b, "e4") == {"e5"}           # 空的斜前方不是落点，只是攻击


# ---- 第 2 关：合法性、将军、将死与逼和 --------------------------------------


def test_a_pinned_piece_is_pseudo_legal_but_has_no_legal_move():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "e2": impl.Knight(impl.Color.WHITE),
                            "e8": impl.Rook(impl.Color.BLACK), "a8": impl.King(impl.Color.BLACK)}))
    assert targets(game.board, "e2")            # 按马的走法当然有落点
    assert legal_targets(game, "e2") == set()   # 但每一个都会把自己的王暴露给 e8 的车


def test_moving_into_check_is_rejected():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "d8": impl.Rook(impl.Color.BLACK),
                            "a8": impl.King(impl.Color.BLACK)}))
    with pytest.raises(impl.IllegalMoveError):
        game.move("e1", "d1")                   # d 线被车控制
    assert "d1" not in legal_targets(game, "e1")
    assert "e2" in legal_targets(game, "e1")


def test_fools_mate_is_checkmate_and_black_wins():
    game = impl.Game()
    for origin, target in (("f2", "f3"), ("e7", "e5"), ("g2", "g4"), ("d8", "h4")):
        game.move(origin, target)
    assert game.status is impl.GameStatus.CHECKMATE
    assert game.winner is BLACK
    assert game.in_check
    with pytest.raises(impl.GameOverError):
        game.move("e1", "f2")


def test_stalemate_is_no_legal_move_without_check():
    game = impl.Game(board({"h8": impl.King(impl.Color.BLACK), "g6": impl.Queen(impl.Color.WHITE),
                            "f6": impl.King(impl.Color.WHITE)}), to_move=impl.Color.BLACK)
    assert game.legal_moves() == ()
    assert not game.in_check
    assert game.status is impl.GameStatus.STALEMATE
    assert game.winner is None


def test_the_two_kings_can_never_stand_next_to_each_other():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "e3": impl.King(impl.Color.BLACK)}))
    assert legal_targets(game, "e1") == {"d1", "f1"}


def test_perft_matches_the_known_counts_for_the_opening_position():
    b = impl.Board.initial()
    assert perft(b, WHITE, 1) == 20
    assert perft(b, WHITE, 2) == 400
    assert perft(b, WHITE, 3) == 8902
    assert b.piece_count == 32 and b.castling_rights == frozenset("KQkq")


def test_perft_on_a_position_full_of_castling_pins_and_captures():
    # 棋界常用的 "Kiwipete" 自检局面：两边都还能双向易位，盘上到处是牵制和吃子。
    b = from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -")
    assert perft(b, WHITE, 1) == 48
    assert perft(b, WHITE, 2) == 2039


# ---- 第 3 关：王车易位、吃过路兵、升变 --------------------------------------


def test_castling_moves_both_the_king_and_the_rook():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "h1": impl.Rook(impl.Color.WHITE),
                            "a1": impl.Rook(impl.Color.WHITE), "e8": impl.King(impl.Color.BLACK)},
                           rights="KQ"))
    move = game.move("e1", "g1")
    assert move.kind is impl.MoveKind.CASTLE
    assert game.board.piece_at(impl.Square.of("g1")).letter == "K"
    assert game.board.piece_at(impl.Square.of("f1")).letter == "R"
    assert game.board.piece_at(impl.Square.of("h1")) is None
    assert game.board.castling_rights == frozenset()    # 王一动，两边的权利都没了


def test_queen_side_castling_puts_the_rook_on_d1():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "a1": impl.Rook(impl.Color.WHITE),
                            "e8": impl.King(impl.Color.BLACK)}, rights="Q"))
    assert game.move("e1", "c1").notation() == "O-O-O"
    assert game.board.piece_at(impl.Square.of("d1")).letter == "R"


def test_castling_rights_are_lost_when_the_rook_moves_or_is_captured():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "h1": impl.Rook(impl.Color.WHITE),
                            "e8": impl.King(impl.Color.BLACK), "h8": impl.Rook(impl.Color.BLACK)},
                           rights="Kk"))
    game.move("h1", "h8")                       # 白车吃掉黑车，自己也离开了 h1
    assert game.board.castling_rights == frozenset()


def test_castling_is_refused_out_of_through_and_into_check():
    plain = {"e1": impl.King(impl.Color.WHITE), "h1": impl.Rook(impl.Color.WHITE),
             "a8": impl.King(impl.Color.BLACK)}
    for attacker_square in ("e8", "f8", "g8"):  # 依次是"从被将中易位""经过被攻击的格""易位到被将"
        game = impl.Game(board({**plain, attacker_square: impl.Rook(impl.Color.BLACK)}, rights="K"))
        assert "g1" not in legal_targets(game, "e1")
    free = impl.Game(board({**plain, "h7": impl.Rook(impl.Color.BLACK)}, rights="K"))
    assert "g1" in legal_targets(free, "e1")


def test_castling_is_refused_when_a_square_between_is_occupied():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "h1": impl.Rook(impl.Color.WHITE),
                            "g1": impl.Knight(impl.Color.WHITE),
                            "a8": impl.King(impl.Color.BLACK)}, rights="K"))
    assert "g1" not in legal_targets(game, "e1")


def test_en_passant_is_legal_only_immediately_after_the_double_push():
    def position():
        return impl.Game(board({"e5": impl.Pawn(impl.Color.WHITE), "e1": impl.King(impl.Color.WHITE),
                                "d7": impl.Pawn(impl.Color.BLACK), "h8": impl.King(impl.Color.BLACK)}))

    game = position()
    game.move("e1", "f1")
    game.move("d7", "d5")
    assert game.board.en_passant_target == impl.Square.of("d6")
    assert "d6" in legal_targets(game, "e5")

    late = position()
    late.move("e1", "f1")
    late.move("d7", "d5")
    late.move("f1", "e1")                       # 白方等了一手
    late.move("h8", "g8")
    assert late.board.en_passant_target is None
    assert "d6" not in legal_targets(late, "e5")


def test_the_en_passant_target_left_by_your_own_pawn_is_not_capturable():
    # 白兵 e2-e4 之后目标格是 e3。黑兵可以吃它；同为白方的 d2 兵绝不能"吃"到一个空的 e3
    # 上去——那会凭空多出一手斜走的幽灵棋。
    game = impl.Game(board({"e2": impl.Pawn(impl.Color.WHITE), "d2": impl.Pawn(impl.Color.WHITE),
                            "e1": impl.King(impl.Color.WHITE), "d4": impl.Pawn(impl.Color.BLACK),
                            "h8": impl.King(impl.Color.BLACK)}))
    game.move("e2", "e4")
    assert game.board.en_passant_target == impl.Square.of("e3")
    assert "e3" in {m.target.name for m in game.board.legal_moves(BLACK)
                    if m.origin == impl.Square.of("d4")}
    assert "e3" not in targets(game.board, "d2")        # 白兵不能吃白方自己留下的过路格


def test_castling_rights_that_do_not_match_the_placement_are_ignored():
    # 易位权说"还能易位"，但王根本不在 e1：不能因此崩掉，只是生不出易位着法。
    b = board({"a1": impl.Rook(impl.Color.WHITE), "d3": impl.King(impl.Color.WHITE),
               "h8": impl.King(impl.Color.BLACK)}, rights="KQ")
    assert all(m.kind is not impl.MoveKind.CASTLE for m in b.legal_moves(WHITE))
    assert b.legal_moves(WHITE)


def test_en_passant_removes_a_pawn_from_a_square_that_is_not_the_target():
    game = impl.Game(board({"e5": impl.Pawn(impl.Color.WHITE), "e1": impl.King(impl.Color.WHITE),
                            "d7": impl.Pawn(impl.Color.BLACK), "h8": impl.King(impl.Color.BLACK)}))
    game.move("e1", "f1")
    game.move("d7", "d5")
    move = game.move("e5", "d6")
    assert move.kind is impl.MoveKind.EN_PASSANT
    assert move.captured_square == impl.Square.of("d5")
    assert game.board.piece_at(impl.Square.of("d5")) is None
    assert game.board.piece_count == 3
    assert move.notation() == "e5xd6 e.p."


def test_promotion_must_be_declared_and_can_be_an_underpromotion():
    def position():
        return impl.Game(board({"a7": impl.Pawn(impl.Color.WHITE), "e1": impl.King(impl.Color.WHITE),
                                "h8": impl.King(impl.Color.BLACK)}))

    with pytest.raises(impl.PromotionRequiredError):
        position().move("a7", "a8")
    queened = position()
    assert queened.move("a7", "a8", "Q").notation() == "a7-a8=Q"
    assert queened.board.piece_at(impl.Square.of("a8")).letter == "Q"
    knighted = position()
    knighted.move("a7", "a8", "N")
    assert knighted.board.piece_at(impl.Square.of("a8")).letter == "N"
    with pytest.raises(impl.IllegalMoveError):
        position().move("a7", "a8", "K")        # 不能升变成王


# ---- 第 4 关：悔棋、和棋规则与记谱 ------------------------------------------


def test_undo_restores_the_board_and_every_piece_of_position_state():
    game = impl.Game()
    before = (game.board.rows(), game.board.castling_rights,
              game.board.en_passant_target, game.board.halfmove_clock, game.to_move)
    for origin, target in (("e2", "e4"), ("e7", "e5"), ("g1", "f3"), ("b8", "c6")):
        game.move(origin, target)
    while game.history:
        game.undo()
    assert (game.board.rows(), game.board.castling_rights,
            game.board.en_passant_target, game.board.halfmove_clock, game.to_move) == before
    assert game.board.piece_count == 32


def test_undo_puts_back_a_castled_rook_and_an_en_passant_victim():
    castled = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "h1": impl.Rook(impl.Color.WHITE),
                               "a8": impl.King(impl.Color.BLACK)}, rights="K"))
    castled.move("e1", "g1")
    castled.undo()
    assert castled.board.piece_at(impl.Square.of("h1")).letter == "R"
    assert castled.board.piece_at(impl.Square.of("e1")).letter == "K"
    assert castled.board.castling_rights == frozenset("K")

    passing = impl.Game(board({"e5": impl.Pawn(impl.Color.WHITE), "e1": impl.King(impl.Color.WHITE),
                               "d7": impl.Pawn(impl.Color.BLACK), "h8": impl.King(impl.Color.BLACK)}))
    passing.move("e1", "f1")
    passing.move("d7", "d5")
    passing.move("e5", "d6")
    passing.undo()
    assert passing.board.piece_at(impl.Square.of("d5")).letter == "P"
    assert passing.board.en_passant_target == impl.Square.of("d6")
    assert passing.board.piece_count == 4


def test_undo_of_a_promotion_brings_the_pawn_back():
    game = impl.Game(board({"a7": impl.Pawn(impl.Color.WHITE), "e1": impl.King(impl.Color.WHITE),
                            "h8": impl.King(impl.Color.BLACK)}))
    game.move("a7", "a8", "Q")
    game.undo()
    assert game.board.piece_at(impl.Square.of("a7")).letter == "P"
    assert game.board.piece_at(impl.Square.of("a8")) is None


def test_undo_on_an_empty_history_raises():
    with pytest.raises(impl.NothingToUndoError):
        impl.Game().undo()


def test_the_fifty_move_clock_counts_up_and_a_pawn_move_resets_it():
    quiet = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "a1": impl.Rook(impl.Color.WHITE),
                             "e8": impl.King(impl.Color.BLACK), "h8": impl.Rook(impl.Color.BLACK)},
                            halfmove=99))
    quiet.move("e1", "e2")
    assert quiet.board.halfmove_clock == 100
    assert quiet.status is impl.GameStatus.DRAW_FIFTY_MOVE

    pushed = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "b2": impl.Pawn(impl.Color.WHITE),
                              "e8": impl.King(impl.Color.BLACK), "h8": impl.Rook(impl.Color.BLACK)},
                             halfmove=99))
    pushed.move("b2", "b3")
    assert pushed.board.halfmove_clock == 0
    assert pushed.status is impl.GameStatus.IN_PROGRESS


def test_threefold_repetition_is_a_draw_and_undo_shrinks_the_position_table():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "g1": impl.Knight(impl.Color.WHITE),
                            "e8": impl.King(impl.Color.BLACK), "g8": impl.Knight(impl.Color.BLACK)}))
    start = game.distinct_positions
    cycle = (("g1", "f3"), ("g8", "f6"), ("f3", "g1"), ("f6", "g8"))
    for _ in range(2):
        for origin, target in cycle:
            game.move(origin, target)
    assert game.repetition_count == 3
    assert game.status is impl.GameStatus.DRAW_REPETITION
    while game.history:
        game.undo()
    assert game.distinct_positions == start     # 计数表必须缩回去，不能留一堆 0
    assert game.repetition_count == 1


def test_a_position_repeated_with_different_castling_rights_is_not_a_repetition():
    game = impl.Game(board({"e1": impl.King(impl.Color.WHITE), "h1": impl.Rook(impl.Color.WHITE),
                            "e8": impl.King(impl.Color.BLACK), "a8": impl.Rook(impl.Color.BLACK)},
                           rights="Kq"))
    for origin, target in (("h1", "g1"), ("a8", "b8"), ("g1", "h1"), ("b8", "a8")):
        game.move(origin, target)
    assert game.board.castling_rights == frozenset()
    assert game.repetition_count == 1           # 子力摆放一样，但易位权变了，不是同一个局面


def test_notation_covers_quiet_moves_captures_castling_and_promotion():
    game = impl.Game()
    for origin, target in (("e2", "e4"), ("d7", "d5"), ("e4", "d5"), ("g8", "f6")):
        game.move(origin, target)
    assert [m.notation() for m in game.history] == ["e2-e4", "d7-d5", "e4xd5", "Ng8-f6"]


def test_a_move_is_pure_data_and_can_be_replayed_on_another_board():
    game = impl.Game()
    game.move("e2", "e4")
    replay = impl.Board.initial()
    replay.apply(game.history[0])               # Move 不引用任何棋盘，所以能在别的盘上重放
    assert replay.rows() == game.board.rows()


def test_illegal_input_is_named_not_silently_ignored():
    game = impl.Game()
    with pytest.raises(impl.IllegalMoveError):
        game.move("e2", "e5")
    with pytest.raises(impl.IllegalMoveError):
        game.move("e3", "e4")                   # 起点上根本没有子
    assert game.board.piece_count == 32
    assert game.to_move is WHITE
