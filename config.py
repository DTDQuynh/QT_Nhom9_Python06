import os

# 1. Cau hinh duong dan tuong doi (chay duoc tren moi may tinh)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Tu dong tao thu muc data neu chua ton tai
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Duong dan den cac file du lieu JSON
FILE_BAN = os.path.join(DATA_DIR, "ban.json")
FILE_KHACH_HANG = os.path.join(DATA_DIR, "khach_hang.json")
FILE_PHIEU_DAT = os.path.join(DATA_DIR, "phieu_dat.json")
FILE_THUC_DON = os.path.join(DATA_DIR, "thuc_don.json")
FILE_USERS = os.path.join(DATA_DIR, "users.json")


# 2. Cau hinh cua so ung dung
APP_TITLE = "HỆ THỐNG QUẢN LÝ ĐẶT BÀN NHÀ HÀNG - NHÓM 9"
WINDOW_SIZE = "1180x720"
WINDOW_MIN_SIZE = (1024, 600)


# 3. Mau sac trang thai ban an
MAU_BAN_TRONG = "#10B981"       # Xanh la: ban trong
MAU_BAN_DA_DAT = "#F59E0B"      # Vang: ban da dat truoc
MAU_BAN_PHUC_VU = "#EF4444"     # Do: ban dang phuc vu
MAU_BAN_BAO_TRI = "#94A3B8"     # Xam: ban dang bao tri


# 4. Mau sac giao dien chinh
COLOR_PRIMARY = "#0F172A"       # Xanh den dam (Header)
COLOR_SIDEBAR = "#1E293B"       # Xanh navy (Menu ben trai)
COLOR_BACKGROUND = "#F8FAFC"    # Xam nhat (Nen ung dung)
COLOR_CARD = "#FFFFFF"          # Trang (Nen khung card, bang, canvas)

# Mau nut bam
COLOR_ACCENT = "#2563EB"        # Xanh duong (Nut chinh: Them, Dat ban)
COLOR_ACCENT_HOVER = "#1D4ED8"  # Xanh dam khi di chuot vao nut
COLOR_SUCCESS = "#10B981"       # Xanh la (Nut Xac nhan, Luu)
COLOR_DANGER = "#DC2626"        # Do (Nut Huy, Xoa)
COLOR_WARNING = "#D97706"       # Cam (Nut Sua, Cap nhat)

# Mau chu va vien
COLOR_TEXT_MAIN = "#0F172A"     # Chu chinh mau den xam
COLOR_TEXT_MUTED = "#64748B"    # Chu phu mau xam
COLOR_BORDER = "#E2E8F0"        # Mau vien khung va bang


# 5. Cau hinh font chu
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_HEADER = ("Segoe UI", 12, "bold")
FONT_SUBHEADER = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_BODY_BOLD = ("Segoe UI", 10, "bold")
FONT_BUTTON = ("Segoe UI", 10, "bold")
FONT_SMALL = ("Segoe UI", 9)