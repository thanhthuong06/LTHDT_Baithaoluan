import os
import csv

ACCOUNT_FILE = "accounts.txt"
READERS_FILE = "readers.csv"
STAFFS_FILE = "staffs.csv"

# ===== LƯU TÀI KHOẢN VÀO FILE =====
def save_account(user_id, password, role):
    with open(ACCOUNT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user_id},{password},{role}\n")

# ===== ĐỌC TẤT CẢ TÀI KHOẢN =====
def load_accounts():
    accounts = {}
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    user, pw, role = parts
                    accounts[user] = {"password": pw, "role": role}
    return accounts

# ===== HÀM KIỂM TRA ID CÓ TỒN TẠI TRONG FILE STAFF HOẶC READER KHÔNG =====
def id_exists(user_id, role):
    filename = STAFFS_FILE if role == "staff" else READERS_FILE
    if not os.path.exists(filename):
        return False

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0 and row[0].strip() == user_id:  # cột đầu tiên là ID
                return True
    return False

# ===== TẠO TÀI KHOẢN =====
def register():
    print("\n===== ĐĂNG KÝ TÀI KHOẢN MỚI =====")
    accounts = load_accounts()

    print("Chọn vai trò:")
    print("1. Nhân viên (staff)")
    print("2. Độc giả (reader)")
    role_choice = input("→ Nhập 1 hoặc 2: ").strip()
    role = "staff" if role_choice == "1" else "reader"

    # --- Nhập ID và kiểm tra có tồn tại trong file danh sách không ---
    while True:
        user_id = input("Nhập mã ID (ví dụ: NV001 hoặc DG001): ").strip()
        if not id_exists(user_id, role):
            print(f"ID '{user_id}' không tồn tại trong danh sách {role}. Vui lòng kiểm tra lại!")
        elif user_id in accounts:
            print("Tài khoản này đã được tạo trước đó!")
        else:
            break

    password = input("Nhập mật khẩu: ").strip()
    save_account(user_id, password, role)
    print(f"Tạo tài khoản thành công cho {user_id} ({role})!")

# ===== ĐĂNG NHẬP =====
def login():
    print("\n===== ĐĂNG NHẬP HỆ THỐNG =====")
    accounts = load_accounts()
    attempts = 3  # cho phép nhập sai tối đa 3 lần

    while attempts > 0:
        username = input("Tên đăng nhập (ID): ").strip()
        password = input("Mật khẩu: ").strip()

        if username in accounts and accounts[username]["password"] == password:
            print(f"Đăng nhập thành công với vai trò: {accounts[username]['role']}")
            return accounts[username]["role"]
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Sai tên đăng nhập hoặc mật khẩu! Còn {attempts} lần thử.")
            else:
                print("Bạn đã nhập sai quá 3 lần. Vui lòng thử lại sau.")
                return None
