# Ô Ăn Quan AI

Phiên bản `OAnQuan_AI` là một game Ô Ăn Quan với chế độ PvP và PvE, dùng Pygame cho giao diện và Minimax cho AI.

## Yêu cầu hệ thống

| Yêu cầu | Chi tiết |
| **Python** | 3.10 trở lên |
| **pip** | Đi kèm Python (phiên bản bất kỳ) |
| **Hệ điều hành** | Windows / macOS / Linux (cần giao diện đồ họa desktop) |
| **Font hệ thống** | Arial, Verdana (Windows/macOS có sẵn. Linux: `sudo apt install fonts-liberation`) |
| **Âm thanh** | Loa hoặc tai nghe (tuỳ chọn — game vẫn chạy nếu không có) |

## Chạy game

1. Mở terminal tại thư mục `OAnQuan_AI`
2. Tạo môi trường ảo (tuỳ chọn):

   **2.1** Tạo môi trường ảo:
   ```bash
   python -m venv .venv
   ```

   **2.2** Kích hoạt môi trường ảo:

   - **Windows:**
     ```bash
     .\.venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
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
- Chế độ chọn độ khó cho AI (Easy / Medium / Hard)
- Game PvP và PvE
- Giao diện với nút chọn hướng và hiển thị điểm
- Âm thanh nền và hiệu ứng đi quân (có thể tuỳ chỉnh trong Settings)

## Cấu trúc

- `main.py`: vòng lặp game, menu, và xử lý sự kiện
- `constants.py`: cấu hình màu sắc, kích thước, FPS
- `src/board.py`: trạng thái bàn cờ, luật rải quân, kiểm tra game over
- `src/game_logic.py`: thuật toán Minimax và mô phỏng nước đi
- `src/ai_engine.py`: lựa chọn nước đi cho máy
- `src/renderer.py`: vẽ giao diện và font cache
- `src/audio.py`: khởi tạo âm thanh và phát hiệu ứng
- `src/utils.py`: hàm tiện ích lấy đường dẫn tài nguyên

## Kiểm thử

Chạy kiểm thử bằng `pytest`:

```bash
pytest tests
```
