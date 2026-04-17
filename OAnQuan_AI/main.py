import pygame
from src.board import BoardState
from src.ai_engine import choose_ai_move
import src.audio as audio
from src.audio import init_audio, play_bgm, play_move_sound, adjust_bgm_volume, cycle_sfx, get_current_sfx_name
from src.renderer import init_renderer, draw_button, draw_interface_game, get_cell_rects
from constants import WIDTH, HEIGHT, FPS, BG_COLOR


def draw_rules_screen(screen, font_title, font_body):
    screen.fill(BG_COLOR)
    width = screen.get_width()
    height = screen.get_height()
    title = font_title.render("RULES", True, (80, 70, 60))
    screen.blit(title, (width // 2 - title.get_width() // 2, 80))

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

    back_rect = pygame.Rect(width // 2 - 120, height - 120, 240, 50)
    pygame.draw.rect(screen, (120, 110, 100), back_rect, border_radius=12)
    back_text = font_body.render("BACK", True, (255, 255, 255))
    screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))
    return back_rect


def main():
    pygame.mixer.pre_init(44100, -16, 2, 256)
    pygame.init()
    init_audio()
    play_bgm()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Ô ĂN QUAN AI - Nhóm 14")
    clock = pygame.time.Clock()
    init_renderer()

    font_menu_title = pygame.font.SysFont("Arial", 45, bold=True)
    font_rules_title = pygame.font.SysFont("Arial", 40, bold=True)
    font_rules_body = pygame.font.SysFont("Arial", 22)
    font_status = pygame.font.SysFont("Arial", 22, bold=True)

    game_state = 0
    ai_difficulty = 3
    is_pvp = False
    board_state = BoardState.new()
    move_step_delay = 300 # co the tang hoac giam toc do rai quan tai day
    player_turn_count = 0
    ai_turn_count = 0

    def delay(milliseconds):
        nonlocal running
        target_time = pygame.time.get_ticks() + milliseconds
        while running and pygame.time.get_ticks() < target_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(FPS)

    def render_frame(extra_delay: int = 0, left_status: str | None = None, right_status: str | None = None):
        draw_interface_game(screen, board_state, is_pvp, left_status, right_status)
        pygame.display.flip()
        clock.tick(FPS)
        if extra_delay > 0:
            delay(extra_delay)

    def sound_and_render(left_status: str | None = None, right_status: str | None = None):
        play_move_sound()
        render_frame(move_step_delay, left_status, right_status)

    running = True
    while running:
        if game_state == 0:
            screen.fill(BG_COLOR)
            width = screen.get_width()
            title = font_menu_title.render("Ô ĂN QUAN AI", True, (80, 70, 60))
            screen.blit(title, (width // 2 - title.get_width() // 2, 150))
            if draw_button(screen, "PLAYER VS PLAYER", width // 2 - 150, 270, 300, 60, (120, 110, 100), (180, 170, 160)):
                is_pvp = True
                board_state.reset()
                player_turn_count = 0
                ai_turn_count = 0
                game_state = 2
                delay(200)
            if draw_button(screen, "PLAYER VS AI", width // 2 - 150, 360, 300, 60, (120, 110, 100), (180, 170, 160)):
                is_pvp = False
                player_turn_count = 0
                ai_turn_count = 0
                game_state = 1
                delay(200)
            if draw_button(screen, "RULES", width // 2 - 150, 450, 300, 60, (100, 140, 200), (120, 170, 220)):
                game_state = 4
                delay(200)
            if draw_button(screen, "SETTINGS", width // 2 - 150, 540, 300, 60, (100, 140, 200), (120, 170, 220)):
                game_state = 5
                delay(200)

        elif game_state == 1:
            screen.fill(BG_COLOR)
            width = screen.get_width()
            title = font_menu_title.render("CHOOSE DIFFICULTY", True, (80, 70, 60))
            screen.blit(title, (width // 2 - title.get_width() // 2, 150))
            if draw_button(screen, "EASY", width // 2 - 150, 280, 300, 50, (100, 180, 100), (120, 200, 120)):
                ai_difficulty = 1
                board_state.reset()
                game_state = 3
                delay(200)
            if draw_button(screen, "MEDIUM", width // 2 - 150, 360, 300, 50, (200, 150, 50), (220, 170, 70)):
                ai_difficulty = 3
                board_state.reset()
                game_state = 3
                delay(200)
            if draw_button(screen, "HARD", width // 2 - 150, 440, 300, 50, (180, 50, 50), (200, 70, 70)):
                ai_difficulty = 5
                board_state.reset()
                game_state = 3
                delay(200)
            if draw_button(screen, "BACK", width // 2 - 150, 520, 300, 50, (100, 100, 100), (150, 150, 150)):
                game_state = 0
                delay(200)

        elif game_state == 4:
            back_rect = draw_rules_screen(screen, font_rules_title, font_rules_body)
            if back_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
                game_state = 0
                delay(200)

        elif game_state == 5:
            screen.fill(BG_COLOR)
            width = screen.get_width()
            title = font_rules_title.render("SETTINGS", True, (80, 70, 60))
            screen.blit(title, (width // 2 - title.get_width() // 2, 150))
            
            vol_percent = int(audio.bgm_volume * 100)
            vol_text = f"VOLUME: {vol_percent}%"
            # Draw volume display (middle)
            draw_button(screen, vol_text, width // 2 - 75, 270, 150, 60, (120, 110, 100), (120, 110, 100))
            # Draw Minus button
            if draw_button(screen, "-", width // 2 - 175, 270, 80, 60, (200, 100, 100), (220, 120, 120)):
                adjust_bgm_volume(-0.1)
                delay(150)
            # Draw Plus button
            if draw_button(screen, "+", width // 2 + 95, 270, 80, 60, (100, 200, 100), (120, 220, 120)):
                adjust_bgm_volume(0.1)
                delay(150)
                
            sfx_name = get_current_sfx_name()
            sfx_text = f"EFFECTS: {sfx_name}"
            if draw_button(screen, sfx_text, width // 2 - 175, 360, 350, 60, (120, 110, 100), (180, 170, 160)):
                cycle_sfx()
                play_move_sound() # Play sound to preview
                delay(200)

            if draw_button(screen, "BACK", width // 2 - 175, 450, 350, 60, (100, 140, 200), (120, 170, 220)):
                game_state = 0
                delay(200)
        elif game_state in [2, 3]:
            left_status = None
            right_status = None
            
            p1_label = "P1"
            p2_label = "P2" if is_pvp else "AI"
            
            left_status = f"{p1_label}: {player_turn_count} turns"
            right_status = f"{p2_label}: {ai_turn_count} turns"
            
            if board_state.current_player == 0:
                left_status += " - Your turn"
            else:
                right_status += " - Your turn"

            btn_l, btn_r = draw_interface_game(screen, board_state, is_pvp, left_status, right_status)
            if draw_button(screen, "EXIT", 20, 70, 100, 40, (150, 70, 70), (180, 90, 90)):
                game_state = 0
                delay(200)

            if game_state == 3 and board_state.current_player == 1 and not board_state.is_animating and not board_state.game_over:
                delay(500)
                ai_idx, ai_dir = choose_ai_move(board_state.board, board_state.score, ai_difficulty)
                if ai_idx is not None:
                    board_state.apply_move(ai_idx, ai_dir, lambda: sound_and_render(left_status, right_status))
                    ai_turn_count += 1

        rects = get_cell_rects()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and not board_state.is_animating and not board_state.game_over:
                pos = pygame.mouse.get_pos()
                if game_state in [2, 3]:
                    if btn_l and btn_l.collidepoint(pos):
                        board_state.apply_move(board_state.selected_index, -1, lambda: sound_and_render(left_status, right_status))
                        if board_state.current_player == 1: # After apply_move, player already swapped in some implementations, but here apply_move might be async or inside. 
                                                           # Actually current_player is swapped AFTER animation usually or inside apply_move.
                                                           # Let's check BoardState.apply_move
                            player_turn_count += 1
                        else:
                            ai_turn_count += 1
                    elif btn_r and btn_r.collidepoint(pos):
                        board_state.apply_move(board_state.selected_index, 1, lambda: sound_and_render(left_status, right_status))
                        if board_state.current_player == 1:
                            player_turn_count += 1
                        else:
                            ai_turn_count += 1
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
