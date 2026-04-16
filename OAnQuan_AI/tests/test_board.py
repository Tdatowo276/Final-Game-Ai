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
    state = BoardState.new()
    state.board[0] = 0
    state.board[6] = 0
    state.board[1] = 2
    state.board[7] = 3

    ended = state.check_game_over()
    assert ended is True
    assert state.game_over is True
    assert state.score[0] == 2
    assert state.score[1] == 3
    assert state.board[1] == 0
    assert state.board[7] == 0


def test_apply_move_captures_after_empty_cell():
    state = BoardState.new()
    state.board = [10, 1, 0, 0, 3, 0, 10, 0, 0, 0, 0, 0]
    state.current_player = 0
    state.apply_move(1, 1)

    assert state.score[0] == 3
    assert state.board[4] == 0
    assert state.current_player == 1
