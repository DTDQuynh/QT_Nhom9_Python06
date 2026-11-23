import os
import sys

# Đảm bảo import được các module từ thư mục dự án
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from services.quan_ly import QuanLyDatBan


def in_tieu_de(text):
    print("\n" + "=" * 55)
    print(f" {text.upper()}")
    print("=" * 55)


def main():
    print("Đang khởi tạo hệ thống và nạp dữ liệu từ các file JSON...")
    try:
        ql = QuanLyDatBan()
        print("-> Nạp dữ liệu thành công!")
    except Exception as e:
        print(f"-> Lỗi khi nạp dữ liệu: {e}")
        return

    while True:
        in_tieu_de("HỆ THỐNG QUẢN LÝ ĐẶT BÀN NHÀ HÀNG - CONSOLE CLI")
        print("1. Xem danh sách tất cả Bàn ăn & Trạng thái")
        print("2. Xem danh sách Khách hàng")
        print("3. Đặt bàn mới (Tự động kiểm tra trùng lịch)")
        print("4. Tìm kiếm phiếu đặt theo SĐT khách hàng")
        print("5. Thống kê bàn trống & Doanh thu cọc")
        print("6. Lưu dữ liệu & Thoát chương trình")
        print("-" * 55)

        luot_chon = input("Nhập lựa chọn của bạn (1-6): ").strip()

        if luot_chon == "1":
            in_tieu_de("DANH SÁCH BÀN ĂN TRONG HỆ THỐNG")
            if not ql.ds_ban:
                print("Chưa có dữ liệu bàn ăn!")
            else:
                print(f"{'Mã Bàn':<10} | {'Loại Bàn':<12} | {'Số Ghế':<8} | {'Đơn Giá (VNĐ)':<15} | {'Trạng Thái':<12}")
                print("-" * 68)
                for b in ql.ds_ban:
                    loai = b.__class__.__name__
                    print(f"{b.ma_ban:<10} | {loai:<12} | {b.so_ghe:<8} | {b.don_gia_ban:<15,.0f} | {b.trang_thai:<12}")

        elif luot_chon == "2":
            in_tieu_de("DANH SÁCH KHÁCH HÀNG")
            if not ql.ds_khach:
                print("Chưa có dữ liệu khách hàng!")
            else:
                print(f"{'Mã KH':<8} | {'Họ và Tên':<20} | {'Số Điện Thoại':<15} | {'Email':<25}")
                print("-" * 73)
                for k in ql.ds_khach:
                    email_str = k.email if k.email else "(Chưa có)"
                    print(f"{k.ma_kh:<8} | {k.ten_kh:<20} | {k.sdt:<15} | {email_str:<25}")

        elif luot_chon == "3":
            in_tieu_de("ĐẶT BÀN MỚI")
            try:
                ma_phieu = input("Nhập Mã phiếu đặt (vd: PD03): ").strip()
                if not ma_phieu:
                    print("Lỗi: Mã phiếu không được rỗng!")
                    continue

                ten_kh = input("Nhập Tên khách hàng: ").strip()
                sdt = input("Nhập Số điện thoại (10 số, bắt đầu bằng 0): ").strip()
                email = input("Nhập Email (để trống nếu không có): ").strip()

                print("\nCác bàn hiện có trong hệ thống:")
                for b in ql.ds_ban:
                    print(f" - Mã bàn: {b.ma_ban} | Số ghế: {b.so_ghe} | Loại: {b.__class__.__name__} | Trạng thái: {b.trang_thai}")

                ma_ban = input("Nhập Mã bàn chọn đặt: ").strip()
                ngay_dat = input("Nhập Ngày đặt (định dạng DD/MM/YYYY, vd: 25/11/2026): ").strip()
                gio_dat = input("Nhập Giờ đặt (định dạng HH:MM, vd: 18:30): ").strip()
                tien_coc_input = input("Nhập Tiền cọc (nhấn Enter để tự tính theo quy định): ").strip()
                tien_coc = float(tien_coc_input) if tien_coc_input else 0.0

                phieu_moi = ql.dat_ban_moi(
                    ma_phieu=ma_phieu,
                    ten_kh=ten_kh,
                    sdt=sdt,
                    email=email,
                    ma_ban=ma_ban,
                    ngay_dat=ngay_dat,
                    gio_dat=gio_dat,
                    tien_coc=tien_coc,
                )

                print("\n-> ĐẶT BÀN THÀNH CÔNG!")
                print(f" + Mã phiếu: {phieu_moi.ma_phieu}")
                print(f" + Khách hàng: {phieu_moi.khach_hang.ten_kh} ({phieu_moi.khach_hang.sdt})")
                print(f" + Bàn ăn: {phieu_moi.ban.ma_ban}")
                print(f" + Tiền cọc: {phieu_moi.tien_coc:,.0f} VNĐ")
                print(f" + Còn phải trả (dự kiến): {phieu_moi.tinh_thanh_toan_du_kien():,.0f} VNĐ")

            except Exception as ex:
                print(f"\n[LỖI ĐẶT BÀN]: {ex}")

        elif luot_chon == "4":
            in_tieu_de("TÌM KIẾM PHIẾU ĐẶT THEO SĐT KHÁCH HÀNG")
            sdt_tim = input("Nhập SĐT khách hàng cần tìm: ").strip()
            ds_tim = ql.tim_phieu_theo_sdt_khach(sdt_tim)
            if not ds_tim:
                print(f"Không tìm thấy phiếu đặt nào cho SĐT '{sdt_tim}'!")
            else:
                print(f"Tìm thấy {len(ds_tim)} phiếu đặt:")
                for p in ds_tim:
                    print(f" - {p}")

        elif luot_chon == "5":
            in_tieu_de("THỐNG KÊ HỆ THỐNG")
            tk_ban = ql.thong_ke_ty_le_ban()
            tk_dt = ql.thong_ke_doanh_thu()

            print(f"TỔNG SỐ BÀN: {tk_ban['tong_so_ban']}")
            print(f" + Bàn Trống: {tk_ban['so_luong'].get('Trong', 0)} ({tk_ban['ty_le_trong']:.1f}%)")
            print(f" + Bàn Đã đặt: {tk_ban['so_luong'].get('Da dat', 0)} ({tk_ban['ty_le_da_dat']:.1f}%)")
            print("-" * 40)
            print(f"TỔNG SỐ PHIẾU ĐẶT: {tk_dt['tong_so_phieu']}")
            print(f" + Tổng tiền cọc đã thu: {tk_dt['tong_tien_coc']:,.0f} VNĐ")
            print(f" + Tổng giá trị phiếu đặt: {tk_dt['tong_gia_tri_phieu']:,.0f} VNĐ")

        elif luot_chon == "6":
            print("\nĐang tiến hành lưu toàn bộ dữ liệu xuống file JSON...")
            ql.luu_tat_ca_du_lieu()
            print("-> Đã lưu dữ liệu thành công! Cảm ơn bạn đã sử dụng chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ! Vui lòng nhập từ 1 đến 6.")


if __name__ == "__main__":
    main()