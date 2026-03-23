import pygame
import random
import copy

# --- CẤU HÌNH HỆ THỐNG ---
pygame.init()
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ô Ăn Quan AI - Bản Hoàn Thiện Cuối Cùng")
clock = pygame.time.Clock()

# --- MÀU SẮC ---
BG_COLOR = (248, 245, 237)
BOARD_BORDER = (160, 145, 130)
SEED_COLOR = (100, 85, 70)
HIGHLIGHT = (210, 200, 255)
TEXT_COLOR = (80, 70, 60)
BTN_COLOR = (100, 200, 100)
HAND_COLOR = (255, 100, 100)

# --- KHỞI TẠO DỮ LIỆU ---
board = [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5]
score = [0, 0] 
selected_index = -1
current_player = 0 
is_animating = False
current_hand_pos = -1
game_over = False

def get_cell_rects():
    board_w, board_h = 700, 200
    start_x = (WIDTH - board_w) // 2
    start_y = (HEIGHT - board_h) // 2
    cell_size = 100
    rects = [None] * 12
    rects[0] = pygame.Rect(start_x, start_y, 100, 200)
    rects[6] = pygame.Rect(start_x + 600, start_y, 100, 200)
    for i in range(5):
        rects[i+1] = pygame.Rect(start_x + 100 + (i * cell_size), start_y + 100, cell_size, cell_size)
        rects[11-i] = pygame.Rect(start_x + 100 + (i * cell_size), start_y, cell_size, cell_size)
    return rects

# --- HÀM KIỂM TRA HẾT DÂN (REPLENISH) ---
def handle_empty_rows():
    global score, board
    # Kiểm tra P1 (index 1-5)
    if sum(board[1:6]) == 0 and (board[0] > 0 or board[6] > 0):
        print("P1 hết dân, tự động rải 5 quân.")
        score[0] -= 5
        for i in range(1, 6): board[i] = 1

    # Kiểm tra P2 (index 7-11)
    if sum(board[7:12]) == 0 and (board[0] > 0 or board[6] > 0):
        print("AI hết dân, tự động rải 5 quân.")
        score[1] -= 5
        for i in range(7, 12): board[i] = 1

# --- HÀM KIỂM TRA KẾT THÚC ---
def check_game_over():
    global game_over, score
    if board[0] == 0 and board[6] == 0:
        for i in range(1, 6): score[0] += board[i]; board[i] = 0
        for i in range(7, 12): score[1] += board[i]; board[i] = 0
        game_over = True
        return True
    return False

# --- LOGIC GIẢ LẬP AI ---
def simulate_move(curr_board, curr_scores, start_idx, direction, player_idx):
    temp_b = list(curr_board)
    temp_s = list(curr_scores)
    actual_dir = direction if player_idx == 0 else -direction
    hand = temp_b[start_idx]
    temp_b[start_idx] = 0
    pos = start_idx
    while hand > 0:
        while hand > 0:
            pos = (pos + actual_dir) % 12
            temp_b[pos] += 1
            hand -= 1
        next_p = (pos + actual_dir) % 12
        if temp_b[next_p] > 0 and next_p != 0 and next_p != 6:
            hand = temp_b[next_p]; temp_b[next_p] = 0; pos = next_p
        elif temp_b[next_p] == 0:
            while temp_b[next_p] == 0:
                target = (next_p + actual_dir) % 12
                if temp_b[target] > 0:
                    temp_s[player_idx] += temp_b[target]; temp_b[target] = 0
                    next_p = (target + actual_dir) % 12
                    if temp_b[next_p] != 0: break
                else: break
            break
        else: break
    return temp_b, temp_s

def minimax(b, s, depth, alpha, beta, is_max):
    if depth == 0 or (b[0] == 0 and b[6] == 0):
        return s[1] - s[0], None, None
    best_move = (None, None)
    if is_max:
        max_eval = float('-inf')
        for i in range(7, 12):
            if b[i] > 0:
                for d in [1, -1]:
                    nb, ns = simulate_move(b, s, i, d, 1)
                    ev, _, _ = minimax(nb, ns, depth-1, alpha, beta, False)
                    if ev > max_eval: max_eval = ev; best_move = (i, d)
                    alpha = max(alpha, ev)
                    if beta <= alpha: break
        return max_eval, best_move[0], best_move[1]
    else:
        min_eval = float('inf')
        for i in range(1, 6):
            if b[i] > 0:
                for d in [1, -1]:
                    nb, ns = simulate_move(b, s, i, d, 0)
                    ev, _, _ = minimax(nb, ns, depth-1, alpha, beta, True)
                    if ev < min_eval: min_eval = ev; best_move = (i, d)
                    beta = min(beta, ev)
                    if beta <= alpha: break
        return min_eval, best_move[0], best_move[1]

