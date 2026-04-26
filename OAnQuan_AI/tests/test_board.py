import pytest
from src.board import BoardState


def test_new_board_state():
    state = BoardState.new()
    assert state.board == [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5]
    assert state.score == [0, 0]
    assert state.current_player == 0
    assert state.game_over is False


def test_handle_empty_rows_adds_seeds_and_penalty():
    state = BoardState.new()
    state.board[1:6] = [0, 0, 0, 0, 0]
    state.board[0] = 5
    state.handle_empty_rows()

    assert state.score[0] == -5
    assert state.board[1:6] == [1, 1, 1, 1, 1]


def test_check_game_over_collects_remaining_seeds():
    # Tạo trạng thái chỉ có quân ở ô 1 và ô 7, 2 ô quan = 0
    state = BoardState([0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0])

    ended = state.check_game_over()
    assert ended is True
    assert state.game_over is True
    assert state.score[0] == 2
    assert state.score[1] == 3
    assert state.board[1] == 0
    assert state.board[7] == 0


def test_apply_move_captures_after_empty_cell():
    # Board: ô 1 có 1 quân, ô 2,3 trống, ô 4 có 3 quân, ô 0,6 là quan
    state = BoardState([10, 1, 0, 0, 3, 0, 10, 0, 0, 0, 0, 0], [0, 0])
    state.current_player = 0
    state.apply_move(1, 1)

    # Rải 1 quân từ ô 1 theo hướng +1: ô 2 nhận 1 quân
    # Ô tiếp (3) trống -> kiểm tra ô sau (4) có 3 quân -> ăn 3 quân
    # Ô tiếp (5) trống -> kiểm tra ô sau (6) có 10 quân (ô Quan) -> ăn 10 quân
    # Ô tiếp (7) trống -> kiểm tra ô sau (8) trống -> dừng
    assert state.score[0] == 13
    assert state.board[4] == 0
    assert state.board[6] == 0
