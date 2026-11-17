
import re


class KhachHang:
    def __init__(self, ma_kh, ten_kh, sdt, email):
        self.ma_kh = ma_kh
        self.ten_kh = ten_kh
        self.sdt = sdt
        self.email = email

    @property
    def ma_kh(self):
        return self.__ma_kh

    @ma_kh.setter
    def ma_kh(self, ma_kh):
        if not ma_kh or not ma_kh.strip():
            raise ValueError("Ma khach hang khong duoc rong")
        self.__ma_kh = ma_kh.strip()

    @property
    def ten_kh(self):
        return self.__ten_kh

    @ten_kh.setter
    def ten_kh(self, ten_kh):
        if not ten_kh or not ten_kh.strip():
            raise ValueError("Ten khach hang khong duoc rong")
        self.__ten_kh = ten_kh.strip()

    @property
    def sdt(self):
        return self.__sdt

    @sdt.setter
    def sdt(self, sdt):
        sdt = str(sdt).strip()
        if not re.fullmatch(r"0\d{9}", sdt):
            raise ValueError("SDT phai co 10 chu so va bat dau bang 0")
        self.__sdt = sdt

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if not isinstance(email, str):
            raise ValueError("Email khong hop le")

        email = email.strip()
        mau_email = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        if not re.fullmatch(mau_email, email):
            raise ValueError("Email khong dung dinh dang")

        self.__email = email

    def to_dict(self):
        return {
            "ma_kh": self.ma_kh,
            "ten_kh": self.ten_kh,
            "sdt": self.sdt,
            "email": self.email
        }

    def __str__(self):
        return f"{self.ma_kh} - {self.ten_kh} - {self.sdt} - {self.email}"

