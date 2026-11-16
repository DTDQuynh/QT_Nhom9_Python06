from models.ban import Ban
from models.khach_hang import KhachHang


class PhieuDatBan:
    def __init__(self, ma_phieu, khach_hang: KhachHang, ban: Ban, thoi_gian):
        self.ma_phieu = ma_phieu
        self.khach_hang = khach_hang
        self.ban = ban
        self.thoi_gian = thoi_gian

    @property
    def ma_phieu(self):
        return self.__ma_phieu

    @ma_phieu.setter
    def ma_phieu(self, value):
        if not value or not str(value).strip():
            raise ValueError("Mã phiếu không được để trống!")
        self.__ma_phieu = value

    @property
    def khach_hang(self):
        return self.__khach_hang

    @khach_hang.setter
    def khach_hang(self, value):
        if not isinstance(value, KhachHang):
            raise TypeError("khach_hang phải là đối tượng thuộc lớp KhachHang!")
        self.__khach_hang = value

    @property
    def ban(self):
        return self.__ban

    @ban.setter
    def ban(self, value):
        if not isinstance(value, Ban):
            raise TypeError("ban phải là đối tượng thuộc lớp Ban!")
        self.__ban = value

    @property
    def thoi_gian(self):
        return self.__thoi_gian

    @thoi_gian.setter
    def thoi_gian(self, value):
        if not value or not str(value).strip():
            raise ValueError("Thời gian đặt không được để trống!")
        self.__thoi_gian = value

    def tinh_tong_tien_phieu(self):
        # Lấy trực tiếp đơn giá bàn từ class của Thảo
        return self.ban.don_gia_ban

    def tinh_thanh_toan_du_kien(self):
        # Thanh toán dự kiến = Tổng tiền - Tiền cọc (gọi hàm đa hình tinh_tien_coc() từ Thảo)
        return self.tinh_tong_tien_phieu() - self.ban.tinh_tien_coc()