# Hệ thống quản lý đặt bàn nhà hàng

Đồ án môn Python - Nhóm 9

## Thành viên


1 Đặng Thị Diễm Quỳnh: Nhóm trưởng 
   Công việc: Thiết kế các class trong `models/`, đăng nhập và phân quyền, xử lý đặt bàn không trùng giờ (`services/`), giao diện chính `app_main.py` 
   Đóng góp:34%
2  Nguyễn Diệu Thảo: Thành viên 
  Công việc: Quản lý bàn thường/VIP, sơ đồ bàn kéo thả trên Canvas (`gui/canvas_ban.py`), TableWidget tự viết, thống kê tỷ lệ sử dụng bàn 
  Đóng góp:33%
3 Trần Bảo Quyên: Thành viên 
  Công việc: Quản lý khách hàng và đặt món trước, kiểm tra SĐT/email/ngày bằng regex, đọc ghi và backup JSON, lấy dữ liệu thực đơn từ web/API 
  Đóng góp:33%

## Chức năng

- Đăng nhập, tạo tài khoản, đổi mật khẩu. Có 2 quyền: quản lý và lễ tân.
- Sơ đồ bàn vẽ bằng Canvas, chia theo khu vực. Màu bàn đổi theo trạng thái (trống, đã đặt, đang phục vụ), kéo thả để đổi vị trí.
- Đặt bàn, hủy, chuyển bàn. Chương trình tự kiểm tra trùng khung giờ, tính tiền cọc và nhắc các lịch sắp tới.
- Tìm phiếu đặt theo số điện thoại hoặc theo ngày, thống kê tỷ lệ sử dụng bàn.
- Lấy thực đơn mẫu từ nguồn bên ngoài, làm sạch rồi lưu ra JSON.
- Dữ liệu lưu bằng JSON, có backup và bắt lỗi khi đọc/ghi file.

## Cấu trúc thư mục

```QT_Nhom9_Python06/
├── data/          # file JSON: ban, khach_hang, dat_ban, users
├── models/        # Ban, BanVIP, KhachHang, PhieuDat, NguoiDung
├── services/      # nghiệp vụ, đọc/ghi JSON, regex, crawl dữ liệu
├── gui/           # giao diện Tkinter, canvas sơ đồ bàn, TableWidget
├── config.py      # đường dẫn, màu sắc, font
├── app_main.py    # chạy chương trình
└── README.md

## Cách chạy

python app_main.py
