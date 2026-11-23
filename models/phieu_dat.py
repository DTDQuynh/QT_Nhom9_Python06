import re
from datetime import datetime

from models.ban import Ban
from models.khach_hang import KhachHang


class PhieuDatBan:
    def __init__(
        self,
        ma_phieu,
        khach_hang: KhachHang,
        ban: Ban,
        ngay_dat,
        gio_dat,
        ds_mon_dat=None,
        tien_coc=None,
    ):
        self.ma_phieu = ma_phieu
        self.khach_hang = khach_hang
        self.ban = ban
        self.ngay_dat = ngay_dat
        self.gio_dat = gio_dat
        self.ds_mon_dat = ds_mon_dat if ds_mon_dat is not None else []
        self.tien_coc = tien_coc

    # Kiem tra ma phieu
    @property
    def ma_phieu(self):
        return self.__ma_phieu

    @ma_phieu.setter
    def ma_phieu(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Ma phieu khong duoc de trong")

        self.__ma_phieu = value.strip()

    # Kiem tra doi tuong khach hang
    @property
    def khach_hang(self):
        return self.__khach_hang

    @khach_hang.setter
    def khach_hang(self, value):
        if not isinstance(value, KhachHang):
            raise TypeError("Khach hang phai la doi tuong KhachHang")

        self.__khach_hang = value

    # Kiem tra doi tuong ban
    @property
    def ban(self):
        return self.__ban

    @ban.setter
    def ban(self, value):
        if not isinstance(value, Ban):
            raise TypeError("Ban phai la doi tuong Ban")

        self.__ban = value

    # Kiem tra ngay dat
    @property
    def ngay_dat(self):
        return self.__ngay_dat

    @ngay_dat.setter
    def ngay_dat(self, value):
        if not isinstance(value, str):
            raise ValueError("Ngay dat phai la chuoi")

        value_clean = value.strip()

        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", value_clean):
            raise ValueError("Ngay dat phai co dang DD/MM/YYYY")

        try:
            datetime.strptime(value_clean, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Ngay dat khong hop le")

        self.__ngay_dat = value_clean

    # Kiem tra gio dat
    @property
    def gio_dat(self):
        return self.__gio_dat

    @gio_dat.setter
    def gio_dat(self, value):
        if not isinstance(value, str):
            raise ValueError("Gio dat phai la chuoi")

        value_clean = value.strip()

        if not re.fullmatch(r"\d{2}:\d{2}", value_clean):
            raise ValueError("Gio dat phai co dang HH:MM")

        try:
            datetime.strptime(value_clean, "%H:%M")
        except ValueError:
            raise ValueError("Gio dat khong hop le")

        self.__gio_dat = value_clean

    # Kiem tra danh sach mon dat
    @property
    def ds_mon_dat(self):
        return self.__ds_mon_dat

    @ds_mon_dat.setter
    def ds_mon_dat(self, value):
        if not isinstance(value, list):
            raise TypeError("Danh sach mon dat phai la list")

        self.__ds_mon_dat = value

    # Kiem tra va gan tien coc (mac dinh lay theo ban neu khong nhap hoac <= 0)
    @property
    def tien_coc(self):
        return self.__tien_coc

    @tien_coc.setter
    def tien_coc(self, value):
        if value is None:
            self.__tien_coc = self.ban.tinh_tien_coc()
            return

        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("Tien coc phai la so")

        if value < 0:
            raise ValueError("Tien coc khong duoc am")

        if value == 0:
            self.__tien_coc = self.ban.tinh_tien_coc()
        else:
            self.__tien_coc = value

    def _tinh_gia_mot_mon(self, mon):
        if isinstance(mon, dict):
            if "thanh_tien" in mon:
                return mon["thanh_tien"]
            don_gia = mon.get("don_gia", mon.get("gia", 0))
            so_luong = mon.get("so_luong", 1)
            return don_gia * so_luong

        if hasattr(mon, "tinh_thanh_tien") and callable(mon.tinh_thanh_tien):
            return mon.tinh_thanh_tien()
        if hasattr(mon, "thanh_tien"):
            return mon.thanh_tien

        don_gia = getattr(mon, "don_gia", getattr(mon, "gia", 0))
        so_luong = getattr(mon, "so_luong", 1)
        return don_gia * so_luong

    # Tinh tong tien cac mon an dat truoc
    def tinh_tong_tien_mon(self):
        return sum(self._tinh_gia_mot_mon(mon) for mon in self.ds_mon_dat)

    # Tinh tong tien phieu (tien ban + tien mon dat truoc)
    def tinh_tong_tien_phieu(self):
        return self.ban.don_gia_ban + self.tinh_tong_tien_mon()

    # Tinh so tien thanh toan du kien
    def tinh_thanh_toan_du_kien(self):
        return max(0, self.tinh_tong_tien_phieu() - self.tien_coc)

    # Chuyen doi doi tuong thanh Dictionary de luu JSON
    def to_dict(self):
        ds_mon_json = [
            mon.to_dict() if hasattr(mon, "to_dict") else mon
            for mon in self.ds_mon_dat
        ]

        return {
            "ma_phieu": self.ma_phieu,
            "khach_hang": self.khach_hang.to_dict(),
            "ban": self.ban.to_dict(),
            "ngay_dat": self.ngay_dat,
            "gio_dat": self.gio_dat,
            "ds_mon_dat": ds_mon_json,
            "tien_coc": self.tien_coc,
        }
