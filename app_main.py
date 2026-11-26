import tkinter as tk
from tkinter import messagebox
import config
from services.quan_ly import QuanLyDatBan
from gui.login_gui import LoginFrame
from gui.main_dashboard import MainDashboard


class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.minsize(*config.WINDOW_MIN_SIZE)
        self.configure(bg=config.COLOR_BACKGROUND)

        try:
            self.quan_ly = QuanLyDatBan()
        except Exception as e:
            messagebox.showerror("Lỗi khởi tạo dữ liệu", f"Không thể nạp dữ liệu hệ thống: {e}")
            self.destroy()
            return

        self.current_frame = None
        self.mo_man_hinh_dang_nhap()

    def xoa_man_hinh_hien_tai(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def mo_man_hinh_dang_nhap(self):
        self.xoa_man_hinh_hien_tai()
        self.current_frame = LoginFrame(
            self,
            quan_ly_service=self.quan_ly,
            on_login_success=self.mo_dashboard
        )

    def mo_dashboard(self, nguoi_dung):
        self.xoa_man_hinh_hien_tai()
        self.current_frame = MainDashboard(
            self,
            quan_ly_service=self.quan_ly,
            nguoi_dung=nguoi_dung,
            on_logout=self.mo_man_hinh_dang_nhap
        )


if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()