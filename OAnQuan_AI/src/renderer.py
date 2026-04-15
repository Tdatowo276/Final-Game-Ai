import random
import pygame
from constants import BOARD_BORDER, BG_COLOR, SEED_COLOR, HIGHLIGHT, TEXT_COLOR, BTN_COLOR, BTN_HOVER, HAND_COLOR
from src.board import BoardState

FONT_MAIN = None
FONT_SUB = None


def init_renderer():
    global FONT_MAIN, FONT_SUB
    FONT_MAIN = pygame.font.SysFont("Arial", 45, bold=True)
    FONT_SUB = pygame.font.SysFont("Arial", 25, bold=True)


def draw_button(screen, text, x, y, w, h, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    is_hover = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = active_color if is_hover else inactive_color
    pygame.draw.rect(screen, color, rect, border_radius=12)

    txt_surf = FONT_SUB.render(text, True, (255, 255, 255))
    txt_rect = txt_surf.get_rect(center=rect.center)
    screen.blit(txt_surf, txt_rect)
    return is_hover and click[0] == 1


def get_cell_rects():
    board_w, board_h = 700, 200
    start_x = (pygame.display.get_surface().get_width() - board_w) // 2
    start_y = (pygame.display.get_surface().get_height() - board_h) // 2
    cell_size = 100
    rects = [None] * 12
    rects[0] = pygame.Rect(start_x, start_y, 100, 200)
    rects[6] = pygame.Rect(start_x + 600, start_y, 100, 200)
    for i in range(5):
        rects[i + 1] = pygame.Rect(start_x + 100 + (i * cell_size), start_y + 100, cell_size, cell_size)
        rects[11 - i] = pygame.Rect(start_x + 100 + (i * cell_size), start_y, cell_size, cell_size)
    return rects


def draw_interface_game(screen, board_state: BoardState, is_pvp: bool):
    screen.fill(BG_COLOR)
    rects = get_cell_rects()
    pygame.draw.rect(screen, BOARD_BORDER, (rects[0].x, rects[0].y, 700, 200), 2, border_radius=25)

    for i in range(12):
        if i == board_state.selected_index:
            pygame.draw.rect(screen, HIGHLIGHT, rects[i].inflate(-4, -4))
        if i == board_state.current_hand_pos:
            pygame.draw.rect(screen, HAND_COLOR, rects[i].inflate(-2, -2), 4, border_radius=10)

        txt = pygame.font.SysFont("Verdana", 14, bold=True).render(str(board_state.board[i]), True, TEXT_COLOR)
        screen.blit(txt, (rects[i].x + 8, rects[i].y + 8))

        if i in (0, 6) and board_state.board[i] >= 10:
            pygame.draw.ellipse(screen, SEED_COLOR, (rects[i].centerx - 20, rects[i].centery - 40, 40, 80))
        elif board_state.board[i] > 0:
            cell_random = random.Random(i)
            for _ in range(min(board_state.board[i], 15)):
                rx = cell_random.randint(rects[i].x + 25, rects[i].right - 25)
                ry = cell_random.randint(rects[i].y + 25, rects[i].bottom - 25)
                pygame.draw.circle(screen, SEED_COLOR, (rx, ry), 4)

        if i != 0 and i != 6:
            pygame.draw.rect(screen, BOARD_BORDER, rects[i], 1)

    font_s = pygame.font.SysFont("Arial", 22, bold=True)
    p2_label = "MÁY (P2)" if not is_pvp else "NGƯỜI 2 (P2)"
    screen.blit(font_s.render(f"NGƯỜI 1 (P1): {board_state.score[0]}", True, (50, 50, 150)), (50, pygame.display.get_surface().get_height() - 60))
    screen.blit(font_s.render(f"{p2_label}: {board_state.score[1]}", True, (150, 50, 50)), (pygame.display.get_surface().get_width() - 300, 40))

    if board_state.game_over:
        msg = "HÒA!" if board_state.score[0] == board_state.score[1] else ("BẠN THẮNG!" if board_state.score[0] > board_state.score[1] else f"{p2_label} THẮNG!")
        txt = font_s.render(f"KẾT THÚC: {msg}", True, (200, 0, 0))
        screen.blit(txt, (pygame.display.get_surface().get_width() // 2 - txt.get_width() // 2, pygame.display.get_surface().get_height() - 100))

    left_btn = None
    right_btn = None
    if board_state.selected_index != -1 and not board_state.is_animating and not board_state.game_over:
        r = rects[board_state.selected_index]
        left_btn = pygame.Rect(r.centerx - 45, r.centery - 15, 40, 30)
        right_btn = pygame.Rect(r.centerx + 5, r.centery - 15, 40, 30)
        pygame.draw.rect(screen, BTN_COLOR, left_btn, border_radius=5)
        pygame.draw.rect(screen, BTN_COLOR, right_btn, border_radius=5)
        font_btn = pygame.font.SysFont("Arial", 20, bold=True)
        screen.blit(font_btn.render("<", True, (255, 255, 255)), (left_btn.centerx - 7, left_btn.centery - 12))
        screen.blit(font_btn.render(">", True, (255, 255, 255)), (right_btn.centerx - 7, right_btn.centery - 12))

    return left_btn, right_btn
