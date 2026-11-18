
import json
import os
import shutil
import tempfile
from pathlib import Path

from models.khach_hang import KhachHang
from models.phieu_dat import PhieuDatBan
from models.nguoi_dung import NguoiDung
from models.ban import BanThuong, BanVIP

# Xac dinh duong dan thu muc goc cua project
THU_MUC_GOC = Path(__file__).resolve().parent.parent
THU_MUC_DATA = THU_MUC_GOC / "data"

FILE_KHACH = THU_MUC_DATA / "khach_hang.json"
FILE_PHIEU = THU_MUC_DATA / "phieu_dat.json"
FILE_USERS = THU_MUC_DATA / "users.json"

def _tao_thu_muc_data():
    """Tao thu muc data neu chua ton tai."""
    THU_MUC_DATA.mkdir(parents=True, exist_ok=True)


def _tao_ban_sao(path, hau_to):
    """Tao ban sao file, khong ghi de ban sao cu."""
    ban_sao = path.with_suffix(path.suffix + hau_to)
    so_thu_tu = 1

    while ban_sao.exists():
        ban_sao = path.with_suffix(
            path.suffix + f"{hau_to}.{so_thu_tu}"
        )
        so_thu_tu += 1

    shutil.copy2(path, ban_sao)
    return ban_sao


def _doc_json(path, mac_dinh):
    """
    Doc file JSON an toan.
    Neu file khong ton tai hoac rong thi tra ve mac dinh.
    Neu JSON sai dinh dang thi sao luu file loi.
    """
    _tao_thu_muc_data()

    try:
        with open(path, "r", encoding="utf-8") as file:
            noi_dung = file.read()

        if not noi_dung.strip():
            return mac_dinh

        return json.loads(noi_dung)

    except FileNotFoundError:
        return mac_dinh

    except json.JSONDecodeError as loi:
        try:
            _tao_ban_sao(path, ".corrupt")
        except OSError as loi_sao_luu:
            raise RuntimeError(
                f"JSON tai {path.name} bi loi va khong the sao luu file goc."
            ) from loi_sao_luu

        print(
            f"Canh bao: {path.name} sai dinh dang JSON. "
            "Da giu ban goc va tao ban sao .corrupt."
        )

        _ghi_json(path, mac_dinh)
        return mac_dinh

    except PermissionError as loi:
        raise PermissionError(
            f"Khong co quyen doc file {path.name}."
        ) from loi

    except OSError as loi:
        raise OSError(
            f"Khong the doc file {path.name}: {loi}"
        ) from loi


def _ghi_json(path, du_lieu):
    """
    Ghi JSON an toan.
    Tao file tam, sao luu file cu roi thay the file chinh.
    """
    _tao_thu_muc_data()
    file_tam = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            suffix=".tmp",
            delete=False
        ) as file:
            file_tam = Path(file.name)

            json.dump(
                du_lieu,
                file,
                ensure_ascii=False,
                indent=4,
                allow_nan=False
            )

            file.flush()
            os.fsync(file.fileno())

        if path.exists():
            _tao_ban_sao(path, ".bak")

        os.replace(file_tam, path)
        print(f"Da luu du lieu vao {path.name}.")

    except PermissionError as loi:
        raise PermissionError(
            f"Khong co quyen ghi file {path.name}."
        ) from loi

    except (OSError, TypeError, ValueError) as loi:
        raise RuntimeError(
            f"Khong the ghi file {path.name}: {loi}"
        ) from loi

    finally:
        if file_tam is not None and file_tam.exists():
            try:
                file_tam.unlink()
            except OSError:
                pass


def _kiem_tra_danh_sach(danh_sach, ten_danh_sach):
    """Kiem tra du lieu dau vao co phai list hay khong."""
    if not isinstance(danh_sach, list):
        raise TypeError(
            f"{ten_danh_sach} phai la mot danh sach (list)."
        )


