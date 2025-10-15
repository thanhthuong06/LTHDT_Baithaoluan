import csv
import os
from Lop import Book   # import lớp Book từ file Book.py

class DataBook:
    def __init__(self, filename="books.csv"):
        self.books = []
        self.filename = filename
        self.load_from_csv()  # tự động đọc dữ liệu khi khởi tạo

    # === Đọc dữ liệu từ CSV ===
    def load_from_csv(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    book = Book(
                        book_id=row["book_id"],
                        title=row["title"],
                        author=row["author"],
                        publisher=row["publisher"],
                        status=row["status"]
                    )
                    self.books.append(book)
            print(f"Đã tải {len(self.books)} sách từ file {self.filename}.")
        else:
            print("Chưa có file dữ liệu, sẽ tạo mới khi lưu.")

    # === Ghi dữ liệu ra CSV ===
    def save_to_csv(self):
        with open(self.filename, mode="w", encoding="utf-8", newline="") as f:
            fieldnames = ["book_id", "title", "author", "publisher", "status"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for b in self.books:
                writer.writerow({
                    "book_id": b.book_id,
                    "title": b.title,
                    "author": b.author,
                    "publisher": b.publisher,
                    "status": b.status
                })
        print(f"Đã lưu dữ liệu vào file {self.filename}.")

    # === Thêm sách ===
    def add_book(self):
        print("\n=== THÊM SÁCH MỚI ===")
        book = Book()
        book.input_info()
        for b in self.books:
            if b.book_id == book.book_id:
                print("Mã sách đã tồn tại, không thể thêm.")
                return
        self.books.append(book)
        print("Đã thêm sách thành công!")
        self.save_to_csv()

    # === Sửa sách ===
    def update_book(self):
        print("\n=== CẬP NHẬT THÔNG TIN SÁCH ===")
        bid = input("Nhập mã sách cần sửa: ").strip()
        for b in self.books:
            if b.book_id == bid:
                print("Tìm thấy sách. Nhập thông tin mới (bỏ trống nếu giữ nguyên):")
                new_title = input("Tên sách mới: ").strip()
                new_author = input("Tác giả mới: ").strip()
                new_publisher = input("Nhà xuất bản mới: ").strip()
                new_status = input("Tình trạng mới (Còn/Đã mượn/Hư hỏng/Mất): ").strip()

                if new_title:
                    b.title = new_title
                if new_author:
                    b.author = new_author
                if new_publisher:
                    b.publisher = new_publisher
                if new_status in ["Còn", "Đã mượn", "Hư hỏng", "Mất"]:
                    b.status = new_status

                print("Đã cập nhật thông tin sách!")
                self.save_to_csv()
                return
        print("Không tìm thấy mã sách cần sửa!")

    # === Xóa sách ===
    def delete_book(self):
        print("\n=== XÓA SÁCH ===")
        bid = input("Nhập mã sách cần xóa: ").strip()
        for b in self.books:
            if b.book_id == bid:
                self.books.remove(b)
                print("Đã xóa sách thành công!")
                self.save_to_csv()
                return
        print("Không tìm thấy mã sách cần xóa!")

    # === Tìm kiếm sách ===
    def search_book(self):
        print("\n=== TÌM KIẾM SÁCH ===")
        keyword = input("Nhập từ khóa (mã / tên / tác giả): ").strip().lower()
        found = False
        for b in self.books:
            if (keyword in b.book_id.lower() or
                keyword in b.title.lower() or
                keyword in b.author.lower()):
                b.display_info()
                print("-" * 30)
                found = True
        if not found:
            print("Không tìm thấy sách phù hợp.")

    # === Hiển thị toàn bộ ===
    def display_all(self):
        print("\n=== DANH SÁCH TẤT CẢ SÁCH ===")
        if not self.books:
            print("Danh sách trống.")
        else:
            for b in self.books:
                b.display_info()
                print("-" * 30)


