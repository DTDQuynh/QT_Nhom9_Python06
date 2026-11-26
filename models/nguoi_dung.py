class NguoiDung:
    def __init__(self, ten_dang_nhap, mat_khau, vai_tro="Lễ tân", ho_ten=None):
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro
        self.ho_ten = ho_ten

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
        if not isinstance(mat_khau, str) or len(mat_khau.strip()) < 6:
            raise ValueError("Mat khau phai co it nhat 6 ky tu khong tinh khoang trang thua")

        self.__mat_khau = mat_khau.strip()

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

        if not isinstance(vai_tro, str) or vai_tro.strip() not in danh_sach_vai_tro:
            raise ValueError(
                "Vai tro phai la Admin, Le tan hoac Quan ly"
            )

        self.__vai_tro = vai_tro.strip()

    # Kiem tra va chuan hoa ho ten
    @property
    def ho_ten(self):
        return self.__ho_ten

    @ho_ten.setter
    def ho_ten(self, ho_ten):
        if not isinstance(ho_ten, str) or not ho_ten.strip():
            self.__ho_ten = self.ten_dang_nhap
        else:
            self.__ho_ten = ho_ten.strip()

    # Kiem tra quyen quan tri
    def is_admin(self):
        return self.vai_tro in ["Admin", "Quản lý"]

    # Chuyen doi doi tuong thanh Dictionary
    def to_dict(self):
        return {
            "ten_dang_nhap": self.ten_dang_nhap,
            "ho_ten": self.ho_ten,
            "mat_khau": self.mat_khau,
            "vai_tro": self.vai_tro
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            ten_dang_nhap=data.get("ten_dang_nhap", ""),
            mat_khau=data.get("mat_khau", ""),
            vai_tro=data.get("vai_tro", "Lễ tân"),
            ho_ten=data.get("ho_ten")
        )

    def __str__(self):
        return f"{self.ho_ten} ({self.ten_dang_nhap}) - {self.vai_tro}"
