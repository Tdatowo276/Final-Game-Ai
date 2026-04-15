import pygame
from src.board import BoardState
from src.ai_engine import choose_ai_move
from src.audio import init_audio, play_bgm, play_move_sound
from src.renderer import init_renderer, draw_button, draw_interface_game, get_cell_rects
from constants import WIDTH, HEIGHT, FPS, BG_COLOR


def draw_rules_screen(screen):
    screen.fill(BG_COLOR)
    font_title = pygame.font.SysFont("Arial", 40, bold=True)
    font_body = pygame.font.SysFont("Arial", 22)
    title = font_title.render("LUẬT CHƠI Ô ĂN QUAN", True, (80, 70, 60))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    rules = [
        "- Mỗi bên có 5 ô nhỏ tương ứng với 5 ô dân, 2 ô quan lớn ở hai đầu.",
        "- Người chơi chọn 1 ô dân trên phần mình, rồi chọn hướng < hoặc > để bắt đầu rải quân.",
        "- Rải quân lần lượt sang các ô theo hướng đã chọn.",
        "- Nếu ô tiếp theo còn quân, tiếp tục nhặt và rải tiếp.",
        "- Nếu ô tiếp theo trống, ăn quân ở ô kế tiếp (nếu có).",
        "- Nếu 5 ô quân của bên mình hết hạt, mất 5 điểm để rải cho mỗi ô 1 quân.",
        "- Trò chơi kết thúc khi cả 2 ô quan đều hết quân.",
        "- Ai nhiều điểm hơn sẽ là người thắng.",
        "Nhấn THOÁT hoặc nhấp vào nút TRỞ VỀ để quay lại MENU.",
    ]

    y = 160
    for line in rules:
        text = font_body.render(line, True, (70, 60, 50))
        screen.blit(text, (80, y))
        y += 36

    back_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 120, 240, 50)
    pygame.draw.rect(screen, (120, 110, 100), back_rect, border_radius=12)
    back_text = font_body.render("TRỞ VỀ MENU", True, (255, 255, 255))
    screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))
    return back_rect


def main():
    pygame.mixer.pre_init(44100, -16, 2, 256)
    pygame.init()
    init_audio()
    play_bgm()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ô ĂN QUAN AI - Nhóm 14")
    clock = pygame.time.Clock()
    init_renderer()

    game_state = 0
    ai_difficulty = 3
    is_pvp = False
    board_state = BoardState.new()
    rects = get_cell_rects()

    def render_frame():
        draw_interface_game(screen, board_state, is_pvp)
        pygame.display.flip()
        pygame.time.wait(180)

    def sound_and_render():
        play_move_sound()
        render_frame()

    running = True
    while running:
        if game_state == 0:
            screen.fill(BG_COLOR)
            title = pygame.font.SysFont("Arial", 45, bold=True).render("Ô ĂN QUAN AI", True, (80, 70, 60))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
            if draw_button(screen, "NGƯỜI VS NGƯỜI", WIDTH // 2 - 150, 300, 300, 60, (120, 110, 100), (180, 170, 160)):
                is_pvp = True
                board_state.reset()
                game_state = 2
                pygame.time.wait(200)
            if draw_button(screen, "NGƯỜI VS MÁY", WIDTH // 2 - 150, 400, 300, 60, (120, 110, 100), (180, 170, 160)):
                is_pvp = False
                game_state = 1
                pygame.time.wait(200)
            if draw_button(screen, "LUẬT CHƠI", WIDTH // 2 - 150, 500, 300, 60, (100, 140, 200), (120, 170, 220)):
                game_state = 4
                pygame.time.wait(200)

        elif game_state == 1:
            screen.fill(BG_COLOR)
            title = pygame.font.SysFont("Arial", 45, bold=True).render("CHỌN MỨC ĐỘ", True, (80, 70, 60))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
            if draw_button(screen, "DỄ (AI NON NỚT)", WIDTH // 2 - 150, 280, 300, 50, (100, 180, 100), (120, 200, 120)):
                ai_difficulty = 1
                board_state.reset()
                game_state = 3
                pygame.time.wait(200)
            if draw_button(screen, "KHÓ (AI CÂN TẤT)", WIDTH // 2 - 150, 360, 300, 50, (200, 150, 50), (220, 170, 70)):
                ai_difficulty = 3
                board_state.reset()
                game_state = 3
                pygame.time.wait(200)
            if draw_button(screen, "SIÊU KHÓ (MASTER)", WIDTH // 2 - 150, 440, 300, 50, (180, 50, 50), (200, 70, 70)):
                ai_difficulty = 5
                board_state.reset()
                game_state = 3
                pygame.time.wait(200)
            if draw_button(screen, "BACK", WIDTH // 2 - 150, 520, 300, 50, (100, 100, 100), (150, 150, 150)):
                game_state = 0
                pygame.time.wait(200)

        elif game_state == 4:
            back_rect = draw_rules_screen(screen)
            if draw_button(screen, "THOÁT", 20, 20, 100, 40, (150, 70, 70), (180, 90, 90)):
                game_state = 0
                pygame.time.wait(200)
            if back_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
                game_state = 0
                pygame.time.wait(200)
        elif game_state in [2, 3]:
            btn_l, btn_r = draw_interface_game(screen, board_state, is_pvp)
            if draw_button(screen, "THOÁT", 20, 20, 100, 40, (150, 70, 70), (180, 90, 90)):
                game_state = 0
                pygame.time.wait(200)

            if game_state == 3 and board_state.current_player == 1 and not board_state.is_animating and not board_state.game_over:
                pygame.display.flip()
                pygame.time.wait(800)
                ai_idx, ai_dir = choose_ai_move(board_state.board, board_state.score, ai_difficulty)
                if ai_idx is not None:
                    board_state.apply_move(ai_idx, ai_dir, sound_and_render)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not board_state.is_animating and not board_state.game_over:
                pos = pygame.mouse.get_pos()
                if game_state in [2, 3]:
                    if btn_l and btn_l.collidepoint(pos):
                        board_state.apply_move(board_state.selected_index, -1, sound_and_render)
                    elif btn_r and btn_r.collidepoint(pos):
                        board_state.apply_move(board_state.selected_index, 1, sound_and_render)
                    else:
                        v_range = range(1, 6) if board_state.current_player == 0 else range(7, 12)
                        if game_state == 3 and board_state.current_player == 1:
                            v_range = range(0)
                        for i in v_range:
                            if rects[i].collidepoint(pos) and board_state.board[i] > 0:
                                board_state.selected_index = i

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
