import math
from abc import ABC, abstractmethod


def _la_so(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    return isinstance(value, float) and math.isfinite(value)


class Ban(ABC):
    TRANG_THAI_HOP_LE = ("Trong", "Da dat", "Dang phuc vu", "Bao tri")

    def __init__(self, ma_ban, so_ghe, trang_thai, don_gia_ban):
        self.ma_ban = ma_ban
        self.so_ghe = so_ghe
        self.trang_thai = trang_thai
        self.don_gia_ban = don_gia_ban

    @property
    def ma_ban(self):
        return self.__ma_ban

    @ma_ban.setter
    def ma_ban(self, value):
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            raise TypeError("Ma ban phai la chuoi hoac so")
        value = str(value).strip()
        if not value:
            raise ValueError("Ma ban khong duoc de trong")
        self.__ma_ban = value

    @property
    def so_ghe(self):
        return self.__so_ghe

    @so_ghe.setter
    def so_ghe(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("So ghe phai la so nguyen")
        if value <= 0:
            raise ValueError("So ghe phai lon hon 0")
        self.__so_ghe = value

    @property
    def trang_thai(self):
        return self.__trang_thai

    @trang_thai.setter
    def trang_thai(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Trang thai khong duoc de trong")
        chuan_hoa = {tt.lower(): tt for tt in self.TRANG_THAI_HOP_LE}
        khoa = " ".join(value.split()).lower()
        if khoa not in chuan_hoa:
            raise ValueError(
                "Trang thai khong hop le, chi chap nhan: "
                + ", ".join(self.TRANG_THAI_HOP_LE)
            )
        self.__trang_thai = chuan_hoa[khoa]

    @property
    def don_gia_ban(self):
        return self.__don_gia_ban

    @don_gia_ban.setter
    def don_gia_ban(self, value):
        if not _la_so(value):
            raise TypeError("Don gia ban phai la so")
        if value < 0:
            raise ValueError("Don gia ban khong duoc am")
        self.__don_gia_ban = value

    @abstractmethod
    def tinh_tien_coc(self):
        raise NotImplementedError

    def to_dict(self):
        return {
            "loai_ban": self.__class__.__name__,
            "ma_ban": self.ma_ban,
            "so_ghe": self.so_ghe,
            "trang_thai": self.trang_thai,
            "don_gia_ban": self.don_gia_ban,
            "tien_coc": self.tinh_tien_coc()
        }

    def __str__(self):
        return (
            f"{self.__class__.__name__}(ma_ban={self.ma_ban}, "
            f"so_ghe={self.so_ghe}, trang_thai={self.trang_thai}, "
            f"don_gia_ban={self.don_gia_ban}, "
            f"tien_coc={self.tinh_tien_coc()})"
        )

    def __repr__(self):
        return self.__str__()

class BanThuong(Ban):
    TY_LE_COC = 0.1

    def tinh_tien_coc(self):
        return self.don_gia_ban * self.TY_LE_COC


class BanVIP(Ban):
    TY_LE_COC = 0.2

    def __init__(self, ma_ban, so_ghe, trang_thai, don_gia_ban, phu_phi):
        super().__init__(ma_ban, so_ghe, trang_thai, don_gia_ban)
        self.phu_phi = phu_phi

    @property
    def phu_phi(self):
        return self.__phu_phi

    @phu_phi.setter
    def phu_phi(self, value):
        if not _la_so(value):
            raise TypeError("Phu phi phai la so")
        if value < 0:
            raise ValueError("Phu phi khong duoc am")
        self.__phu_phi = value

    def tinh_tien_coc(self):
        return self.don_gia_ban * self.TY_LE_COC + self.phu_phi

    def to_dict(self):
        data = super().to_dict()
        data["phu_phi"] = self.phu_phi
        return data