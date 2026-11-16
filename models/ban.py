class Ban:
    def __init__(self, ma_ban, so_ghe, trang_thai, don_gia_ban):
        self.__ma_ban = ma_ban
        self.__so_ghe = so_ghe
        self.__trang_thai = trang_thai
        self.__don_gia_ban = don_gia_ban

    @property
    def ma_ban(self):
        return self.__ma_ban

    @ma_ban.setter
    def ma_ban(self, value):
        if not value or not value.strip():
            raise ValueError("Ma ban khong duoc de trong")
        self.__ma_ban = value

    @property
    def so_ghe(self):
        return self.__so_ghe

    @so_ghe.setter
    def so_ghe(self, value):
        if value <= 0:
            raise ValueError("So ghe phai lon hon 0")
        self.__so_ghe = value

    @property
    def trang_thai(self):
        return self.__trang_thai

    @trang_thai.setter
    def trang_thai(self, value):
        self.__trang_thai = value

    @property
    def don_gia_ban(self):
        return self.__don_gia_ban

    @don_gia_ban.setter
    def don_gia_ban(self, value):
        if value < 0:
            raise ValueError("Don gia ban khong duoc am")
        self.__don_gia_ban = value

    def tinh_tien_coc(self):
        pass


class BanThuong(Ban):
    def __init__(self, ma_ban, so_ghe, trang_thai, don_gia_ban):
        super().__init__(ma_ban, so_ghe, trang_thai, don_gia_ban)

    def tinh_tien_coc(self):
        return self.don_gia_ban * 0.1


class BanVIP(Ban):
    def __init__(self, ma_ban, so_ghe, trang_thai, don_gia_ban, phu_phi):
        super().__init__(ma_ban, so_ghe, trang_thai, don_gia_ban)
        self.phu_phi = phu_phi

    def tinh_tien_coc(self):
        return self.don_gia_ban * 0.2 + self.phu_phi
