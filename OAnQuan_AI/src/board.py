from dataclasses import dataclass
from typing import List


@dataclass
class BoardState:
    board: List[int]#mang luu 12 o (0 va 6 la quan)
    score: List[int]#mang luu diem cua 2 nguoi
    current_player: int = 0#nguoi choi hien tai (0: player1 hoac 1: player2/AI)
    selected_index: int = -1#vi tri o dang duoc chon
    current_hand_pos: int = -1#vi tri o dang duoc rai quan
    is_animating: bool = False#trang thai dang hoat anh // neu value=true -> nguoi choi khong click vao ban co
    game_over: bool = False#trang thai ket thuc game

    @classmethod
    def new(cls): #method tao ra ban co 
        return cls([10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5], [0, 0])

    def reset(self):  #reset trang thai ban co
        self.board = [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5]
        self.score = [0, 0]
        self.current_player = 0
        self.selected_index = -1
        self.current_hand_pos = -1
        self.is_animating = False
        self.game_over = False

    def clone(self):#tao ra ban sao cua trang thai de AI mo phong nuoc di trong tuong lai
        return BoardState(self.board.copy(), self.score.copy(), self.current_player,
                          self.selected_index, self.current_hand_pos,
                          self.is_animating, self.game_over)

    def handle_empty_rows(self):#kiem tra neu hang cua nguoi choi het dan thi se -5đ va rai 1 quan vao cac o
        if sum(self.board[1:6]) == 0 and (self.board[0] > 0 or self.board[6] > 0):
            self.score[0] -= 5
            for i in range(1, 6):
                self.board[i] = 1

        if sum(self.board[7:12]) == 0 and (self.board[0] > 0 or self.board[6] > 0):
            self.score[1] -= 5
            for i in range(7, 12):
                self.board[i] = 1

    def check_game_over(self) -> bool:#kiem tra xem game ket thuc chua
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

    def apply_move(self, start_idx: int, direction: int, render_callback=None):#thuc hien nuoc di
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
            # 1. Nếu hạt cuối rơi vào ô Quan (0 hoặc 6) -> Dừng lượt
            if pos in (0, 6):
                break
            next_pos = (pos + actual_dir) % 12
            # 2. Nếu ô tiếp theo là ô Quan -> Dừng lượt (không được bốc quân từ ô Quan)
            if next_pos in (0, 6):
                break
            # 3. Phân nhánh: Ô tiếp theo có quân hay không?
            if self.board[next_pos] > 0:
                # Bốc quân rải tiếp (vì không phải ô Quan và có quân)
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
                continue  # Quay lại kiểm tra sau khi rải xong nắm quân mới
            else:
                # Ô tiếp theo trống -> Kiểm tra ô sau nó để ăn quân
                while True:
                    empty_pos = next_pos
                    target_pos = (empty_pos + actual_dir) % 12
                    
                    if self.board[target_pos] > 0:
                        # ĂN QUÂN
                        self.score[self.current_player] += self.board[target_pos]
                        self.board[target_pos] = 0
                        self.current_hand_pos = target_pos
                        if render_callback:
                            render_callback()
                        
                        # KIỂM TRA ĂN CHUỖI: Ô tiếp sau ô vừa ăn phải trống thì mới được ăn tiếp ô sau nữa
                        next_empty_pos = (target_pos + actual_dir) % 12
                        if self.board[next_empty_pos] == 0:
                            next_pos = next_empty_pos
                            continue # Lặp lại để kiểm tra ăn ô tiếp theo
                        else:
                            break # Ô sau ô vừa ăn có quân -> Dừng
                    else:
                        # Ô sau ô trống cũng trống -> Hai ô trống liên tiếp -> Dừng
                        break
                break # Kết thúc chuỗi ăn quân hoặc dừng do 2 ô trống

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