def _chuyen_sang_json(value):
    """Chuyen du lieu thanh kieu du lieu JSON."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, list):
        return [_chuyen_sang_json(item) for item in value]

    if isinstance(value, tuple):
        return [_chuyen_sang_json(item) for item in value]

    if isinstance(value, dict):
        return {
            str(key): _chuyen_sang_json(item)
            for key, item in value.items()
        }

    if hasattr(value, "to_dict") and callable(value.to_dict):
        return _chuyen_sang_json(value.to_dict())

    raise TypeError(
        f"Du lieu {type(value).__name__} khong the chuyen thanh JSON."
    )


def _doc_danh_sach(path):
    """Doc du lieu dang danh sach tu file JSON."""
    du_lieu = _doc_json(path, [])

    if not isinstance(du_lieu, list):
        raise ValueError(
            f"Du lieu trong {path.name} phai la mot danh sach."
        )

    if not path.exists() or path.stat().st_size == 0:
        _ghi_json(path, [])

    return du_lieu

# PHAN 1: DOC/GHI FILE JSON KHACH HANG

def load_khach_json():
    """Doc danh sach KhachHang tu file khach_hang.json."""
    du_lieu = _doc_danh_sach(FILE_KHACH)
    danh_sach_khach = []

    for vi_tri, item in enumerate(du_lieu, start=1):
        try:
            if not isinstance(item, dict):
                raise TypeError(
                    "Moi khach hang phai la Dictionary."
                )

            khach = KhachHang(
                item["ma_kh"],
                item["ten_kh"],
                item["sdt"],
                item["email"]
            )

            danh_sach_khach.append(khach)

        except (KeyError, TypeError, ValueError) as loi:
            raise ValueError(
                f"Du lieu khach hang o dong {vi_tri} "
                f"khong hop le: {loi}"
            ) from loi

    return danh_sach_khach


def save_khach_json(danh_sach_khach):
    """Ghi danh sach doi tuong KhachHang vao file JSON."""
    _kiem_tra_danh_sach(
        danh_sach_khach,
        "Danh sach khach hang"
    )

    du_lieu = []

    for vi_tri, khach in enumerate(danh_sach_khach, start=1):
        if not isinstance(khach, KhachHang):
            raise TypeError(
                f"Phan tu thu {vi_tri} phai la doi tuong KhachHang."
            )

        du_lieu.append(khach.to_dict())

    _ghi_json(
        FILE_KHACH,
        _chuyen_sang_json(du_lieu)
    )


# PHAN 2: DOC/GHI FILE JSON PHIEU DAT BAN

def _chuyen_dict_sang_ban(data):
    """Tao doi tuong BanThuong hoac BanVIP tu Dictionary."""
    if not isinstance(data, dict):
        raise TypeError(
            "Thong tin ban phai la Dictionary."
        )

    loai_ban = data.get("loai_ban")

    try:
        if loai_ban == "BanThuong":
            return BanThuong(
                data["ma_ban"],
                data["so_ghe"],
                data["trang_thai"],
                data["don_gia_ban"]
            )

        if loai_ban == "BanVIP":
            return BanVIP(
                data["ma_ban"],
                data["so_ghe"],
                data["trang_thai"],
                data["don_gia_ban"],
                data["phu_phi"]
            )

        raise ValueError(
            f"Loai ban '{loai_ban}' khong hop le."
        )

    except KeyError as loi:
        raise ValueError(
            f"Thieu truong du lieu ban: {loi}"
        ) from loi


def load_phieu_json():
    """Doc danh sach PhieuDatBan tu file phieu_dat.json."""
    du_lieu = _doc_danh_sach(FILE_PHIEU)
    danh_sach_phieu = []

    for vi_tri, item in enumerate(du_lieu, start=1):
        try:
            if not isinstance(item, dict):
                raise TypeError(
                    "Moi phieu dat phai la Dictionary."
                )

            du_lieu_khach = item["khach_hang"]

            if not isinstance(du_lieu_khach, dict):
                raise TypeError(
                    "Thong tin khach hang trong phieu "
                    "phai la Dictionary."
                )

            khach = KhachHang(
                du_lieu_khach["ma_kh"],
                du_lieu_khach["ten_kh"],
                du_lieu_khach["sdt"],
                du_lieu_khach["email"]
            )

            ban = _chuyen_dict_sang_ban(item["ban"])

            phieu = PhieuDatBan(
                item["ma_phieu"],
                khach,
                ban,
                item["ngay_dat"],
                item["gio_dat"],
                item.get("ds_mon_dat", [])
            )

            danh_sach_phieu.append(phieu)

        except (KeyError, TypeError, ValueError) as loi:
            raise ValueError(
                f"Du lieu phieu dat o dong {vi_tri} "
                f"khong hop le: {loi}"
            ) from loi

    return danh_sach_phieu


def save_phieu_json(danh_sach_phieu):
    """Ghi danh sach doi tuong PhieuDatBan vao file JSON."""
    _kiem_tra_danh_sach(
        danh_sach_phieu,
        "Danh sach phieu dat"
    )

    du_lieu = []

    for vi_tri, phieu in enumerate(danh_sach_phieu, start=1):
        if not isinstance(phieu, PhieuDatBan):
            raise TypeError(
                f"Phan tu thu {vi_tri} phai la doi tuong PhieuDatBan."
            )

        du_lieu.append(phieu.to_dict())

    _ghi_json(
        FILE_PHIEU,
        _chuyen_sang_json(du_lieu)
    )

# PHAN 3: DOC/GHI FILE JSON TAI KHOAN NGUOI DUNG / ADMIN

def _tao_admin_mac_dinh():
    """Tao tai khoan Admin mac dinh."""
    return NguoiDung(
        "admin",
        "123456",
        "Admin"
    )


def load_users_json():
    """
    Doc danh sach tai khoan nguoi dung.
    Neu file chua ton tai, rong hoac chua co tai khoan,
    tu dong tao tai khoan Admin admin/123456.
    """
    du_lieu = _doc_danh_sach(FILE_USERS)
    danh_sach_users = []

    for vi_tri, item in enumerate(du_lieu, start=1):
        try:
            if not isinstance(item, dict):
                raise TypeError(
                    "Moi tai khoan phai la Dictionary."
                )

            user = NguoiDung(
                item["ten_dang_nhap"],
                item["mat_khau"],
                item["vai_tro"]
            )

            danh_sach_users.append(user)

        except (KeyError, TypeError, ValueError) as loi:
            raise ValueError(
                f"Du lieu tai khoan o dong {vi_tri} "
                f"khong hop le: {loi}"
            ) from loi

    if not danh_sach_users:
        admin = _tao_admin_mac_dinh()
        danh_sach_users.append(admin)

        save_users_json(danh_sach_users)

        print(
            "Da tao tai khoan Admin mac dinh: admin / 123456."
        )

    return danh_sach_users


def save_users_json(danh_sach_users):
    """Ghi danh sach doi tuong NguoiDung vao file users.json."""
    _kiem_tra_danh_sach(
        danh_sach_users,
        "Danh sach nguoi dung"
    )

    du_lieu = []

    for vi_tri, user in enumerate(danh_sach_users, start=1):
        if not isinstance(user, NguoiDung):
            raise TypeError(
                f"Phan tu thu {vi_tri} phai la doi tuong NguoiDung."
            )

        du_lieu.append(user.to_dict())

    _ghi_json(
        FILE_USERS,
        _chuyen_sang_json(du_lieu)
    )
