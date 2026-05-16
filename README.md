# BÀI TẬP LẬP TRÌNH 1: CỜ CARO AI

**Họ và tên:** Nguyễn Phúc Gia Bảo  
**Mã sinh viên:** 24022265  
**Mã đề:** Đề 1  

---

## 1. Giới thiệu dự án
Cờ Caro AI là chương trình Trí tuệ nhân tạo chơi cờ Caro (phiên bản 4 quân liên tiếp chiến thắng, không xét luật chặn 2 đầu) trên bàn cờ kích thước 9x9. 

Chương trình cung cấp 2 thuật toán tìm kiếm có đối thủ:
* **Minimax** (với giới hạn độ sâu).
* **Alpha-Beta Pruning** (tối ưu hóa cắt nhánh).

## 2. Cấu trúc thư mục
```text
24022265_NGUYENPHUCGIABAO_CAROAI_DE1/
│
├── source_code/             # Thư mục chứa mã nguồn Python
│   ├── config.py            # Cấu hình hằng số (kích thước bàn cờ, biến người chơi...)
│   ├── board.py             # Quản lý trạng thái bàn cờ và kiểm tra thắng/thua
│   ├── ai.py                # Thuật toán Minimax, Alpha-Beta và Hàm đánh giá
│   ├── main.py              # File chạy game tương tác trực tiếp
│   └── benchmark.py         # File chạy kiểm thử tự động sinh số liệu báo cáo
│
├── requirements.txt         # Danh sách các thư viện cần thiết
├── README.md                # File hướng dẫn chạy chương trình
└── report.pdf               # Báo cáo thực nghiệm (được xuất từ hệ thống LaTeX)