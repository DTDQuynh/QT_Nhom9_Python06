import tkinter as tk
from tkinter import messagebox, ttk
import config


class MainDashboard(tk.Frame):
    def __init__(self, parent, quan_ly_service, nguoi_dung, on_logout):
        super().__init__(parent, bg=config.COLOR_BACKGROUND)
        self.quan_ly = quan_ly_service
        self.nguoi_dung = nguoi_dung
        self.on_logout = on_logout
        self.pack(fill=tk.BOTH, expand=True)
        self.tao_bo_cuc()

    def tao_bo_cuc(self):
        # 1. Thanh Header tren cung
        header = tk.Frame(self, bg=config.COLOR_PRIMARY, height=55)
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text=config.APP_TITLE,
            font=config.FONT_HEADER,
            bg=config.COLOR_PRIMARY,
            fg="white"
        ).pack(side=tk.LEFT, padx=20)

        btn_logout = tk.Button(
            header,
            text="Đăng xuất",
            font=config.FONT_SMALL,
            bg=config.COLOR_DANGER,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.xac_nhan_dang_xuat
        )
        btn_logout.pack(side=tk.RIGHT, padx=(5, 20), pady=12)

        btn_change_pwd = tk.Button(
            header,
            text="Đổi mật khẩu",
            font=config.FONT_SMALL,
            bg=config.COLOR_WARNING,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.mo_cua_so_doi_mat_khau
        )
        btn_change_pwd.pack(side=tk.RIGHT, padx=5, pady=12)

        tk.Label(
            header,
            text=f"Xin chào: {self.nguoi_dung.ten_dang_nhap} ({self.nguoi_dung.vai_tro})",
            font=config.FONT_BODY,
            bg=config.COLOR_PRIMARY,
            fg="#CBD5E1"
        ).pack(side=tk.RIGHT, padx=10)

        # 2. Khung than ben duoi
        body = tk.Frame(self, bg=config.COLOR_BACKGROUND)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Thanh menu ben trai
        sidebar = tk.Frame(body, bg=config.COLOR_SIDEBAR, width=230)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="DANH MỤC CHỨC NĂNG",
            font=config.FONT_SMALL,
            bg=config.COLOR_SIDEBAR,
            fg="#94A3B8"
        ).pack(pady=(20, 10), padx=15, anchor="w")

        cac_muc_menu = [
            ("Sơ đồ bàn ăn", self.hien_thi_so_do_ban),
            ("Quản lý đặt bàn", self.hien_thi_dat_ban),
            ("Khách hàng & Thực đơn", self.hien_thi_khach_hang),
            ("Thống kê doanh thu", self.hien_thi_thong_ke),
            ("Quản lý tài khoản", self.hien_thi_quan_ly_tai_khoan)
        ]

        for ten_muc, ham_xu_ly in cac_muc_menu:
            btn = tk.Button(
                sidebar,
                text=f"  {ten_muc}",
                font=config.FONT_BODY_BOLD,
                bg=config.COLOR_SIDEBAR,
                fg="white",
                activebackground=config.COLOR_ACCENT,
                activeforeground="white",
                relief=tk.FLAT,
                anchor="w",
                cursor="hand2",
                command=ham_xu_ly
            )
            btn.pack(fill=tk.X, padx=10, pady=4, ipady=8)

        # Vung hien thi noi dung chinh ben phai
        self.content_area = tk.Frame(body, bg=config.COLOR_BACKGROUND, padx=20, pady=20)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.hien_thi_so_do_ban()

    def xoa_noi_dung_cu(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def tao_khung_cho(self, tieu_de, mo_ta, phu_trach):
        self.xoa_noi_dung_cu()
        card = tk.Frame(
            self.content_area,
            bg=config.COLOR_CARD,
            highlightbackground=config.COLOR_BORDER,
            highlightthickness=1,
            padx=25,
            pady=25
        )
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            card,
            text=tieu_de,
            font=config.FONT_TITLE,
            bg=config.COLOR_CARD,
            fg=config.COLOR_TEXT_MAIN
        ).pack(anchor="w")

        tk.Label(
            card,
            text=mo_ta,
            font=config.FONT_BODY,
            bg=config.COLOR_CARD,
            fg=config.COLOR_TEXT_MUTED
        ).pack(anchor="w", pady=(8, 15))

        tk.Label(
            card,
            text=f"Phụ trách module: {phu_trach}",
            font=config.FONT_BODY_BOLD,
            bg="#EFF6FF",
            fg=config.COLOR_ACCENT,
            padx=12,
            pady=6
        ).pack(anchor="w")

    def hien_thi_so_do_ban(self):
        self.tao_khung_cho(
            "SƠ ĐỒ BÀN ĂN NHÀ HÀNG (CANVAS)",
            "Khu vực hiển thị trực quan trạng thái bàn (Trống, Đã đặt, Đang phục vụ, Bảo trì) và kéo thả vị trí bàn.",
            "Nguyễn Diệu Thảo (gui/canvas_ban.py)"
        )

    def hien_thi_dat_ban(self):
        self.tao_khung_cho(
            "QUẢN LÝ PHIẾU ĐẶT BÀN & CHUYỂN BÀN",
            "Khu vực tạo phiếu đặt mới, kiểm tra trùng khung giờ, tính tiền cọc và thanh toán.",
            "Đặng Thị Diễm Quỳnh (services/quan_ly.py)"
        )

    def hien_thi_khach_hang(self):
        self.tao_khung_cho(
            "QUẢN LÝ KHÁCH HÀNG & THỰC ĐƠN MÓN ĐẶT TRƯỚC",
            "Khu vực hiển thị bảng danh sách khách hàng, tra cứu SĐT và nạp thực đơn từ JSON.",
            "Trần Bảo Quyên (gui/khach_hang_gui.py)"
        )

    def hien_thi_thong_ke(self):
        if self.nguoi_dung.vai_tro not in ["Admin", "Quản lý"]:
            messagebox.showwarning("Phân quyền", "Chỉ tài khoản Quản lý hoặc Admin mới được xem thống kê!")
            return
        self.tao_khung_cho(
            "THỐNG KÊ TỶ LỆ SỬ DỤNG BÀN & DOANH THU",
            "Khu vực vẽ biểu đồ cột/tròn trực quan trên Canvas thống kê công suất bàn và tổng tiền cọc.",
            "Nguyễn Diệu Thảo (gui/thong_ke_gui.py)"
        )

    # Chuc nang tao tai khoan moi (danh cho Quan ly / Admin)
    def hien_thi_quan_ly_tai_khoan(self):
        if self.nguoi_dung.vai_tro not in ["Admin", "Quản lý"]:
            messagebox.showwarning("Phân quyền", "Chỉ tài khoản Quản lý hoặc Admin mới có quyền quản lý tài khoản!")
            return

        self.xoa_noi_dung_cu()
        card = tk.Frame(
            self.content_area,
            bg=config.COLOR_CARD,
            highlightbackground=config.COLOR_BORDER,
            highlightthickness=1,
            padx=25,
            pady=20
        )
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            card,
            text="QUẢN LÝ & TẠO TÀI KHOẢN NHÂN VIÊN",
            font=config.FONT_TITLE,
            bg=config.COLOR_CARD,
            fg=config.COLOR_PRIMARY
        ).pack(anchor="w", pady=(0, 15))

        form_frame = tk.LabelFrame(
            card,
            text="Tạo tài khoản mới",
            font=config.FONT_BODY_BOLD,
            bg=config.COLOR_CARD,
            fg=config.COLOR_TEXT_MAIN,
            padx=15,
            pady=15
        )
        form_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(form_frame, text="Tên đăng nhập:", font=config.FONT_BODY, bg=config.COLOR_CARD).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_new_user = tk.Entry(form_frame, font=config.FONT_BODY, width=20)
        entry_new_user.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Mật khẩu (>= 6 ký tự):", font=config.FONT_BODY, bg=config.COLOR_CARD).grid(row=0, column=2, sticky="w", padx=(15, 5), pady=5)
        entry_new_pass = tk.Entry(form_frame, font=config.FONT_BODY, width=20, show="*")
        entry_new_pass.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Vai trò:", font=config.FONT_BODY, bg=config.COLOR_CARD).grid(row=0, column=4, sticky="w", padx=(15, 5), pady=5)
        combo_role = ttk.Combobox(form_frame, values=["Lễ tân", "Quản lý", "Admin"], state="readonly", font=config.FONT_BODY, width=15)
        combo_role.set("Lễ tân")
        combo_role.grid(row=0, column=5, padx=5, pady=5)

        # Bang danh sach tai khoan hien co
        columns = ("user", "vai_tro")
        tree = ttk.Treeview(card, columns=columns, show="headings", height=8)
        tree.heading("user", text="Tên đăng nhập")
        tree.heading("vai_tro", text="Vai trò phân quyền")
        tree.column("user", width=250)
        tree.column("vai_tro", width=200)
        tree.pack(fill=tk.BOTH, expand=True)

        def nap_danh_sach_user():
            for item in tree.get_children():
                tree.delete(item)
            for u in self.quan_ly.ds_users:
                tree.insert("", tk.END, values=(u.ten_dang_nhap, u.vai_tro))

        def xu_ly_tao_tai_khoan():
            try:
                user = entry_new_user.get()
                pwd = entry_new_pass.get()
                role = combo_role.get()

                self.quan_ly.tao_tai_khoan(user, pwd, role)
                messagebox.showinfo("Thành công", f"Đã tạo tài khoản '{user.strip()}' thành công!")
                entry_new_user.delete(0, tk.END)
                entry_new_pass.delete(0, tk.END)
                nap_danh_sach_user()
            except ValueError as e:
                messagebox.showerror("Lỗi dữ liệu", str(e))
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể tạo tài khoản: {e}")

        btn_them = tk.Button(
            form_frame,
            text="Tạo tài khoản",
            font=config.FONT_BUTTON,
            bg=config.COLOR_ACCENT,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            command=xu_ly_tao_tai_khoan
        )
        btn_them.grid(row=0, column=6, padx=(20, 5), ipady=4)

        nap_danh_sach_user()

    # Chuc nang doi mat khau (cho tat ca nguoi dung)
    def mo_cua_so_doi_mat_khau(self):
        popup = tk.Toplevel(self)
        popup.title("Đổi mật khẩu tài khoản")
        popup.geometry("380x290")
        popup.resizable(False, False)
        popup.configure(bg=config.COLOR_CARD)
        popup.grab_set()

        frame = tk.Frame(popup, bg=config.COLOR_CARD, padx=25, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="ĐỔI MẬT KHẨU", font=config.FONT_HEADER, bg=config.COLOR_CARD, fg=config.COLOR_PRIMARY).pack(pady=(0, 15))

        tk.Label(frame, text="Mật khẩu hiện tại:", font=config.FONT_BODY_BOLD, bg=config.COLOR_CARD, anchor="w").pack(fill=tk.X)
        entry_old = tk.Entry(frame, font=config.FONT_BODY, show="*")
        entry_old.pack(fill=tk.X, pady=(3, 10), ipady=3)

        tk.Label(frame, text="Mật khẩu mới (ít nhất 6 ký tự):", font=config.FONT_BODY_BOLD, bg=config.COLOR_CARD, anchor="w").pack(fill=tk.X)
        entry_new = tk.Entry(frame, font=config.FONT_BODY, show="*")
        entry_new.pack(fill=tk.X, pady=(3, 10), ipady=3)

        tk.Label(frame, text="Nhập lại mật khẩu mới:", font=config.FONT_BODY_BOLD, bg=config.COLOR_CARD, anchor="w").pack(fill=tk.X)
        entry_confirm = tk.Entry(frame, font=config.FONT_BODY, show="*")
        entry_confirm.pack(fill=tk.X, pady=(3, 15), ipady=3)

        def xac_nhan_doi():
            mk_cu = entry_old.get().strip()
            mk_moi = entry_new.get().strip()
            mk_xac_nhan = entry_confirm.get().strip()

            if not mk_cu or not mk_moi or not mk_xac_nhan:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các trường!", parent=popup)
                return

            if mk_moi != mk_xac_nhan:
                messagebox.showerror("Lỗi xác nhận", "Mật khẩu mới nhập lại không khớp!", parent=popup)
                return

            try:
                self.quan_ly.doi_mat_khau(self.nguoi_dung.ten_dang_nhap, mk_cu, mk_moi)
                messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!", parent=popup)
                popup.destroy()
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e), parent=popup)
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể đổi mật khẩu: {e}", parent=popup)

        tk.Button(
            frame,
            text="XÁC NHẬN ĐỔI MẬT KHẨU",
            font=config.FONT_BUTTON,
            bg=config.COLOR_SUCCESS,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=xac_nhan_doi
        ).pack(fill=tk.X, ipady=6)

    def xac_nhan_dang_xuat(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất khỏi hệ thống?"):
            self.on_logout()