from dataclasses import dataclass
from typing import List


@dataclass
class BoardState:
    board: List[int]
    score: List[int]
    current_player: int = 0
    selected_index: int = -1
    current_hand_pos: int = -1
    is_animating: bool = False
    game_over: bool = False

    @classmethod
    def new(cls):
        return cls([10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5], [0, 0])

    def reset(self):
        self.board = [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5]
        self.score = [0, 0]
        self.current_player = 0
        self.selected_index = -1
        self.current_hand_pos = -1
        self.is_animating = False
        self.game_over = False

    def clone(self):
        return BoardState(self.board.copy(), self.score.copy(), self.current_player,
                          self.selected_index, self.current_hand_pos,
                          self.is_animating, self.game_over)

    def handle_empty_rows(self):
        if sum(self.board[1:6]) == 0 and (self.board[0] > 0 or self.board[6] > 0):
            self.score[0] -= 5
            for i in range(1, 6):
                self.board[i] = 1

        if sum(self.board[7:12]) == 0 and (self.board[0] > 0 or self.board[6] > 0):
            self.score[1] -= 5
            for i in range(7, 12):
                self.board[i] = 1

    def check_game_over(self) -> bool:
        if self.board[0] == 0 and self.board[6] == 0:
            for i in range(1, 6):
                self.score[0] += self.board[i]
                self.board[i] = 0
            for i in range(7, 12):
                self.score[1] += self.board[i]
                self.board[i] = 0
            self.game_over = True
            return True
        return False

    def apply_move(self, start_idx: int, direction: int, render_callback=None):
        self.is_animating = True
        actual_dir = direction if self.current_player == 0 else -direction
        hand = self.board[start_idx]
        self.board[start_idx] = 0
        pos = start_idx

        while hand > 0:
            pos = (pos + actual_dir) % 12
            self.current_hand_pos = pos
            self.board[pos] += 1
            hand -= 1
            if render_callback:
                render_callback()

        while True:
            next_pos = (pos + actual_dir) % 12
            if self.board[next_pos] > 0 and next_pos not in (0, 6):
                hand = self.board[next_pos]
                self.board[next_pos] = 0
                pos = next_pos
                while hand > 0:
                    pos = (pos + actual_dir) % 12
                    self.current_hand_pos = pos
                    self.board[pos] += 1
                    hand -= 1
                    if render_callback:
                        render_callback()
                continue

            if self.board[next_pos] == 0:
                target = (next_pos + actual_dir) % 12
                if self.board[target] > 0:
                    self.score[self.current_player] += self.board[target]
                    self.board[target] = 0
                    self.current_hand_pos = target
                    if render_callback:
                        render_callback()
                break

            break

        self.current_hand_pos = -1
        self.selected_index = -1
        self.is_animating = False

        if not self.check_game_over():
            self.current_player = 1 - self.current_player
            self.handle_empty_rows()

    def get_valid_moves(self) -> list[tuple[int, int]]:
        if self.current_player == 0:
            indexes = range(1, 6)
        else:
            indexes = range(7, 12)
        return [(i, d) for i in indexes if self.board[i] > 0 for d in (1, -1)]
