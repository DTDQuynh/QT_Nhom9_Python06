
from datetime import datetime 

from models.ban import Ban
from models.khach_hang import KhachHang

class PhieuDatBan:
    def __init__(self, ma_phieu, khach_hang: KhachHang, ban: Ban,
                 ngay_dat, gio_dat, ds_mon_dat=None):

        self.ma_phieu = ma_phieu
        self.khach_hang = khach_hang
        self.ban = ban
        self.ngay_dat = ngay_dat
        self.gio_dat = gio_dat
        self.ds_mon_dat = ds_mon_dat if ds_mon_dat is not None else []

    @property
    def ma_phieu(self):
        return self.__ma_phieu

    @ma_phieu.setter
    def ma_phieu(self, value):
        if not value or not str(value).strip():
            raise ValueError("Ma phieu khong duoc de trong")
        self.__ma_phieu = value

    @property
    def khach_hang(self):
        return self.__khach_hang

    @khach_hang.setter
    def khach_hang(self, value):
        if not isinstance(value, KhachHang):
            raise TypeError("khach_hang phai la doi tuong KhachHang")
        self.__khach_hang = value

    @property
    def ban(self):
        return self.__ban

    @ban.setter
    def ban(self, value):
        if not isinstance(value, Ban):
            raise TypeError("ban phai la doi tuong Ban")
        self.__ban = value

    @property
    def ngay_dat(self):
        return self.__ngay_dat

    @ngay_dat.setter
    def ngay_dat(self, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except (ValueError, TypeError):
            raise ValueError("Ngay dat phai co dinh dang DD/MM/YYYY")
        self.__ngay_dat = value

    @property
    def gio_dat(self):
        return self.__gio_dat

    @gio_dat.setter
    def gio_dat(self, value):
        try:
            datetime.strptime(value, "%H:%M")
        except (ValueError, TypeError):
            raise ValueError("Gio dat phai co dinh dang HH:MM")
        self.__gio_dat = value

    @property
    def ds_mon_dat(self):
        return self.__ds_mon_dat

    @ds_mon_dat.setter
    def ds_mon_dat(self, value):
        if not isinstance(value, list):
            raise TypeError("ds_mon_dat phai la danh sach list")
        self.__ds_mon_dat = value

    def tinh_tong_tien_phieu(self):
        return self.ban.don_gia_ban

    def tinh_thanh_toan_du_kien(self):
        return self.tinh_tong_tien_phieu() - self.ban.tinh_tien_coc()
