import csv
import os
from Lop_doi_tuong import Reader, Staff

class BaseDataManager:
    def __init__(self, filename, cls, fieldnames, id_field):
        """
        filename: tên file CSV
        cls: lớp đối tượng (Reader, Staff, ...)
        fieldnames: danh sách tên cột CSV
        id_field: tên thuộc tính dùng để xác định đối tượng duy nhất (VD: reader_id, staff_id)
        """
        self.filename = filename
        self.cls = cls
        self.fieldnames = fieldnames
        self.id_field = id_field
        self.items = []
        self.load_from_file()

    # ================== ĐỌC / GHI FILE ==================
    def load_from_file(self):
        """Đọc dữ liệu từ file CSV"""
        if not os.path.exists(self.filename):
            return
        with open(self.filename, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            self.items = []
            for row in reader:
                # Chuyển borrowed_books về int nếu có
                if 'borrowed_books' in row:
                    row['borrowed_books'] = int(row['borrowed_books'])
                # Chuyển borrowed_books_list từ chuỗi sang list
                if 'borrowed_books_list' in row:
                    row['borrowed_books_list'] = row['borrowed_books_list'].split('|') if row['borrowed_books_list'] else []
                self.items.append(self.cls(**row))

    def save_to_file(self):
        """Ghi toàn bộ dữ liệu ra file CSV"""
        with open(self.filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for obj in self.items:
                # Chuyển list sang chuỗi để lưu CSV
                data = obj.__dict__.copy()
                if 'borrowed_books_list' in data:
                    data['borrowed_books_list'] = '|'.join(data['borrowed_books_list'])
                writer.writerow(data)

    # ================== CÁC PHƯƠNG THỨC ==================
    def add_item(self, obj):
        """Thêm đối tượng mới"""
        if any(getattr(x, self.id_field) == getattr(obj, self.id_field) for x in self.items):
            print(f"{self.id_field} đã tồn tại.")
            return False
        self.items.append(obj)
        self.save_to_file()
        print("Thêm mới thành công!")
        return True

    def update_item(self, item_id):
        """Cập nhật thông tin đối tượng (không cho phép sửa borrowed_books/borrowed_books_list)"""
        for obj in self.items:
            if getattr(obj, self.id_field) == item_id:
                print("Nhập thông tin mới (nhấn Enter để bỏ qua):")
                for field in self.fieldnames:
                    if field == self.id_field or field in ['borrowed_books', 'borrowed_books_list']:
                        continue
                    current_value = getattr(obj, field)
                    new_value = input(f"{field} ({current_value}): ").strip()
                    if new_value:
                        setattr(obj, field, new_value)
                self.save_to_file()
                print("Cập nhật thành công!")
                return True
        print("Không tìm thấy đối tượng cần sửa.")
        return False

    def delete_item(self, item_id):
        """Xóa đối tượng theo ID"""
        for obj in self.items:
            if getattr(obj, self.id_field) == item_id:
                self.items.remove(obj)
                self.save_to_file()
                print("Xóa thành công!")
                return True
        print("Không tìm thấy đối tượng cần xóa.")
        return False

    def search_item(self, keyword):
        """Tìm kiếm theo ID hoặc tên"""
        result = []
        for obj in self.items:
            for val in obj.__dict__.values():
                if keyword.lower() in str(val).lower():
                    result.append(obj)
                    break
        return result

    def display_all(self):
        """Hiển thị tất cả dữ liệu"""
        if not self.items:
            print("Danh sách trống.")
            return
        print("\n===== DANH SÁCH =====")
        print(" | ".join([f"{col.upper():<15}" for col in self.fieldnames]))
        print("-" * 120)
        for obj in self.items:
            row = []
            for f in self.fieldnames:
                val = getattr(obj, f)
                if isinstance(val, list):
                    val = ','.join(val) if val else "Không có"
                row.append(f"{str(val):<15}")
            print(" | ".join(row))


# ========================== DataReader ==========================
class DataReader(BaseDataManager):
    def __init__(self):
        super().__init__(
            filename="readers.csv",
            cls=Reader,
            fieldnames=["reader_id", "full_name", "age", "class_name", "register_date", "borrowed_books", "borrowed_books_list"],
            id_field="reader_id"
        )

    def add_reader(self):
        r = Reader()  # borrowed_books = 0, borrowed_books_list = []
        r.input_info()  # nhập tên, tuổi, lớp, ngày đăng ký, mã độc giả
        self.add_item(r)

    def update_reader(self, reader_id):
        self.update_item(reader_id)

    def delete_reader(self, reader_id):
        self.delete_item(reader_id)

    def search_reader(self, keyword):
        results = self.search_item(keyword)
        for r in results:
            borrowed_list_str = ','.join(r.borrowed_books_list) if r.borrowed_books_list else "Không có"
            print(f"{r.reader_id} | {r.full_name} | {r.age} | {r.class_name} | {r.register_date} | {r.borrowed_books} | {borrowed_list_str}")

    def display_all(self):
        if not self.items:
            print("Danh sách độc giả trống.")
            return
        print("\n===== DANH SÁCH ĐỘC GIẢ =====")
        print(f"{'ID':<10} | {'HỌ TÊN':<25} | {'TUỔI':<5} | {'LỚP':<6} | {'NGÀY ĐK':<12} | {'SLSH':<5} | {'SÁCH MƯỢN':<30}")
        print("-" * 120)
        for r in self.items:
            borrowed_list_str = ','.join(r.borrowed_books_list) if r.borrowed_books_list else "Không có"
            print(f"{r.reader_id:<10} | {r.full_name:<25} | {r.age:<5} | {r.class_name:<6} | {r.register_date:<12} | {r.borrowed_books:<5} | {borrowed_list_str:<30}")


# ========================== DataStaff ==========================
class DataStaff(BaseDataManager):
    def __init__(self):
        super().__init__(
            filename="staff.csv",
            cls=Staff,
            fieldnames=["staff_id", "full_name", "age", "position", "start_date"],
            id_field="staff_id"
        )

    def add_staff(self):
        s = Staff()
        s.input_info()
        self.add_item(s)

    def update_staff(self, staff_id):
        self.update_item(staff_id)

    def delete_staff(self, staff_id):
        self.delete_item(staff_id)

    def search_staff(self, keyword):
        results = self.search_item(keyword)
        for s in results:
            print(f"{s.staff_id} | {s.full_name} | {s.age} | {s.position} | {s.start_date}")

    def display_all(self):
        if not self.items:
            print("Danh sách nhân viên trống.")
            return
        print("\n===== DANH SÁCH NHÂN VIÊN =====")
        print(f"{'ID NV':<15} | {'HỌ TÊN':<25} | {'TUỔI':<5} | {'CHỨC VỤ':<15} | {'NGÀY VÀO LÀM':<12}")
        print("-" * 120)
        for s in self.items:
            print(f"{s.staff_id:<15} | {s.full_name:<25} | {s.age:<5} | {s.position:<15} | {s.start_date:<12}")
