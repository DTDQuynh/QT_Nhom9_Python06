import tkinter as tk
from tkinter import messagebox
import config


class LoginFrame(tk.Frame):
    def __init__(self, parent, quan_ly_service, on_login_success):
        super().__init__(parent, bg=config.COLOR_BACKGROUND)
        self.quan_ly = quan_ly_service
        self.on_login_success = on_login_success
        self.hien_mat_khau = False
        self.pack(fill=tk.BOTH, expand=True)
        self.tao_giao_dien()

    def tao_giao_dien(self):
        # Khung dang nhap 
        card = tk.Frame(
            self,
            bg=config.COLOR_CARD,
            highlightbackground=config.COLOR_BORDER,
            highlightthickness=1,
            padx=40,
            pady=35
        )
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(
            card,
            text="ĐĂNG NHẬP HỆ THỐNG",
            font=config.FONT_TITLE,
            bg=config.COLOR_CARD,
            fg=config.COLOR_PRIMARY
        ).pack(pady=(0, 5))

        tk.Label(
            card,
            text="Hệ thống Quản lý Đặt bàn Nhà hàng",
            font=config.FONT_SMALL,
            bg=config.COLOR_CARD,
            fg=config.COLOR_TEXT_MUTED
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="Tên đăng nhập:",
            font=config.FONT_BODY_BOLD,
            bg=config.COLOR_CARD,
            fg=config.COLOR_TEXT_MAIN,
            anchor="w"
        ).pack(fill=tk.X)

        self.entry_user = tk.Entry(card, font=config.FONT_BODY, width=34)
        self.entry_user.pack(fill=tk.X, pady=(5, 15), ipady=4)
        self.entry_user.focus_set()

        
        tk.Label(
            card,
            text="Mật khẩu:",
            font=config.FONT_BODY_BOLD,
            bg=config.COLOR_CARD,
            fg=config.COLOR_TEXT_MAIN,
            anchor="w"
        ).pack(fill=tk.X)

        frame_pass = tk.Frame(card, bg=config.COLOR_CARD)
        frame_pass.pack(fill=tk.X, pady=(5, 25))

        self.entry_pass = tk.Entry(frame_pass, font=config.FONT_BODY, show="*")
        self.entry_pass.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        self.btn_eye = tk.Button(
            frame_pass,
            text="Hiện",
            font=config.FONT_SMALL,
            bg=config.COLOR_BORDER,
            fg=config.COLOR_TEXT_MAIN,
            relief=tk.FLAT,
            cursor="hand2",
            width=6,
            command=self.chuyen_doi_hien_mat_khau
        )
        self.btn_eye.pack(side=tk.LEFT, padx=(6, 0), ipady=3)

        # Nut dang nhap
        btn_login = tk.Button(
            card,
            text="ĐĂNG NHẬP",
            font=config.FONT_BUTTON,
            bg=config.COLOR_ACCENT,
            fg="white",
            activebackground=config.COLOR_ACCENT_HOVER,
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.xu_ly_dang_nhap
        )
        btn_login.pack(fill=tk.X, ipady=7)

        
        self.entry_pass.bind("<Return>", lambda event: self.xu_ly_dang_nhap())

    def chuyen_doi_hien_mat_khau(self):
        if self.hien_mat_khau:
            self.entry_pass.config(show="*")
            self.btn_eye.config(text="Hiện")
            self.hien_mat_khau = False
        else:
            self.entry_pass.config(show="")
            self.btn_eye.config(text="Ẩn")
            self.hien_mat_khau = True

    def xu_ly_dang_nhap(self):
        ten_dn = self.entry_user.get().strip()
        mat_khau = self.entry_pass.get().strip()

        if not ten_dn or not mat_khau:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return

        nguoi_dung = self.quan_ly.dang_nhap(ten_dn, mat_khau)
        if nguoi_dung is not None:
            self.on_login_success(nguoi_dung)
        else:
            messagebox.showerror("Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng!")