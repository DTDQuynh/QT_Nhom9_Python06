import re
from datetime import datetime

# 1. KIỂM TRA SỐ ĐIỆN THOẠI
def kiem_tra_sdt(sdt):
    """
    Kiểm tra số điện thoại:
    - Có đúng 10 chữ số.
    - Bắt đầu bằng 03, 05, 07, 08 hoặc 09.
    """
    if sdt is None or not isinstance(sdt, str):
        return False, "Số điện thoại không được để trống."

    sdt = sdt.strip()

    if not sdt:
        return False, "Số điện thoại không được để trống."

    if any(char.isspace() for char in sdt):
        return False, "Số điện thoại không được chứa khoảng trắng."

    if not sdt.isdigit():
        return False, "Số điện thoại chỉ được chứa chữ số."

    if len(sdt) != 10:
        return False, "Số điện thoại phải có đúng 10 chữ số."

    if not sdt.startswith(("03", "05", "07", "08", "09")):
        return False, (
            "Số điện thoại phải bắt đầu bằng đầu số "
            "nhà mạng 03/05/07/08/09."
        )

    return True, "Số điện thoại hợp lệ."

# 2. KIỂM TRA EMAIL
def kiem_tra_email(email, cho_phep_trong=False):
    """
    Kiểm tra định dạng email bằng biểu thức chính quy.
    Nếu cho_phep_trong=True thì chuỗi rỗng/None được coi là hợp lệ.
    """
    if email is None or not isinstance(email, str):
        if cho_phep_trong:
            return True, "Email để trống (hợp lệ)."
        return False, "Email không được để trống."

    email = email.strip()

    if not email:
        if cho_phep_trong:
            return True, "Email để trống (hợp lệ)."
        return False, "Email không được để trống."

    if any(char.isspace() for char in email):
        return False, "Email không được chứa khoảng trắng."

    mau_email = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(mau_email, email):
        return False, "Email không đúng định dạng. Ví dụ: abc@gmail.com."

    return True, "Email hợp lệ."

# 3. KIỂM TRA NGÀY GIỜ
def kiem_tra_ngay_gio(ngay_gio):
    """
    Kiểm tra ngày giờ theo định dạng:
    DD/MM/YYYY HH:MM

    Ví dụ: 25/11/2026 13:30
    """
    if ngay_gio is None or not isinstance(ngay_gio, str):
        return False, "Ngày giờ không được để trống."

    ngay_gio = re.sub(r"\s+", " ", ngay_gio.strip())

    if not ngay_gio:
        return False, "Ngày giờ không được để trống."

    mau_ngay_gio = r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$"

    if not re.fullmatch(mau_ngay_gio, ngay_gio):
        return False, (
            "Ngày giờ phải đúng định dạng "
            "DD/MM/YYYY HH:MM."
        )

    try:
        datetime.strptime(ngay_gio, "%d/%m/%Y %H:%M")
    except ValueError:
        return False, (
            "Ngày giờ không hợp lệ. "
            "Vui lòng kiểm tra ngày, tháng, năm và giờ."
        )

    return True, "Ngày giờ hợp lệ."

# 4. KIỂM TRA TỔNG HỢP
def kiem_tra_thong_tin(sdt, email, ngay_gio, cho_phep_email_trong=False):
    """
    Kiểm tra đồng thời số điện thoại, email và ngày giờ.
    Trả về danh sách các lỗi nếu có.
    """
    ket_qua = {
        "sdt": kiem_tra_sdt(sdt),
        "email": kiem_tra_email(email, cho_phep_trong=cho_phep_email_trong),
        "ngay_gio": kiem_tra_ngay_gio(ngay_gio),
    }

    danh_sach_loi = []

    for truong, (hop_le, thong_bao) in ket_qua.items():
        if not hop_le:
            danh_sach_loi.append(f"{truong}: {thong_bao}")

    return len(danh_sach_loi) == 0, danh_sach_loi
