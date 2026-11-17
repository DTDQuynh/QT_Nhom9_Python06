
class NguoiDung:
    def __init__(self, ten_dang_nhap, mat_khau, vai_tro):
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro

    @property
    def ten_dang_nhap(self):
        return self.__ten_dang_nhap

    @ten_dang_nhap.setter
    def ten_dang_nhap(self, ten_dang_nhap):
        if not ten_dang_nhap or not ten_dang_nhap.strip():
            raise ValueError("Ten dang nhap khong duoc rong")
        self.__ten_dang_nhap = ten_dang_nhap.strip()

    @property
    def mat_khau(self):
        return self.__mat_khau

    @mat_khau.setter
    def mat_khau(self, mat_khau):
        if not mat_khau or len(mat_khau) < 6:
            raise ValueError("Mat khau phai co it nhat 6 ky tu")
        self.__mat_khau = mat_khau 

    @property
    def vai_tro(self):
        return self.__vai_tro

    @vai_tro.setter
    def vai_tro(self, vai_tro):
        if vai_tro not in ["Admin", "Lễ tân", "Quản lý"]:
            raise ValueError("Vai tro phai la Admin, Le tan hoac Quan ly")
        self.__vai_tro = vai_tro

    def is_admin(self):
        return self.vai_tro == "Admin"

    def __str__(self):
        return f"{self.ten_dang_nhap} - {self.vai_tro}"