# --- VẼ GIAO DIỆN ---
def draw_interface():
    screen.fill(BG_COLOR)
    rects = get_cell_rects()
    pygame.draw.rect(screen, BOARD_BORDER, (rects[0].x, rects[0].y, 700, 200), 2, border_radius=25)
    for i in range(12):
        if i == selected_index: pygame.draw.rect(screen, HIGHLIGHT, rects[i].inflate(-4, -4))
        if i == current_hand_pos: pygame.draw.rect(screen, HAND_COLOR, rects[i].inflate(-2, -2), 4, border_radius=10)
        font = pygame.font.SysFont("Verdana", 14, bold=True)
        txt = font.render(str(board[i]), True, TEXT_COLOR)
        screen.blit(txt, (rects[i].x + 8, rects[i].y + 8))
        if (i == 0 or i == 6) and board[i] >= 10:
            pygame.draw.ellipse(screen, SEED_COLOR, (rects[i].centerx-20, rects[i].centery-40, 40, 80))
        elif board[i] > 0:
            random.seed(i)
            for _ in range(min(board[i], 15)):
                rx, ry = random.randint(rects[i].x+25, rects[i].right-25), random.randint(rects[i].y+25, rects[i].bottom-25)
                pygame.draw.circle(screen, SEED_COLOR, (rx, ry), 4)
        if i != 0 and i != 6: pygame.draw.rect(screen, BOARD_BORDER, rects[i], 1)
    font_s = pygame.font.SysFont("Arial", 22, bold=True)
    screen.blit(font_s.render(f"NGƯỜI CHƠI (P1): {score[0]}", True, (50, 50, 150)), (50, HEIGHT - 60))
    screen.blit(font_s.render(f"TRÍ TUỆ NHÂN TẠO (AI): {score[1]}", True, (150, 50, 50)), (WIDTH - 320, 40))
    if game_over:
        msg = "HÒA!" if score[0] == score[1] else ("BẠN THẮNG!" if score[0] > score[1] else "AI THẮNG!")
        txt = font_s.render(f"GAME OVER: {msg}", True, (200, 0, 0))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 40))
    if selected_index != -1 and not is_animating and not game_over:
        r = rects[selected_index]
        btn_l, btn_r = pygame.Rect(r.centerx - 45, r.centery - 15, 40, 30), pygame.Rect(r.centerx + 5, r.centery - 15, 40, 30)
        pygame.draw.rect(screen, BTN_COLOR, btn_l, border_radius=5); pygame.draw.rect(screen, BTN_COLOR, btn_r, border_radius=5)
        font_btn = pygame.font.SysFont("Arial", 20, bold=True)
        screen.blit(font_btn.render("<", True, (255,255,255)), (btn_l.centerx-7, btn_l.centery-12))
        screen.blit(font_btn.render(">", True, (255,255,255)), (btn_r.centerx-7, btn_r.centery-12))
        return btn_l, btn_r
    return None, None

# --- LOGIC DI CHUYỂN ---
def move_logic(start_idx, direction):
    global current_player, selected_index, is_animating, current_hand_pos
    is_animating = True
    actual_dir = direction if current_player == 0 else -direction
    hand = board[start_idx]; board[start_idx] = 0; pos = start_idx
    while hand > 0:
        while hand > 0:
            pos = (pos + actual_dir) % 12
            current_hand_pos = pos; board[pos] += 1; hand -= 1
            draw_interface(); pygame.display.flip(); pygame.time.wait(300)
        pygame.time.wait(500)
        next_p = (pos + actual_dir) % 12
        current_hand_pos = next_p; draw_interface(); pygame.display.flip()
        if board[next_p] > 0 and next_p != 0 and next_p != 6:
            hand = board[next_p]; board[next_p] = 0; pos = next_p; pygame.time.wait(400)
        elif board[next_p] == 0:
            while board[next_p] == 0:
                target = (next_p + actual_dir) % 12
                if board[target] > 0:
                    score[current_player] += board[target]; board[target] = 0; current_hand_pos = target
                    draw_interface(); pygame.display.flip(); pygame.time.wait(800)
                    next_p = (target + actual_dir) % 12
                    if board[next_p] != 0: break
                else: break
            break
        else: break
    current_hand_pos = -1; selected_index = -1; is_animating = False
    if not check_game_over():
        current_player = 1 - current_player
        handle_empty_rows() # KIỂM TRA HẾT DÂN NGAY SAU KHI ĐỔI LƯỢT

# --- MAIN LOOP ---
rects = get_cell_rects()
running = True
handle_empty_rows() # Kiểm tra rải quân lúc bắt đầu game
while running:
    btn_l, btn_r = draw_interface()
    if current_player == 1 and not is_animating and not game_over:
        pygame.display.flip(); pygame.time.wait(800)
        _, ai_idx, ai_dir = minimax(board, score, 3, float('-inf'), float('inf'), True)
        if ai_idx is not None: move_logic(ai_idx, ai_dir)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not is_animating and not game_over and current_player == 0:
            pos = pygame.mouse.get_pos()
            if btn_l and btn_l.collidepoint(pos): move_logic(selected_index, -1)
            elif btn_r and btn_r.collidepoint(pos): move_logic(selected_index, 1)
            else:
                for i in range(1, 6):
                    if rects[i].collidepoint(pos) and board[i] > 0: selected_index = i
    pygame.display.flip(); clock.tick(60)
pygame.quit()