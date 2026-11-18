
class NguoiDung:
    def __init__(self, ten_dang_nhap, mat_khau, vai_tro):
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro

    # Kiem tra ten dang nhap
    @property
    def ten_dang_nhap(self):
        return self.__ten_dang_nhap

    @ten_dang_nhap.setter
    def ten_dang_nhap(self, ten_dang_nhap):
        if not isinstance(ten_dang_nhap, str) or not ten_dang_nhap.strip():
            raise ValueError("Ten dang nhap khong duoc rong")

        self.__ten_dang_nhap = ten_dang_nhap.strip()

    # Kiem tra mat khau
    @property
    def mat_khau(self):
        return self.__mat_khau

    @mat_khau.setter
    def mat_khau(self, mat_khau):
        if not isinstance(mat_khau, str) or len(mat_khau) < 6:
            raise ValueError("Mat khau phai co it nhat 6 ky tu")

        self.__mat_khau = mat_khau

    # Kiem tra vai tro nguoi dung
    @property
    def vai_tro(self):
        return self.__vai_tro

    @vai_tro.setter
    def vai_tro(self, vai_tro):
        danh_sach_vai_tro = [
            "Admin",
            "Lễ tân",
            "Quản lý"
        ]

        if vai_tro not in danh_sach_vai_tro:
            raise ValueError(
                "Vai tro phai la Admin, Le tan hoac Quan ly"
            )

        self.__vai_tro = vai_tro

    # Kiem tra quyen quan tri
    def is_admin(self):
        return self.vai_tro == "Admin"

    # Chuyen doi doi tuong thanh Dictionary
    def to_dict(self):
        return {
            "ten_dang_nhap": self.ten_dang_nhap,
            "mat_khau": self.mat_khau,
            "vai_tro": self.vai_tro
        }

    def __str__(self):
        return f"{self.ten_dang_nhap} - {self.vai_tro}"
