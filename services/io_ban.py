
import json
from pathlib import Path

from models.ban import BanThuong, BanVIP


# Xac dinh duong dan goc cua project
THU_MUC_GOC = Path(__file__).resolve().parent.parent
DUONG_DAN_FILE = THU_MUC_GOC / "data" / "ban.json"


# Tao 5 ban mau ban dau
def tao_5_ban_mau():
    return [
        BanThuong("B01", 4, "Trong", 500000),
        BanThuong("B02", 6, "Trong", 700000),
        BanThuong("B03", 4, "Da dat", 500000),
        BanVIP("VIP01", 8, "Trong", 1500000, 200000),
        BanVIP("VIP02", 10, "Da dat", 2000000, 300000)
    ]


# Chuyen Dictionary thanh doi tuong Ban
def chuyen_dict_sang_ban(data):

    if not isinstance(data, dict):
        raise ValueError("Du lieu ban phai la Dictionary")

    loai_ban = data.get("loai_ban")

    if loai_ban == "BanThuong":
        return BanThuong(
            data["ma_ban"],
            data["so_ghe"],
            data["trang_thai"],
            data["don_gia_ban"]
        )

    elif loai_ban == "BanVIP":
        return BanVIP(
            data["ma_ban"],
            data["so_ghe"],
            data["trang_thai"],
            data["don_gia_ban"],
            data["phu_phi"]
        )

    else:
        raise ValueError("Loai ban khong hop le")


# Doc du lieu ban tu file JSON
def load_ban_json():

    try:
        with open(DUONG_DAN_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Kiem tra file JSON rong hoac khong co ban
        if not data:
            print("Du lieu rong. Dang khoi phuc 5 ban mau...")

            danh_sach_ban = tao_5_ban_mau()
            save_ban_json(danh_sach_ban)

            return danh_sach_ban

        if not isinstance(data, list):
            raise ValueError("Du lieu JSON phai la mot danh sach")

        # Chuyen tung Dictionary thanh doi tuong Ban
        danh_sach_ban = []

        for item in data:
            ban = chuyen_dict_sang_ban(item)
            danh_sach_ban.append(ban)

        return danh_sach_ban

    except FileNotFoundError:
        print("Khong tim thay file ban.json. Dang khoi phuc...")

        danh_sach_ban = tao_5_ban_mau()
        save_ban_json(danh_sach_ban)

        return danh_sach_ban

    except json.JSONDecodeError:
        print("File JSON bi rong hoac sai dinh dang. Dang khoi phuc...")

        danh_sach_ban = tao_5_ban_mau()
        save_ban_json(danh_sach_ban)

        return danh_sach_ban


# Ghi danh sach ban vao file JSON
def save_ban_json(danh_sach_ban):

    # Tao thu muc data neu chua ton tai
    DUONG_DAN_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = []

    for ban in danh_sach_ban:

        # Su dung ham to_dict() cua lop Ban o buoi 1
        data.append(ban.to_dict())

    with open(DUONG_DAN_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Da luu danh sach ban vao file JSON thanh cong!")
