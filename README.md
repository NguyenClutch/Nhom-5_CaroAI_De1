# Caro AI

Caro AI là chương trình chơi cờ Caro viết bằng Python. Dự án hỗ trợ giao diện Pygame để chơi trực tiếp, chế độ AI đấu AI cho kiểm thử nhanh và chế độ benchmark để so sánh Minimax với Alpha-Beta.

## Yêu cầu

- Python 3.10 trở lên
- `pip`
- Hệ điều hành Windows, Linux hoặc macOS có thể chạy Python và Pygame

Thư viện chính được khai báo trong `requirements.txt`:

- `pygame`
- `numpy`

## Cài đặt


Tạo môi trường ảo:

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Nếu dùng Command Prompt:

```bat
.\.venv\Scripts\activate.bat
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

## Cách chạy chương trình

### 1. Chơi bằng giao diện Pygame

Chạy lệnh:

```bash
python main.py
```

Chương trình sẽ mở cửa sổ game Caro. Người chơi có thể chọn các chế độ trên giao diện:

- `Người - Người`: hai người chơi trên cùng máy.
- `Người - Máy`: người chơi đánh với AI.
- `Máy - Máy`: hai AI tự đánh với nhau.
- `Minimax` hoặc `Alpha-Beta`: chọn thuật toán AI.
- `Chơi lại`: tạo ván mới.
- `Thoát`: đóng chương trình.

Trong chế độ `Người - Máy`, người chơi đi quân `X`, AI đi quân `O`.

### 2. Chạy chế độ AI vs AI trên terminal

Chạy:

```bash
python main.py --dev
```

Mặc định độ sâu tìm kiếm là `2`. Có thể đổi độ sâu bằng tham số `--depth`:

```bash
python main.py --dev --depth 3
```

Chế độ này in bàn cờ và thông tin từng nước đi ra terminal, phù hợp để kiểm tra nhanh thuật toán.

### 3. Chạy benchmark

Chạy:

```bash
python main.py --benchmark
```

Benchmark đọc cấu hình từ:

```text
config/benchmark_config.json
```

Mỗi test case gồm trạng thái bàn cờ và độ sâu tìm kiếm. Kết quả sẽ được in ra terminal, gồm nước đi, điểm đánh giá, số node đã xét và thời gian chạy của Minimax và Alpha-Beta.

## Một số lệnh hữu ích

Xem trợ giúp dòng lệnh:

```bash
python main.py -h
```

Chạy chương trình sau khi đã kích hoạt môi trường ảo:

```bash
python main.py
```

Thoát môi trường ảo:

```bash
deactivate
```

## Cấu trúc chính

```text
main.py                 Entry point của chương trình
requirements.txt        Danh sách thư viện cần cài đặt
caro_ai/app.py          Xử lý giao diện, chế độ chạy và dòng lệnh
caro_ai/ai/agent.py     Cài đặt AI Minimax và Alpha-Beta
caro_ai/game/board.py   Logic bàn cờ và kiểm tra thắng/thua
config/                 Cấu hình benchmark
```

