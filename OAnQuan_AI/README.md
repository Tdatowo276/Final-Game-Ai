# Ô Ăn Quan AI

Phiên bản `OAnQuan_AI` là một game Ô Ăn Quan với chế độ PvP và PvE, dùng Pygame cho giao diện và Minimax cho AI.

## Chạy game

1. Mở terminal tại thư mục `OAnQuan_AI`
2. Tạo môi trường ảo (tuỳ chọn):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Cài dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Chạy game:
   ```bash
   python main.py
   ```

## Chức năng

- Menu chính: chọn `NGƯỜI VS NGƯỜI`, `NGƯỜI VS MÁY`, hoặc `LUẬT CHƠI`
- Chế độ chọn độ khó cho AI
- Game PvP và PvE
- Giao diện với nút chọn hướng và hiển thị điểm
- Âm thanh nền và hiệu ứng đi quân

## Cấu trúc

- `main.py`: vòng lặp game, menu, và xử lý sự kiện
- `constants.py`: cấu hình màu sắc, kích thước, FPS
- `src/board.py`: trạng thái bàn cờ, luật rải quân, kiểm tra game over
- `src/game_logic.py`: thuật toán Minimax và mô phỏng nước đi
- `src/ai_engine.py`: lựa chọn nước đi cho máy
- `src/renderer.py`: vẽ giao diện và font cache
- `src/audio.py`: khởi tạo âm thanh và phát hiệu ứng

## Kiểm thử

Chạy kiểm thử bằng `pytest`:

```bash
pytest tests
```
