import csv
import os
from Lop import Reader  # import class Reader từ file Reader.py

class DataReader:
    def __init__(self, filename="readers.csv"):
        self.filename = filename
        self.readers = []
        self.load_from_file()

    # ================== ĐỌC / GHI FILE ==================
    def load_from_file(self):
        """Đọc danh sách độc giả từ file CSV"""
        if not os.path.exists(self.filename):
            return
        with open(self.filename, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            self.readers = [
                Reader(
                    r["reader_id"],
                    r["full_name"],
                    r["class_name"],
                    r["register_date"]
                )
                for r in reader
            ]

    def save_to_file(self):
        """Ghi danh sách độc giả xuống file CSV"""
        with open(self.filename, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["reader_id", "full_name", "class_name", "register_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for r in self.readers:
                writer.writerow({
                    "reader_id": r.reader_id,
                    "full_name": r.full_name,
                    "class_name": r.class_name,
                    "register_date": r.register_date
                })

    # ================== CHỨC NĂNG CHÍNH ==================
    def add_reader(self):
        """Thêm độc giả mới"""
        reader = Reader()
        reader.input_info()
        # Kiểm tra trùng mã
        if any(r.reader_id == reader.reader_id for r in self.readers):
            print("❌ Mã độc giả đã tồn tại.")
            return
        self.readers.append(reader)
        self.save_to_file()
        print("✅ Thêm độc giả thành công!")

    def update_reader(self, reader_id):
        """Sửa thông tin độc giả theo mã"""
        for r in self.readers:
            if r.reader_id == reader_id:
                print("Nhập thông tin mới (nhấn Enter để bỏ qua):")
                new_name = input("Họ tên mới: ").strip()
                new_class = input("Lớp mới: ").strip()
                new_date = input("Ngày đăng ký mới (DD/MM/YYYY): ").strip()

                if new_name: r.full_name = new_name
                if new_class: r.class_name = new_class
                if new_date: r.register_date = new_date

                self.save_to_file()
                print("✅ Cập nhật độc giả thành công!")
                return
        print("❌ Không tìm thấy mã độc giả.")

    def delete_reader(self, reader_id):
        """Xóa độc giả theo mã"""
        for r in self.readers:
            if r.reader_id == reader_id:
                self.readers.remove(r)
                self.save_to_file()
                print("✅ Xóa độc giả thành công!")
                return
        print("❌ Không tìm thấy mã độc giả cần xóa.")

    def search_reader(self, keyword):
        """Tìm kiếm độc giả theo mã hoặc họ tên"""
        result = [
            r for r in self.readers
            if keyword.lower() in r.reader_id.lower() or keyword.lower() in r.full_name.lower()
        ]
        if result:
            print("\n📚 KẾT QUẢ TÌM KIẾM:")
            for r in result:
                r.display_info()
        else:
            print("❌ Không tìm thấy độc giả nào phù hợp.")

    def display_all(self):
        """Hiển thị toàn bộ danh sách độc giả"""
        if not self.readers:
            print("Danh sách trống.")
            return
        print("\n===== DANH SÁCH ĐỘC GIẢ =====")
        for r in self.readers:
            print(f"{r.reader_id:<12} | {r.full_name:<25} | {r.class_name:<8} | {r.register_date}")
