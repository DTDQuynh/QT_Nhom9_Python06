from models.ban import BanThuong, BanVIP
from models.khach_hang import KhachHang
from models.phieu_dat import PhieuDatBan
from models.nguoi_dung import NguoiDung
from services.io_ban import load_ban_json, save_ban_json
from services.io_khach_phieu import (
    load_khach_json,
    save_khach_json,
    load_phieu_json,
    save_phieu_json,
    load_users_json,
    save_users_json,
)


class QuanLyDatBan:
    def __init__(self):
        self.ds_ban = []
        self.ds_khach = []
        self.ds_phieu = []
        self.ds_users = []
        self.load_tat_ca_du_lieu()

    # 1. Đọc và lưu dữ liệu JSON
    def load_tat_ca_du_lieu(self):
        self.ds_ban = load_ban_json()
        self.ds_khach = load_khach_json()
        self.ds_phieu = load_phieu_json()
        self.ds_users = load_users_json()

    def luu_tat_ca_du_lieu(self):
        save_ban_json(self.ds_ban)
        save_khach_json(self.ds_khach)
        save_phieu_json(self.ds_phieu)
        save_users_json(self.ds_users)

    # 2. Xử lý đăng nhập và tài khoản
    def dang_nhap(self, ten_dang_nhap, mat_khau):
        for u in self.ds_users:
            if u.ten_dang_nhap == ten_dang_nhap and u.mat_khau == mat_khau:
                return u
        return None

    def tao_tai_khoan(self, ten_dang_nhap, mat_khau, vai_tro="Lễ tân"):
        for u in self.ds_users:
             if u.ten_dang_nhap == ten_dang_nhap.strip():
                raise ValueError(f"Tên đăng nhập '{ten_dang_nhap}' đã tồn tại!")

        nguoi_dung_moi = NguoiDung(ten_dang_nhap, mat_khau, vai_tro)
        self.ds_users.append(nguoi_dung_moi)
        self.luu_tat_ca_du_lieu()
        return nguoi_dung_moi

    def doi_mat_khau(self, ten_dang_nhap, mat_khau_cu, mat_khau_moi):
        for u in self.ds_users:
            if u.ten_dang_nhap == ten_dang_nhap:
                if u.mat_khau != mat_khau_cu:
                    raise ValueError("Mật khẩu hiện tại không chính xác!")
                u.mat_khau = mat_khau_moi
                self.luu_tat_ca_du_lieu()
                return True
        raise ValueError("Không tìm thấy tài khoản người dùng!")

    # 3. Quản lý bàn ăn và tìm kiếm
    def tim_ban_theo_ma(self, ma_ban):
        for b in self.ds_ban:
            if b.ma_ban == ma_ban:
                return b
        return None

    def tim_ban_trong(self):
        return [b for b in self.ds_ban if b.trang_thai == "Trong"]

    # 4. Quản lý khách hàng
    def tim_khach_theo_sdt(self, sdt):
        for k in self.ds_khach:
            if k.sdt == sdt:
                return k
        return None

    def them_khach_hang_moi(self, ma_kh, ten_kh, sdt, email=""):
        kh_cu = self.tim_khach_theo_sdt(sdt)
        if kh_cu:
            return kh_cu
        kh_moi = KhachHang(ma_kh, ten_kh, sdt, email)
        self.ds_khach.append(kh_moi)
        save_khach_json(self.ds_khach)
        return kh_moi

    # 5. Kiểm tra trùng lịch đặt bàn
    def kiem_tra_trung_lich(self, ma_ban, ngay_dat, gio_dat, ma_phieu_bo_qua=None):
        for p in self.ds_phieu:
            if ma_phieu_bo_qua and p.ma_phieu == ma_phieu_bo_qua:
                continue
            if p.ban.ma_ban == ma_ban and p.ngay_dat == ngay_dat and p.gio_dat == gio_dat:
                return True
        return False

    # 6. Nghiệp vụ đặt bàn, hủy bàn và chuyển bàn
    def dat_ban_moi(self, ma_phieu, ten_kh, sdt, email, ma_ban, ngay_dat, gio_dat, ds_mon_dat=None, tien_coc=0.0):
        ban = self.tim_ban_theo_ma(ma_ban)
        if not ban:
            raise ValueError(f"Không tìm thấy bàn có mã '{ma_ban}'!")
        if self.kiem_tra_trung_lich(ma_ban, ngay_dat, gio_dat):
            raise ValueError(f"Bàn '{ma_ban}' đã có người đặt vào khung giờ {gio_dat} ngày {ngay_dat}!")

        khach = self.tim_khach_theo_sdt(sdt)
        if not khach:
            ma_kh_moi = f"KH{len(self.ds_khach) + 1:02d}"
            khach = self.them_khach_hang_moi(ma_kh_moi, ten_kh, sdt, email)

        phieu = PhieuDatBan(ma_phieu, khach, ban, ngay_dat, gio_dat, ds_mon_dat, tien_coc)
        ban.trang_thai = "Da dat"
        self.ds_phieu.append(phieu)
        self.luu_tat_ca_du_lieu()
        return phieu

    def huy_phieu_dat(self, ma_phieu):
        phieu_tim = None
        for p in self.ds_phieu:
            if p.ma_phieu == ma_phieu:
                phieu_tim = p
                break
        if not phieu_tim:
            raise ValueError(f"Không tìm thấy phiếu đặt bàn mã '{ma_phieu}'!")

        phieu_tim.ban.trang_thai = "Trong"
        self.ds_phieu.remove(phieu_tim)
        self.luu_tat_ca_du_lieu()
        return True

    def chuyen_ban(self, ma_phieu, ma_ban_moi):
        phieu_tim = None
        for p in self.ds_phieu:
            if p.ma_phieu == ma_phieu:
                phieu_tim = p
                break
        if not phieu_tim:
            raise ValueError(f"Không tìm thấy phiếu đặt bàn mã '{ma_phieu}'!")

        ban_moi = self.tim_ban_theo_ma(ma_ban_moi)
        if not ban_moi:
            raise ValueError(f"Bàn mới mã '{ma_ban_moi}' không tồn tại!")

        if self.kiem_tra_trung_lich(ma_ban_moi, phieu_tim.ngay_dat, phieu_tim.gio_dat, ma_phieu_bo_qua=ma_phieu):
            raise ValueError(f"Bàn mới '{ma_ban_moi}' đã có lịch đặt vào {phieu_tim.gio_dat} ngày {phieu_tim.ngay_dat}!")

        phieu_tim.ban.trang_thai = "Trong"
        phieu_tim.ban = ban_moi
        ban_moi.trang_thai = "Da dat"
        self.luu_tat_ca_du_lieu()
        return True

    def thanh_toan_phieu(self, ma_phieu):
        phieu_tim = None
        for p in self.ds_phieu:
            if p.ma_phieu == ma_phieu:
                phieu_tim = p
                break
        if not phieu_tim:
            raise ValueError(f"Không tìm thấy phiếu đặt bàn mã '{ma_phieu}'!")

        so_tien_con_tra = phieu_tim.tinh_thanh_toan_du_kien()
        phieu_tim.ban.trang_thai = "Trong"
        self.luu_tat_ca_du_lieu()
        return so_tien_con_tra

    # 7. Tìm kiếm và thống kê doanh thu
    def tim_phieu_theo_sdt_khach(self, sdt):
        return [p for p in self.ds_phieu if p.khach_hang.sdt == sdt]

    def tim_phieu_theo_ngay(self, ngay_str):
        return [p for p in self.ds_phieu if p.ngay_dat == ngay_str]

    def thong_ke_ty_le_ban(self):
        tong_so_ban = len(self.ds_ban)
        if tong_so_ban == 0:
            return {"tong_so_ban": 0, "so_luong": {}, "ty_le_trong": 0, "ty_le_da_dat": 0}

        dem = {"Trong": 0, "Da dat": 0, "Dang phuc vu": 0, "Bao tri": 0}
        for b in self.ds_ban:
            tt = b.trang_thai
            dem[tt] = dem.get(tt, 0) + 1

        return {
            "tong_so_ban": tong_so_ban,
            "so_luong": dem,
            "ty_le_trong": (dem["Trong"] / tong_so_ban) * 100,
            "ty_le_da_dat": (dem["Da dat"] / tong_so_ban) * 100,
        }

    def thong_ke_doanh_thu(self):
        tong_tien_coc = sum(p.tien_coc for p in self.ds_phieu)
        tong_gia_tri_phieu = sum(p.tinh_tong_tien_phieu() for p in self.ds_phieu)
        return {
            "tong_so_phieu": len(self.ds_phieu),
            "tong_tien_coc": tong_tien_coc,
            "tong_gia_tri_phieu": tong_gia_tri_phieu,
        }