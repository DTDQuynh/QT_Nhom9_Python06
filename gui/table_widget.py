
import tkinter as tk
from tkinter import messagebox


class TableWidget(tk.Frame):
    """
    Custom Widget hiển thị thông tin một bàn ăn.

    Chức năng:
    - Hiển thị mã bàn, số ghế, đơn giá và trạng thái.
    - Thay đổi màu viền khi di chuột vào thẻ.
    - Nhấn đúp để mở hộp thoại thông tin bàn.
    """

    # Màu hiển thị theo trạng thái bàn
    STATUS_COLORS = {
        "trong": {
            "background": "#E8F5E9",
            "foreground": "#2E7D32"
        },
        "da dat": {
            "background": "#FFF8E1",
            "foreground": "#F9A825"
        },
        "dang phuc vu": {
            "background": "#FFEBEE",
            "foreground": "#C62828"
        },
        "bao tri": {
            "background": "#EEEEEE",
            "foreground": "#616161"
        }
    }

    def __init__(self, master, ban, **kwargs):
        super().__init__(
            master,
            bg="white",
            highlightthickness=1,
            highlightbackground="#BDBDBD",
            highlightcolor="#2196F3",
            bd=0,
            padx=12,
            pady=10,
            **kwargs
        )

        # Kiểm tra dữ liệu bàn
        required_attributes = (
            "ma_ban",
            "so_ghe",
            "don_gia_ban",
            "trang_thai"
        )

        for attribute in required_attributes:
            if not hasattr(ban, attribute):
                raise AttributeError(
                    f"Đối tượng bàn thiếu thuộc tính: {attribute}"
                )

        self.ban = ban
        self._is_hovered = False

        # Lấy màu theo trạng thái
        status_key = " ".join(
            str(self.ban.trang_thai).strip().lower().split()
        )

        self.status_color = self.STATUS_COLORS.get(
            status_key,
            {
                "background": "#EEEEEE",
                "foreground": "#616161"
            }
        )

        self._create_widgets()
        self._bind_events()

    def _format_price(self):
        """Định dạng đơn giá bàn."""
        return f"{self.ban.don_gia_ban:,.0f} đ"

    def _create_widgets(self):
        """Tạo các thành phần hiển thị trên thẻ bàn."""

        # Tiêu đề mã bàn
        self.lbl_ma_ban = tk.Label(
            self,
            text=f"BÀN {self.ban.ma_ban}",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#263238"
        )
        self.lbl_ma_ban.pack(anchor="w", pady=(0, 8))

        # Số ghế
        self.lbl_so_ghe = tk.Label(
            self,
            text=f"Số ghế: {self.ban.so_ghe}",
            font=("Arial", 11),
            bg="white",
            fg="#455A64"
        )
        self.lbl_so_ghe.pack(anchor="w", pady=3)

        # Đơn giá
        self.lbl_don_gia = tk.Label(
            self,
            text=f"Đơn giá: {self._format_price()}",
            font=("Arial", 11),
            bg="white",
            fg="#455A64"
        )
        self.lbl_don_gia.pack(anchor="w", pady=3)

        # Trạng thái
        self.lbl_trang_thai = tk.Label(
            self,
            text=f"● {self.ban.trang_thai}",
            font=("Arial", 10, "bold"),
            bg=self.status_color["background"],
            fg=self.status_color["foreground"],
            padx=8,
            pady=5
        )
        self.lbl_trang_thai.pack(
            anchor="w",
            pady=(8, 0),
            fill="x"
        )

    def _bind_events(self):
        """Gắn sự kiện hover và nhấn đúp cho thẻ bàn."""

        widgets = [
            self,
            self.lbl_ma_ban,
            self.lbl_so_ghe,
            self.lbl_don_gia,
            self.lbl_trang_thai
        ]

        for widget in widgets:
            widget.bind(
                "<Enter>",
                self._on_mouse_enter,
                add="+"
            )
            widget.bind(
                "<Leave>",
                self._on_mouse_leave,
                add="+"
            )
            widget.bind(
                "<Double-Button-1>",
                self._on_double_click,
                add="+"
            )

    def _on_mouse_enter(self, event):
        """Xử lý khi chuột đi vào thẻ bàn."""
        self._is_hovered = True
        self._update_border()

    def _on_mouse_leave(self, event):
        """Kiểm tra vị trí chuột trước khi bỏ hiệu ứng hover."""
        self.after_idle(self._check_hover)

    def _check_hover(self):
        """Tránh mất hiệu ứng khi chuột di chuyển giữa các thành phần."""
        if not self.winfo_exists():
            return

        widget = self.winfo_containing(
            self.winfo_pointerx(),
            self.winfo_pointery()
        )

        inside = False

        while widget is not None:
            if widget is self:
                inside = True
                break
            widget = widget.master

        self._is_hovered = inside
        self._update_border()

    def _update_border(self):
        """Cập nhật màu viền theo trạng thái hover."""

        if self._is_hovered:
            self.configure(
                highlightbackground="#2196F3",
                highlightthickness=3
            )
        else:
            self.configure(
                highlightbackground="#BDBDBD",
                highlightthickness=1
            )

    def _on_double_click(self, event):
        """Mở hộp thoại thông tin khi nhấn đúp vào thẻ bàn."""

        information = (
            f"Mã bàn: {self.ban.ma_ban}\n"
            f"Số ghế: {self.ban.so_ghe}\n"
            f"Đơn giá: {self._format_price()}\n"
            f"Trạng thái: {self.ban.trang_thai}\n"
            f"Loại bàn: {self.ban.__class__.__name__}\n"
            f"Tiền cọc: {self.ban.tinh_tien_coc():,.0f} đ"
        )

        if hasattr(self.ban, "phu_phi"):
            information += (
                f"\nPhụ phí: {self.ban.phu_phi:,.0f} đ"
            )

        messagebox.showinfo(
            title=f"Thông tin bàn {self.ban.ma_ban}",
            message=information,
            parent=self.winfo_toplevel()
        )
